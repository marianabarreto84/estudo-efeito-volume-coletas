"""
Fase 3 — E3: a conclusao e do recorte de TERMOS ou do fenomeno?

O artigo coletou por seis termos-indice em portugues: vacina, vacinacao, vacinar,
anti-vacinacao, anti-vax, vacinacao infantil. Este script recomputa, POR TERMO, as
duas conclusoes que o caso mede — o balanco pro x anti (AV6) e a composicao
tematica (AV5) — para ver se elas dependem do termo que trouxe o tweet.

Por que da para rodar agora
---------------------------
A coluna `hashtags` esta vazia na fonte (ver FASE1, Achado 1), mas `texto` esta 100%
preenchido no snapshot local. O casamento por termo sai por regex sobre o texto,
sem VPN e sem re-extracao.

⚠ Os subconjuntos NAO formam particao: "vacina" e prefixo de quase todos os outros
termos, entao os grupos se sobrepoem de proposito. Cada linha e "tweets que contem
o termo X", nao "tweets trazidos exclusivamente por X".

Uso: PYTHONIOENCODING=utf-8 python -u analise/e3_por_termo.py
Saidas: stdout + data/repl/vacinas2022/e3_por_termo.json
"""
import collections
import csv
import json
import pathlib
import re
import sqlite3
import time
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
ROT = RAIZ / "data/repl/vacinas2022/rotulos_llm"
OUT_JSON = RAIZ / "data/repl/vacinas2022/e3_por_termo.json"

# padroes sobre texto SEM acento e em minusculas
TERMOS = {
    "vacina (generico)":   r"\bvacinas?\b",
    "vacinacao":           r"\bvacinacao\b",
    "vacinar":             r"\bvacinar\w*\b",
    "anti-vacinacao":      r"\banti[\s-]?vacinacao\b",
    "anti-vax":            r"\banti[\s-]?vax\w*\b",
    "vacinacao infantil":  r"\bvacinacao infantil\b",
}
CATS = [f"cat_{i}" for i in range(1, 15)]
NOMES_CAT = {
    "cat_1": "Politics", "cat_2": "Children", "cat_3": "Restrictive policies",
    "cat_4": "Disadvantages of vaccines", "cat_5": "Anti-vaccine people",
    "cat_6": "International", "cat_7": "Advantages of vaccines",
    "cat_8": "COVID risks", "cat_9": "Misinformation sources",
    "cat_10": "Information sources", "cat_11": "Science",
    "cat_12": "Vaccines type or laboratories", "cat_13": "Religion",
    "cat_14": "Other drugs",
}


def log(m):
    print(m, flush=True)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def main():
    t0 = time.time()

    log("== 1. Carregando rotulos (p6, tres classes) e textos ==")
    rot = {}
    with open(ROT / "e1_lim10_pt_p6/rotulos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rot[r["ID"]] = r
    log(f"   {len(rot):,} tweets rotulados")

    db = sqlite3.connect(SNAP)
    textos = {}
    for tid, txt in db.execute(
            "SELECT twitter_id, texto FROM originais WHERE idioma='pt'"):
        s = str(tid)
        if s in rot:
            textos[s] = sem_acento(txt or "")
    db.close()
    log(f"   {len(textos):,} textos casados com rotulo")

    log("\n== 2. Balanco pro x anti por termo ==")
    log(f"   {'termo':<22} {'n':>8} {'%pro':>7} {'%anti':>7} {'%neutro':>8} "
        f"{'razao':>7}")
    linhas = []
    compilados = {t: re.compile(p) for t, p in TERMOS.items()}
    for termo, rx in compilados.items():
        ids = [i for i, t in textos.items() if rx.search(t)]
        c = collections.Counter(rot[i]["stance"] for i in ids)
        n = len(ids)
        if not n:
            continue
        pro, anti, nen = c["pro"], c["anti"], c["nenhum"]
        com_lado = pro + anti
        razao = pro / anti if anti else None
        linhas.append({
            "termo": termo, "n": n, "pro": pro, "anti": anti, "nenhum": nen,
            "pct_pro": round(100 * pro / n, 1), "pct_anti": round(100 * anti / n, 1),
            "pct_neutro": round(100 * nen / n, 1),
            "pct_pro_entre_com_lado": round(100 * pro / com_lado, 1) if com_lado else None,
            "razao_pro_anti": round(razao, 3) if razao else None,
        })
        log(f"   {termo:<22} {n:>8,} {100*pro/n:>6.1f}% {100*anti/n:>6.1f}% "
            f"{100*nen/n:>7.1f}% {(razao or 0):>7.2f}")

    # referencia: corpus inteiro rotulado
    c = collections.Counter(r["stance"] for r in rot.values())
    n = sum(c.values())
    razao_geral = c["pro"] / c["anti"]
    log(f"   {'TODOS (referencia)':<22} {n:>8,} {100*c['pro']/n:>6.1f}% "
        f"{100*c['anti']/n:>6.1f}% {100*c['nenhum']/n:>7.1f}% {razao_geral:>7.2f}")

    log("\n== 3. Composicao tematica por termo (top-5 categorias) ==")
    temas = {}
    for termo, rx in compilados.items():
        ids = [i for i, t in textos.items() if rx.search(t)]
        if not ids:
            continue
        pct = {cat: round(100 * sum(1 for i in ids if rot[i][cat] == "1") / len(ids), 1)
               for cat in CATS}
        temas[termo] = pct
        top = sorted(pct.items(), key=lambda kv: -kv[1])[:5]
        log(f"   {termo:<22} " +
            " · ".join(f"{NOMES_CAT[c]} {v}%" for c, v in top))

    log("\n== 4. Leitura ==")
    razoes = [x["razao_pro_anti"] for x in linhas if x["razao_pro_anti"]]
    log(f"   razao pro/anti entre termos: {min(razoes):.2f} a {max(razoes):.2f} "
        f"(corpus inteiro: {razao_geral:.2f})")
    invertem = [x["termo"] for x in linhas if x["razao_pro_anti"] and x["razao_pro_anti"] < 1]
    log(f"   termos em que o lado ANTI e majoritario: {invertem or 'nenhum'}")

    OUT_JSON.write_text(json.dumps({
        "script": "analise/e3_por_termo.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "esquema": "p6 (tres classes)",
        "aviso": "subconjuntos se sobrepoem; nao sao particao",
        "referencia_corpus": {"n": n, "pro": c["pro"], "anti": c["anti"],
                              "nenhum": c["nenhum"],
                              "razao_pro_anti": round(razao_geral, 3)},
        "por_termo": linhas,
        "temas_por_termo": temas,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
