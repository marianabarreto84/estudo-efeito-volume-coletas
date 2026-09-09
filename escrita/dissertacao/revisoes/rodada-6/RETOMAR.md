# Rodada `revisao-5.pdf` → `revisao-6.pdf` — ✅ **CONCLUÍDA**

> ✅ **A rodada foi retomada e fechada em 24/ago/2026.** O `aplica6.py` rodou sem
> erro, o `revisao-6.pdf` (77 p., zero erros, zero indefinidas, zero `Overfull`)
> está publicado, e o mapa comentário→mudança está em
> [`REVISOES.md`](../REVISOES.md). **Nada aqui pede ação.**
>
> O texto abaixo é o registro de como a sessão de 22/ago foi interrompida e
> retomada — histórico, e não estado. Vale como procedimento para a próxima vez
> que um script de aplicação abortar no meio.
>
> ⚠ **Não rode o `aplica6.py` de novo.** Ele é idempotente nas substituições, mas
> não há razão para reexecutá-lo, e a rodada 7 terá o seu próprio script.
>
> **De passagem, a rodada fez uma correção que não estava no plano:** o título
> corrente encavalava no número da página no Cap. 8 e quebrava em duas linhas no
> Cap. 6. Corrigido com `\chaptermark` curto nos cinco capítulos de caso —
> [`ajusta_cabecalho.py`](ajusta_cabecalho.py).

---

## Registro da interrupção (22/ago/2026)

> Sessão suspensa por pedido da Mariana antes de a rodada fechar.

---

## 1. Estado exato dos arquivos (o que já está no disco)

| Arquivo | Estado | O que já mudou |
|---|---|---|
| `dissertacao.tex` | ✅ **JÁ EDITADO E SALVO** | bloco `\captionsetup{...}` (legenda menor, rótulo em negrito, travessão, recuo) + parâmetros de colocação de float (`\topfraction` etc.), logo depois do `\usepackage{abntex2cite}` |
| `referencias.bib` | ✅ **JÁ EDITADO E SALVO** | entrada nova `@mastersthesis{heine2025amostragem,...}`, antes de `salgueiro2022dbmodels` |
| `corpo.tex` | ❌ **INTOCADO** | nenhuma das ~30 edições foi gravada. O script abortou num `assert` **antes** do `c.salva()` |
| `revisao-6.pdf` | ❌ não existe | nada foi recompilado nem publicado |
| `REVISOES.md` | ❌ não atualizado | falta a seção `revisao-5.pdf → revisao-6.pdf` |
| `ESTADO.md` (raiz) | ❌ não atualizado | falta o registro da rodada |

⚠ **`corpo.tex` não foi corrompido nem truncado.** A gravação é atômica
(`.tmp` + `os.replace`) e o script morreu antes de chegar nela. Confirmado por
`grep -c "Uma palavra antes sobre o termo" corpo.tex` → 1 (o parágrafo que a
rodada vai remover ainda está lá).

## 2. Como retomar (é um comando)

```bash
cd escrita/dissertacao
PYTHONUTF8=1 python revisoes/rodada-6/aplica6.py
```

O `rep()` do script foi tornado **idempotente**: se o trecho antigo não existe
mais mas o novo já está lá, ele pula em silêncio. Por isso rodar de novo **não**
duplica as edições já gravadas em `dissertacao.tex` e `referencias.bib`.

Depois de rodar, seguir a skill
[`revisao-dissertacao`](../../../../.claude/skills/revisao-dissertacao/SKILL.md)
a partir do passo 6:

```bash
pdflatex -interaction=nonstopmode dissertacao && bibtex dissertacao \
  && pdflatex -interaction=nonstopmode dissertacao \
  && pdflatex -interaction=nonstopmode dissertacao
grep -n '^!' dissertacao.log ; grep -ic undefined dissertacao.log ; grep -c Overfull dissertacao.log
cp dissertacao.pdf revisoes/revisao-6.pdf
```

Aceitar só com **zero** erros, zero referências indefinidas e zero `Overfull`.
E abrir o PDF nas páginas das tabelas — o objeto desta rodada é justamente a
aparência das legendas e a colocação das tabelas.

## 3. O que faltava fazer quando a sessão parou

1. **Rodar `aplica6.py`** (o script está completo e revisado; ver §4 para a
   última correção pendente de verificação).
2. Recompilar e publicar `revisao-6.pdf`.
3. Escrever em `REVISOES.md` a seção `revisao-5.pdf → revisao-6.pdf` com a
   **tabela comentário → mudança** (23 linhas — os comentários estão em
   [`comentarios_revisao-5.md`](comentarios_revisao-5.md), e o plano de cada um
   está na §5 abaixo) e a lista de pendências não resolvidas.
4. Atualizar o `ESTADO.md` da raiz (skill `docs-em-dia`).

## 4. O erro que interrompeu, e o que foi corrigido

