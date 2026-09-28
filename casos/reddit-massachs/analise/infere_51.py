"""
Engenharia reversa da lista dos 51 subreddits do grupo focal (caso Massachs).

Entrada: data/repl/massachs2016/contagem_por_usuario.jsonl (pipeline/contagem_por_usuario.py),
         com os comentarios por subreddit, em 2012 e em 2016, de uma amostra sorteada dos
         44.924 usuarios do grupo focal publicado pelos autores.

Logica
------
Todo usuario do grupo tem >=10 comentarios em 2012 E >=10 em 2016 somados nos 51
subreddits da lista (regra declarada pelos autores). A lista nao foi publicada; o
dataset deixa ver 34 nomes (colunas de interacao). Entao:

1. Com so os 34 conhecidos, quantos usuarios da amostra ja atingem o limiar nos dois anos?
2. Os que NAO atingem ("deficitarios") precisam de subreddits fora dos 34 — que sao,
   por construcao, candidatos aos 17 que faltam. Ranqueamos os subreddits pela
   frequencia entre os deficitarios.
3. Guloso: acrescenta o candidato que mais fecha deficits ate todos atingirem o limiar.
   Se a hipotese estiver certa, basta um conjunto de <=17 subreddits, e eles devem ser
   plausivelmente "similares a r/politics".

Limite: so ha exemplos POSITIVOS (usuarios do grupo). Isso mostra o que a lista precisa
conter, nao o que ela nao contem. Um subreddit a mais na lista so apareceria por usuarios
que entrariam indevidamente, e esses nao estao na amostra.

Uso: PYTHONIOENCODING=utf-8 python -u analise/infere_51.py
"""
import collections
import json
import pathlib

D = pathlib.Path("data/repl/massachs2016")
ENT = D / "contagem_por_usuario.jsonl"
OUT = D / "infere_51.json"
LIMIAR = 10
MAX_FALTANTES = 17

CONHECIDOS = ["AmericanPolitics", "Ask_Politics", "Conservative", "Documentaries",
              "Economics", "Futurology", "GaryJohnson", "Liberal", "Libertarian",
              "NeutralPolitics", "POLITIC", "PoliticalDiscussion", "PoliticalHumor",
              "Republican", "ShitPoliticsSays", "TrueReddit", "WikiLeaks", "atheism",
              "conspiracy", "dataisbeautiful", "democrats", "economy", "inthenews", "law",
              "lostgeneration", "moderatepolitics", "news", "on", "politics",
              "progressive", "todayilearned", "uspolitics", "worldnews", "worldpolitics"]


def soma(cont, lista):
    return sum(cont.get(s, 0) for s in lista)


def main():
    regs = [json.loads(l) for l in ENT.read_text(encoding="utf-8").splitlines()]
    validos = [r for r in regs if r.get("2012") is not None and r.get("2016") is not None]
    vazios = [r for r in validos if not r["2012"] or not r["2016"]]
    print(f"registros {len(regs)}; com as duas contagens {len(validos)}; "
          f"com algum ano vazio (conta apagada?) {len(vazios)}")
    usar = [r for r in validos if r["2012"] and r["2016"]]

    lista = list(CONHECIDOS)

    def deficit(r, lst):
        return [a for a in ("2012", "2016") if soma(r[a], lst) < LIMIAR]

    ok = [r for r in usar if not deficit(r, lista)]
    falta = [r for r in usar if deficit(r, lista)]
    print(f"\n1) so com os 34 conhecidos: {len(ok)}/{len(usar)} "
          f"({100 * len(ok) / len(usar):.1f}%) atingem >=10 nos dois anos")
    anos_def = collections.Counter(a for r in falta for a in deficit(r, lista))
    print(f"   deficitarios: {len(falta)}  (por ano: {dict(anos_def)})")

    # 2) candidatos: subreddits fora dos 34 onde os deficitarios comentam, no ano do deficit
    freq = collections.Counter()
    for r in falta:
        for a in deficit(r, lista):
            for s, c in r[a].items():
                if s not in lista and c > 0:
                    freq[(s)] += 1
    print("\n2) subreddits mais frequentes entre os deficitarios (no ano do deficit):")
    for s, c in freq.most_common(25):
        print(f"   {s:28s} {c}")

    # 3) guloso
    escolhidos = []
    restantes = list(falta)
    while restantes and len(escolhidos) < 40:
        melhor, ganho = None, -1
        cands = {s for r in restantes for a in deficit(r, lista + escolhidos) for s in r[a]
                 if s not in lista + escolhidos}
        for s in cands:
            g = sum(1 for r in restantes if not deficit(r, lista + escolhidos + [s]))
            if g > ganho:
                melhor, ganho = s, g
        if melhor is None or ganho <= 0:
            # nenhum subreddit isolado fecha um deficit: escolhe o de maior soma
            soma_s = collections.Counter()
            for r in restantes:
                for a in deficit(r, lista + escolhidos):
                    for s, c in r[a].items():
                        if s not in lista + escolhidos:
                            soma_s[s] += c
            if not soma_s:
                break
            melhor, ganho = soma_s.most_common(1)[0][0], 0
        escolhidos.append(melhor)
        restantes = [r for r in restantes if deficit(r, lista + escolhidos)]
        print(f"   + {melhor:28s} fecha {ganho:3d}; ainda deficitarios: {len(restantes)}")

    print(f"\n3) guloso: {len(escolhidos)} subreddits alem dos 34 "
          f"(o artigo implica {MAX_FALTANTES}); sem fechar: {len(restantes)}")
    OUT.write_text(json.dumps({
        "n_amostra_valida": len(usar), "n_ano_vazio": len(vazios),
        "ok_so_com_34": len(ok), "deficitarios": len(falta),
        "deficit_por_ano": dict(anos_def),
        "candidatos_top25": freq.most_common(25),
        "guloso": escolhidos, "sem_fechar": len(restantes),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"escrito {OUT}")


if __name__ == "__main__":
    main()
