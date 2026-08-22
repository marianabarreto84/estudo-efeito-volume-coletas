# Expansão do corpus — Fase 1: recuperação em acesso aberto

> Medido em **21/ago/2026**. Nenhum número aqui foi digitado à mão: a taxa vem de
> um lote de 400 executado por `scripts/retry_pdfs.py`, e a estimativa prévia de
> uma sondagem de 70 DOIs contra a API do Unpaywall.
>
> **Nada disto usou o proxy institucional da PUC-Rio** — ver §4.

---

## 1. O problema

A survey catalogou **13.395** artigos e extraiu **2.139**. A diferença não é
critério de inclusão: **10.075** estavam marcados `pdf_inaccessible=1`, atrás de
*paywall*. Essa é a maior limitação declarada do trabalho, e corresponde à
**decisão em aberto nº 1** do [STATUS.md](STATUS.md) — reportar a fração
inacessível como limitação ou como trabalho futuro — e ao comentário **[9]** da
1ª rodada de revisão da dissertação.

## 2. O achado: a marcação está desatualizada

Sondagem de **70 DOIs sorteados** do estrato pago contra a API do Unpaywall:

| | valor | IC95% (Wilson) |
|---|---:|---|
| marcados como acesso aberto | **18,6%** (13/70) | 11,2% – 29,2% |

Onde: 7 em repositórios, 5 na própria editora, 1 indeterminado. A varredura
original simplesmente não consultou o Unpaywall na época — e repositórios enchem
com o tempo, então parte destes artigos abriu **depois** da catalogação.

## 3. A medição real: 13,25%

Estimativa não é recuperação. Um lote de **400 artigos sorteados** (semente
`20260821`) foi processado pela cadeia Unpaywall → OpenAlex → Semantic Scholar →
arXiv:

| | valor | IC95% (Wilson) |
|---|---:|---|
| **PDFs efetivamente baixados** | **13,25%** (53/400) | 10,3% – 16,9% |

A medida cai **dentro** do IC da estimativa, o que valida a sondagem. A distância
entre 18,6% e 13,25% também informa: cerca de **29% das localizações que o
Unpaywall marca como abertas não entregam PDF** — são páginas de destino, links
mortos ou bloqueios.

**Extrapolação** para os 10.074 restantes: **~1.334 artigos** (IC95% 1.035–1.704).

| | hoje | projetado |
|---|---:|---:|
| base de extração | 2.139 | **~3.473** |
| aumento | — | **+62%** |

Custo: **3,7 s por artigo**, ~11 h para a fila inteira com 4 *workers*. Grátis.

## 3b. A varredura em escala: 12,4% no estrato pago (22/ago/2026)

A varredura da fila inteira rodou por ~9 h em 21–22/ago e caiu às 07:15, a **31%**
da fila (sem erro no log; a máquina suspendeu). Retomada às 17:02 de 22/ago. O que
já dá para medir, sobre **3.742 artigos tentados** e com o estrato lido do
`estratos.json` (nunca da coluna volátil):

| estrato | recuperados | taxa | IC95% |
|---|---:|---:|---|
| **pago** (`closed` no DBLP) | 412/3.321 | **12,4%** | 11,3–13,6 |
| aberto que já falhara | 28/399 | 7,0% | 4,9–10,0 |
| **total tentado** | 443/3.742 | 11,8% | 10,8–12,9 |

Os 12,4% ficam **dentro** do IC do lote de 400 (13,25%) e **acima** do piso de 11%
da condição de parada. A projeção para os **6.718** artigos pagos ainda não
tentados é de **+833** (IC95% +761 a +912), o que põe a base projetada perto de
**3.400** — na mesma ordem da estimativa original.

Por editora, dentro do estrato pago, as duas que o proxy mais bloqueia são
justamente as que **melhor** respondem à rota aberta:

| editora | recuperados | taxa |
|---|---:|---:|
| ACM | 112/776 | **14,4%** |
| IEEE | 82/613 | **13,4%** |
| Springer | 79/717 | 11,0% |
| Elsevier | 42/382 | 11,0% |
| SAGE | 10/111 | 9,0% |
| Taylor & Francis | 3/64 | 4,7% |

