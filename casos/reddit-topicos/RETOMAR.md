# Onde retomar — caso `reddit-topicos`

> Escrito em **22/ago/2026**, ao suspender a sessão que abriu o caso. Este arquivo
> existe para que a próxima sessão (ou a Mariana) recomece **sem depender de nada da
> conversa anterior**. Tudo o que está afirmado aqui tem arquivo em disco por trás.
>
> Leia junto: [`README.md`](README.md) (o caso) ·
> [`data/repl/melton2021/PORTAO1_relatorio.md`](data/repl/melton2021/PORTAO1_relatorio.md)
> (o relatório do portão) · [`ARTIGO_MELTON_alvo.md`](ARTIGO_MELTON_alvo.md) (o alvo).

---

## 1. Em uma frase

O caso está **parado no Portão 1**, esperando decisão da Mariana — mas a **descoberta
mais importante da sessão chegou depois** do relatório do portão e **muda a
recomendação dele**: *agregar* (contar) falha nos subreddits grandes, mas *coletar*
(paginar) funciona bem. A rota do caso está **aberta**, não fechada.

## 2. O que está FEITO e congelado em disco

| o quê | onde | estado |
|---|---|---|
| Full text lido, afirmações numeradas (M1–M7, A1–A7, T1, T2) | [`ARTIGO_MELTON_alvo.md`](ARTIGO_MELTON_alvo.md) | ✅ |
| Gabarito: o modelo LDA **ajustado pelos autores** (7 pyLDAvis) | `data/repl/melton2021/gabarito_lda_autores.json` | ✅ auto-confere com a Fig. 4 do artigo |
| Dimensionamento por agregação, **6 de 13** subreddits | `data/repl/melton2021/volume_portao1_parcial.json` | ✅ 2 rodadas concordantes |
| Diagnóstico do rate limit | `PORTAO1_relatorio.md` §3 + [ESTADO.md §4.23](../../ESTADO.md) | ✅ |
| ⭐ **Teste de coleta paginada** | `data/repl/melton2021/teste_coleta.json` | ✅ ver §3 |
| Relatório do Portão 1 | `data/repl/melton2021/PORTAO1_relatorio.md` | ✅ ⚠ §5 e §6 desatualizados — ver §3 aqui |

## 3. ⭐ A descoberta que muda a recomendação (a mais recente)

São **dois endpoints diferentes**, e eles não se comportam igual:

| | agregar `/search/aggregate` (contar) | coletar `/search` paginado (trazer os itens) |
|---|---|---|
| `conspiracy` submissões | ❌ falha em 166d, 83d, 41,5d, 20,8d, 10,4d **e 5,2d**, sempre após 300 s de descanso | ✅ **684 itens, 7 páginas, 13 s** |
| `conspiracy` comentários | ❌ falha | ✅ **5.050 itens, 51 páginas, 97 s, zero falhas** |

**Leitura:** o custo da agregação não depende da janela e sim do tamanho do subreddit
no índice — encolher o intervalo não ajuda. Já a paginação é barata por chamada e não
estrangula. **A Fase 1 não precisa contar; precisa coletar.**

Números medidos (r/conspiracy, o maior dos 13):

- **52,3 itens/s** — mas ~metade do tempo é a pausa de 1 s que o próprio script põe
  entre páginas (`PACING` em `pipeline/testa_coleta.py`). Sem ela fica perto dos
  **95 itens/s** medidos no caso `reddit-buntain`.
- **0,29 kB/item** (comentário com texto), **0,46 kB/item** (submissão com texto).
- Extrapolação linear: **~3,35 M comentários** de `conspiracy` na janela de 166 dias,
  **~1 GB**, **~18 h** de API à taxa com pausa (menos da metade disso sem a pausa).

⚠ **Isto ainda não é a população dos 13**, é um subreddit só. Ver §4.

## 4. O que estava sendo feito quando a sessão parou

### 4.1 ⏳ INTERROMPIDO no meio: o teste de coleta do `r/politics` (Massachs)

Rodou-se `--sub politics --tipo comments --inicio 2016-11-01 --horas 2` e a **1ª página
falhou** (`http:422 ... "Timeout. Maybe slow down a bit"`). **Este resultado NÃO vale**:
ele veio logo depois de puxar 5.050 comentários de `conspiracy`, ou seja, muito
provavelmente é estrangulamento, não incapacidade. Estava-se descansando 300 s para
repetir quando a sessão foi suspensa.

