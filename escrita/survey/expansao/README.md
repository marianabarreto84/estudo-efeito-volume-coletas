# Expansão do corpus da survey

Aplicação do protocolo da dissertação — *coletar mais e medir se a conclusão
muda* — à própria survey. O objetivo **não** é aumentar a base: é medir se o
viés de acesso alterava os achados. Uma base maior com os mesmos achados é o
melhor desfecho, e fecha a decisão em aberto nº 1 do [STATUS.md](../STATUS.md).

Comece pelo [**PRE_REGISTRO_expansao.md**](PRE_REGISTRO_expansao.md): semente,
tamanho da amostra, achados testados, critérios de "mudou", a aposta, as travas
e as condições de parada. Foi escrito e commitado **antes** de qualquer extração.

---

## ⚠ Uma corrida de recuperação por vez

Em 21/ago/2026 **três** corridas de `retry_pdfs` foram lançadas por sessões
diferentes em 30 minutos. Elas se atrapalham de três formas, todas observadas:

1. **Escrevem no mesmo `pdfs/.progress.txt`** — a taxa que aparece lá vira
   mistura de duas corridas e não vale para nada.
2. **Somam workers nas mesmas APIs abertas** (Unpaywall, OpenAlex, Semantic
   Scholar, arXiv). Dez workers simultâneos é o tipo de carga que motiva
   bloqueio — e bloqueio é condição de parada pré-registrada.
3. **Commitam no mesmo `research.db`**, e o commit reescreve
   `pdf_inaccessible`, que era o rótulo de estrato (ver abaixo).

**A corrida canônica é `--shuffle 20260821`, sobre a fila inteira.**
O `--shuffle` é o que não dá para acrescentar depois: sem ele a fila anda em
ordem de `id`, que concentra artigos de 2025–26 — os menos prováveis de estar em
repositório aberto. Com ele, **qualquer prefixo da fila é amostra não enviesada
dela**, e a corrida pode ser interrompida a qualquer momento sem invalidar nem a
taxa nem o sorteio.

Se precisar parar e retomar, retome **com a mesma semente**.

### Como se retoma (mudou em 22/ago/2026)

A corrida longa caiu três vezes — duas em 21/ago e uma às **07:15 de 22/ago**, a
31% da fila, sem erro no log (a máquina suspendeu). O jeito de retomar mudou:

- **`bash scripts/varredura_em_blocos.sh` é o comando único**, e é idempotente:
  rodar de novo continua de onde parou. Ele roda blocos de 400 (grava a cada
  bloco), reconcilia depois de cada um e para sozinho quando a fila acaba.
- **`--skip-file` substituiu o `--offset`.** A fila é "sem `pdf_path`", e uma
  tentativa que falha **continua** sem `pdf_path`: retomar sem excluir o que já
  falhou refaz milhares de buscas a ~3,7 s cada, com rendimento zero. O
  `--offset` tentava resolver isso por posição, mas a fila encolhe a cada
  sucesso, então o offset escorregava e pulava artigos **nunca tentados**. O
  `skip-file` exclui **por DOI** o que os logs registram como tentado —
  `scripts/gera_lista_tentados.py` o gera, e o laço o refaz a cada bloco.
- ⚠ **`--shuffle` ignorava `--offset`** (corrigido no mesmo dia): rodar em blocos
  com shuffle repetia o mesmo prefixo a cada bloco em vez de avançar.

## ⚠ `pdf_inaccessible` não é rótulo de estrato

`retry_pdfs.py` reescreve a coluna enquanto roda: sucesso → `False`, falha →
`True`. **O ato de medir apaga a variável pela qual se mede.** Artigo recuperado
sai do estrato pago; artigo que o DBLP dizia aberto entra nele ao falhar.

Isso já produziu números falsos nesta sessão: entre duas leituras, o estrato pago
"caiu" de 10,4% para 5,1% sem que nada real tivesse mudado.

O rótulo estável está em [`estratos.json`](estratos.json), reconstruído do campo
`<access>` dos dumps XML do DBLP (13.780 DOIs; 3.211 `open`, 10.531 `closed`),
que é a mesma fonte que definiu a coluna na importação original. **Toda medida de
taxa por estrato usa esse arquivo, nunca a coluna.**

## Os arquivos