⚠ **Dois artefatos de medição foram corrigidos no mesmo dia**, ambos no
`expansao/taxa_recuperacao.py`, e ambos empurravam a taxa para baixo: o estrato
vinha da coluna `pdf_inaccessible` (que o próprio ato de recuperar reescreve, o
que fixava o estrato pago em 0,0%) e o denominador era a fila inteira em vez do
conjunto tentado. Antes da correção o script imprimia `!! PARAR: estrato pago em
0.0%` — a condição de parada pré-registrada, disparada por um número que não
existia. Detalhe no [expansao/README.md](expansao/README.md).

## 4. ⚠ Por que o proxy institucional NÃO foi usado

O `.env` do repo já tinha `PUCRIO_PROXY`, `_USER` e `_PASS` configurados, e o
`retry_pdfs.py --via-proxy` existe. Testado em 21/ago/2026 com ~10 requisições de
diagnóstico: **o proxy autentica e roteia** (`example.com` e `doi.org` devolvem
200). Mas as editoras bloqueiam automação:

| editora | artigos no estrato | pelo proxy |
|---|---:|---|
| ACM | 2.305 | **403** |
| Springer | 2.155 | 200 |
| IEEE | 2.052 | **202**, corpo vazio (desafio antibot) |
| Elsevier | 1.155 | **403** na ScienceDirect (832 KB de página de bloqueio) |
| SAGE | 323 | **403** |
| Taylor & Francis | 167 | **403** |

Não é falta de assinatura, é detecção de automação. **Rodar volume por ali
arrisca o acesso da PUC-Rio inteira, não só o da Mariana.** A Springer é a única
que respondeu normalmente; se um dia for usada, deve ser devagar e com parada ao
primeiro 403.

## 5. ⚠ Incidente de método: a ordem da fila é um esquema de amostragem

O primeiro lote rodou na ordem padrão do script (`order_by(id)`) e recuperou
**0 de 15**. Não era a estimativa que estava errada — era o lote: os 400
primeiros por `id` são **391 artigos de 2025–2026**, justamente os menos
propensos a estar em repositório, por embargo e atraso de depósito.

Reportar "0% de recuperação" dali teria enterrado um ganho de ~1.300 artigos com
base num artefato de ordenação. O script ganhou a opção **`--shuffle SEED`**, com
o comentário explicando por que a ordem padrão engana.

É a terceira pergunta do protocolo da dissertação — *o esquema de amostragem é
não-viesado para a quantidade de interesse?* — aplicada ao nosso próprio
pipeline, e a resposta foi não.

## 5b. Segundo incidente de método: retomar não é recomeçar

A fila do `retry_pdfs` é "artigos sem `pdf_path`", e **uma tentativa que falha
continua sem `pdf_path`**. Retomar a varredura interrompida sem excluir o que já
falhou refaria ~3.300 buscas a ~3,7 s cada, com rendimento esperado zero. O
`--offset` que existia resolvia por posição, mas a fila encolhe a cada sucesso, e
o offset escorregava — pulando artigos **nunca tentados**, que é o oposto do que
se queria. Desde 22/ago a exclusão é **por DOI**, lida dos logs de tentativa
(`--skip-file`), o que torna a retomada exata e idempotente.

## 6. O que vem depois (⏳ não feito)

Recuperar PDF é barato; **extrair não é**. O próximo passo **não** é extrair os
~1.300, e sim:

1. **Pré-registrar** semente, tamanho da amostra, achados a testar (mediana de
   itens, fração abaixo de 1 milhão, amostragem × filtragem, fatia de Twitter) e
   a aposta — antes de extrair qualquer coisa.
2. Extrair uma amostra dimensionada **pelo orçamento**, com `analyze_pdfs`.
3. Recomputar com `agg_results.py` e comparar com banda de reamostragem.
4. Se algum número mover, propagar para a dissertação com
   `audita_numeros.py` e `audita_contas.py` rodando antes e depois.

⚠ **Orçamento é a trava.** A extração usa Gemini e OpenAI (chaves no `.env` do
repo da survey, saldo desconhecido). O teto de US$ 25 do
`ANTHROPIC_VACINAS_API_KEY` é do rotulador do *stance* e está em **US$ 9,58** —
não pode ser gasto aqui.

O prompt para retomar isto numa sessão nova está em
[PROMPT_expansao.md](PROMPT_expansao.md).
