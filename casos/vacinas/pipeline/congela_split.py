"""
Eixo B / passo 2 — Congela o split dev/teste do gabarito (PRE-REGISTRO).

Roda UMA VEZ, ANTES de qualquer chamada de API. O conjunto de desenvolvimento
e o unico onde se pode olhar o resultado e ajustar o prompt; o conjunto de
teste fica cego ate o rotulador estar congelado. Sem esta separacao feita
antes, o kappa reportado mede overfitting ao proprio teste e nao vale nada na
banca.

Estratificacao: stance (pro/anti/nenhum) x categoria mais rara presente no
tweet. A segunda dimensao existe porque Religiao (n=46) e Outras drogas (n=32)
sumiriam de um dos lados num sorteio simples — e sao justamente as categorias
onde o rotulador tem mais chance de falhar.

Uso:
    PYTHONIOENCODING=utf-8 python -u pipeline/congela_split.py
    (--refazer para sobrescrever um split ja congelado — exige confirmacao)

Gera em data/repl/vacinas2022/:
  - split_dev_teste.csv     (ID, particao, stance, estrato)
  - PRE_REGISTRO_split.md   (seed, hash, criterio de aceite, aposta registrada)
"""
import argparse
import hashlib
import json
import pathlib
import random
import sys
from collections import Counter, defaultdict

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "data" / "repl" / "vacinas2022"
XLSX = SAIDA / "suplementar_rotulos.xlsx"
CODEBOOK = SAIDA / "codebook_v1.json"
CSV = SAIDA / "split_dev_teste.csv"
MD = SAIDA / "PRE_REGISTRO_split.md"

# Seed fixa e publicada: quem replicar reproduz exatamente este split.
SEED = 20260726
FRACAO_DEV = 1 / 3  # ~508 dev / ~1017 teste, na faixa dos ~500/~1000 do plano

CRITERIO_ACEITE = {
    "stance_kappa_min": 0.70,
    "categorias_kappa_mediana_min": 0.60,
}


def stance_de(linha):
    if linha["Tweet_ProVax"] == 1:
        return "pro"
    if linha["Tweet_AntiVax"] == 1:
        return "anti"
    return "nenhum"


def monta_estratos(gab, categorias):
    """
    Estrato = stance + a categoria MAIS RARA presente no tweet (ou 'sem_cat').
    Amarrar pela mais rara e o que garante que Religiao/Outras drogas caiam
    proporcionalmente nos dois lados.
    """
    # da mais rara para a mais comum
    ordem = sorted(categorias, key=lambda c: c["total_publicado"])
    estratos = []
    for _, linha in gab.iterrows():
        rara = "sem_cat"
        for c in ordem:
            if linha[c["coluna"]] == 1:
                rara = c["nome_en"]
                break
        estratos.append(f"{stance_de(linha)}|{rara}")
    return estratos