| Arquivo | O que é |
|---|---|
| [`PRE_REGISTRO_expansao.md`](PRE_REGISTRO_expansao.md) | o pré-registro — leia primeiro |
| `baseline_agg.txt` | saída literal de `agg_results.py` antes da expansão (N=1.718) |
| `baseline_ids.json` | ids que já tinham PDF (2.298) e análise (2.139), congelados |
| `estratos.json` | rótulo de estrato estável, vindo dos dumps do DBLP |
| `congela_estratos.py` | gera o `estratos.json` |
| `sorteia_amostra.py` | aplica a regra de sorteio pré-registrada (n=800, semente 20260929) |
| `compara.py` | os dois critérios de "mudou"; **aborta** se a base antiga deixar de reproduzir o baseline |
| `taxa_recuperacao.py` | taxa por estrato e por editora. ⚠ **corrigido em 22/ago/2026** — lia o estrato da coluna volátil e dividia pela fila inteira; ver abaixo |
| `reconcilia_pdfs.py` | religa PDFs em disco ao banco (o `retry_pdfs` só commita no fim da fila) |
| `audita_rotulo_conteudo.py` | audita o rótulo "análise de conteúdo" contra o texto integral do PDF |
| [`SONDAGEM_tdm_biblioteca.md`](SONDAGEM_tdm_biblioteca.md) | mensagem pronta para a DBD sobre direitos de TDM. ⏸ **não enviada** — depende de terceiros (biblioteca + editora), e a Mariana optou pela sonda manual |
| `proxy_springer.py` | recuperação via proxy **com parada dura em bloqueio**. ⛔ inútil na prática: foi ele que provou que a Springer fechou (§4b do EXPANSAO) |
| `sonda_springer.py` | **sonda humano-no-laço** do estrato comercial: sorteia, monta as URLs, abre as abas, recolhe do `Downloads` e casa com o DOI |
| `sonda_springer.json` | a amostra congelada (n=200, semente `20260929`) + o poder declarado |
| `auditoria/` | `audita_numeros.py` e `audita_contas.py` da dissertação, saída **antes** da expansão |

## ⚠ Duas medidas falsas que o `taxa_recuperacao.py` produzia

Corrigidas em 22/ago/2026. As duas empurravam a taxa **para baixo**, e a segunda
chegou a imprimir um `!! PARAR` — a condição de parada pré-registrada — sobre um
número que não existia:

1. **O estrato vinha da coluna `pdf_inaccessible`**, a mesma que as corridas
   reescrevem a cada sucesso. Todo artigo pago recuperado saía do estrato pago no
   instante em que era recuperado, então a taxa do estrato pago só podia dar
   **0,0%** — é a armadilha da seção anterior, agora aplicada ao próprio medidor.
   O estrato passou a vir do `estratos.json`.
2. **O denominador era a fila inteira**, mas a varredura cobriu 34% dela.
   Dividir os recuperados pela fila toda mede **cobertura**, não taxa. O
   denominador passou a ser o conjunto **tentado**, lido dos logs.

Com as duas correções, o estrato pago mede **12,4%** (412/3.321, IC95%
11,3–13,6), coerente com os 13,25% do lote pré-registrado de 400 e **acima** do
piso de 11%.

## Ordem de execução

Os passos 1 a 4 estão **encadeados** desde 22/ago/2026: `varredura_em_blocos.sh`
roda a recuperação, e `extrai_apos_varredura.sh` espera ela acabar, sorteia e
extrai. O passo pago só dispara quando **não resta artigo por tentar** — sortear
com a fila pela metade sortearia de uma população ainda em crescimento, e o
sorteio deixaria de ser o pré-registrado.

```
1. bash scripts/varredura_em_blocos.sh           (no repo da survey; idempotente)
2. reconcilia_pdfs.py                            (o laço já faz isso a cada bloco)
3. sorteia_amostra.py                            -> amostra.json
4. analyze_pdfs --models gemini --ids <amostra>  (no repo da survey, <= R$43)
   (3 e 4 saem de graca em scripts/extrai_apos_varredura.sh)
5. compara.py --json resultado.json
6. audita_numeros.py / audita_contas.py          -> diff contra auditoria/
```

