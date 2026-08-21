"""
Fase 1 — Extrai o snapshot congelado da coleta vacinas (busca 178, vm031) para
SQLite local.

Uso:
    PYTHONIOENCODING=utf-8 python -u pipeline/extrai_snapshot_vacinas.py
    (opcionais: --busca 178 --out data/repl/vacinas2022/snapshot_vacinas.sqlite)

Gera duas tabelas:
  - originais   (~2,05 M) — tweets nao-RT com texto, autor e engajamento
                (eixo B: conteudo/framing + limiares de viralidade);
  - rt_arestas  (~4,5 M)  — retweets como arestas retuitador -> tweet/autor
                original, SEM texto (redundante; eixo A: grafo/modularidade).
Mais `meta` (proveniencia: busca, query, datas, contagens) para rastreabilidade.

Streaming com cursor server-side (nao carrega 6,5 M linhas em memoria); insercao
em lotes; indices criados no final. Roda de novo do zero se interrompido (drop).
"""
import argparse
import json
import pathlib
import sqlite3
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar

RAIZ = pathlib.Path(__file__).resolve().parents[1]

# tweet -> dia_de_busca (id_dia) -> busca (schema antigo da vm031)
FILTRO_BUSCA = """
    t.id_dia_busca_id IN (SELECT id_dia FROM dia_de_busca WHERE id_busca_id = %(busca)s)
"""

COLS_ORIGINAIS = """
    t.twitter_id, t.autor, t.autor_id, t.nome_autor, t.texto, t.data,
    t.idioma, t.likes, t.retweets, t.replies, t.quotes,
    t.num_seguidores, t.status_verificado, t.tweet_tipo,
    t.tweet_referenciado_id, t.autor_original, t.conversa_id,
    t.hashtags, t.mencoes
"""

COLS_ARESTAS = """
    t.twitter_id, t.autor, t.autor_id, t.data,
    t.tweet_referenciado_id, t.autor_original, t.autor_referenciado
"""

DDL = """
CREATE TABLE originais (
    twitter_id            INTEGER PRIMARY KEY,
    autor                 TEXT,
    autor_id              INTEGER,
    nome_autor            TEXT,
    texto                 TEXT,
    data                  TEXT,
    idioma                TEXT,
    likes                 INTEGER,
    retweets              INTEGER,
    replies               INTEGER,
    quotes                INTEGER,
    num_seguidores        INTEGER,
    status_verificado     INTEGER,
    tweet_tipo            TEXT,
    tweet_referenciado_id INTEGER,
    autor_original        TEXT,
    conversa_id           INTEGER,
    hashtags              TEXT,   -- JSON
    mencoes               TEXT    -- JSON
);
CREATE TABLE rt_arestas (
    twitter_id            INTEGER,  -- id do proprio RT (nao e unico se re-coletado; sem PK)
    autor                 TEXT,     -- retuitador
    autor_id              INTEGER,
    data                  TEXT,
    tweet_referenciado_id INTEGER,  -- tweet original retuitado
    autor_original        TEXT,
    autor_referenciado    INTEGER
);
CREATE TABLE meta (chave TEXT PRIMARY KEY, valor TEXT);
"""

INDICES = """
CREATE INDEX idx_orig_retweets ON originais(retweets);
CREATE INDEX idx_orig_autor    ON originais(autor);
CREATE INDEX idx_orig_data     ON originais(data);
CREATE INDEX idx_are_ref       ON rt_arestas(tweet_referenciado_id);
CREATE INDEX idx_are_autor     ON rt_arestas(autor);
CREATE INDEX idx_are_autor_ori ON rt_arestas(autor_original);
"""


def _norm(v):
    """Converte tipos do psycopg2 para algo que o sqlite aceita."""
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, bool):
        return int(v)
    if hasattr(v, "isoformat"):
        return v.isoformat()
    return v


