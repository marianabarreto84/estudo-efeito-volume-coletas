---
name: revisao-dissertacao
description: Executa uma rodada do ciclo de revisão da dissertação — extrai os comentários que a Mariana deixou num revisao-N.pdf, planeja as mudanças, aplica no fonte LaTeX, recompila e publica o revisao-N+1.pdf. Use quando pedirem "faz a revisão N", "aplica os comentários do PDF", "revisa o texto com os meus comentários", ou quando houver um revisao-N.pdf novo com anotações em escrita/dissertacao/revisoes/.
---

# Ciclo de revisão da dissertação

A Mariana lê o último PDF, deixa **destaques com balão** (anotações `/Highlight`
com `/Contents`) e devolve o arquivo. Uma rodada de revisão consome esses
comentários e devolve um PDF novo para a leitura seguinte. O ciclo mora em
[`escrita/dissertacao/revisoes/`](../../../escrita/dissertacao/revisoes/).

> **Regra de ouro:** nunca sobrescrever um `revisao-N.pdf` que já foi comentado.
> A rodada N produz o `revisao-N+1.pdf`; o anterior fica como registro do que
> ela viu quando comentou.

---

## 1. Extrair os comentários

```bash
cd escrita/dissertacao/revisoes
PYTHONUTF8=1 python extrai_comentarios.py revisao-N.pdf > /tmp/coment.md
```

O script recorta o texto destacado a partir dos `/QuadPoints` (pdfplumber) e o
imprime ao lado do balão (`/Contents`, via pypdf). Precisa de `PYTHONUTF8=1` e de
redirecionar para arquivo — o console do Windows é cp1252 e engasga com `τ`, `—`
e afins.

Anotações **sem** `COMENTARIO` são só marcação: quase sempre estão cobertas pelo
comentário vizinho, ou apontam um problema de **formatação** naquele ponto (foi
o caso da tabela que estourava a margem na rodada 1→2). Vale olhar o `.log` do
LaTeX à procura de `Overfull \hbox` na região antes de concluir que não pediam nada.

## 2. Ler tudo antes de mexer em qualquer coisa

Esta etapa não é opcional, e é o que a Mariana pede explicitamente:

- **Nem todo comentário vira edição.** Muitos são perguntas ("tá certo isso?",
  "é pra botar a banca aqui?"). A resposta certa pode ser *responder*, não editar
  — mas se ela se confundiu, o texto costuma ter culpa, e vale um ajuste.
- **Comentários de baixo desfazem comentários de cima.** Ela lê em ordem; um
  parágrafo adiante muitas vezes já resolve a objeção anterior. Nesse caso a
  edição certa é fazer o trecho de cima **parar de contradizer** o de baixo, e não
  reescrever os dois.
- **Alguns comentários são decisões estruturais disfarçadas de bilhete.** "acho
  que a gente vai acabar não usando instagram e facebook, trate a dissertação sem
  incluir isso" muda tabela, prosa, contagem de redes, limitações, próximos passos
  e todas as listas que citam o caso. Essas vêm primeiro no plano, porque
  atravessam capítulos.
- **A Mariana é coautora de um dos artigos replicados** (o do debate vacinal).
  Quando ela duvida de uma afirmação sobre *aquele* artigo, ela tem informação que
  o PDF publicado não tem. Trate como fonte, e confira contra os `.md` do caso —
  na rodada 2→3 uma dúvida dela reencontrou uma retratação que já estava escrita
  em `DECISOES_ROTULADOR.md` e que o `corpo.tex` ainda não refletia.

Escreva o plano antes de editar, agrupado por capítulo, com uma seção separada
para as decisões estruturais e outra para "o que não muda, e por quê".

## 3. Investigar o que o comentário questiona

Comentário que pergunta por um número **manda conferir o número**, não reescrever
a frase. Os dados vencem o texto (regra do `CLAUDE.md` da raiz). Na rodada 2→3:

- "tá certo isso? não é muito precisamente o mesmo resultado?" → o
  `curva_midia.json` dizia 35,74 a 36,11, e não "36,1 em todos os tamanhos".
- "isso com certeza é um ERRO do artigo?" → o `DECISOES_regras.md` do caso tinha
  as quatro frases literais do artigo; a contradição era real e ficou, mas
  reenquadrada.

## 4. Aplicar no fonte

Edições em `escrita/dissertacao/corpo.tex` e `dissertacao.tex`, **na cópia do
repositório** (`Documents/GitHub/dissertacao-mestrado/`), que é a canônica.