def divide(gab, estratos, seed=SEED, fracao_dev=FRACAO_DEV):
    """
    Sorteio estratificado deterministico. Dentro de cada estrato embaralha com
    a seed e manda os primeiros round(n*fracao) para dev. Estratos com 1 unico
    tweet vao inteiros para o TESTE (nao gastamos raridade em calibracao).
    """
    rng = random.Random(seed)
    por_estrato = defaultdict(list)
    for id_tweet, estrato in zip(gab["ID"], estratos):
        por_estrato[estrato].append(id_tweet)

    particao = {}
    for estrato in sorted(por_estrato):  # sorted: independe da ordem do dict
        ids = sorted(por_estrato[estrato])
        rng.shuffle(ids)
        n_dev = 0 if len(ids) < 2 else round(len(ids) * fracao_dev)
        for i, id_tweet in enumerate(ids):
            particao[id_tweet] = "dev" if i < n_dev else "teste"
    return particao


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true",
                    help="sobrescreve um split ja congelado (quebra o pre-registro)")
    args = ap.parse_args()

    if CSV.exists() and not args.refazer:
        raise SystemExit(
            f"[erro] split ja congelado em {CSV}.\n"
            "       Refazer o split DEPOIS de olhar o teste invalida o kappa.\n"
            "       Use --refazer so se nenhuma chamada de API foi feita ainda."
        )
    if not CODEBOOK.exists():
        raise SystemExit(f"[erro] rode antes: python pipeline/extrai_codebook.py")

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    categorias = codebook["categorias"]
    gab = pd.read_excel(XLSX, "Spreadsheet 1")

    estratos = monta_estratos(gab, categorias)
    particao = divide(gab, estratos)

    df = pd.DataFrame({
        "ID": gab["ID"],
        "particao": [particao[i] for i in gab["ID"]],
        "stance": [stance_de(l) for _, l in gab.iterrows()],
        "estrato": estratos,
    })
    df.to_csv(CSV, index=False, encoding="utf-8")
    sha = hashlib.sha256(CSV.read_bytes()).hexdigest()

    n_dev = int((df.particao == "dev").sum())
    n_teste = int((df.particao == "teste").sum())

    # cobertura por categoria nos dois lados — o que justifica a estratificacao
    cobertura = []
    for c in categorias:
        marca = gab.set_index("ID")[c["coluna"]]
        d = int(sum(marca[i] for i in df[df.particao == "dev"].ID))
        t = int(sum(marca[i] for i in df[df.particao == "teste"].ID))
        cobertura.append((c["numero"], c["nome_en"], c["total_publicado"], d, t))

    L = [
        "# Pre-registro do split dev/teste — eixo B (rotulador de conteudo)",
        "",
        "> **Congelado ANTES de qualquer chamada a API.** Este arquivo e o",
        "> compromisso: o conjunto de teste so foi olhado depois que o prompt",
        "> do rotulador ficou congelado. Refazer o split depois disso invalida",
        "> o kappa reportado.",
        "",
        "## Parametros (reprodutiveis)",
        "",
        f"- Gabarito: `suplementar_rotulos.xlsx` / aba `Spreadsheet 1` "
        f"({len(df)} tweets virais >500 RT)",
        f"- Codebook: `codebook_{codebook['versao']}.json` "
        f"({len(categorias)} categorias amplas)",
        f"- Seed: `{SEED}` | fracao dev: `{FRACAO_DEV:.4f}`",
        f"- Estratificacao: stance x categoria mais rara presente "
        f"({len(set(estratos))} estratos)",
        f"- Estratos de tamanho 1 vao inteiros para o TESTE",
        "",
        "## Resultado",
        "",
        f"- **dev = {n_dev}** (ajuste de prompt permitido)",
        f"- **teste = {n_teste}** (cego ate o rotulador congelar)",
        f"- `split_dev_teste.csv` SHA-256: `{sha}`",
        "",
        "| Stance | dev | teste |",
        "|---|---:|---:|",
    ]
    for s in ("pro", "anti", "nenhum"):
        L.append(f"| {s} | {int(((df.particao=='dev')&(df.stance==s)).sum())} | "
                 f"{int(((df.particao=='teste')&(df.stance==s)).sum())} |")
    L += [
        "",
        "### Cobertura por categoria (nenhuma categoria fica fora de um dos lados)",
        "",
        "| # | Categoria | Total | dev | teste |",
        "|---|---|---:|---:|---:|",
    ]
    for numero, nome, total, d, t in cobertura:
        L.append(f"| {numero} | {nome} | {total} | {d} | {t} |")
    L += [
        "",
        "## Criterio de aceite (registrado antes de rodar)",
        "",
        f"- kappa de Cohen do **stance** >= **{CRITERIO_ACEITE['stance_kappa_min']:.2f}**",
        f"- **mediana** dos kappas das {len(categorias)} categorias >= "
        f"**{CRITERIO_ACEITE['categorias_kappa_mediana_min']:.2f}**",
        "- Ambos medidos **no teste cego**, uma unica vez.",
        "- Se reprovar: nao se ajusta o prompt contra o teste. Ou se volta ao dev,",
        "  ou se troca de modelo (Sonnet), ou se reporta a reprovacao e o eixo B",
        "  fica limitado ao estrato ja rotulado a mao pelo paper.",
        "",
        "## Aposta pre-registrada (principio da rastreabilidade do projeto)",
        "",
        "- Stance passa folgado (tarefa binaria, sinal forte no texto).",
        "- A mediana das categorias passa, mas as categorias raras",
        "  (Religion n=46, Other drugs n=32, Vaccines type/labs n=86) ficam",
        "  abaixo do corte individualmente — e esse e um achado a favor da tese:",
        "  analise composta exige mais dados do que parece.",
        "- Categorias agregadas amplas (Politics n=719, Children n=592) devem ter",
        "  os melhores kappas.",
        "",
        "> Reportar honestamente se a aposta falhar.",
    ]
    MD.write_text("\n".join(L), encoding="utf-8")

    print(f"[ok] dev={n_dev} teste={n_teste} ({len(set(estratos))} estratos)")
    contagem = Counter(df.particao)
    print(f"[ok] stance no dev: "
          f"{dict(Counter(df[df.particao=='dev'].stance))}")
    print(f"[ok] stance no teste: "
          f"{dict(Counter(df[df.particao=='teste'].stance))}")
    for numero, nome, total, d, t in cobertura:
        if d == 0 or t == 0:
            print(f"[aviso] categoria {numero} ({nome}) sem cobertura: dev={d} teste={t}")
    print(f"[ok] escrito: {CSV}  (sha256 {sha[:16]}...)")
    print(f"[ok] escrito: {MD}")


if __name__ == "__main__":
    sys.exit(main())
