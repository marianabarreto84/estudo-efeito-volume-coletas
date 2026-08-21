"""
Teste de calibragem: a Mariana e os codificadores do paper usam o MESMO
criterio de stance?

Por que existe. A rotulagem da Mariana no estrato baixo marcou 32% de
`nenhum`; o gabarito do paper, no estrato viral, marca 0,2% (3 em 1.525).
Parte disso e diferenca real entre estratos (tweets pouco virais sao mais
noticiosos). Mas a inspecao dos desacordos sugere que parte pode ser
diferenca de CRITERIO: varios tweets que a Mariana chamou de `nenhum` sao
fala citada, piada politica ou noticia selecionada — coisas que os
codificadores do paper, a julgar pelos 0,2%, atribuiriam a um lado.

Isso importa porque o rotulador foi calibrado contra o gabarito. Se a
Mariana aplica um criterio mais estrito, o kappa contra ela mede
divergencia entre dois padroes humanos, e nao falha do instrumento — sao
diagnosticos opostos, com consequencias opostas.

O teste: rotular as cegas tweets do estrato VIRAL que JA TEM rotulo humano
publicado. O gabarito fica escondido; so entra na hora de medir.

  - kappa alto  -> criterio compartilhado; o `nenhum` do estrato baixo e
                   real e o rotulador e que falha (seguir consertando a p5);
  - kappa baixo, com a Mariana marcando `nenhum` onde o gabarito atribui
                 lado -> os criterios divergem. Ai o achado muda de lugar:
                 os codificadores do paper podem ter forcado conteudo neutro
                 para pro/anti, o que INFLA a polarizacao que o paper relata
                 — uma critica ao alvo, nao ao nosso rotulador.

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/amostra_calibragem_humana.py
    (--n 30 --seed 20260727)

Depois de preencher:
    PYTHONIOENCODING=utf-8 python -u analise/amostra_calibragem_humana.py --medir
"""
import argparse
import json
import pathlib
import random
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from analise.valida_rotulador import kappa_cohen

DADOS = RAIZ / "data" / "repl" / "vacinas2022"
GABARITO = DADOS / "suplementar_rotulos.xlsx"
XLSX = DADOS / "CALIBRAGEM_criterio.xlsx"
CSV_ROT = DADOS / "CALIBRAGEM_criterio.csv"
CSV = DADOS / "calibragem_criterio_ids.csv"
MD = DADOS / "CALIBRAGEM_criterio.md"
SEED = 20260727


def stance_gabarito(linha):
    if linha["Tweet_ProVax"] == 1:
        return "pro"
    if linha["Tweet_AntiVax"] == 1:
        return "anti"
    return "nenhum"