⚠️ **Escapamento.** Substituir blocos de LaTeX por `sed` ou por heredoc do shell
corrompe as contrabarras — foi assim que um `\ref` virou `ef{...}` e saiu
literalmente no PDF. O jeito seguro é um script Python curto, escrito em arquivo
(não em `python -` nem heredoc), com `PYTHONUTF8=1`, acentos em `\uXXXX`, e um
`assert` de que cada trecho procurado aparece **exatamente uma vez**:

```python
import io, os

def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:80])
    s = s.replace(old, new)

def grava(caminho, texto):            # atômico: nunca trunca o alvo
    tmp = caminho + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)
    os.replace(tmp, caminho)
```

O `assert` impede uma substituição silenciosa de errar de lugar. O `grava()` impede
a outra falha, que é pior e já aconteceu **duas vezes** nesta pasta: abrir o alvo em
modo `"w"` **trunca o arquivo na hora**, e se a escrita falhar depois — tipicamente
num `UnicodeEncodeError` — o arquivo fica **com zero byte**. Em 21/ago/2026 foi assim
que o `ESTADO.md` se perdeu numa sessão e o `FASE0_descoberta.md` do meta-ads noutra;
os dois voltaram por `git checkout`, mas só porque estavam versionados. Escreva no
`.tmp` e só então `os.replace`.

⚠️ **Emoji fora do plano básico multilíngue quebra isso.** `📌` e `📝` viram pares
substitutos (`📌`) quando escritos como escapes `\uXXXX`, e o Python recusa
codificá-los em UTF-8. Use `✅ ⏳ ❌ ⚠ ⛔ ❗ ★ ◐`, que são de plano único, ou escreva o
caractere direto no arquivo em vez de escapá-lo. E não tente casar um emoji desses num
`rep()`: ancore a busca no texto ao redor.

## 5. Figuras e tabelas pedidas na revisão

"adicionar figuras", "esse capítulo tá com muito texto corrido", "formata essa
tabela" são pedidos recorrentes. Duas regras:

- **Nenhum número digitado à mão em figura.** `figuras/gerar_figuras.py` lê os
  JSON congelados dos casos. Se o dado ainda não estiver em JSON, acrescente a
  saída JSON ao script de análise do caso, rode-o **na cópia com dados**
  (`Documents/dissertacao/`, que tem os `.sqlite`) e traga só o JSON de volta.
- Tabela que estoura a margem vira `tabularx` com largura `\textwidth` e
  `\footnotesize`. Confira depois com `grep -c Overfull dissertacao.log`.

## 6. Recompilar e publicar

```bash
cd escrita/dissertacao
pdflatex -interaction=nonstopmode dissertacao && bibtex dissertacao \
  && pdflatex -interaction=nonstopmode dissertacao \
  && pdflatex -interaction=nonstopmode dissertacao
grep -n '^!' dissertacao.log ; grep -ic undefined dissertacao.log ; grep -c Overfull dissertacao.log
cp dissertacao.pdf revisoes/revisao-N+1.pdf
```

Aceite a rodada só com **zero** erros, zero referências indefinidas e zero
`Overfull`. Vale abrir duas ou três páginas do PDF para conferir tabelas e
figuras novas — o LaTeX compila limpo e mesmo assim põe uma legenda em cima de
uma linha.

## 7. Fechar a documentação

Toda rodada termina com:

1. **`revisoes/REVISOES.md`** — uma seção `revisao-N.pdf → revisao-N+1.pdf` com a
   data, quantos comentários entraram, quais páginas foram cobertas, e a **tabela
   comentário → mudança**, uma linha por comentário, inclusive os que **não**
   viraram edição (com o motivo). Mais a lista de pendências que a rodada não
   resolveu.
2. **`ESTADO.md`** da raiz — a rodada é mudança de estado. Ver a skill
   [`docs-em-dia`](../docs-em-dia/SKILL.md).
3. Os `.md` que a rodada tornou falsos. Uma decisão estrutural (um caso sai do
   conjunto, um capítulo muda de tipo de análise) contamina o `CLAUDE.md` da raiz,
   o `escrita/CLAUDE.md`, o `README.md` da dissertação e a
   `casos/RESULTADOS_tabela_mestre.md`. Caso retirado da dissertação **não é caso
   apagado**: o material de trabalho fica, marcado como fora do escopo, para poder
   voltar.
