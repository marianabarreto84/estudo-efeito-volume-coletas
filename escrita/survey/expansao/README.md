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

**A corrida canônica é `--shuffle 20260821 --workers 4`, sobre a fila inteira.**
O `--shuffle` é o que não dá para acrescentar depois: sem ele a fila anda em
ordem de `id`, que concentra artigos de 2025–26 — os menos prováveis de estar em
repositório aberto. Com ele, **qualquer prefixo da fila é amostra não enviesada
dela**, e a corrida pode ser interrompida a qualquer momento sem invalidar nem a
taxa nem o sorteio.

Se precisar parar e retomar, retome **com a mesma semente**.

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
| `taxa_recuperacao.py` | taxa por estrato e por editora |
| `reconcilia_pdfs.py` | religa PDFs em disco ao banco (o `retry_pdfs` só commita no fim da fila) |
| `audita_rotulo_conteudo.py` | audita o rótulo "análise de conteúdo" contra o texto integral do PDF |
| `auditoria/` | `audita_numeros.py` e `audita_contas.py` da dissertação, saída **antes** da expansão |

## Ordem de execução

```
1. retry_pdfs --shuffle 20260821 --workers 4     (no repo da survey)
2. reconcilia_pdfs.py --aplicar                  (depois que a corrida terminar)
3. sorteia_amostra.py                            -> amostra.json
4. analyze_pdfs --models gemini --ids <amostra>  (no repo da survey, ~R$45)
5. compara.py --json resultado.json
6. audita_numeros.py / audita_contas.py          -> diff contra auditoria/
```

O passo 2 espera o 1 terminar de propósito: o `retry_pdfs` faz um único
`db.commit()` no fim, e escrever no `research.db` antes disso arrisca um lock no
momento em que ele grava.

## Estado

Ver [ESTADO.md](../../../ESTADO.md) da raiz. Em 21/ago/2026: pré-registro fechado,
recuperação rodando, extração ainda não iniciada — **nenhum número da survey ou da
dissertação foi alterado até aqui**.
