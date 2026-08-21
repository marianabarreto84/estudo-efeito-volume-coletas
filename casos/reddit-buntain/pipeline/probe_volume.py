#!/usr/bin/env python3
"""Sonda de volume (Fase 1, caso Buntain) — conta submissions e estima comentários
dos 13 subreddits do paper em julho/2013, via Arctic Shift API.

Não coleta o corpus; só dimensiona antes do pull completo. Rastreável: fonte é
arctic-shift.photon-reddit.com. Gerado 7/ago/2026.
"""
import urllib.request, urllib.parse, json, time, sys

UA = "Mozilla/5.0 (academic replication; buntain-2014; contact via PUC-Rio)"
BASE = "https://arctic-shift.photon-reddit.com/api"
AFTER = 1372636800   # 2013-07-01 00:00 UTC
BEFORE = 1375315200  # 2013-08-01 00:00 UTC
SUBS = ["AskScienceDiscussion", "AskMen", "AskScience", "AskWomen", "CompSci",
        "DesMoines", "IAmA", "MachineLearning", "Movies", "MyLittlePony",
        "PersonalFinance", "TalesFromTechSupport", "WashingtonDC"]

def get(path, params, tries=4):
    qs = urllib.parse.urlencode(params)
    url = f"{BASE}/{path}?{qs}"
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            raw = urllib.request.urlopen(req, timeout=45).read()
            d = json.loads(raw)
            return d.get("data", d) if isinstance(d, dict) else d
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(1.5 * (k + 1))

def count_submissions(sub, cap_pages=400):
    """Pagina submissions asc por created_utc; conta e soma num_comments."""
    n = 0; ncom = 0; lo = hi = None; after = AFTER; pages = 0
    while pages < cap_pages:
        data = get("posts/search", {
            "subreddit": sub, "after": after, "before": BEFORE,
            "sort": "asc", "limit": 100,
            "fields": "created_utc,num_comments",
        })
        if not data:
            break
        pages += 1
        for it in data:
            c = it.get("created_utc")
            if c is None:
                continue
            n += 1
            ncom += it.get("num_comments") or 0
            lo = c if lo is None else min(lo, c)
            hi = c if hi is None else max(hi, c)
        last = data[-1].get("created_utc")
        if last is None or len(data) < 100:
            break
        after = last + 1
        time.sleep(0.15)
    return n, ncom, lo, hi, pages >= cap_pages

def main():
    print(f"Sonda jul/2013 (Arctic Shift) — 13 subreddits\n{'sub':<22} {'#subs':>7} {'~#coment':>9}  cobertura")
    tot_s = tot_c = 0
    for sub in SUBS:
        try:
            n, ncom, lo, hi, capped = count_submissions(sub)
        except Exception as e:
            print(f"{sub:<22} ERRO {type(e).__name__}: {str(e)[:60]}")
            continue
        tot_s += n; tot_c += ncom
        cov = ""
        if lo:
            cov = f"{time.strftime('%d/%m', time.gmtime(lo))}–{time.strftime('%d/%m', time.gmtime(hi))}"
        flag = " [CAP!]" if capped else ""
        print(f"{sub:<22} {n:>7} {ncom:>9}  {cov}{flag}")
        sys.stdout.flush()
    print(f"{'TOTAL':<22} {tot_s:>7} {tot_c:>9}")
    print("\n(~#coment = soma de num_comments das submissions; estimativa do volume de comentários a coletar)")

if __name__ == "__main__":
    main()
