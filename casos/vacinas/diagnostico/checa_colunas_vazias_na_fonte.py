"""
Diagnostico — as colunas vazias do snapshot estao vazias NA FONTE?

Contexto (ver data/repl/vacinas2022/FASE1_snapshot.md, Achado 1): 7 de 19 colunas
de `originais` e 3 de 7 de `rt_arestas` vieram 100% NULL no snapshot congelado,
entre elas `hashtags`, `mencoes`, `tweet_tipo` e `tweet_referenciado_id`. A extracao
SELECIONOU todas elas e nao deu erro, entao elas existem na fonte — mas nao da para
saber, so com o snapshot, se:

  (a) a coleta da busca 178 realmente nao preenche esses campos; ou
  (b) o dado mora em OUTRA tabela do schema antigo da vm031, que a extracao
      nao visitou (hipotese forte para hashtags/mencoes, que schemas antigos
      costumam guardar em tabelas de relacao).

Este script decide entre (a) e (b). **Somente leitura** — nenhum INSERT/UPDATE/DDL.
Amostra limitada; nao traz volume.

REQUER A VPN DA CLOUD-DI CONECTADA (adaptador TAP com IP 10.x e rota 10.50.0.0).
Teste antes: `ping 10.50.0.32`.

Uso: PYTHONIOENCODING=utf-8 python -u diagnostico/checa_colunas_vazias_na_fonte.py
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar          # vm EXPLICITA — ver nota abaixo

# ⚠ Usar vm="vm031", como faz `pipeline/extrai_snapshot_vacinas.py`. A busca 178
# vive la. Com `conectar_auto` cai-se na vm067 (a da coleta continua e da
# `ituassu_2014`), e o diagnostico responde sobre o servidor errado.
VM = "vm031"
BUSCA = 178
COLS_SUSPEITAS = ("hashtags", "mencoes", "tweet_tipo", "tweet_referenciado_id",
                  "autor_original", "conversa_id", "autor_id", "autor_referenciado")

FILTRO = """
    t.id_dia_busca_id IN (SELECT id_dia FROM dia_de_busca WHERE id_busca_id = %s)
"""


def log(m):
    print(m, flush=True)


def main():
    with conectar(vm=VM, dbname="eTC_Producao") as conn:
        log(f"(conectado a {VM} / eTC_Producao)")
        cur = conn.cursor()

        # ---------- 1. qual tabela guarda os tweets ----------
        log("== 1. Tabelas candidatas no schema ==")
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema='public'
              AND (table_name ILIKE '%tweet%' OR table_name ILIKE '%hashtag%'
                   OR table_name ILIKE '%mencao%' OR table_name ILIKE '%mention%'
                   OR table_name ILIKE '%entidade%')
            ORDER BY 1""")
        tabelas = [r[0] for r in cur.fetchall()]
        for t in tabelas:
            log(f"   {t}")

        # ---------- 2. a tabela de tweets tem mesmo essas colunas? ----------
        log("\n== 2. Colunas suspeitas na tabela de tweets ==")
        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema='public' AND column_name = ANY(%s)
            ORDER BY table_name, column_name""", (list(COLS_SUSPEITAS),))
        for tab, col, tipo in cur.fetchall():
            log(f"   {tab:<28} {col:<24} {tipo}")

        # ---------- 3. preenchimento NA FONTE, na busca 178 ----------
        log(f"\n== 3. Preenchimento na fonte (busca {BUSCA}, amostra de 200k) ==")
        alvo = "tweet"          # ajustar se a §1 mostrar outro nome
        try:
            cur.execute("""SELECT column_name FROM information_schema.columns
                           WHERE table_schema='public' AND table_name=%s""", (alvo,))
            existentes = {r[0] for r in cur.fetchall()}
            cols = [c for c in COLS_SUSPEITAS if c in existentes]
            ausentes = [c for c in COLS_SUSPEITAS if c not in existentes]
            if ausentes:
                log(f"   (nao existem em `{alvo}`: {ausentes})")
            campos = ", ".join(f"count(t.{c}) AS n_{c}" for c in cols)
            cur.execute(f"""
                SELECT count(*) AS n, {campos}
                FROM (SELECT * FROM {alvo} t WHERE {FILTRO} LIMIT 200000) t
            """, (BUSCA,))
            nomes = [d[0] for d in cur.description]
            for nome, val in zip(nomes, cur.fetchone()):
                log(f"   {nome:<28} {val:>10,}")
        except Exception as e:
            conn.rollback()
            log(f"   ⚠ falhou em `{alvo}`: {e}")
            log("   -> use a lista da secao 1 para achar o nome certo e reexecutar")

        # ---------- 4. existe tabela de relacao para hashtag/mencao? ----------
        log("\n== 4. Tabelas de relacao (hashtag/mencao) — amostra ==")
        for t in tabelas:
            if any(k in t.lower() for k in ("hashtag", "mencao", "mention", "entidade")):
                try:
                    cur.execute(f"SELECT count(*) FROM {t}")
                    n = cur.fetchone()[0]
                    cur.execute(f"SELECT * FROM {t} LIMIT 3")
                    cols = [d[0] for d in cur.description]
                    log(f"   {t}: {n:,} linhas · colunas {cols}")
                    for r in cur.fetchall():
                        log(f"      {r}")
                except Exception as e:
                    conn.rollback()
                    log(f"   {t}: erro {e}")

    log("\nOK — compare com FASE1_snapshot.md Achado 1 e conclua (a) ou (b).")


if __name__ == "__main__":
    main()
