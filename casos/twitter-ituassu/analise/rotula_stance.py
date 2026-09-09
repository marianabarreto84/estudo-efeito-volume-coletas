# -*- coding: utf-8 -*-
"""Rotulador automatico do eixo *stance* -- roda sobre o teste cego (210).

E a segunda metade da medida: o gabarito humano ja existe
(`gold_stance_teste_MARIANA.csv`, fechado em 9/set/2026) e o numero que fecha a
linha da tabela mestre e o kappa entre os dois.

DUAS ASSIMETRIAS DECLARADAS (nenhuma delas e defeito; as duas vao ao capitulo)
-----------------------------------------------------------------------------
1. **O perfil vivo.** O codebook §1 permite a Mariana abrir o perfil na web
   quando handle, nome e metricas nao decidem o portao `cidadao`. O rotulador
   nao tem essa informacao. Por isso a acuracia do portao e reportada em duas
   bases -- todos os itens e so os decidiveis pelo CSV congelado -- exatamente
   como o PRE_REGISTRO §4.2 mandou.

2. **O apendice §7 do codebook fica FORA do prompt.** Ele mede o lado das
   hashtags por co-ocorrencia nos proprios dados. O codebook o declara
   "contexto, nao regra", e o PRE_REGISTRO §5 registra o risco: se a mesma
   heuristica entrar dos dois lados, humano e maquina concordam por usarem a
   mesma tabela, e o kappa passa a medir a tabela, nao a validade. A §2 (sinais
   explicitos tirados do proprio artigo) entra, porque e regra.

O modelo fica **pinado**. Trocar de modelo invalida o kappa medido.

Uso:
    python analise/rotula_stance.py --dry-run     # estima e nao gasta nada
    python analise/rotula_stance.py               # roda de verdade
"""
import argparse
import csv
import io
import json
import os
import pathlib
import re
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]           # casos/twitter-ituassu
PROJETO = RAIZ.parents[1]                                    # dissertacao/
# O teto de gasto e do PROJETO, nao de um caso: o mesmo livro-caixa de US$ 25
# do caso vacinas vale aqui, senao o teto deixaria de ser teto.
sys.path.insert(0, str(PROJETO / "casos" / "vacinas"))
from core.llm import cliente, MODELO_PADRAO                  # noqa: E402
from core import orcamento as orc_mod                        # noqa: E402

STANCE = RAIZ / "data" / "repl" / "compos2014" / "stance"
GOLD = STANCE / "gold_stance_teste_MARIANA.csv"
SAIDA = STANCE / "prerotulagem_teste_LLM.csv"

MODELO = MODELO_PADRAO          # claude-haiku-4-5-20251001, pinado
LOTE = 15                       # tweets por chamada
MAX_SAIDA_POR_TWEET = 160       # pior caso de tokens de saida, para a reserva
                                # (70 truncou o lote 7 em 9/set/2026: o modelo
                                #  escreveu justificativa longa dentro de `notas`)

# Campos que o rotulador ve. E o mesmo contexto que a planilha da humana traz,
# menos o que so o perfil vivo daria (ver assimetria 1).
CONTEXTO = ["autor", "nome_autor", "verificado", "seguidores", "tweets_do_autor",
            "eh_retweet", "autor_original", "idioma", "texto", "host1", "hashtags"]

