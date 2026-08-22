#!/usr/bin/env python3
"""Cliente de AGREGACAO do Arctic Shift, paciente com o rate limit.

Este modulo existe porque o endpoint de agregacao
(`.../{posts,comments}/search/aggregate`) devolve a MESMA mensagem de erro por duas
causas diferentes, e tratar as duas do mesmo jeito estraga a medicao:

  {"data":null,"error":"Timeout. Maybe slow down a bit"}

  (a) ESTRANGULAMENTO — o servidor esta pedindo para diminuir o ritmo. Medido em
      22/ago/2026: uma consulta trivial (subreddit de 222 submissoes) falha sob uso
      intenso e passa depois de ~300 s de silencio. 30 s e 120 s nao bastam.
  (b) TAMANHO — a janela e grande demais para o servidor contar no tempo dele.
      Medido: `conspiracy` em 166 dias falha em 14 s mesmo apos 300 s de silencio.

**O discriminador e o descanso**: se a MESMA consulta passa depois de descansar, era
(a); se falha de novo, era (b).

A primeira sonda deste caso dividia o intervalo ao meio a cada falha. Isso e certo
para (b) e **contraproducente** para (a) — dividir significa mais chamadas, que e o
oposto do que o servidor pediu. Deu para medir a espiral: a mesma contagem de
`Vaccines` custou 4 chamadas numa rodada e 16 na seguinte.

Estrategia daqui: LADRILHO ADAPTATIVO. Varre a janela com um ladrilho e **aprende**
o tamanho que o servidor aguenta, em vez de redescobri-lo por recursao a cada pedaco.
Assim o custo do descanso so e pago quando ha estrangulamento de fato, e um ladrilho
ja provado grande demais nunca e retentado.

Nao tem dependencia externa: so a biblioteca padrao.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api"
UA = "Mozilla/5.0 (academic replication; PUC-Rio; contato via inf.puc-rio.br)"

DESCANSO = 300      # s de silencio que curam o estrangulamento (medido em 22/ago/2026)
PACING = 15         # s entre chamadas bem-sucedidas, para nao provocar o limite
PISO = 3600         # ladrilho minimo: 1 h. Abaixo disso, desiste.

DIA = 86400


def _uma_chamada(kind, sub, ini, fim, timeout=180):
    """Uma consulta de agregacao.

    Devolve (contagem|None, motivo). `motivo` e 'ok' ou uma etiqueta de falha:
    'limite' (mensagem de rate limit), 'http:<codigo>', 'rede:<Excecao>', 'erro'.
    """
    qs = urllib.parse.urlencode({"subreddit": sub, "after": int(ini),
                                 "before": int(fim), "aggregate": "subreddit"})
    url = "%s/%s/search/aggregate?%s" % (BASE, kind, qs)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        bruto = urllib.request.urlopen(req, timeout=timeout).read()
        d = json.loads(bruto)
    except urllib.error.HTTPError as e:
        # ⚠ O Arctic Shift devolve a mensagem de erro DENTRO do corpo de um 4xx
        # (observado: HTTP 422 com {"error":"Timeout. Maybe slow down a bit"}). O
        # urllib levanta antes de ler o corpo, entao e preciso ler aqui — senao a
        # unica evidencia que separa estrangulamento de tamanho se perde.
        corpo = ""
        try:
            corpo = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        ra = None
        try:
            ra = e.headers.get("Retry-After")
        except Exception:
            pass
        if "slow down" in corpo.lower():
            return None, "limite(http:%s)%s" % (e.code,
                                                "/retry-after=%s" % ra if ra else "")
        return None, "http:%s%s%s" % (e.code, "/retry-after=%s" % ra if ra else "",
                                      " " + corpo.replace("\n", " ") if corpo else "")
    except Exception as e:
        return None, "rede:%s" % type(e).__name__
    if isinstance(d, dict) and d.get("error"):
        msg = str(d["error"]).lower()
        return None, "limite" if "slow down" in msg else "erro:%s" % str(d["error"])[:40]
    dados = d.get("data") if isinstance(d, dict) else d
    return sum(int(x.get("count", 0)) for x in (dados or [])), "ok"


def conta_janela(kind, sub, ini, fim, log=print,
                 descanso=DESCANSO, pacing=PACING, piso=PISO, ladrilho_inicial=None):
    """Conta itens de `sub` em [ini, fim) por ladrilho adaptativo.

    Devolve um dict com o total, se fechou, o ladrilho final e a contabilidade de
    chamadas/descansos — a contabilidade e evidencia, nao enfeite: e ela que diz se
    o endpoint aguenta o subreddit ou nao.
    """
    cursor = int(ini)
    fim = int(fim)
    ladrilho = int(ladrilho_inicial or (fim - cursor))
    total = 0
    chamadas = descansos = encolhidas = 0
    motivos = []
    t0 = time.time()

    while cursor < fim:
        alto = min(cursor + ladrilho, fim)
        c, motivo = _uma_chamada(kind, sub, cursor, alto)
        chamadas += 1
        if motivo == "ok":
            total += c
            cursor = alto
            if cursor < fim:
                time.sleep(pacing)
            continue

        motivos.append(motivo)
        log("      %s/%s: janela de %.1fd falhou (%s) — descansando %ds"
            % (sub, kind, (alto - cursor) / DIA, motivo, descanso))
        descansos += 1
        time.sleep(descanso)

        # a MESMA janela de novo: se passar, era estrangulamento; se nao, era tamanho
        c, motivo = _uma_chamada(kind, sub, cursor, alto)
        chamadas += 1
        if motivo == "ok":
            log("      -> era ESTRANGULAMENTO (passou apos o descanso)")
            total += c
            cursor = alto
            if cursor < fim:
                time.sleep(pacing)
            continue

        if alto - cursor <= piso:
            log("      -> DESISTIU: nem %.0fh passa apos descanso (%s)"
                % (piso / 3600, motivo))
            return {"total": total, "completo": False, "ladrilho_final_d": ladrilho / DIA,
                    "chamadas": chamadas, "descansos": descansos,
                    "encolhidas": encolhidas, "motivos": motivos,
                    "segundos": round(time.time() - t0, 1)}

        ladrilho = max(piso, ladrilho // 2)
        encolhidas += 1
        log("      -> era TAMANHO; ladrilho -> %.1fd" % (ladrilho / DIA))

    return {"total": total, "completo": True, "ladrilho_final_d": ladrilho / DIA,
            "chamadas": chamadas, "descansos": descansos, "encolhidas": encolhidas,
            "motivos": motivos, "segundos": round(time.time() - t0, 1)}