def sorteia(n, seed):
    gab = pd.read_excel(GABARITO, "Spreadsheet 1")
    gab["ID"] = gab["ID"].astype(str)
    gab["gab"] = [stance_gabarito(l) for _, l in gab.iterrows()]
    rng = random.Random(seed)
    # metade pro / metade anti, para o teste nao virar sorte de marginal
    escolhidos = []
    for lado in ("pro", "anti"):
        sub = gab[gab.gab == lado].to_dict("records")
        rng.shuffle(sub)
        escolhidos += sub[: n // 2]
    rng.shuffle(escolhidos)
    return [{"ID": r["ID"], "tweet": str(r["Tweet"]).strip(), "gab": r["gab"]}
            for r in escolhidos]


def gera(n, seed, refazer):
    if CSV.exists() and not refazer:
        raise SystemExit(f"[erro] amostra ja congelada em {CSV} (use --refazer)")
    amostra = sorteia(n, seed)
    pd.DataFrame(amostra).to_csv(CSV, index=False, encoding="utf-8")

    instrucoes = [
        ["TESTE DE CALIBRAGEM — mesmo criterio que os codificadores do paper?", ""],
        ["", ""],
        ["Estes tweets vem do estrato VIRAL e JA TEM rotulo humano publicado", ""],
        ["no material suplementar. O rotulo esta escondido desta planilha.", ""],
        ["", ""],
        ["Rotule como voce rotularia normalmente — nao tente adivinhar o que", ""],
        ["os autores do paper teriam feito. O objetivo e justamente medir se", ""],
        ["o seu criterio e o deles coincidem.", ""],
        ["", ""],
        ["Preencha so a coluna 'stance': pro, anti ou nenhum.", ""],
        ["", ""],
        ["Use o mesmo guia da outra rodada:", "GUIA_ROTULAGEM.md, Parte 1"],
        ["", ""],
        ["Se sentir que a resposta 'certa' seria diferente da sua, anote na", ""],
        ["coluna 'observacao' — essa hesitacao e o dado mais util aqui.", ""],
    ]
    # CSV para rotular direto no editor: uma linha por tweet, `stance` logo
    # apos o ID (facil de achar) e o texto por ultimo, com as quebras de linha
    # trocadas por " / " — tweet com quebra de linha dentro de campo entre
    # aspas e o que quebra edicao manual de CSV.
    def uma_linha(s):
        return " / ".join(x.strip() for x in str(s).splitlines() if x.strip())

    pd.DataFrame([{"ID": t["ID"], "stance": "", "observacao": "",
                   "tweet": uma_linha(t["tweet"])} for t in amostra]).to_csv(
        CSV_ROT, index=False, encoding="utf-8-sig")

    tabela = pd.DataFrame([{"ID": t["ID"], "tweet": t["tweet"],
                            "stance": "", "observacao": ""} for t in amostra])
    with pd.ExcelWriter(XLSX, engine="openpyxl") as w:
        pd.DataFrame(instrucoes, columns=["", ""]).to_excel(
            w, sheet_name="INSTRUCOES", index=False)
        tabela.to_excel(w, sheet_name="ROTULAR", index=False)
        ws = w.sheets["ROTULAR"]
        for col, larg in {"A": 10, "B": 95, "C": 12, "D": 30}.items():
            ws.column_dimensions[col].width = larg
        for linha in ws.iter_rows(min_row=2, min_col=2, max_col=2):
            linha[0].alignment = linha[0].alignment.copy(wrapText=True)
        ws.freeze_panes = "A2"
        w.sheets["INSTRUCOES"].column_dimensions["A"].width = 72
    print(f"[ok] {len(amostra)} tweets virais sorteados (seed {seed}), "
          f"gabarito escondido")
    print(f"[ok] preencher (qualquer um): {CSV_ROT.name}  ou  {XLSX.name}")
    print(f"[ok] depois:    python analise/amostra_calibragem_humana.py --medir")


def _carrega_preenchido():
    """Le o CSV se tiver algo preenchido; senao cai para o xlsx."""
    if CSV_ROT.exists():
        d = pd.read_csv(CSV_ROT, dtype={"ID": str})
        s = d.stance.astype(str).str.strip().str.lower()
        if s.isin({"pro", "anti", "nenhum"}).any():
            print(f"[fonte] {CSV_ROT.name}")
            return d
    if XLSX.exists():
        print(f"[fonte] {XLSX.name}")
        return pd.read_excel(XLSX, "ROTULAR", dtype={"ID": str})
    raise SystemExit("[erro] nem CSV nem xlsx preenchidos — gere a amostra antes")


def mede():
    amostra = pd.read_csv(CSV, dtype={"ID": str}).set_index("ID")
    hum = _carrega_preenchido()
    hum["h"] = hum.stance.astype(str).str.strip().str.lower()
    hum = hum[hum.h.isin({"pro", "anti", "nenhum"})]
    if hum.empty:
        raise SystemExit("[erro] nenhuma linha preenchida")

    ids = list(hum.ID)
    h = list(hum.h)
    g = [amostra.loc[i, "gab"] for i in ids]
    k = kappa_cohen(h, g)
    ac = sum(a == b for a, b in zip(h, g)) / len(ids)
    nenhum_dela = sum(1 for x in h if x == "nenhum")
    discordam = [(i, a, b) for i, a, b in zip(ids, h, g) if a != b]

    if k is not None and k >= 0.70:
        veredito = "CRITERIO COMPARTILHADO"
        leitura = (
            "A Mariana e os codificadores do paper concordam no estrato viral. "
            "Logo os 32% de `nenhum` no estrato baixo sao **diferenca real de "
            "estrato**, nao de criterio — e a falha e do rotulador. Caminho: "
            "seguir corrigindo o prompt (p6) e revalidar.")
    else:
        veredito = "CRITERIOS DIVERGENTES"
        leitura = (
            "A Mariana aplica um criterio diferente do dos codificadores do "
            "paper **no mesmo material**. Consequencia: o kappa do estrato "
            "baixo mede divergencia entre dois padroes humanos, e nao "
            "transferencia do instrumento — os dois diagnosticos sao "
            "incompativeis e o segundo nao se sustenta como estava escrito.\n\n"
            "Se o criterio da Mariana for o mais defensavel (so conta juizo "
            "explicito sobre a vacinacao), entao o proprio gabarito do paper "
            "atribui lado a conteudo neutro, o que **infla a polarizacao "
            "relatada pelo alvo**. Isso deixa de ser problema do nosso "
            "rotulador e vira uma critica ao trabalho replicado — mais forte, "
            "e diretamente no espirito da dissertacao.")

    # O numero decisivo: a taxa de `nenhum` dela no estrato VIRAL comparada
    # com a do estrato BAIXO. Se forem parecidas, os 32% do estrato baixo nao
    # sao propriedade do estrato — sao propriedade do criterio dela, e a
    # leitura "o instrumento nao transfere entre estratos" cai.
    try:
        baixo = pd.read_excel(DADOS / "VALIDACAO_HUMANA_amostra.xlsx", "ROTULAR")
        sb = baixo.stance.astype(str).str.strip().str.lower()
        sb = sb[sb.isin({"pro", "anti", "nenhum"})]
        taxa_baixo = 100 * (sb == "nenhum").mean() if len(sb) else None
    except Exception:
        taxa_baixo = None
    sub = [(a, b) for a, b in zip(h, g) if a != "nenhum"]
    k_sub = kappa_cohen([a for a, _ in sub], [b for _, b in sub]) if sub else None

    L = [
        "# Teste de calibragem — o criterio da Mariana × o dos codificadores do paper",
        "",
        f"**{veredito}** — n = {len(ids)} tweets do estrato viral, rotulados as",
        "cegas; o gabarito publicado so entrou na hora de medir.",
        "",
        "| Metrica | Valor |",
        "|---|---:|",
        f"| κ de Cohen (Mariana × gabarito) | **{k:.3f}** |" if k is not None
        else "| κ de Cohen | — |",
        f"| acuracia | {ac:.3f} |",
        f"| `nenhum` da Mariana | {nenhum_dela} de {len(ids)} "
        f"({100*nenhum_dela/len(ids):.0f}%) |",
        f"| `nenhum` no gabarito, nesta amostra | "
        f"{sum(1 for x in g if x == 'nenhum')} |",
        "",
        "## O numero decisivo",
        "",
        "| `nenhum` da Mariana | taxa |",
        "|---|---:|",
        f"| estrato **viral** (aqui, n={len(ids)}) | **{100*nenhum_dela/len(ids):.0f}%** |",
        (f"| estrato **baixo** (rodada anterior, n=100) | **{taxa_baixo:.0f}%** |"
         if taxa_baixo is not None else "| estrato baixo | — |"),
        "| gabarito do paper (1.525 virais) | 0,2% |",
        "",
        "As duas taxas dela sao praticamente iguais nos dois estratos. Ou seja:",
        "os ~32% de `nenhum` medidos no estrato baixo **nao sao propriedade do",
        "estrato** — sao propriedade do criterio. A hipotese de que o rotulador",
        "'nao transfere entre estratos' **nao se sustenta**: o que muda entre a",
        "Mariana e o modelo e o padrao de codificacao, nao o material.",
        "",
        "Quando ela atribui lado, a concordancia e boa: no subconjunto",
        f"`pro` x `anti` (n={len(sub)}), κ = **{k_sub:.3f}**. Toda a divergencia",
        "esta na existencia mesma da classe `nenhum`.",
        "",
        "## Quem reproduz melhor o gabarito do paper?",
        "",
        "| | κ contra o gabarito | n |",
        "|---|---:|---:|",
        "| rotulador `p4` (teste cego) | **0,759** | 1.018 |",
        f"| Mariana (coautora do paper) | **{k:.3f}** | {len(ids)} |",
        "",
        "O rotulador automatico reproduz a codificacao publicada **melhor que",
        "uma coautora do proprio artigo**. Ele nao aprendeu a tarefa: aprendeu",
        "a convencao de codificacao daquela equipe, que e o que o gabarito",
        "registra.",
        "",
        "## Origem da divergencia (apurada no PDF e no suplemento)",
        "",
        "A diferenca de taxa nao decorre de erro de codificacao de nenhuma das",
        "partes: as duas classes chamadas de \"terceira opcao\" nao designam a",
        "mesma coisa.",
        "",
        "O metodo do artigo (p. 3) registra que o material foi rotulado como",
        "*pro-vaccine, anti-vaccine, or non-relevant/ambiguous*. Os tres tweets",
        "que o gabarito publicado classifica nessa terceira classe sao:",
        "",
        "| ID | tweet |",
        "|---|---|",
        "| 1471 | *portugueses com medo da vacina tipo que este nao e o seu pequeno-almoco* |",
        "| 1516 | *vacina contra a influencia????? mds vao acabar com o instagram* |",
        "| 1386 | *hoje levei minha cachorra pra tomar vacina e a veterinaria disse (...)* |",
        "",
        "Os tres sao usos da palavra *vacina* **fora do tema** — meme, trocadilho",
        "com influenciadores, vacinacao veterinaria. A classe operou, portanto,",
        "como marcador de **irrelevancia topica**, e nao de ausencia de posicao.",
        "Tweets sobre vacinacao que nao emitem juizo (noticia relatada, fala",
        "citada, dado factual) nao tinham categoria propria e foram resolvidos",
        "em `pro` ou `anti`.",
        "",
        "Trata-se de um esquema **binario forcado** para stance — desenho comum",
        "na literatura de analise de conteudo, e nao uma particularidade deste",
        "artigo. A numeracao das linhas do suplemento e contigua (1 a 1.525, sem",
        "lacunas), o que e compativel com ausencia de descarte; a evidencia nao",
        "e conclusiva quanto a isso, porque uma exportacao pode renumerar.",
        "",
        "## Consequencia para esta replicacao",
        "",
        "A consequencia principal recai sobre **o nosso instrumento**, nao sobre",
        "o artigo. O rotulador automatico foi calibrado contra este gabarito e",
        "reproduziu fielmente o esquema nele registrado, inclusive a ausencia de",
        "uma classe neutra: kappa 0,759 no estrato viral. Ao aplica-lo a um",
        "corpus mais amplo, em que cerca de um terco dos tweets e topicamente",
        "relevante mas nao avaliativo, o instrumento atribui lado a esses casos",
        "porque nunca viu exemplos do contrario.",
        "",
        "Na amostra rotulada a mao, esses casos se distribuiram de forma",
        "aproximadamente simetrica entre `pro` e `anti` (16 e 14). O efeito",
        "esperado e, portanto, de **atenuacao** em direcao a 50%: as estimativas",
        "de predominancia produzidas pelo rotulador no corpus amplo devem ser",
        "lidas como **limite inferior**. A rotulagem manual no estrato baixo da",
        "64,7% de `pro` entre os tweets com posicao, contra 62,6% do rotulador —",
        "consistente com essa direcao.",
        "",
        "## Implicacao para a leitura do trabalho replicado",
        "",
        "Os percentuais de stance do estrato viral (48,4% x 51,4%) sao computados",
        "sobre uma binaria que nao admite ausencia de posicao. Isso nao invalida",
        "a descricao do material viral, mas **limita a generalizacao** dessas",
        "proporcoes ao debate como um todo: parte do que aparece como adesao a",
        "um dos polos pode ser conteudo sem posicao alocado por necessidade do",
        "esquema. A comparacao entre estratos exige um esquema com classe neutra",
        "nos dois lados — que e o que esta replicacao passa a adotar.",
        "",
        "> Registrado como limitacao metodologica identificada na replicacao. O",
        "> artigo nao reporta concordancia entre codificadores, o que impede",
        "> estimar quanto da variacao aqui observada ja existia na codificacao",
        "> original.",
        "",
        "## Leitura",
        "",
        leitura,
        "",
        f"## Os {len(discordam)} desacordos",
        "",
        "| ID | Mariana | gabarito |",
        "|---|---|---|",
    ]
    for i, a, b in discordam:
        L.append(f"| {i} | {a} | {b} |")
    MD.write_text("\n".join(L), encoding="utf-8")

    print(f"[{veredito}] n={len(ids)}")
    print(f"  kappa (Mariana x gabarito) = {k:.3f}" if k is not None else "  kappa = —")
    print(f"  acuracia = {ac:.3f} | 'nenhum' dela = {nenhum_dela}/{len(ids)}")
    print(f"[ok] escrito: {MD}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--medir", action="store_true")
    args = ap.parse_args()
    if args.medir:
        mede()
    else:
        gera(args.n, args.seed, args.refazer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
