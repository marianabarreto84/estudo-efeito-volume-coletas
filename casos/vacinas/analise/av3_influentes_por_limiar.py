"""
Fase 3 / eixo A — AV3 por limiar de influencia.

A afirmacao do alvo (Tabela 3)
------------------------------
"Dos 602 autores influentes: 353 pro-vacina (58,6%) x 246 anti-vacina (40,9%)."
"Autor influente" = autor de ao menos 1 tweet viral (>500 RT) no periodo.

O teste de volume
-----------------
Baixar o limiar que define "influente" (500 -> 250 -> 100 -> 50 -> 25 -> 10) e ver
se a composicao pro/anti do conjunto de influentes se mantem. E a TERCEIRA
operacionalizacao do mesmo desequilibrio ja visto por dois caminhos independentes:
  - eixo A / AV1: razao pro/anti dos POSTS (1,50-1,56 x 1,02 do paper);
  - eixo B / AV6: fatia pro entre tweets com lado, por limiar de RT.
Aqui a unidade e o AUTOR, nao o post nem o tweet.

Atribuicao de lado
------------------
Por TOPOLOGIA, nao por conteudo: cada autor herda o lado da sua comunidade, pela
mesma regra de `atribui_lado_comunidades.py` (maioria das 599 sementes publicadas;
comunidade sem semente -> nao identificado). Assim o resultado e independente do
rotulador LLM do eixo B.

Expectativa declarada antes de rodar (⚠ contaminada)
----------------------------------------------------
Espero que a fatia pro entre os influentes CRESCA ao baixar o limiar, acompanhando
os outros dois eixos. A expectativa NAO e cega: ja conheco a direcao dos eixos A e B,
e registro isso em vez de apresenta-la como predicao independente. O informativo
aqui e a MAGNITUDE e se o ponto em >500 RT reproduz os 58,6% x 40,9% publicados.

Saidas: stdout + data/repl/vacinas2022/av3_influentes.json
Uso: PYTHONIOENCODING=utf-8 python -u analise/av3_influentes_por_limiar.py
"""
import collections
import json
import pathlib
import sqlite3
import time

import openpyxl

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
SUPL = RAIZ / "data/repl/vacinas2022/suplementar_rotulos.xlsx"
OUT_JSON = RAIZ / "data/repl/vacinas2022/av3_influentes.json"

LIMIARES = (500, 250, 100, 50, 25, 10)
PAPER = {"n": 602, "pro": 353, "anti": 246, "pro_pct": 58.6, "anti_pct": 40.9}


def log(msg):
    print(msg, flush=True)


def norm(a):
    return a.strip().lstrip("@").lower() if a else None


def main():
    t0 = time.time()
    db = sqlite3.connect(SNAP)
    cur = db.cursor()

    # ---------- 1. lado por comunidade (mesma regra do AV1) ----------
    log("== 1. Lado das comunidades (regra do AV1: maioria das sementes) ==")
    lado_semente = {}
    for r in list(openpyxl.load_workbook(SUPL, read_only=True, data_only=True)
                  ["Authors"].iter_rows(values_only=True))[1:]:
        pro, anti, autor = r[0], r[1], r[2]
        a = norm(autor)
        if not a:
            continue
        if pro == 1 and anti != 1:
            lado_semente[a] = "pro"
        elif anti == 1 and pro != 1:
            lado_semente[a] = "anti"

    com_de = {norm(a): c for a, c in
              cur.execute("SELECT autor, comunidade FROM comunidades_autores")}
    votos = collections.defaultdict(collections.Counter)
    for a, lado in lado_semente.items():
        c = com_de.get(a)
        if c is not None:
            votos[c][lado] += 1
    lado_com = {}
    for c, v in votos.items():
        ordem = v.most_common()
        if len(ordem) > 1 and ordem[0][1] == ordem[1][1]:
            continue
        lado_com[c] = ordem[0][0]
    log(f"   {len(lado_semente)} sementes -> {len(lado_com)} comunidades com lado")

    # ---------- 2. influentes por limiar ----------
    log("== 2. Autores influentes por limiar (>= 1 original pt acima do limiar) ==")
    log(f"   {'limiar':>7} {'autores':>9} {'pro':>8} {'anti':>8} {'n/ident':>9} "
        f"{'%pro*':>7} {'%anti*':>7} {'razao':>7}")
    linhas = []
    for lim in LIMIARES:
        autores = [norm(a) for (a,) in cur.execute(
            "SELECT DISTINCT autor FROM originais "
            "WHERE idioma='pt' AND retweets > ?", (lim,))]
        c = collections.Counter(lado_com.get(com_de.get(a), "nao_ident")
                                for a in autores)
        pro, anti, ni = c["pro"], c["anti"], c["nao_ident"]
        com_lado = pro + anti
        pro_pct = 100 * pro / com_lado if com_lado else 0
        anti_pct = 100 * anti / com_lado if com_lado else 0
        razao = pro / anti if anti else None
        linhas.append({"limiar": lim, "n_autores": len(autores),
                       "pro": pro, "anti": anti, "nao_ident": ni,
                       "pro_pct_entre_com_lado": round(pro_pct, 1),
                       "anti_pct_entre_com_lado": round(anti_pct, 1),
                       "razao_pro_anti": round(razao, 3) if razao else None})
        log(f"   {lim:>7} {len(autores):>9,} {pro:>8,} {anti:>8,} {ni:>9,} "
            f"{pro_pct:>6.1f}% {anti_pct:>6.1f}% {razao:>7.2f}")

    # ---------- 3. o ponto do paper ----------
    log("== 3. Ponto de comparacao: >500 RT ==")
    p500 = linhas[0]
    log(f"   paper  : {PAPER['n']} autores | pro {PAPER['pro']} ({PAPER['pro_pct']}%) "
        f"| anti {PAPER['anti']} ({PAPER['anti_pct']}%) | razao "
        f"{PAPER['pro']/PAPER['anti']:.2f}")
    log(f"   replica: {p500['n_autores']} autores | pro {p500['pro']} "
        f"({p500['pro_pct_entre_com_lado']}%) | anti {p500['anti']} "
        f"({p500['anti_pct_entre_com_lado']}%) | razao {p500['razao_pro_anti']:.2f}")
    log("   (o conjunto e maior que 602 porque as contagens de RT sao da re-coleta"
        " de mai/2022, posteriores as do paper)")

    # ---------- 4. leitura ----------
    log("== 4. Leitura ==")
    r0, r1 = linhas[0]["razao_pro_anti"], linhas[-1]["razao_pro_anti"]
    d = linhas[-1]["pro_pct_entre_com_lado"] - linhas[0]["pro_pct_entre_com_lado"]
    log(f"   razao pro/anti entre influentes: {r0:.2f} (>500 RT) -> {r1:.2f} (>10 RT)")
    log(f"   fatia pro entre os com lado: {d:+.1f} p.p. ao descer o limiar")
    log(f"   referencia: razao dos POSTS (AV1) = 1,50-1,56; razao do paper = "
        f"{PAPER['pro']/PAPER['anti']:.2f}")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/av3_influentes_por_limiar.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "regra_lado": "topologia (comunidade), maioria das 599 sementes publicadas",
        "unidade": "autor com >= 1 tweet original pt acima do limiar de RT",
        "paper_tabela3": PAPER,
        "por_limiar": linhas,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    db.close()
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
