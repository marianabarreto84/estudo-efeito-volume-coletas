"""
Fase 1 — Extrai um snapshot congelado da vm067 para SQLite local.

Uso: python extrai_snapshot.py [hashtag|full]
  hashtag  -> A_mais_hashtag: hashtag normalizada == 'eleicoes2014'      (~141k)
  full     -> A_mais_full: qualquer hashtag eleitoral da coleta eTC 2014 (~214k)

Saida: data/repl/compos2014/snapshot_<modo>.sqlite + MANIFEST_<modo>.txt

Depois disso, TODA a analise roda localmente sobre o snapshot (reprodutivel,
sem depender da VPN/banco compartilhado).
"""
import json, sqlite3, sys, time
from pathlib import Path
from urllib.parse import urlparse
import sys as _sys, pathlib as _pathlib
_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar
from core.midia_dominios import classificar_host, _norm_host

OUT_DIR = Path("data/repl/compos2014")
OUT_DIR.mkdir(parents=True, exist_ok=True)

NORM = "translate(lower({c}),'áàâãäçéèêëíìîïóòôõöúùûüýÿñō','aaaaaceeeeiiiiooooouuuuyyno')"

# hashtags eleitorais normalizadas (termos reais da coleta eTC 2014)
HASHTAGS_ELEITORAIS = ("eleicoes2014", "pt", "psdb", "aeciopelobrasil", "dilmamudamais", "13", "45")

# filtro WHERE por modo
FILTROS = {
    "hashtag": (f"EXISTS (SELECT 1 FROM unnest(hashtags) t WHERE {NORM.format(c='t')}='eleicoes2014')",
                "hashtag normalizada == 'eleicoes2014' (#Eleicoes2014)"),
    "full":    (f"EXISTS (SELECT 1 FROM unnest(hashtags) t WHERE {NORM.format(c='t')} = ANY(%(tags)s))",
                "qualquer hashtag eleitoral: " + ", ".join("#"+h for h in HASHTAGS_ELEITORAIS)),
}

COLS = [
    "id_tweet", "twitter_id", "autor", "nome_autor", "autor_id", "texto", "idioma",
    "hashtags", "links", "urls_detalhes",
    "likes", "retweets", "replies", "quotes",
    "status_retweet", "status_verificado", "num_seguidores", "num_seguindo", "num_tweets",
    "autor_original", "tweet_tipo", "conversa_id", "tweet_referenciado_id", "resposta_a_id",
]
ARRAY_COLS = {"hashtags", "links", "urls_detalhes"}


def primeiro_host(links):
    """Host do 1o link (regra do paper: so o 1o link conta)."""
    if not links:
        return None
    try:
        return _norm_host(urlparse(links[0]).netloc)
    except Exception:
        return None


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "hashtag"
    if modo not in FILTROS:
        raise SystemExit(f"modo invalido: {modo} (use {list(FILTROS)})")
    where, descricao = FILTROS[modo]
    db_path = OUT_DIR / f"snapshot_{modo}.sqlite"
    select_sql = (f"SELECT {', '.join(COLS)}, (data AT TIME ZONE 'America/Sao_Paulo') AS data_brt "
                  f"FROM ituassu_2014 WHERE {where}")
    params = {"tags": list(HASHTAGS_ELEITORAIS)} if modo == "full" else None
    print(f"modo={modo} | filtro: {descricao}\n-> {db_path}")

    if db_path.exists():
        db_path.unlink()
    loc = sqlite3.connect(db_path)
    cols_ddl = ", ".join(f'"{c}" TEXT' if c in ARRAY_COLS else f'"{c}"' for c in COLS)
    loc.execute(f'''CREATE TABLE tweets (
        {cols_ddl},
        data_brt TEXT,
        primeiro_host TEXT,
        classe_midia TEXT
    );''')

    t0 = time.time()
    n = 0
    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor(name="stream_snapshot")  # server-side cursor (streaming)
        cur.itersize = 5000
        cur.execute(select_sql, params)
        ins = f'INSERT INTO tweets VALUES ({",".join("?"*(len(COLS)+3))})'
        batch = []
        for row in cur:
            d = dict(zip(COLS, row[:len(COLS)]))
            data_brt = row[len(COLS)]
            links = d["links"] or []
            host = primeiro_host(links)
            classe = classificar_host(host) if host else "NDA"
            vals = []
            for c in COLS:
                v = d[c]
                vals.append(json.dumps(v, ensure_ascii=False) if c in ARRAY_COLS else v)
            vals.append(data_brt.isoformat() if data_brt else None)
            vals.append(host)
            vals.append(classe)
            batch.append(vals)
            if len(batch) >= 5000:
                loc.executemany(ins, batch); loc.commit(); n += len(batch); batch = []
                print(f"  ...{n} linhas", flush=True)
        if batch:
            loc.executemany(ins, batch); loc.commit(); n += len(batch)
        cur.close()

    # indices locais uteis
    loc.execute("CREATE INDEX ix_data ON tweets(data_brt);")
    loc.execute("CREATE INDEX ix_classe ON tweets(classe_midia);")
    loc.commit()
    dt = time.time() - t0

    manifest = OUT_DIR / f"MANIFEST_{modo}.txt"
    manifest.write_text(
        f"Snapshot A_mais_{modo} (Fase 1)\n"
        "origem: vm067 / eTC_Producao / public.ituassu_2014\n"
        f"filtro: {descricao}\n"
        f"linhas: {n}\n"
        f"colunas: {', '.join(COLS)}, data_brt, primeiro_host, classe_midia\n"
        "data_brt: timestamp em America/Sao_Paulo (naive)\n"
        f"extraido_em_segundos: {dt:.1f}\n",
        encoding="utf-8")

    print(f"\n[ok] {n} linhas -> {db_path}  ({dt:.1f}s)")
    print(f"[ok] manifesto -> {manifest}")


if __name__ == "__main__":
    main()
