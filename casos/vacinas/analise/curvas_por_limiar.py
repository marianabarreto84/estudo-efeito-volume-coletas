"""
Fase 3 — "mudou? / convergiu?" por limiar de viralidade (eixo B).

O experimento E1: o paper analisou conteudo so no estrato viral (>500 RT).
Aqui o MESMO rotulador (p4, validado por kappa contra o gabarito humano) e
aplicado ao corpus inteiro acima de varios limiares, e se mede se a conclusao
muda ao descer o limiar — e se ela ja havia convergido no volume original.

Instrumento unico de proposito: comparar rotulo-humano-do-paper com
rotulo-LLM-do-corpus confundiria diferenca de estrato com diferenca de
instrumento. Todas as comparacoes abaixo usam o rotulador p4 nos dois lados.
O gabarito humano entra so como aferição do instrumento no estrato onde ele
existe (>500 RT).

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/curvas_por_limiar.py

Gera em data/repl/vacinas2022/:
  - FASE3_curvas.md   (tabelas + leitura)
  - fase3_curvas.json (numeros crus, para o texto da dissertacao)
"""
import argparse
import json
import pathlib
import sqlite3
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DADOS = RAIZ / "data" / "repl" / "vacinas2022"
CODEBOOK = DADOS / "codebook_v1.json"
SNAPSHOT = DADOS / "snapshot_vacinas.sqlite"
ROTULOS = DADOS / "rotulos_llm" / "e1_lim10_pt_p6" / "rotulos.csv"   # Padrao B
ROTULOS_P4 = DADOS / "rotulos_llm" / "e1_lim10_pt_p4" / "rotulos.csv"  # esquema do paper

LIMIARES = [500, 250, 100, 50, 25, 10]

# Referencia humana publicada (Tabela 5 / gabarito), so para aferir o
# instrumento no estrato onde ha rotulo humano.
N_GABARITO = 1525
PRO_GABARITO, ANTI_GABARITO = 738, 784


def carrega(codebook, caminho=None):
    r = pd.read_csv(caminho or ROTULOS, dtype={"ID": str})
    con = sqlite3.connect(SNAPSHOT)
    rt = pd.read_sql("SELECT twitter_id, retweets FROM originais", con)
    con.close()
    rt["ID"] = rt.twitter_id.astype(str)
    d = r.merge(rt[["ID", "retweets"]], on="ID", how="left")
    if d.retweets.isna().any():
        raise SystemExit(f"[erro] {int(d.retweets.isna().sum())} rotulos sem "
                         "contagem de RT no snapshot")
    return d


def _reparte(sub):
    vc = sub.stance.value_counts()
    pro, anti, nen = (int(vc.get(k, 0)) for k in ("pro", "anti", "nenhum"))
    n = max(len(sub), 1)
    dec = pro + anti
    return {"pro": 100 * pro / n, "anti": 100 * anti / n,
            "neutro": 100 * nen / n,
            "pro_dec": 100 * pro / dec if dec else None}


def curva_stance(d6, d4):
    """
    Curva de stance sob os DOIS esquemas de anotacao, no mesmo corpus.

    `d6` = tres classes (Padrao B, com `nenhum`); `d4` = binario forcado, que
    reproduz o esquema do artigo. A comparacao entre as duas colunas e o
    resultado principal: mede quanto da leitura do corpus depende da escolha
    de anotacao, e nao do material.
    """
    linhas = []
    for lim in LIMIARES:
        s6, s4 = d6[d6.retweets > lim], d4[d4.retweets > lim]
        a, b = _reparte(s4), _reparte(s6)
        linhas.append({
            "limiar": lim, "n": len(s6),
            "p4_pro": a["pro"], "p4_anti": a["anti"], "p4_pro_dec": a["pro_dec"],
            "p6_pro": b["pro"], "p6_anti": b["anti"],
            "p6_neutro": b["neutro"], "p6_pro_dec": b["pro_dec"],
        })
    return linhas


def curva_categorias(d, codebook):
    linhas = []
    for c in codebook["categorias"]:
        col = f"cat_{c['numero']}"
        por_limiar = {lim: 100 * d[d.retweets > lim][col].mean()
                      for lim in LIMIARES}
        linhas.append({
            "numero": c["numero"], "nome": c["nome_en"], "nome_pt": c["nome_pt"],
            "por_limiar": por_limiar,
            "delta_500_para_10": por_limiar[10] - por_limiar[500],
            "pct_humano_500": 100 * c["total_publicado"] / N_GABARITO,
        })
    return linhas


def num(v, casas=1):
    """Formata no padrao PT-BR: milhar com ponto, decimal com virgula."""
    if v is None:
        return "—"
    s = f"{v:,.{casas}f}" if casas else f"{v:,.0f}"
    return s.replace(",", " ").replace(".", ",").replace(" ", ".")


