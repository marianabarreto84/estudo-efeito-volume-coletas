"""
Eixo B — Estatística quantitativa (replica Cap. 5 do Heine) agregando no servidor.

Não baixa as 57,9 M linhas: roda GROUP BY/count/sum no Postgres e traz só os agregados.
Auto-detecta as colunas de data e de engajamento (likes/retweets/quotes/replies).

Uso: PYTHONIOENCODING=utf-8 python analise/quantitativa_heine.py <tabela>

Produz (stdout + data/repl/heine2022/RESULTADOS_quantitativa.md):
  B2 — contagem de postagens por dia (picos nos dias de votação: 2/out e 30/out);
  B1 — ETA + pesos por parâmetro e distribuição por faixa de engajamento.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.db import conectar_auto as conectar

COL_DATA_CANDS = ("data", "created_at", "data_criacao", "timestamp", "date")
ENG_MAP = {  # nome canônico -> candidatos de coluna
    "like":    ("likes", "num_likes", "like_count", "favorite_count"),
    "retweet": ("retweets", "num_retweets", "retweet_count"),
    "quote":   ("quotes", "num_quotes", "quote_count"),
    "reply":   ("replies", "num_replies", "reply_count"),
}


def q(cur, sql, args=None):
    cur.execute(sql, args); return cur.fetchall()


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python analise/quantitativa_heine.py <tabela>")
    tabela = sys.argv[1]
    if not tabela.replace("_", "").isalnum():
        raise SystemExit(f"nome de tabela inválido: {tabela}")

    linhas_md = ["# Resultados — eixo quantitativo (caso Heine 2022)\n"]
    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()
        nomes = {r[0] for r in q(cur, """SELECT column_name FROM information_schema.columns
                 WHERE table_schema='public' AND table_name=%s;""", (tabela,))}
        col_data = next((c for c in COL_DATA_CANDS if c in nomes), None)
        eng = {k: next((c for c in cands if c in nomes), None) for k, cands in ENG_MAP.items()}
        eng = {k: v for k, v in eng.items() if v}
        print(f"tabela={tabela}  col_data={col_data}  engajamento={eng}")

        # ---- B2: postagens por dia ----
        if col_data:
            print("\n== B2 — postagens por dia ==")
            linhas_md.append("## B2 — postagens por dia\n\n| dia | tweets |\n|---|--:|")
            for r in q(cur, f"""SELECT ({col_data} AT TIME ZONE 'America/Sao_Paulo')::date d, count(*)
                                FROM {tabela} GROUP BY 1 ORDER BY 1;"""):
                print(f"  {r[0]}  {r[1]:>12,}")
                linhas_md.append(f"| {r[0]} | {r[1]:,} |")

        # ---- B1: ETA + pesos + faixas ----
        if len(eng) >= 1:
            print("\n== B1 — ETA e pesos por parâmetro ==")
            somas = q(cur, f"SELECT {', '.join(f'sum(coalesce({c},0))' for c in eng.values())} FROM {tabela};")[0]
            eta = sum(int(s or 0) for s in somas)
            print(f"  ETA (soma de todos os parâmetros) = {eta:,}")
            linhas_md.append(f"\n## B1 — engajamento\n\nETA = {eta:,}\n\n| parâmetro | soma | peso (ETA/soma) |\n|---|--:|--:|")
            pesos = {}
            for (k, c), s in zip(eng.items(), somas):
                s = int(s or 0)
                peso = (eta / s) if s else 0.0   # peso ~ inverso da frequência (parâmetros raros pesam mais)
                pesos[c] = peso
                print(f"  {k:<8} soma={s:>14,}  peso={peso:.4f}")
                linhas_md.append(f"| {k} | {s:,} | {peso:.4f} |")

            # engajamento por tweet = soma ponderada; distribuição por faixa (log10)
            expr = " + ".join(f"coalesce({c},0)*{pesos[c]:.6f}" for c in eng.values())
            print("\n== B1 — distribuição por faixa de engajamento (log10) ==")
            linhas_md.append("\n### faixas de engajamento (log10 do engajamento ponderado)\n\n| faixa (10^k) | tweets |\n|---|--:|")
            for r in q(cur, f"""
                WITH e AS (SELECT ({expr}) AS eng FROM {tabela})
                SELECT CASE WHEN eng < 1 THEN 0 ELSE floor(log(10, eng))::int END AS faixa, count(*)
                FROM e GROUP BY 1 ORDER BY 1;"""):
                print(f"  10^{r[0]:<2}  {r[1]:>12,}")
                linhas_md.append(f"| 10^{r[0]} | {r[1]:,} |")
        cur.close()

    out = pathlib.Path("data/repl/heine2022/RESULTADOS_quantitativa.md")
    out.write_text("\n".join(linhas_md) + "\n", encoding="utf-8")
    print(f"\n[ok] -> {out}")


if __name__ == "__main__":
    main()