O passo 2 espera o 1 terminar de propósito: o `retry_pdfs` faz um único
`db.commit()` no fim, e escrever no `research.db` antes disso arrisca um lock no
momento em que ele grava.

## Estado

Ver [ESTADO.md](../../../ESTADO.md) da raiz. Em **9/set/2026**:

- ✅ **Varredura ENCERRADA** em 23/ago, fila **100% tentada** (11.093). **811 PDFs**
  recuperados; base de PDFs de 2.298 → **3.109**.
- ⚠ **Taxa final: 7,7%** no estrato pago (772/10.039, IC95% 7,2–8,2) — **não** os
  12,4% intermediários, que a seção acima ainda registra como histórico da execução.
  Os ICs não se sobrepõem; a hipótese (307 órfãos de disco no numerador) está em
  [EXPANSAO_recuperacao.md §3c](../EXPANSAO_recuperacao.md) e **segue por conferir**.
- ⛔ **Condição de parada pré-registrada disparada** (piso de 11%). A Mariana
  **decidiu prosseguir**; o adendo de decisão está no
  [PRE_REGISTRO §11](PRE_REGISTRO_expansao.md), escrito **antes** da execução.
- ⛔ **A extração encadeada nunca rodou** em 23/ago — bug de shell com `codigo 0` por
  cima do erro. Relançada em 9/set às 08:47, com a lista passada por arquivo.
- ⛔ **Rota do proxy fechada por inteiro** — a Springer também passou a servir desafio
  anti-automação (§4b). Os ~2.000 artigos dela **não** são folga.
- ◐ **Sonda humano-no-laço** aberta no lugar: n=200 congelado, 0 baixados.

## A sonda do estrato comercial (9/set/2026)

Depois que a rota do *proxy* fechou por inteiro
([EXPANSAO_recuperacao.md §4b](../EXPANSAO_recuperacao.md)), o que restou de
legítimo para alcançar conteúdo assinado é **um humano no navegador**. O desafio
anti-automação da Springer existe para verificar que há uma pessoa presente; se há,
ele está sendo satisfeito, não contornado. O `sonda_springer.py` automatiza tudo
**menos** essa parte, que é justamente a que não deve ser automatizada.

⚠ **O poder é declarado antes, e é modesto de propósito.** n=200 detecta diferenças
de ~15 p.p. entre estratos; **não** detecta os 2–6 p.p. que a aposta A4 do
pré-registro prevê (isso exigiria n≈1.500, ~8 h de clique). A sonda responde *"o
estrato comercial é categoricamente diferente?"* — não *"de quanto ele difere"*.
Os dois desfechos são publicáveis, e nenhum deles bloqueia a defesa.

### Como rodar

**Uma vez, no navegador — e é por PROXY, não por login no site.** A Springer
reconhece o **IP institucional**, não uma conta: o PAC da DBD roteia
`link.springer.com` (verificado em 9/set/2026: PAC no ar, 18,6 KB, domínio na
lista) pelo gateway `139.82.115.33:16000`. ⚠ Se a página mostrar **"Log in via an
institution"**, o proxy **não** está ativo naquela aba — não adianta clicar ali.

No **Firefox** (recomendado, porque a configuração é só do navegador e sai num
clique, sem rotear o resto da máquina):

1. Configurações → buscar `proxy` → *Configurações de rede* → **Editar**
2. **URL de configuração automática de proxy (PAC)**: `http://dbd.puc-rio.br/proxy.pac`
3. Na primeira requisição ele pede usuário/senha do proxy (as mesmas do `.env`,
   `PUCRIO_PROXY_USER`/`PUCRIO_PROXY_PASS`)
4. Configurações → *Aplicativos* → **PDF** → **Salvar arquivo**. Sem isso o
   Firefox abre o PDF no visualizador embutido em vez de baixar, e cada aba
   vira um Ctrl+S manual — com 200 artigos, isso dobra o trabalho.

**Como saber que está valendo:** abra qualquer artigo Springer. Com o proxy
ativo aparece *Download PDF* / o banner de acesso institucional; sem ele aparece
*Log in* e *Access this chapter*.

⚠ Chrome e Edge usam o proxy **do sistema** no Windows, o que roteia a máquina
inteira pela PUC-Rio. Dá para fazer (Configurações → Rede e Internet → Proxy →
*Usar script de configuração*), mas é mais invasivo e mais fácil de esquecer
ligado.