SISTEMA = """\
Você rotula tweets brasileiros da eleição presidencial de 2014 (2º turno, \
Dilma Rousseff × Aécio Neves), na janela de 19 a 25 de outubro de 2014.

Para cada tweet, produza três rótulos.

## 1. `cidadao` — a conta é de um cidadão comum?
- `N` para: veículo de imprensa e perfis-satélite; empresa, marca ou agência; \
órgão público, partido, campanha oficial ou candidato; agregador automático ou \
bot (só manchete + link, dezenas por dia, sem 1ª pessoa); ativismo organizado \
com marca própria.
- `S` para pessoa física, mesmo militante, mesmo com nome fantasia.
- `?` quando o handle não decide e o texto não ajuda.
Volume alto de tweets sugere agregador mas **não decide sozinho**: marque `N` \
só com outros sinais; na dúvida, `?`.

## 2. `stance` — preferência expressa NESTE tweet
Valores: `EA` (eleitor de Aécio), `ED` (eleitor de Dilma), `NDA` (não dá para afirmar).

Camada 1 — sinal explícito. Se o tweet traz hashtag/expressão que já declara lado:
- ED: #Dilma13, #EuVotoDilma13, #MelhorComDilma13, #QueroDilmaTreze, \
#SomosTodosDilma, #13rasilTodoComDilma, #DilmaEMichel13, **#AecioNever** \
(«Aécio never» = nunca Aécio, logo pró-Dilma).
- EA: #Aecio45, #Aecio45PeloBrasil, #EAecio45Confirma, #EuVotoAecio45, \
#VotoAecioPeloBR45il, #AecioPresidente, #ForaDilma, #ForaPT.
Hashtags temáticas (#G1, #DebateNaGlobo, #Ibope, #Veja, #Datafolha, #Politica, \
#Brasil, #Eleicoes2014) **não** são sinal de lado.

Camada 2 — o tom:
- conteúdo negativo a um candidato/campanha/partido → eleitor do **adversário**;
- conteúdo positivo a um candidato/campanha/partido → eleitor **dele**;
- não dá para decidir, ou é apolítico → **NDA**.
Equivalências: Dilma ≡ PT ≡ Lula ≡ governo — atacar isso ⇒ EA. \
Aécio ≡ PSDB ≡ FHC ≡ governo tucano de MG/SP — atacar isso ⇒ ED.

Casos-limite (decididos; siga-os à risca):
1. RT sem comentário: retuitar é endosso — rotule pelo conteúdo retuitado.
2. RT com comentário que contradiz o conteúdo (ironia): vale o comentário. \
nota `rt_ironico`.
3. Notícia neutra sem valência («Ibope: Dilma 53%, Aécio 47%»): **NDA**. Número \
de pesquisa não é torcida, mesmo que favoreça alguém.
4. Notícia neutra COM comentário valorado: vale o comentário.
5. Apoio a terceiro (Marina, PSOL, nulo, branco): **NDA**, nota `terceiro`.
6. Ironia: julgue pelo alvo; se não der, NDA com confiança 1.
7. Idioma não-português: se entender, rotule; se não, NDA, nota `idioma`.
8. Link morto/opaco (t.co sem host resolvido) e texto que não decide: **NDA**, \
nota `link_morto`. Quando o host resolvido já decide (blogdodilmiro, \
revistaforum, veja.abril), use-o.
9. Conta institucional com lado óbvio: `cidadao=N` **e** o stance real — nunca \
deixe stance vazio.
10. Crítica à mídia: atacar Veja/Globo em 2014 ⇒ **ED**; atacar «mídia \
chapa-branca»/EBC ⇒ **EA**. Confiança no máximo 2.
11. Só hashtags dos dois lados (spam de tags): **NDA**, nota `spam_tag`.
13. Manchete de notícia retuitada sem comentário: depende de quem fala e de quão \
forte é a valência. Se é **fato de terceiro** que fere ou favorece de forma \
inequívoca uma campanha, vale o lado. Se é a **fala do próprio candidato**, ou \
crítica fraca, é **NDA**. nota `manchete`.
14. Nome de exibição declara lado mas o tweet não: **NDA**. O nome só serve ao \
portão `cidadao`, nunca como sinal de lado.

**Regra de ouro: na dúvida entre um lado e NDA, é NDA.**

## 3. `confianca`
`3` óbvio · `2` inferência razoável · `1` chute informado.
Quando o stance for NDA, use: `3` se o tweet não expressa preferência alguma \
(pesquisa, placar, notícia sem valência); `2` se inclina para NDA mas não é \
óbvio; `1` se pode ter lado e não deu para determinar (ironia ambígua, link \
morto, texto truncado).

## Saída
Responda **só** com um array JSON, um objeto por tweet, na mesma ordem da \
entrada, sem texto em volta e sem cercas de código:
[{"id":"<id_tweet>","cidadao":"S|N|?","stance":"EA|ED|NDA","confianca":"3|2|1",\
"notas":"<código ou vazio>"}]

Em `notas` use **só** um destes códigos, ou string vazia: `rt_ironico`, `terceiro`, `idioma`, `link_morto`, `spam_tag`, `manchete`. **Nunca** escreva justificativa — ela não é lida e estoura o limite de saída.
"""


def carrega_itens():
    """Le os 210 SEM os rotulos humanos -- o rotulador nao pode ve-los."""
    with io.open(GOLD, encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh))
    assert len(linhas) == 210, "esperava 210, veio %d" % len(linhas)
    itens = []
    for r in linhas:
        it = {"id_tweet": r["id_tweet"], "n": r["n"]}
        it.update({c: r.get(c, "") for c in CONTEXTO})
        itens.append(it)
    return itens


def bloco_do_tweet(it):
    p = ["id: %s" % it["id_tweet"],
         "autor: %s (%s)" % (it["autor"], it["nome_autor"]),
         "verificado: %s | seguidores: %s | tweets do autor: %s"
         % (it["verificado"], it["seguidores"], it["tweets_do_autor"])]
    if it["eh_retweet"] == "1":
        p.append("é retweet: sim" + (" (de %s)" % it["autor_original"]
                                     if it["autor_original"] else ""))
    if it["idioma"] and it["idioma"] != "pt":
        p.append("idioma: %s" % it["idioma"])
    if it["host1"]:
        p.append("link resolve em: %s" % it["host1"])
    elif "http" in it["texto"]:
        p.append("link presente, host NÃO resolvido (link morto)")
    p.append("texto: %s" % it["texto"])
    return "\n".join(p)


