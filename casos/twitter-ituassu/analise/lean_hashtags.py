"""
Lado declarado das hashtags da janela 19-25/out, por CO-OCORRENCIA com sementes.

Por que existe
--------------
A Camada 1 do artigo ("sinal explicito de preferencia... o uso de uma hashtag,
como, por exemplo, #Aecionever ou #ForaDilma") NAO diz de que lado cada hashtag
esta. O `STANCE_como_o_paper_fez_e_onde_estamos.md` glosou as duas como "contra
Dilma -> EA", e isso esta ERRADO para #Aecionever: ela e PRO-Dilma ("nunca
Aecio"). Este script mede o lado de cada hashtag frequente pelos dados, para que
o codebook nao dependa de intuicao.

Metodo
------
Sementes = hashtags cujo lado e auto-evidente pelo proprio texto da tag
(#EuVotoDilma13, #Aecio45PeloBrasil, ...). Uma hashtag X e contada como "com ED"
num tweet que traz semente ED e NENHUMA semente EA (e vice-versa). O lean e a
fracao entre esses dois. #Aecionever NAO entra nas sementes — e o caso a testar.

Ressalva de circularidade
-------------------------
Esta tabela e CONTEXTO para o anotador humano, nao regra. Se o gold set e o
rotulador automatico usarem a mesma lista, a concordancia entre eles infla sem
que nenhum dos dois esteja certo. Registrado no PRE_REGISTRO_stance.md.

Uso: PYTHONIOENCODING=utf-8 python -u analise/lean_hashtags.py
Saida: stdout + data/repl/compos2014/stance/lean_hashtags.json
"""
import collections
import json
import pathlib
import sqlite3
import unicodedata

D = pathlib.Path("data/repl/compos2014")
OUT = D / "stance" / "lean_hashtags.json"
SNAP = D / "snapshot_hashtag.sqlite"
DIA_INI, DIA_FIM = "2014-10-19", "2014-10-25"

# sementes: lado auto-evidente pelo texto da propria tag
SEED_ED = {"dilma13", "euvotodilma13", "melhorcomdilma13", "querodilmatreze",
           "somostodosdilma", "13rasiltodocomdilma", "dilmaemichel13",
           "dilma13presidenta"}
SEED_EA = {"aecio45", "aecio45pelobrasil", "eaecio45confirma", "euvotoaecio45",
           "aeciopresidente", "votoaeciopelobr45il", "aeciopelobr45il",
           "foradilma", "forapt", "muda45brasil"}

MIN_TOT = 70      # hashtags raras nao entram
MIN_LADEADAS = 15  # abaixo disto o lean nao e reportado


def norm(x):
    if isinstance(x, dict):
        x = x.get("text") or x.get("tag") or ""
    return unicodedata.normalize("NFKD", str(x).lower()).encode("ascii", "ignore").decode()


def main():
    cx = sqlite3.connect(SNAP)
    tot, com_ed, com_ea = collections.Counter(), collections.Counter(), collections.Counter()
    q = ("SELECT hashtags FROM tweets WHERE substr(data_brt,1,10) BETWEEN ? AND ?")
    for (h,) in cx.execute(q, (DIA_INI, DIA_FIM)):
        try:
            hs = json.loads(h) if h else []
        except Exception:
            hs = []
        s = {n for n in (norm(x) for x in hs) if n}
        d, a = bool(s & SEED_ED), bool(s & SEED_EA)
        for x in s:
            tot[x] += 1
            if d and not a:
                com_ed[x] += 1
            if a and not d:
                com_ea[x] += 1
    cx.close()

    out = []
    for k, v in tot.most_common():
        if v < MIN_TOT or k == "eleicoes2014":
            continue
        d, a = com_ed[k], com_ea[k]
        n = d + a
        lado = None
        if n >= MIN_LADEADAS:
            lado = ("ED" if d > a else "EA", round(100 * max(d, a) / n, 1))
        out.append({"hashtag": k, "total": v, "com_ED": d, "com_EA": a,
                    "lado": lado[0] if lado else None,
                    "pureza_pct": lado[1] if lado else None,
                    "semente": "ED" if k in SEED_ED else ("EA" if k in SEED_EA else None)})

    print("%-26s %6s %6s %6s  %s" % ("hashtag", "total", "c/ED", "c/EA", "lado"))
    for r in out:
        lado = "-" if not r["lado"] else "%s %.0f%%" % (r["lado"], r["pureza_pct"])
        sem = "  (semente)" if r["semente"] else ""
        print("%-26s %6d %6d %6d  %s%s"
              % (r["hashtag"], r["total"], r["com_ED"], r["com_EA"], lado, sem))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"janela": [DIA_INI, DIA_FIM], "sementes_ED": sorted(SEED_ED),
         "sementes_EA": sorted(SEED_EA), "min_total": MIN_TOT,
         "min_ladeadas": MIN_LADEADAS, "hashtags": out},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nescrito em " + str(OUT))


if __name__ == "__main__":
    main()
