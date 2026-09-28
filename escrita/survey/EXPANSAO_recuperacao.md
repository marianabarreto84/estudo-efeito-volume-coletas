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

### 4b. ⛔ A Springer também fechou — e a tabela acima media o passo errado (9/set/2026)

> Apurado quando a Mariana autorizou a rota lenta ("está OK expandir mais se for
> feito com cuidado"). O cuidado foi construído primeiro, e foi ele que achou isto.

**A linha "Springer 200" da tabela acima mede a *landing page*, não o PDF.** A
página de destino de fato responde 200 e traz a `citation_pdf_url` normalmente.
O **endpoint do PDF** devolve:

```
HTTP 200 · text/html · 3.038 bytes
"Client Challenge ... JavaScript is disabled in your browser.
 Please enable JavaScript to proceed. A required part of this site couldn't load."
```

Testado em **4 DOIs** diversos — periódico e capítulo/LNCS, de 2015 a 2022 —, com
resposta **byte a byte idêntica**. Não é item sem assinatura nem artigo específico:
é a Springer inteira, por essa via.

⚠ **O sinal não é detectável por status code.** É HTTP **200**, corpo curto, e por
isso passou pelo diagnóstico de agosto e pela primeira versão da trava do
[`proxy_springer.py`](expansao/proxy_springer.py). Os marcadores foram
acrescentados à `CHALLENGE` no mesmo dia.

**Consequência: a rota do proxy está fechada por inteiro.** ACM, Elsevier, SAGE,
T&F, Emerald e Wiley já bloqueavam; a IEEE fechou entre mai e ago/2026 (202 com
corpo vazio); a Springer fechou até set/2026. **Não sobrou editora colhível por
automação**, e os ~2.000 artigos da Springer que pareciam folga não são alcançáveis.

⛔ **O que existe no `PROXIMAS_ETAPAS.md` do repo da survey — `curl_cffi` para
forjar o *fingerprint* TLS do Chrome, ou Playwright para executar o desafio — é
contornar um controle anti-automação, não usar uma assinatura.** Fica registrado
como conhecido e **não implementado**, por decisão: o risco deixa de ser de ritmo e
passa a ser de burlar uma proteção deliberada, com a conta caindo sobre o acesso da
PUC-Rio inteira. As rotas legítimas que sobram são pedir ao autor, COMEX/comutação
bibliográfica, e baixar manualmente pelo navegador — nenhuma automatizável em 2.000
artigos.

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

## 3c. ⭐ A varredura TERMINOU — e a taxa final é **7,7%**, não 12,4% (23/ago/2026)

> Apurado em **9/set/2026**, lendo os logs e o banco. A varredura fechou às
> **05:17 de 23/ago** e ninguém tinha lido o desfecho até aqui.

A fila inteira foi tentada: **11.093 de 11.093** artigos, 100% dela. O resultado
final, por `taxa_recuperacao.py` sobre o `estratos.json`:

| estrato | recuperados | taxa | IC95% |
|---|---:|---:|---|
| **pago** (`closed` no DBLP) | 772/10.039 | **7,7%** | 7,2–8,2 |
| aberto que já falhara | 34/981 | 3,5% | 2,5–4,8 |
| sem rótulo no DBLP | 5/73 | 6,8% | 3,0–15,1 |
| **total** | **811/11.093** | **7,3%** | 6,8–7,8 |

Por editora, dentro do estrato pago: ACM 8,9% (206/2.304), IEEE 7,7% (157/2.045),
Springer 7,6% (164/2.154), Elsevier 6,2% (72/1.155), SAGE 6,5%, Wiley 4,6%,
Taylor & Francis 4,3%, Emerald 3,4%.

**Ganho real: 811 artigos**, 6,1% do catálogo, obtidos **sem credencial nenhuma**.
A base de PDFs foi de 2.298 para **3.109**.

### ⚠ A condição de parada pré-registrada DISPAROU

O [PRE_REGISTRO](expansao/PRE_REGISTRO_expansao.md) §8 diz: *taxa final < 11% →
**Parar**; a sondagem de 70 era otimista, a extrapolação de 1.127–2.944 não vale,
reporta-se a taxa real e o trabalho vira uma nota de método.* O estrato pago
fechou em 7,7% com o **IC95% inteiro abaixo** do piso (teto em 8,2%). O
`sorteia_amostra.py` imprimiu o `!! PARAR` e **mesmo assim sorteou** os 800 — o
sorteio não é bloqueante, só avisa.

⚠ **Decisão da Mariana**, e não automática: a parada foi escrita contra a
*extrapolação*, não contra a extração dos artigos que de fato existem. Os 811
estão em disco. Ver [ESTADO.md](../../ESTADO.md) §3.

### ⚠ Por que 12,4% virou 7,7%

Os dois intervalos **não se sobrepõem** (11,3–13,6 × 7,2–8,2), então não é
flutuação amostral. Com `--shuffle`, qualquer prefixo da fila deveria ser amostra
não enviesada dela — e não foi.

A explicação mais provável, e que **vale conferir antes de ir a qualquer lugar**:
a contagem intermediária foi feita logo depois de o `reconcilia_pdfs` trazer
**307 PDFs órfãos do disco** (§Estado do [expansao/README.md](expansao/README.md)),
recuperados por execuções anteriores em **outra ordem** — inclusive a primeira, em
`order_by(id)`. Esses 307 entraram no **numerador** sem que seus denominadores
estivessem no conjunto tentado daquela medição.

É o **terceiro** artefato de medição desta mesma frente, e o terceiro da mesma
família: o instrumento contamina o que mede (§3b, §5, §5b). A diferença é que os
dois primeiros empurravam a taxa **para baixo** e este empurrava **para cima** —
o que é pior, porque um número otimista não dispara desconfiança.

## 6. O que vem depois (⏳ não feito)

> ⚠ **Desatualizado em parte desde 23/ago/2026** — os passos 1 a 3 **foram
> executados**; o passo 4 (extrair) **falhou e não rodou**. Ver §7. O texto abaixo
> fica como registro do plano.

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

---

## 7. ⛔ A extração NÃO rodou — e o log disse que tinha rodado (23/ago/2026)

> Apurado em **9/set/2026**. Nada disto tinha sido lido.

O `extrai_apos_varredura.sh` esperou a varredura corretamente, sorteou os 800 e
**falhou ao montar o comando de extração**. O trecho, do
`pdfs/.extracao_loop.log`:

```
=== extracao de 0 artigos (~R$ 0) 05:21:35 ===
FileNotFoundError: ... '/c/Users/maria/.../amostra.json'
python.exe -m scripts.analyze_pdfs: error: argument --ids: expected at least one argument
=== extracao terminou 23/08 05:21:49 codigo 0 ===
```

**A causa** é de shell, não de método: o script imprime o caminho da amostra como
caminho **do Windows** (`C:\Users\...`) e o interpola dentro de um `$(python -c
...)` executado pelo **bash**, que o entrega como `/c/Users/...`. O Python do
Windows não abre esse caminho, `--ids` fica sem argumento, e o `analyze_pdfs`
aborta.

⚠ **O laço reportou `codigo 0`** — sucesso — porque o `$?` lido era o do último
comando do bloco, não o do `analyze_pdfs`. É por isso que o fracasso passou
**17 dias** sem ser notado: o log termina com uma linha de sucesso.

**Estado real, conferido no banco em 9/set/2026:**

| | |
|---|---:|
| PDFs em disco e no banco | **3.109** |
| com extração estruturada | **2.147** |
| **PDFs sem extração** | **962** (dos quais os 811 da varredura) |
| sorteados e nunca extraídos | **800** |

**Nada foi gasto** — a conta da extração continua zerada, e os 800 seguem
sorteados pela semente pré-registrada `20260929`. Retomar é rodar o
`analyze_pdfs` com a lista lida do `amostra.json`, **sem** passar pelo shell:

```bash
# do repo da survey; le a amostra em Python, sem interpolacao de caminho
python -m scripts.analyze_pdfs --models gemini --workers 5 --ids $(
  python -c "import json,sys;print(' '.join(map(str,json.load(open(sys.argv[1],encoding='utf-8'))['ids_amostra'])))" \
    "$(cygpath -u 'C:/Users/maria/Documents/GitHub/dissertacao-mestrado/escrita/survey/expansao/amostra.json')"
)
```

⛔ **Não rodar sem decisão da Mariana**: gasta (~R$43) e a condição de parada
pré-registrada disparou (§3c).
