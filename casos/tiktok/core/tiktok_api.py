"""
Cliente da TikTok Research API v2 — coleta LOCAL (sem VPN, sem VM).

Mesma API que o coletor do eTC usa na vm031 (`~/tweetcrawler/new-tiktok/main.py`),
reescrita aqui no padrao dos outros casos: credencial no `.env` (nunca no codigo),
resumivel, com respeito a cota e sem nada hardcoded.

Endpoints (identicos aos do coletor do eTC)
-------------------------------------------
  token : POST https://open.tiktokapis.com/v2/oauth/token/     (client_credentials)
  query : POST https://open.tiktokapis.com/v2/research/video/query/?fields=...

Limites da API que o codigo respeita
------------------------------------
  - `max_count` <= 100 por chamada;
  - a janela `start_date`..`end_date` de UMA query nao pode passar de **30 dias**
    (o coletor fatia a janela pedida automaticamente);
  - pagina por `cursor` + `search_id`; `has_more` diz quando acabou;
  - `access_token` vale ~2 h (`expires_in`), renovado sozinho;
  - HTTP 429 (cota) -> espera exponencial e tenta de novo, com teto.

\u26a0 COTA COMPARTILHADA — leia antes de coletar em escala
--------------------------------------------------------
A credencial e a **do app do eTC**, e o coletor da vm031 roda em LOOP CONTINUO
com ela. A cota da Research API e por aplicacao, nao por maquina: o que for
gasto aqui **sai da mesma cota** que a coleta continua do grupo. Antes de
qualquer coleta grande, combinar com quem opera o crawler (os comentarios do
`execute_tiktok.sh` citam o Tomaz) ou pedir credencial propria.

Uso:
    from core.tiktok_api import TikTokAPI
    api = TikTokAPI()                      # le TIKTOK_CLIENT_KEY/SECRET do .env
    for lote in api.busca_videos(hashtags=["eleicoes2026"], regiao="BR",
                                 inicio="20260801", fim="20260810"):
        ...
"""
import datetime as dt
import os
import pathlib
import time

import requests

TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
QUERY_URL = "https://open.tiktokapis.com/v2/research/video/query/"

# os mesmos campos que o coletor do eTC pede
CAMPOS = ("id,username,video_description,create_time,region_code,share_count,"
          "view_count,like_count,comment_count,music_id,hashtag_names,effect_ids,"
          "playlist_id,voice_to_text")

MAX_DIAS_POR_QUERY = 30
MAX_COUNT = 100


def carrega_env(caminho=None):
    """Le o .env da raiz da dissertacao (CHAVE=valor), sem dependencias."""
    if caminho is None:
        caminho = pathlib.Path(__file__).resolve().parents[3] / ".env"
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, v = linha.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"'))


def _dia(s):
    return dt.datetime.strptime(s, "%Y%m%d").date()


def fatia_janela(inicio, fim, max_dias=MAX_DIAS_POR_QUERY):
    """Quebra [inicio, fim] em pedacos de no maximo `max_dias` (formato YYYYMMDD)."""
    a, b = _dia(inicio), _dia(fim)
    if a > b:
        raise ValueError("inicio depois do fim")
    out = []
    while a <= b:
        c = min(a + dt.timedelta(days=max_dias - 1), b)
        out.append((a.strftime("%Y%m%d"), c.strftime("%Y%m%d")))
        a = c + dt.timedelta(days=1)
    return out


class CotaEsgotada(RuntimeError):
    pass