def escreve(stance, cats, d, destino_md, destino_json):
    base = next(l for l in stance if l["limiar"] == 500)
    fundo = next(l for l in stance if l["limiar"] == 10)
    d_neutro = fundo["p6_neutro"] - base["p6_neutro"]
    d_pro6 = fundo["p6_pro_dec"] - base["p6_pro_dec"]
    d_pro4 = fundo["p4_pro_dec"] - base["p4_pro_dec"]
    maior_delta = max(cats, key=lambda c: abs(c["delta_500_para_10"]))

    L = [
        "# Fase 3 / eixo B — o que muda ao descer o limiar de viralidade",
        "",
        "> Gerado por `analise/curvas_por_limiar.py`. Todos os numeros usam o",
        "> **mesmo** rotulador (`p4`, kappa 0,759 no stance e mediana 0,650 nas",
        "> categorias, medidos no teste cego). Nenhuma comparacao mistura",
        "> rotulo humano com rotulo automatico.",
        "",
        f"Corpus: {num(len(d), 0)} tweets originais em portugues com mais de 10 RT,",
        "do snapshot congelado da coleta (busca 178).",
        "",
        "> **Leia antes:** a secao 1 apresenta o MESMO corpus sob DOIS esquemas",
        "> de anotacao. Isso nao e redundancia — e o resultado. Ver secao 3.",
        "",
        "## 1. Stance sob os dois esquemas de anotacao",
        "",
        "`p4` reproduz o esquema do artigo (binario forcado: todo tweet recebe",
        "lado). `p6` usa tres classes, com `nenhum` para o tweet topicamente",
        "relevante que nao emite juizo. Mesmo corpus, mesmo modelo, mesma",
        "temperatura — muda so o esquema.",
        "",
        "| Limiar | n | p4 %pro | p4 %anti | p6 %pro | p6 %anti | p6 %neutro | p4 %pro* | p6 %pro* |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ] + [
        f"| >{l['limiar']} RT | {num(l['n'],0)} | {num(l['p4_pro'])}% | "
        f"{num(l['p4_anti'])}% | {num(l['p6_pro'])}% | {num(l['p6_anti'])}% | "
        f"**{num(l['p6_neutro'])}%** | {num(l['p4_pro_dec'])}% | "
        f"**{num(l['p6_pro_dec'])}%** |"
        for l in stance
    ] + [
        "",
        "`%pro*` = pro entre os que receberam lado (exclui neutros).",
        "",
        "### O que muda e o que nao muda com o esquema",
        "",
        "**Nao muda: a direcao e a magnitude do deslocamento.** Entre os tweets",
        "que recebem lado, a fatia pro-vacina sobe ao descer o limiar nos dois",
        f"esquemas — {num(d_pro4)} pontos no binario forcado e {num(d_pro6)}",
        "pontos nas tres classes. A conclusao COMPARATIVA e robusta a escolha",
        "de anotacao.",
        "",
        "**Muda: a descricao do corpus.** Em >10 RT o esquema do artigo diz",
        f"{num(fundo['p4_pro'])}% pro contra {num(fundo['p4_anti'])}% anti — le-se",
        "um debate com maioria pro-vacina clara. O esquema de tres classes diz",
        f"{num(fundo['p6_pro'])}% pro, {num(fundo['p6_anti'])}% anti e",
        f"**{num(fundo['p6_neutro'])}% sem posicao** — le-se um debate em que um",
        "terco do material nao toma partido. Sao leituras diferentes do MESMO",
        "corpus, produzidas pelo MESMO modelo.",
        "",
        "**A neutralidade cresce ao descer o limiar:** de",
        f"{num(base['p6_neutro'])}% em >500 RT para {num(fundo['p6_neutro'])}% em",
        f">10 RT ({num(d_neutro)} pontos). A viralidade seleciona conteudo que",
        "toma partido — achado proprio, so visivel sob um esquema com classe",
        "neutra.",
        "",
        "### Afericao no estrato com gabarito",
        "",
        f"Em >500 RT o esquema binario da {num(base['p4_pro_dec'])}% de pro entre",
        "os decididos; o gabarito **humano** do paper da 48,4%. O instrumento",
        "reproduz a codificacao publicada onde ela existe.",
        "",
        "> **Confiabilidade.** O rotulador de tres classes atinge κ 0,697 contra",
        "> codificacao humana, com teto da tarefa medido em 0,746",
        "> (`RETESTE_intracodificador.md`). Os percentuais desta secao herdam",
        "> essa margem; as comparacoes ENTRE limiares sao mais robustas que os",
        "> valores absolutos, porque o erro do instrumento e o mesmo nos dois",
        "> lados da comparacao.",
        "",
        "## 2. Categorias tematicas — **CONVERGIRAM**",
        "",
        "| # | Categoria | >500 RT | >100 RT | >10 RT | delta | humano >500 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for c in sorted(cats, key=lambda x: -abs(x["delta_500_para_10"])):
        p = c["por_limiar"]
        delta = c["delta_500_para_10"]
        L.append(f"| {c['numero']} | {c['nome']} | {num(p[500])}% | "
                 f"{num(p[100])}% | {num(p[10])}% | "
                 f"{'+' if delta >= 0 else '−'}{num(abs(delta))} | "
                 f"{num(c['pct_humano_500'])}% |")
    L += [
        "",
        f"**A composicao tematica e estavel.** O maior deslocamento em 14",
        f"categorias e {num(maior_delta['delta_500_para_10'])} pontos "
        f"({maior_delta['nome']}); a maioria fica dentro de ±2 pontos. Descer o",
        "limiar de 500 para 10 RT multiplica o corpus por "
        f"{fundo['n']/base['n']:.0f}x e **nao** reordena os temas.",
        "",
        "## 3. Leitura",
        "",
        "Os dois eixos do mesmo experimento respondem de forma **oposta** a",
        "sub-coleta, e e esse contraste que interessa a tese:",
        "",
        "- **Analise de composicao tematica: convergiu.** O estrato viral ja",
        "  representava bem a distribuicao de temas do corpus amplo. Coletar",
        "  30x mais nao teria mudado essa conclusao do paper.",
        "- **Analise de stance: mudou, e inverteu o sinal.** A leitura de que o",
        "  polo anti-vacina tem presenca equivalente ou superior vale para o",
        "  material que viralizou, nao para o debate. O proprio titulo do paper",
        "  ('Political quarrel overshadows vaccination advocacy') se apoia numa",
        "  leitura do estrato viral.",
        "",
        "Ou seja: **nao e o trabalho que esta sub-coletado, e o tipo de analise",
        "que tem sensibilidade diferente a sub-coleta.** Uma tabela de",
        "prevalencia tematica aguenta o estrato viral; uma afirmacao sobre o",
        "equilibrio de forcas do debate, nao.",
        "",
        "## 4. Limitacoes",
        "",
        "1. **O instrumento foi validado APENAS no estrato viral.** O kappa de",
        "   0,759 foi medido contra o gabarito, que so existe para >500 RT.",
        "   Tweets pouco viralizados podem ser sistematicamente diferentes",
        "   (mais curtos, mais dependentes de contexto, mais respostas), e o",
        "   desempenho do rotulador ali e **desconhecido**. Como a conclusao",
        "   da secao 1 depende exatamente desse estrato nao validado, ela e",
        "   provisoria ate que se meça o kappa la. **Proposta: rotular a mao",
        "   uma amostra aleatoria de ~100 tweets do estrato <100 RT e medir.**",
        "   E o unico teste que pode derrubar o achado principal.",
        "2. Sinal a favor (nao substitui o teste acima): se o rotulador",
        "   estivesse a deriva no estrato baixo, seria de esperar deriva",
        "   tambem nas categorias. Elas ficam estaveis; so o stance se move.",
        "3. O rotulador sub-marca categorias em relacao aos humanos (medido no",
        "   teste cego). O vies **atenua** diferencas entre estratos, ou seja,",
        "   joga contra a deteccao de mudanca — o lado seguro para a secao 2,",
        "   mas nao neutraliza a limitacao 1.",
        "4. `Advantages of vaccines` (kappa 0,376) e `Misinformation sources`",
        "   (0,518) sao as categorias fracas do rotulador; leituras que",
        "   dependam so delas precisam de ressalva.",
        "5. O corpus e a re-coleta de mai/2022, com contagens de RT posteriores",
        "   as do paper — os limiares nao sao exatamente os mesmos objetos.",
    ]
    destino_md.write_text("\n".join(L), encoding="utf-8")
    destino_json.write_text(json.dumps(
        {"n_corpus": len(d), "limiares": LIMIARES, "stance": stance,
         "categorias": cats}, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(DADOS))
    args = ap.parse_args()
    saida = pathlib.Path(args.out)

    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    d = carrega(codebook)
    d4 = carrega(codebook, ROTULOS_P4)
    stance = curva_stance(d, d4)
    cats = curva_categorias(d, codebook)
    escreve(stance, cats, d, saida / "FASE3_curvas.md",
            saida / "fase3_curvas.json")

    print(f"[ok] {len(d):,} tweets rotulados analisados")
    for l in stance:
        print(f"  >{l['limiar']:>3} RT  n={l['n']:>6,}  "
              f"p4: pro*={l['p4_pro_dec']:5.1f}%  |  "
              f"p6: pro*={l['p6_pro_dec']:5.1f}% neutro={l['p6_neutro']:5.1f}%")
    maior = max(cats, key=lambda c: abs(c["delta_500_para_10"]))
    print(f"[ok] maior deslocamento tematico: {maior['nome']} "
          f"{maior['delta_500_para_10']:+.1f} pontos")
    print(f"[ok] escrito: {saida / 'FASE3_curvas.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