O `assert` falhou no comentário **[6]** (o `boyd` em minúscula): o trecho antigo
que eu procurava tinha as quebras de linha erradas, porque a substituição
anterior (a do comentário **[9]**, que define "dado social") já reescrevia a
frase logo antes, na mesma linha do `\citeonline{boyd2012critical}`.

Duas correções foram aplicadas ao script **depois** da falha e **ainda não
foram executadas**:

- `rep()` ganhou o atalho de idempotência descrito na §2;
- a busca do comentário [6] passou a ancorar em
  `provocações fundadoras, entre elas a de que dado grande não é automaticamente dado bom.`,
  que é o texto como fica **depois** da edição [9].

Se ao rodar aparecer outro `AssertionError`, a mensagem traz
`(arquivo, quantas vezes achou, quantas esperava, começo do trecho)`. Quase
sempre a causa é a mesma: **uma edição anterior do próprio script já mexeu
naquele trecho**, e o `old` precisa ser reescrito com o texto pós-edição.
Nada é gravado até o `salva()` do fim, então é seguro rodar quantas vezes for
preciso.

## 5. Plano da rodada (23 comentários) — o que cada um vira

### Decisões que atravessam capítulos

**[2] + [14] — a legenda de tabela parece texto corrido** (3ª vez que ela pede).
Tratado em duas frentes:
- **global**, no preâmbulo: `\captionsetup{font=footnotesize, labelfont=bf,
  labelsep=endash, justification=raggedright, margin=14pt, skip=6pt}` — legenda
  menor que o corpo, rótulo em negrito e travessão (`Tabela 1.1 – …`), recuada
  das margens do bloco de texto;
- **por tabela**: legenda reduzida a **uma frase**, e a explicação desce para
  uma *nota sob a tabela* em `\footnotesize` (padrão que a `tab:tiktok-temporal`
  e a `tab:mestre` já usavam). Feito em `tab:analises-survey`, `tab:casos`,
  `tab:reddit-rb3`, `tab:youtube-funil`, `tab:youtube-ponto`.
- **colocação** (a queixa de que as tabelas caem em páginas desconexas):
  `[t]` → `[htbp]` nas quatro tabelas dos Caps. 1 e 3, mais o afrouxamento de
  `\topfraction`/`\textfraction`/`\floatpagefraction` no preâmbulo.