class TikTokAPI:
    def __init__(self, client_key=None, client_secret=None, verbose=True):
        carrega_env()
        self.key = client_key or os.getenv("TIKTOK_CLIENT_KEY")
        self.secret = client_secret or os.getenv("TIKTOK_CLIENT_SECRET")
        if not self.key or not self.secret:
            raise SystemExit(
                "faltam TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET no .env da raiz "
                "(c:/Users/maria/Documents/dissertacao/.env)")
        self.verbose = verbose
        self._token = None
        self._expira_em = 0
        self.chamadas = 0

    # ---------- autenticacao ----------
    def token(self):
        if self._token and time.time() < self._expira_em - 60:
            return self._token
        r = requests.post(TOKEN_URL,
                          headers={"Content-Type": "application/x-www-form-urlencoded"},
                          data={"client_key": self.key, "client_secret": self.secret,
                                "grant_type": "client_credentials"}, timeout=30)
        if r.status_code != 200:
            raise RuntimeError("falha no token (HTTP %d): %s" % (r.status_code, r.text[:300]))
        j = r.json()
        if "access_token" not in j:
            raise RuntimeError("resposta de token sem access_token: %s" % str(j)[:300])
        self._token = j["access_token"]
        self._expira_em = time.time() + int(j.get("expires_in", 7200))
        self._log("token obtido (vale %ds)" % int(j.get("expires_in", 7200)))
        return self._token

    def _log(self, m):
        if self.verbose:
            print("[tiktok] " + m, flush=True)

    # ---------- consulta ----------
    def _monta_query(self, hashtags=None, palavras=None, regiao=None, usernames=None):
        cond = []
        if hashtags:
            cond.append({"operation": "IN", "field_name": "hashtag_name",
                         "field_values": list(hashtags)})
        if palavras:
            cond.append({"operation": "IN", "field_name": "keyword",
                         "field_values": list(palavras)})
        if regiao:
            cond.append({"operation": "IN", "field_name": "region_code",
                         "field_values": [regiao] if isinstance(regiao, str) else list(regiao)})
        if usernames:
            cond.append({"operation": "IN", "field_name": "username",
                         "field_values": list(usernames)})
        if not cond:
            raise ValueError("query vazia: passe hashtags, palavras, regiao ou usernames")
        return {"and": cond}

    def busca_videos(self, inicio, fim, hashtags=None, palavras=None, regiao=None,
                     usernames=None, max_paginas=None, pausa=1.0):
        """
        Gera lotes de videos (listas de dict). Fatia a janela em pedacos de 30 dias
        e pagina cada pedaco ate `has_more` virar falso.
        """
        query = self._monta_query(hashtags, palavras, regiao, usernames)
        for ini, f in fatia_janela(inicio, fim):
            self._log("janela %s..%s" % (ini, f))
            cursor, search_id, pagina = 0, None, 0
            while True:
                corpo = {"query": query, "start_date": ini, "end_date": f,
                         "max_count": MAX_COUNT, "cursor": cursor}
                if search_id:
                    corpo["search_id"] = search_id
                j = self._post(corpo)
                dados = (j or {}).get("data", {}) or {}
                videos = dados.get("videos", []) or []
                pagina += 1
                self._log("  pagina %d: %d videos (cursor=%s)" % (pagina, len(videos), cursor))
                if videos:
                    yield videos
                if not dados.get("has_more") or (max_paginas and pagina >= max_paginas):
                    break
                cursor = dados.get("cursor", cursor + len(videos))
                search_id = dados.get("search_id", search_id)
                time.sleep(pausa)

    def _post(self, corpo, tentativas=5):
        url = QUERY_URL + "?fields=" + CAMPOS
        espera = 5
        for t in range(tentativas):
            r = requests.post(url, headers={
                "Authorization": "Bearer " + self.token(),
                "Content-Type": "application/json"}, json=corpo, timeout=60)
            self.chamadas += 1
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                self._log("HTTP 429 (cota/ritmo) — esperando %ds [%d/%d]" % (espera, t + 1, tentativas))
                time.sleep(espera)
                espera *= 2
                continue
            if r.status_code in (401, 403):
                self._token = None          # forca renovacao e tenta 1x
                if t == 0:
                    continue
                raise RuntimeError("sem autorizacao (HTTP %d): %s" % (r.status_code, r.text[:300]))
            if 500 <= r.status_code < 600:
                time.sleep(espera)
                espera *= 2
                continue
            raise RuntimeError("HTTP %d: %s" % (r.status_code, r.text[:400]))
        raise CotaEsgotada("esgotadas %d tentativas (ultimo status %d)" % (tentativas, r.status_code))
