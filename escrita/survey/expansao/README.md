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

Ver [ESTADO.md](../../../ESTADO.md) da raiz. Em **22/ago/2026**: pré-registro
fechado; recuperação **rodando de novo** (retomada às 17:02, ~7.350 artigos nunca
tentados na fila); **443 PDFs** já recuperados, dos quais **307 estavam órfãos no
disco** e entraram no banco pelo `reconcilia_pdfs`; taxa do estrato pago em
**12,4%**; extração **encadeada e ainda não disparada**, exceto um **piloto de 5
artigos** (≈R$0,27) que confirmou chave, esquema e pipeline — ver §10 do
pré-registro. **Nenhum número da survey ou da dissertação foi alterado até
aqui.**