**[18] — "esse caso do TikTok parece forçação, e o desenrolar é muito técnico".**
Ela aprova a ideia (inverter a pergunta) e o capítulo; o problema é a execução.
A §8.3 foi reescrita para: (i) mandar as três séries de denominador para a
**nota da tabela**, deixando no corpo uma frase só; (ii) encurtar o parágrafo da
"assimetria" entre as duas perguntas, que era o trecho mais técnico; (iii)
fechar pelo argumento, não pela mecânica ("dizer quanto se coletou sem dizer
quando se verificou é publicar um número sem sentido definido").

### Mapa comentário → mudança

| # | p. | O que ela pediu | O que o script faz |
|---|----|-----------------|--------------------|
| 1 | 12 | o parágrafo do Salgueiro é estranho pra abrir; virar parêntese no de baixo | Parágrafo removido; o crédito vira parêntese dentro da 1ª frase do levantamento, preservando a justificativa de tratar as 4 redes como um objeto |
| 2 | 13 | legenda × texto corrido, "já não é a primeira vez que eu peço" | Ver acima (global + por tabela) |
| 3 | 14 | o que é "evidência transferível" | Termo eliminado e **explicado por extenso**: a evidência descreve o *tipo de análise*, não a plataforma, e por isso vale onde essas análises forem feitas |
| 4 | 16 | a abertura do Cap. 2 soa defensiva | "encosta em quatro linhas … e não se confundem com ela" → "apoia-se em quatro linhas já estabelecidas"; o fecho agora *localiza* o trabalho em vez de se defender |
| 5 | 16 | cada subcapítulo do Cap. 2 devia ter o autor no título; Morstatter é o "original" | Os 4 títulos ganharam o autor de referência (Morstatter / boyd e Crawford / Liang e Fu / Kossinets), com título curto para o sumário. E o texto passa a dizer que a linha **começa** em Morstatter |
| 6 | 17 | "boyd" com minúscula? | Nota de rodapé: é a grafia que a própria autora adota, não é erro |
| 7 | 17 | o trecho do erro total está artificial | Reescrito sem jargão: decompõem o percurso do dado (quem está na plataforma → o que ela registra → o que a interface devolve → o que o pesquisador filtra) e localizam o erro de cada etapa |
| 8 | 17 | Ruths e Pfeffer ficaram genéricos; falam de rede social? | Sim — trocado pelos três pontos concretos deles (população própria de cada plataforma; filtro por palavra-chave/API não é amostra de nada bem definido; contas automatizadas) e pela recomendação de relato |
| 9 | 17 | o que é "dado social"? | Definido **na primeira menção** (gloss na abertura do capítulo) e por extenso na abertura da §2.2: tradução de *social data*, e o traço que importa é que ninguém o produziu para pesquisar |
| 10 | 17 | "conclusões ficam ao alcance" não se entende | Reescrito: os conjuntos diferem em tamanho, composição e contas centrais, e por isso a escolha do método de coleta já delimita que perguntas o material poderá responder |
| 11 | 17 | "insumo empírico" é rebuscado | → "a evidência" |
| 12 | 17 | a dissertação do Heine tem que entrar; provavelmente em amostragem | Parágrafo novo na §2.1 (ela acertou o enquadramento) + entrada `heine2025amostragem` no `.bib`. Diz o que ele fez (amostras extraídas de 57,9 M já coletados; os tópicos não reproduzem), que é o **antecedente mais direto**, e em que difere; e amarra na linha em aberto da tabela mestre |
| 13 | 19 | as duas ressalvas finais do Cap. 2 não são necessárias | A **primeira** (a busca não achar não prova inexistência) foi **cortada**; a segunda ficou, encurtada. E o parágrafo anterior virou fechamento de verdade |
| 14 | 25 | tabelas em páginas desconexas; a crítica é a **legenda** | Ver acima |
| 15 | 62 | dois "Convém dizer" seguidos; cuidado com repetição no resto | Varredura de todos os 10 "convém" do texto; 6 trocados por formas distintas (Vale localizar / é preciso dizer / Cabe precisar / é preciso identificar / Note-se / Vale dizer) |
| 16 | 62 | "códigos de estado"? não se entende | Explicado: o que os autores publicam não é o motivo do sumiço, é o rótulo que a interface devolveu (`status_deleted`, `status_reviewing`, `status_audit_not_pass`, `author_secret`…), e o artigo não diz quais conta como remoção da plataforma |
| 17 | 62 | isso não é detalhe técnico demais? | Comprimido de 4 frases para 2, **liderando pelo ponto** (é a mesma classe de achado dos outros alvos) em vez de pela mecânica do voto majoritário |
| 18 | 64 | o caso do TikTok parece forçação e é técnico demais | Ver acima |
| 19 | 66 | "companion" em inglês; parágrafo longo demais | As **6** ocorrências de *companion* viraram "projeto de replicação" / "reportado em … como parte do mesmo projeto"; a abertura do Cap. 9 foi quebrada em 4 parágrafos |
| 20 | 71 | me perdi nas duas últimas frases da §9.2 | Reescritas em linguagem direta: declarar quanto se coletou é como se escreve o artigo; poder coletar mais para verificar é que infraestrutura se tem — sem a segunda o número não é verificável nem pelo autor |
| 21 | 72 | "modelo/ algoritmo" → "modelo e/ou algoritmo" | Adotado literalmente |
| 22 | 72 | limitação do "porquê": não entendi | Reescrita com exemplo concreto dos próprios casos (a partição do debate vacinal ainda se movia; a proporção de mídia de 2014 já estava assentada em 100 tweets) e dizendo que explicar isso exigiria estudar o método, não a coleta |
| 23 | 72 | a limitação de teoria de amostragem pode subir | Movida de **7ª para 2ª** na lista, com "sampling" traduzido e uma frase nova: o trabalho não diz quanto se deveria coletar, diz se o que se coletou bastou |

## 6. Pendências que esta rodada **não** resolve

Herdadas da rodada anterior e ainda de pé:

1. **Caps. 4 a 7 seguem quase sem leitura.** A revisão 5 saltou da p. 26 para a
   p. 56; a revisão 6 acrescentou comentários nas pp. 62–72, mas os capítulos do
   debate vacinal, do Reddit e do YouTube continuam sem comentário desde o
   `revisao-2.pdf`.
2. **Modelagem de tópico continua sem caso executado.** O sétimo caso
   (`casos/reddit-topicos`, Melton et al. 2021) está **parado no Portão 1**
   esperando decisão da Mariana — ver
   `casos/reddit-topicos/data/repl/melton2021/PORTAO1_relatorio.md`.
3. **Front-matter:** falta a dedicatória (hoje genérica).
4. **A classe segue com o `\fi` acrescentado** (ver a rodada 3 → 4).

Novas desta rodada:

5. **A entrada `heine2025amostragem` usa as iniciais `A. A. P.`**, que é o que o
   material do caso registra. Se a Mariana tiver o nome por extenso, vale
   completar antes da versão final.
6. **`labelsep=endash`** muda o rótulo de `Tabela 1.1:` para `Tabela 1.1 –` em
   todas as legendas. É o padrão ABNT e ajuda a separar legenda de texto, mas é
   uma mudança visível em todo o documento — se ela não gostar, é uma linha só
   no preâmbulo.