def prompt_do_lote(lote):
    return ("Rotule os %d tweets a seguir.\n\n" % len(lote)
            + "\n\n---\n\n".join(bloco_do_tweet(it) for it in lote))


def extrai_json(txt):
    t = txt.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    i, j = t.find("["), t.rfind("]")
    if i < 0 or j < 0:
        raise ValueError("resposta sem array JSON: %s" % txt[:200])
    return json.loads(t[i:j + 1])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="conta tokens de verdade, estima o custo e NAO gasta")
    ap.add_argument("--lote", type=int, default=LOTE)
    args = ap.parse_args()

    itens = carrega_itens()
    lotes = [itens[k:k + args.lote] for k in range(0, len(itens), args.lote)]
    cli = cliente()

    # ---- contagem real de tokens de entrada (endpoint gratuito) ----
    entradas, total_ent = [], 0
    for lote in lotes:
        r = cli.messages.count_tokens(
            model=MODELO, system=SISTEMA,
            messages=[{"role": "user", "content": prompt_do_lote(lote)}])
        entradas.append(r.input_tokens)
        total_ent += r.input_tokens

    saida_pior = sum(len(l) for l in lotes) * MAX_SAIDA_POR_TWEET
    custo_pior = orc_mod.custo_usd(MODELO, entrada=total_ent, saida=saida_pior,
                                   batch=False)
    orc = orc_mod.Orcamento()

    print("modelo ............ %s (pinado)" % MODELO)
    print("tweets ............ %d em %d lotes de ate %d" % (len(itens), len(lotes), args.lote))
    print("entrada ........... %s tokens (contados via count_tokens)" % f"{total_ent:,}")
    print("saida (pior caso) . %s tokens (%d por tweet)" % (f"{saida_pior:,}", MAX_SAIDA_POR_TWEET))
    print("custo (pior caso) . US$ %.4f" % custo_pior)
    print("saldo do livro .... US$ %.2f de US$ %.2f" % (orc.saldo, orc_mod.TETO_USD))
    print("saldo depois ...... US$ %.2f" % (orc.saldo - custo_pior))

    if args.dry_run:
        print("\n[dry-run] nada foi enviado.")
        return

    ident = orc.reservar(usd=custo_pior,
                         descricao="stance ituassu: teste cego 210",
                         detalhe={"tweets": len(itens), "lotes": len(lotes),
                                  "modelo": MODELO})
    print("\nreserva %s feita. enviando...\n" % ident)

    saidas, ent_real, sai_real = [], 0, 0
    try:
        for k, lote in enumerate(lotes, 1):
            r = cli.messages.create(
                model=MODELO, max_tokens=len(lote) * MAX_SAIDA_POR_TWEET,
                system=SISTEMA,
                messages=[{"role": "user", "content": prompt_do_lote(lote)}])
            ent_real += r.usage.input_tokens
            sai_real += r.usage.output_tokens
            dados = extrai_json(r.content[0].text)
            if len(dados) != len(lote):
                raise ValueError("lote %d: esperava %d objetos, veio %d"
                                 % (k, len(lote), len(dados)))
            for it, d in zip(lote, dados):
                if str(d.get("id")) != it["id_tweet"]:
                    raise ValueError("lote %d: id fora de ordem (%s != %s)"
                                     % (k, d.get("id"), it["id_tweet"]))
                saidas.append({"id_tweet": it["id_tweet"], "n": it["n"],
                               "cidadao": d.get("cidadao", ""),
                               "stance": d.get("stance", ""),
                               "confianca": str(d.get("confianca", "")),
                               "notas": d.get("notas", "") or ""})
            print("  lote %2d/%d ok (%d itens)" % (k, len(lotes), len(lote)))
            time.sleep(0.4)
    except Exception as e:
        # o que ja saiu foi cobrado de verdade: lanca o consumo real e nao apenas
        # solta a reserva, senao o livro-caixa subestima o gasto e o teto de US$ 25
        # deixa de ser teto.
        if ent_real or sai_real:
            orc.concilia(ident, modelo=MODELO, entrada=ent_real, saida=sai_real,
                         batch=False)
            print("[falhou] consumo real lancado: entrada %s / saida %s tokens"
                  % (f"{ent_real:,}", f"{sai_real:,}"))
        else:
            orc.libera(ident, motivo="falhou antes de gastar: %s" % type(e).__name__)
        raise

    orc.concilia(ident, modelo=MODELO, entrada=ent_real, saida=sai_real, batch=False)

    with io.open(SAIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id_tweet", "n", "cidadao", "stance",
                                           "confianca", "notas", "fonte"])
        w.writeheader()
        marca = "LLM_%s_%s" % (MODELO, time.strftime("%Y-%m-%d"))
        for s in saidas:
            w.writerow({**s, "fonte": marca})

    print("\ngravado: %s (%d linhas)" % (SAIDA, len(saidas)))
    print("gasto real: entrada %s / saida %s tokens" % (f"{ent_real:,}", f"{sai_real:,}"))
    print(orc.resumo())


if __name__ == "__main__":
    main()
