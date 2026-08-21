#!/usr/bin/env python3
"""Fase 1 — coleta do universo (caso Buntain).

Baixa TODAS as submissions e comentários dos 13 subreddits do paper em julho/2013
(sem o corte de grau, sem top-100/top-200), via Arctic Shift, para
`data/repl/buntain2013/snapshot_buntain.sqlite`.

Resumível: `collect_log` guarda o último `created_utc` coletado por (subreddit, kind);
reexecutar retoma de onde parou. Não guarda texto (RB3 e o grafo de interação são
estruturais — Buntain é livre de conteúdo).

Uso:  python pipeline/collect.py            # coleta tudo (retomando)
      python pipeline/collect.py --subs AskScience IAmA   # subconjunto
"""
import sqlite3, os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.arctic import iter_items

AFTER = 1372636800   # 2013-07-01 00:00 UTC
BEFORE = 1375315200  # 2013-08-01 00:00 UTC
SUBS = ["AskScienceDiscussion", "AskMen", "AskScience", "AskWomen", "CompSci",
        "DesMoines", "IAmA", "MachineLearning", "Movies", "MyLittlePony",
        "PersonalFinance", "TalesFromTechSupport", "WashingtonDC"]
DB = os.path.join(os.path.dirname(__file__), "..", "data", "repl", "buntain2013",
                  "snapshot_buntain.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions(
  id TEXT PRIMARY KEY, subreddit TEXT, author TEXT, created_utc INTEGER,
  num_comments INTEGER, score INTEGER);
CREATE TABLE IF NOT EXISTS comments(
  id TEXT PRIMARY KEY, subreddit TEXT, author TEXT, created_utc INTEGER,
  parent_id TEXT, link_id TEXT, score INTEGER);
CREATE TABLE IF NOT EXISTS collect_log(
  subreddit TEXT, kind TEXT, last_utc INTEGER, n INTEGER, done INTEGER,
  PRIMARY KEY(subreddit, kind));
CREATE INDEX IF NOT EXISTS ix_c_sub ON comments(subreddit);
CREATE INDEX IF NOT EXISTS ix_c_auth ON comments(author);
CREATE INDEX IF NOT EXISTS ix_s_sub ON submissions(subreddit);
"""

FIELDS = {
    "posts": "id,author,created_utc,num_comments,score",
    "comments": "id,author,created_utc,parent_id,link_id,score",
}


def resume_point(cx, sub, kind):
    r = cx.execute("SELECT last_utc, done FROM collect_log WHERE subreddit=? AND kind=?",
                   (sub, kind)).fetchone()
    return (AFTER, 0, 0) if r is None else (r[0] + 1, 0, r[1])


def collect(cx, sub, kind):
    start, _, done = resume_point(cx, sub, kind)
    if done:
        return 0
    tbl = "submissions" if kind == "posts" else "comments"
    cols = FIELDS[kind].split(",")
    placeholders = ",".join(["?"] * (len(cols) + 1))  # +subreddit
    ins = f"INSERT OR IGNORE INTO {tbl}({FIELDS[kind]},subreddit) VALUES({placeholders})"
    n = 0; batch = []; last = start - 1
    for it in iter_items(kind, sub, start, BEFORE, FIELDS[kind]):
        row = [it.get(c) for c in cols] + [sub]
        batch.append(row)
        last = it.get("created_utc") or last
        n += 1
        if len(batch) >= 500:
            cx.executemany(ins, batch); batch = []
            cx.execute("INSERT OR REPLACE INTO collect_log VALUES(?,?,?,?,0)",
                       (sub, kind, last, n))
            cx.commit()
    if batch:
        cx.executemany(ins, batch)
    cx.execute("INSERT OR REPLACE INTO collect_log VALUES(?,?,?,?,1)", (sub, kind, last, n))
    cx.commit()
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", nargs="*", default=SUBS)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    cx = sqlite3.connect(DB)
    cx.executescript(SCHEMA)
    for sub in args.subs:
        for kind in ("posts", "comments"):
            t = time.time()
            nn = collect(cx, sub, kind)
            print(f"[{time.strftime('%H:%M:%S')}] {sub:<22} {kind:<8} +{nn:>7}  ({time.time()-t:.0f}s)")
            sys.stdout.flush()
    # resumo
    s = cx.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    c = cx.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
    print(f"\nSNAPSHOT: {s} submissions, {c} comentários -> {os.path.abspath(DB)}")


if __name__ == "__main__":
    main()
