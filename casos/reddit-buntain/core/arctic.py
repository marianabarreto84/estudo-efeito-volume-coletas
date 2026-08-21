#!/usr/bin/env python3
"""Cliente Arctic Shift (Fase 1, caso Buntain).

Arctic Shift (arctic-shift.photon-reddit.com) é a fonte pós-Pushshift de dados do
Reddit. A API oficial do Reddit NÃO serve (teto ~1.000/listagem = a sub-coleta do
paper). Requer User-Agent de navegador (senão 403).

Paginação: `sort=asc` + avançar `after` para o último `created_utc`+1. `limit` teto 100.
"""
import urllib.request, urllib.parse, json, time

UA = "Mozilla/5.0 (academic replication; buntain-2014; PUC-Rio)"
BASE = "https://arctic-shift.photon-reddit.com/api"


def _get(path, params, tries=5):
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            raw = urllib.request.urlopen(req, timeout=60).read()
            d = json.loads(raw)
            return d.get("data", d) if isinstance(d, dict) else d
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2.0 * (k + 1))


def iter_items(kind, subreddit, after, before, fields, sleep=0.15):
    """Itera TODOS os itens (kind='posts'|'comments') do subreddit na janela.

    Retoma-friendly: o chamador pode começar de um `after` maior. Rende dicts.
    """
    assert kind in ("posts", "comments")
    cur = after
    while True:
        data = _get(f"{kind}/search", {
            "subreddit": subreddit, "after": cur, "before": before,
            "sort": "asc", "limit": 100, "fields": fields,
        })
        if not data:
            return
        for it in data:
            yield it
        last = data[-1].get("created_utc")
        if last is None or len(data) < 100:
            return
        cur = last + 1
        time.sleep(sleep)