⚠ **Não registre esse "falhou" como achado.** Concluir dele seria repetir exatamente o
erro que este caso documentou em [ESTADO.md §4.23](../../ESTADO.md). A entrada com
`"funciona": false` já está gravada em `teste_coleta.json` — **é preciso repetir com
descanso antes de interpretar.**

**Comando para retomar:**

```bash
cd casos/reddit-topicos
# descanse ~5 min sem tocar no Arctic Shift, depois:
python pipeline/testa_coleta.py --sub politics --tipo comments --inicio 2016-11-01 --horas 2
```

### 4.2 ⏳ Dimensionamento por agregação — parado, e provavelmente não vale a pena

`python pipeline/dimensiona.py` estava rodando e travou em `conspiracy`, descendo o
ladrilho até 5,2 d sem sucesso. **Recomendação: não insistir nesse caminho.** Ele
gasta horas para produzir um número que a coleta entrega de graça. Ver §5.

## 5. Próximos passos, na ordem

1. **Repetir o teste do `politics` com descanso** (§4.1). É o que decide se a Fase 3 do
   [`reddit-massachs`](../reddit-massachs/README.md) volta a ser viável — a Mariana
   pediu explicitamente para avaliar isso depois do caso novo.
2. **Trocar a estratégia de dimensionamento**: em vez de agregar, **amostrar**. Paginar
   algumas janelas de 24 h espalhadas pelos 166 dias, em cada um dos 13 subreddits, e
   extrapolar com incerteza. É barato, funciona nos grandes, e dá a estimativa que o
   Portão 1(d) pede. **Isto ainda não foi implementado** — `dimensiona.py` hoje só sabe
   agregar.
3. **Rodar `pipeline/checa_bans.py`** para fechar o Portão 1(c) (`antivaccine`
   indeterminado). Nunca foi executado.
4. **Atualizar `PORTAO1_relatorio.md` §5 e §6** — eles ainda dizem que a rota é
   desconhecida e que o teste decisivo "não foi feito". **Foi feito e deu positivo**
   (§3 aqui). A recomendação de lá ficou mais otimista do que está escrita.
5. Só então: estimativa final de disco/tempo → **decisão da Mariana** sobre comprometer
   o caso ou deixá-lo como próximo passo instruído.

## 6. Como rodar as coisas (tudo é script, nada depende de terminal aberto)

```bash
cd casos/reddit-topicos

python pipeline/dimensiona.py --listar          # o que já foi medido e o que falta
python pipeline/dimensiona.py                   # agregação (LENTO; ver §4.2)
python pipeline/dimensiona.py --caso massachs   # a reconferência do Massachs
python pipeline/testa_coleta.py --sub conspiracy --tipo comments --horas 6
python pipeline/checa_bans.py                   # Portão 1(c)
python pipeline/baixa_gabarito_lda.py           # re-congela o gabarito dos autores
```

Só precisa de `python` — **sem dependência externa, sem credencial, sem gasto de LLM**.
O `dimensiona.py` é **retomável**: grava progresso a cada janela fechada, em
`volume_portao1_progresso.json`. Não apague esse arquivo no meio.

⚠ **Regra de convívio com o Arctic Shift:** ele estrangula quem insiste, e precisa de
**~300 s de silêncio** para se recuperar (medido: 30 s e 120 s não bastam). **Não
paralelize, não troque o User-Agent, não contorne** — é infraestrutura pública mantida
por voluntários, e os casos `reddit-buntain` e `reddit-massachs` dependem dela. O
prompt do caso manda parar, não contornar.

## 7. O que NÃO fazer ao retomar

- **Não mexer no `corpo.tex`.** Nada deste caso foi para a dissertação, e nada vai
  antes de a Mariana ler o `revisao-5.pdf` e decidir sobre o caso.
- **Não tratar o "falhou" do `politics`** como resultado (§4.1).
- **Não citar a soma de 6/13 como população** — é parcial, e o JSON diz
  `COMPLETO: false`.
- **Não trocar LDA por BERTopic** — é o algoritmo do alvo; trocar confundiria efeito de
  coleta com efeito de método.