```bash
cd escrita/survey/expansao
python sonda_springer.py --estado          # onde a sonda está
python sonda_springer.py --lote 20 --abrir # abre 20 abas
#   ... salvar os PDFs (o navegador passa o desafio) ...
python sonda_springer.py --conferir        # recolhe do ~/Downloads
```

Repetir `--lote`/`--conferir` até 200/200. É retomável: o `--lote` só devolve o que
ainda não está em `pdfs/`, então dá para parar e voltar quando quiser.

Ao final, `python reconcilia_pdfs.py --aplicar` leva ao banco, e a extração desses
200 segue o mesmo caminho dos 800 (`analyze_pdfs --models gemini`).

### ⚠ 75% da amostra é LNCS, e isso pode mudar o desenho (9/set/2026)

Primeiros 6 downloads reais da Mariana: **todos periódicos, zero LNCS**. E a
página que travou era um capítulo de anais (PAM 2023, LNCS 13882).

| | LNCS/capítulo | periódico |
|---|---:|---:|
| amostra (n=200) | **150 (75%)** | 50 (25%) |
| população (2.013) | 1.492 (74%) | 521 (26%) |
| já no corpus (422) | 151 | 271 |

Anais LNCS costumam ser **compra separada** da assinatura de periódicos. Se a
PUC-Rio não os cobrir, a sonda de 200 vira **n≈50 efetivo** — margem de ±13 p.p.,
que não sustenta conclusão nenhuma e não vale uma hora de clique.

✅ **MEDIDO em 9/set/2026, com o proxy ativo — a assinatura NÃO cobre LNCS.**
Diagnóstico de 8 downloads, depois de o PAC estar valendo no Firefox:

| tipo | resultado |
|---|---|
| **periódico** | **3 de 3 baixaram** (809 KB a 1,4 MB) |
| **LNCS/capítulo** | **0 de 5** |

Somando o que a Mariana baixou no total: **9 artigos, todos periódicos, zero
LNCS**. A conclusão é limpa — a PUC-Rio assina os **periódicos** Springer e não
os **anais LNCS**, que são compra separada.

### O redesenho (9/set/2026)

A sonda passou a ser **só de periódicos**, por `--redesenhar-periodicos 200`:

| | antes | depois |
|---|---|---|
| população | 2.013 (74% LNCS) | **521 periódicos** |
| amostra | 150 LNCS + 50 periódicos | **200 periódicos** |
| n efetivo | ~50 | **200** |
| já baixados | 9 | **9 (preservados)** |

**O desenho continua sendo amostra aleatória simples.** O sorteio original foi
uma AAS de 2.013, então seu subconjunto de periódicos (50) é uma AAS dos 521;
completar com 150 sorteados entre os 471 restantes produz exatamente uma AAS de
200 — sortear em duas etapas sem reposição equivale a sortear de uma vez. Nada
do que já foi baixado se perde. A amostra antiga está preservada em
`sonda_springer_v1_lncs.json`, e o `historico` do JSON registra a mudança e o
motivo.

⚠ **O escopo mudou junto, e vai declarado:** a sonda mede o estrato comercial
**de periódico Springer**, não o estrato comercial inteiro. Com n=200 de 521 e
correção de população finita, a margem melhora para **±4,4 p.p.** numa proporção
de 20%.

⭐ **A inacessibilidade dos anais LNCS é resultado, não ruído.** Uma instituição
que assina Springer continua sem alcançar 1.492 artigos de anais do próprio
corpus — o que reforça, do lado de dentro, a tese de que o estrato comercial é
limite estrutural para levantamentos em escala.

### Registrar o que não tem acesso

```bash
python sonda_springer.py --sem-acesso 10.1007/978-3-031-... 10.1007/...
```

Sem isso o `--lote` devolveria eternamente os mesmos artigos, e o denominador
misturaria "ainda não tentei" com "a instituição não assina" — o que tornaria a
taxa da sonda desonesta.

⚠ O `--conferir` **recusa** arquivo que não comece com `%PDF` — é o caso da página
de desafio salva como `.pdf`, que acontece se a aba for salva antes de o JS rodar.
Ele diz quais foram, para reabrir.