def copia(pg, lite, nome, sql_select, params, tabela_destino, ncols, lote=20000):
    """Streaming Postgres -> SQLite com cursor server-side e lotes."""
    cur = pg.cursor(name=f"snap_{nome}")   # server-side
    cur.itersize = lote
    cur.execute(sql_select, params)
    ins = f"INSERT OR REPLACE INTO {tabela_destino} VALUES ({','.join('?' * ncols)})"
    total, t0 = 0, time.time()
    while True:
        linhas = cur.fetchmany(lote)
        if not linhas:
            break
        lite.executemany(ins, [tuple(_norm(v) for v in l) for l in linhas])
        lite.commit()
        total += len(linhas)
        taxa = total / max(time.time() - t0, 1e-9)
        print(f"  {tabela_destino}: {total:>10,} linhas  ({taxa:,.0f}/s)", flush=True)
    cur.close()
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--busca", type=int, default=178)
    ap.add_argument("--out", default=str(RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"))
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        print(f"[aviso] {out} ja existe — recriando do zero.")
        out.unlink()

    lite = sqlite3.connect(out)
    lite.executescript("PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;")
    lite.executescript(DDL)

    with conectar(vm="vm031", dbname="eTC_Producao") as pg:
        # -- proveniencia --------------------------------------------------
        c = pg.cursor()
        c.execute("""SELECT assunto, data_inicio, data_fim, data_insercao
                     FROM busca WHERE id_busca = %s;""", (args.busca,))
        assunto, dt_ini, dt_fim, dt_ins = c.fetchone()
        c.close()
        print(f"== Busca {args.busca}: {assunto}")
        print(f"   janela {dt_ini:%Y-%m-%d} a {dt_fim:%Y-%m-%d} (inserida {dt_ins:%Y-%m-%d})")

        params = {"busca": args.busca}

        # -- originais -----------------------------------------------------
        print("\n== Extraindo ORIGINAIS (nao-RT) ==", flush=True)
        n_orig = copia(pg, lite, "orig",
                       f"""SELECT {COLS_ORIGINAIS} FROM tweet t
                           WHERE {FILTRO_BUSCA}
                             AND NOT coalesce(t.status_retweet, false)""",
                       params, "originais", ncols=19)

        # -- arestas de RT -------------------------------------------------
        print("\n== Extraindo RT_ARESTAS (retweets) ==", flush=True)
        n_rt = copia(pg, lite, "rt",
                     f"""SELECT {COLS_ARESTAS} FROM tweet t
                         WHERE {FILTRO_BUSCA}
                           AND coalesce(t.status_retweet, false)""",
                     params, "rt_arestas", ncols=7)

    # -- meta + indices ----------------------------------------------------
    meta = {
        "busca_id": args.busca,
        "assunto": assunto,
        "janela": f"{dt_ini:%Y-%m-%d} a {dt_fim:%Y-%m-%d}",
        "data_insercao_busca": f"{dt_ins:%Y-%m-%d}",
        "origem": "vm031 / eTC_Producao (Cloud-DI PUC-Rio)",
        "extraido_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_originais": n_orig,
        "n_rt_arestas": n_rt,
        "script": "pipeline/extrai_snapshot_vacinas.py",
    }
    lite.executemany("INSERT INTO meta VALUES (?, ?)",
                     [(k, str(v)) for k, v in meta.items()])
    print("\n== Criando indices ==", flush=True)
    lite.executescript(INDICES)
    lite.commit()
    lite.execute("PRAGMA optimize;")
    lite.close()

    mb = out.stat().st_size / 1e6
    print(f"\n✅ Snapshot pronto: {out} ({mb:,.0f} MB)")
    print(f"   originais={n_orig:,}  rt_arestas={n_rt:,}")
    # Confere com a Fase 0 (2.046.816 originais / 4.507.889 RTs)
    if n_orig != 2_046_816 or n_rt != 4_507_889:
        print("   [nota] difere das contagens da Fase 0 (22/23-jul-2026) — registrar.")


if __name__ == "__main__":
    main()
