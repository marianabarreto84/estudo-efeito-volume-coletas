"""
Cliente da YouTube Data API v3 para o caso AGECovP — com contabilidade de cota.

Por que contabilidade de cota
-----------------------------
A cota gratuita e de **10.000 unidades/dia por projeto**, e os custos sao muito
desiguais:

    search.list          100 unidades  por chamada (ate 50 resultados)
    videos.list            1 unidade   por chamada (ate 50 ids)
    commentThreads.list    1 unidade   por chamada (ate 100 comentarios)

Uma varredura descuidada de busca queima o dia inteiro em 100 chamadas. O cliente
mantem um **livro-caixa persistente** (`cota_youtube.json`) no mesmo espirito do
teto de gasto de LLM do caso vacinas: reserva antes de chamar, recusa quando o teto
do dia acabou, e sobrevive a reinicio do script.

A cota zera a **meia-noite do horario do Pacifico** — nao do Brasil. O livro-caixa
usa a data em US/Pacific para saber quando virar o dia.

Uso:
    from core.youtube_api import YouTube
    yt = YouTube()
    for pagina in yt.busca("elderly coronavirus", depois="2020-01-01",
                           antes="2022-09-01", max_paginas=2):
        ...
"""
import datetime as dt
import json
import os
import pathlib
import time

import requests

BASE = "https://www.googleapis.com/youtube/v3"
CUSTO = {"search": 100, "videos": 1, "commentThreads": 1, "channels": 1}
COTA_DIA = 10000
LIVRO = pathlib.Path(__file__).resolve().parents[1] / "data" / "cota_youtube.json"


def carrega_env():
    raiz = pathlib.Path(__file__).resolve().parents[3] / ".env"
    if not raiz.exists():
        return
    for linha in raiz.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))


def dia_pacifico():
    """
    Data corrente no fuso da cota do YouTube (US/Pacific).

    ⚠ LIMITACAO CONHECIDA (anotada em 18/ago/2026): usa **UTC-7 fixo**, que e o
    horario de verao do Pacifico (PDT). Vale de marco a novembro — e portanto esta
    correto para a entrega de 31/ago/2026. Fora dessa janela o Pacifico volta a
    UTC-8 (PST) e este calculo vira o dia **uma hora antes** do que deveria: o livro
    -caixa zeraria as 04:00 de Brasilia quando a cota real so zera as 05:00, e uma
    chamada feita nessa hora seria contada no dia novo enquanto a API ainda a cobra
    do dia velho (resultado: HTTP 403 quotaExceeded com o livro-caixa achando que ha
    saldo).

    Correcao, se o caso passar de novembro: usar zoneinfo —
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    (nao foi usado agora so para nao adicionar dependencia de tzdata no Windows,
    onde o zoneinfo exige o pacote `tzdata` instalado.)
    """
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).strftime("%Y-%m-%d")


class CotaEsgotada(RuntimeError):
    pass


class YouTube:
    def __init__(self, chave=None, teto=COTA_DIA, verbose=True):
        carrega_env()
        self.chave = chave or os.getenv("YOUTUBE_API_KEY")
        if not self.chave:
            raise SystemExit("falta YOUTUBE_API_KEY no .env da raiz da dissertacao")
        self.teto = teto
        self.verbose = verbose
        LIVRO.parent.mkdir(parents=True, exist_ok=True)
        self.livro = json.loads(LIVRO.read_text(encoding="utf-8")) if LIVRO.exists() else {}

    # ---------- cota ----------
    def gasto_hoje(self):
        return self.livro.get(dia_pacifico(), 0)

    def resta(self):
        return max(0, self.teto - self.gasto_hoje())

    def _cobra(self, endpoint):
        c = CUSTO[endpoint]
        if self.gasto_hoje() + c > self.teto:
            raise CotaEsgotada(
                "cota do dia esgotada (%d/%d un. em %s). Ela zera a meia-noite do "
                "Pacifico; a coleta e resumivel — rode de novo amanha."
                % (self.gasto_hoje(), self.teto, dia_pacifico()))
        d = dia_pacifico()
        self.livro[d] = self.livro.get(d, 0) + c
        LIVRO.write_text(json.dumps(self.livro, indent=1), encoding="utf-8")

    def _log(self, m):
        if self.verbose:
            print("[yt] " + m, flush=True)

    # ---------- chamadas ----------
    def _get(self, endpoint, params, tentativas=4):
        self._cobra(endpoint)
        params = dict(params, key=self.chave)
        espera = 4
        for t in range(tentativas):
            r = requests.get("%s/%s" % (BASE, endpoint), params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            j = {}
            try:
                j = r.json()
            except Exception:
                pass
            motivo = ""
            try:
                motivo = j["error"]["errors"][0].get("reason", "")
            except Exception:
                pass
            if motivo in ("quotaExceeded", "dailyLimitExceeded"):
                raise CotaEsgotada("a API recusou por cota (%s). Volta amanha." % motivo)
            if r.status_code in (403, 400) and motivo not in ("rateLimitExceeded",):
                raise RuntimeError("HTTP %d (%s): %s" % (r.status_code, motivo, r.text[:300]))
            time.sleep(espera)
            espera *= 2
        raise RuntimeError("falhou apos %d tentativas: HTTP %d" % (tentativas, r.status_code))

    def busca(self, termo, depois=None, antes=None, max_paginas=2, idioma="en"):
        """Gera paginas de resultados de busca (listas de item da API)."""
        token = None
        for pagina in range(max_paginas):
            p = {"part": "snippet", "q": termo, "type": "video", "maxResults": 50,
                 "order": "relevance"}
            if idioma:
                p["relevanceLanguage"] = idioma
            if depois:
                p["publishedAfter"] = depois + "T00:00:00Z"
            if antes:
                p["publishedBefore"] = antes + "T00:00:00Z"
            if token:
                p["pageToken"] = token
            j = self._get("search", p)
            itens = j.get("items", [])
            if itens:
                yield itens
            token = j.get("nextPageToken")
            if not token:
                return

    def detalhes_videos(self, ids):
        """Metadados completos (ate 50 ids por chamada)."""
        out = []
        for i in range(0, len(ids), 50):
            j = self._get("videos", {"part": "snippet,statistics,contentDetails,topicDetails",
                                     "id": ",".join(ids[i:i + 50])})
            out += j.get("items", [])
        return out

    def canais(self, ids):
        """
        Metadados dos canais (ate 50 ids por chamada, 1 unidade cada).

        Existe porque a Fase 3 media UGC so nos canais presentes no gabarito dos
        autores — e um canal so esta no gabarito se sobreviveu ao filtro DELES.
        Medir "o filtro remove UGC" nessa base e circular. Com este metodo a
        comparacao passa a cobrir os dois lados do filtro por igual.
        """
        out = []
        for i in range(0, len(ids), 50):
            j = self._get("channels", {"part": "snippet,statistics,topicDetails",
                                       "id": ",".join(ids[i:i + 50])})
            out += j.get("items", [])
        return out

    def comentarios(self, video_id, max_paginas=5):
        """Comentarios de topo de um video. Silencioso quando estao desativados."""
        token = None
        for _ in range(max_paginas):
            p = {"part": "snippet", "videoId": video_id, "maxResults": 100,
                 "textFormat": "plainText"}
            if token:
                p["pageToken"] = token
            try:
                j = self._get("commentThreads", p)
            except RuntimeError:
                return          # comentarios desativados / video privado
            itens = j.get("items", [])
            if itens:
                yield itens
            token = j.get("nextPageToken")
            if not token:
                return
