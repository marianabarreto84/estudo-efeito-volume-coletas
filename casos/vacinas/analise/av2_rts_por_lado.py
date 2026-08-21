"""
Fase 3 / eixo A — AV2 por limiar: os tweets pro recebem mais RTs que os anti?

A afirmacao do alvo (Tabela 2): "entre os virais (>500 RT), os tweets pro-vacina
MAIS POPULARES receberam 2x mais retweets que os anti-vacina mais populares."

A frase e ambigua, entao medem-se as DUAS leituras plausiveis:
  (A) AGREGADA  — soma de RTs dos tweets pro / soma dos anti no estrato.
      E o que a Tabela 2 do suplemento permite conferir: 1.489.372 / 884.224 = 1,68.
  (B) TOPO      — soma dos N tweets mais retuitados de cada lado (N=1 e N=10).
      E a leitura mais literal de "os mais populares".

O teste de volume: descer o limiar e ver se a razao se mantem.

Dados
-----
  - RTs por tweet: coluna `retweets` dos originais (a mesma que reproduziu o AV4).
  - Lado por tweet: rotulos do eixo B (`rotulos_llm/e1_lim10_pt_p4/rotulos.csv`,
    esquema BINARIO do artigo, k 0,759). Sensibilidade com `p6` (tres classes).
  - Cobertura: os rotulos existem para tweets pt com >10 RT (29.978), entao os
    limiares abaixo de 10 nao sao calculaveis.

Uso: PYTHONIOENCODING=utf-8 python -u analise/av2_rts_por_lado.py
Saidas: stdout + data/repl/vacinas2022/av2_rts_por_lado.json
"""
import collections
import csv
import json
import pathlib
import sqlite3
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
ROT = RAIZ / "data/repl/vacinas2022/rotulos_llm"
OUT_JSON = RAIZ / "data/repl/vacinas2022/av2_rts_por_lado.json"

LIMIARES = (500, 250, 100, 50, 25, 10)
ESQUEMAS = {"p4": "e1_lim10_pt_p4", "p6": "e1_lim10_pt_p6"}
# Tabela 2 do suplemento (estrato >500 RT, rotulagem HUMANA do artigo)
PAPER = {"tweets_pro": 738, "tweets_anti": 784,
         "rts_pro": 1_489_372, "rts_anti": 884_224}


def log(m):
    print(m, flush=True)


def carrega_rotulos(pasta):
    d = {}
    with open(ROT / pasta / "rotulos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d[r["ID"]] = r["stance"]
    return d


def main():
    t0 = time.time()

    log("== 0. Referencia: Tabela 2 do suplemento (>500 RT, rotulo humano) ==")
    r_paper = PAPER["rts_pro"] / PAPER["rts_anti"]
    log(f"   tweets  pro {PAPER['tweets_pro']} x anti {PAPER['tweets_anti']}")
    log(f"   RTs     pro {PAPER['rts_pro']:,} x anti {PAPER['rts_anti']:,}")
    log(f"   >>> razao AGREGADA = {r_paper:.2f}  (o artigo diz '2x')")

    db = sqlite3.connect(SNAP)
    cur = db.cursor()
    rts = {str(i): n for i, n in cur.execute(
        "SELECT twitter_id, retweets FROM originais "
        "WHERE idioma='pt' AND retweets IS NOT NULL")}
    db.close()
    log(f"\n   {len(rts):,} tweets pt com contagem de RT no snapshot")

    resultado = {}
    for esq, pasta in ESQUEMAS.items():
        rot = carrega_rotulos(pasta)
        log(f"\n== Esquema {esq} ({len(rot):,} tweets rotulados) ==")
        log(f"   {'limiar':>7} {'n_pro':>7} {'n_anti':>7} {'RTs_pro':>11} "
            f"{'RTs_anti':>11} {'agreg':>7} {'top10':>7} {'top1':>7}")
        linhas = []
        for lim in LIMIARES:
            por_lado = collections.defaultdict(list)
            for tid, lado in rot.items():
                n = rts.get(tid)
                if n is not None and n > lim:
                    por_lado[lado].append(n)
            pro = sorted(por_lado.get("pro", []), reverse=True)
            anti = sorted(por_lado.get("anti", []), reverse=True)
            if not pro or not anti:
                continue
            agreg = sum(pro) / sum(anti)
            top10 = sum(pro[:10]) / sum(anti[:10])
            top1 = pro[0] / anti[0]
            linhas.append({
                "limiar": lim, "n_pro": len(pro), "n_anti": len(anti),
                "rts_pro": sum(pro), "rts_anti": sum(anti),
                "razao_agregada": round(agreg, 3),
                "razao_top10": round(top10, 3),
                "razao_top1": round(top1, 3),
            })
            log(f"   {lim:>7} {len(pro):>7,} {len(anti):>7,} {sum(pro):>11,} "
                f"{sum(anti):>11,} {agreg:>7.2f} {top10:>7.2f} {top1:>7.2f}")
        resultado[esq] = linhas

    log("\n== Leitura ==")
    p4 = resultado["p4"]
    v500 = next(x for x in p4 if x["limiar"] == 500)
    v10 = next(x for x in p4 if x["limiar"] == 10)
    log(f"   >500 RT (o estrato do artigo): agregada {v500['razao_agregada']:.2f} "
        f"| topo-10 {v500['razao_top10']:.2f} | topo-1 {v500['razao_top1']:.2f}")
    log(f"   paper, agregada: {r_paper:.2f}")
    log(f"   >10 RT (corpus amplo): agregada {v10['razao_agregada']:.2f} "
        f"| topo-10 {v10['razao_top10']:.2f} | topo-1 {v10['razao_top1']:.2f}")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/av2_rts_por_lado.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "fonte_rts": "coluna `retweets` dos originais (pt)",
        "fonte_lado": "rotulos do eixo B (E1, >10 RT, pt)",
        "paper_tabela2": PAPER,
        "paper_razao_agregada": round(r_paper, 3),
        "por_esquema": resultado,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
