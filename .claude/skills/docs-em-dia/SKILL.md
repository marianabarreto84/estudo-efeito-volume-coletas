---
name: docs-em-dia
description: Mantém a documentação da dissertação (os .md de cada parte) sempre atualizada e coerente entre si. Use SEMPRE que terminar um trabalho que muda o estado do projeto — rodou script/análise, concluiu uma fase de um caso, achou/descartou uma fonte de dados, mudou um número, criou/moveu/renomeou arquivos ou pastas, fechou uma decisão, ou está encerrando a sessão. Também use quando pedirem "atualiza a documentação", "documenta isso", "o README tá desatualizado" ou para auditar quais .md estão fora de sincronia.
---

# Documentação em dia

A documentação desta pasta **não é registro opcional pós-fato**: é o estado do
projeto. Um resultado que existe só no terminal, num script ou no histórico da
conversa **não existe**. O trabalho só está terminado quando o `.md` correspondente
reflete a realidade.

## A regra

> **Toda mudança de estado do projeto termina com a atualização do(s) `.md`
> afetado(s), na mesma sessão em que a mudança aconteceu.**

"Mudança de estado" = qualquer coisa que faria alguém lendo a documentação de ontem
tirar hoje uma conclusão errada.

## Onde cada coisa mora (hierarquia)

```
CLAUDE.md (raiz)              a tese, o mapa, o lineup, a infra compartilhada
ESTADO.md (raiz)              O QUE DÁ PARA AVANÇAR AGORA — desbloqueado / travado /
│                             decisões pendentes / divergências. Atualizado TODA sessão.
├── escrita/CLAUDE.md         regras da redação
│   ├── INVENTARIO.md         índice do material (o que é, de onde veio, por quê)
│   ├── dissertacao/README.md como compilar, pendências
│   └── survey/CLAUDE.md      regras da survey
│       └── survey/STATUS.md  progresso da redação, decisões fechadas, seção a seção
└── casos/<caso>/
    ├── README.md             porta de entrada: estrutura, pré-requisitos, ESTADO ATUAL
    ├── REPLICACAO_CASO_*.md  plano de fases (o mapa do caso)
    ├── *_alvo.md             o trabalho replicado, destrinchado
    ├── EIXO_*.md             cada eixo de análise
    └── data/repl/<dataset>/
        └── FASE*_.md / RESULTADOS_*.md   os números, com proveniência
```

Regra de altura: **números e método vão nos `FASE*/RESULTADOS_*`**; o `README.md` do
caso resume em 1–3 linhas com link; o `CLAUDE.md` da raiz só muda quando o **estado do
caso na tabela do lineup** muda.

## O `ESTADO.md` da raiz (regra própria)

O [`ESTADO.md`](../../../ESTADO.md) responde a **uma** pergunta: *sentando agora, o que
dá para fazer sem depender de ninguém?* Ele é o **primeiro** arquivo a ler ao abrir a
pasta e o **último** a atualizar antes de fechar a sessão.

- **Não** guarda números, método nem histórico — isso vive nos `FASE*/RESULTADOS_*`.
  Guarda: o que está **desbloqueado**, o que está **travado e em quê**, o que espera
  **decisão da Mariana**, e as **divergências** entre documentos ainda não resolvidas.
- **Atualize-o em toda sessão que mexa no estado do projeto**, mesmo que nenhum outro
  `.md` mude: item concluído sai do §1, bloqueio novo entra no §2, decisão tomada sai
  do §3, divergência corrigida sai do §4, e a data do cabeçalho muda sempre.
- Se a sessão foi só conversa e nada mudou de estado, **não** mexa nele (não bumpe a
  data por hábito) — um `ESTADO.md` que muda sem motivo perde a função de sinal.
- Divergência encontrada e **não** corrigida na hora **tem** de virar linha do §4. É o
  único lugar onde é aceitável registrar em vez de consertar.

## Gatilho → o que atualizar

| O que aconteceu | Atualize |
|---|---|
| Rodou uma análise / produziu números | `data/repl/<dataset>/RESULTADOS_*.md` ou `FASE*_*.md` (novo ou existente) → e a linha de estado no `README.md` do caso |
| Concluiu (ou travou) uma fase | `FASE*_*.md` + "Estado atual" do `README.md` + tabela do lineup no `CLAUDE.md` raiz, se mudou de coluna |
| Achou / descartou uma fonte de dados | `FASE0_descoberta.md` do caso + §5 do `CLAUDE.md` raiz se afeta a viabilidade |
| Criou/moveu/renomeou arquivo ou pasta | bloco de estrutura (```árvore```) do `README.md`/`CLAUDE.md` da pasta; se é material de escrita, `escrita/INVENTARIO.md` |
| Escreveu/revisou seção do texto | tabela de seções do `survey/STATUS.md` + "Feito nesta sessão" |
| Fechou uma decisão (venue, escopo, método) | "Decisões fechadas" do `STATUS.md` ou seção correspondente; se vale para tudo, `CLAUDE.md` |
| Mudou um número já citado em outro `.md` | **todos** os lugares onde ele aparece (ver "Propagação") |
| Novo script no pipeline/análise | linha na estrutura do `README.md` do caso + como rodar, se não for óbvio |
| Nova pendência / bloqueio | onde ele bloqueia (⏳ no "Estado atual"), não num TODO solto — **e** §2 do `ESTADO.md` |
| Destravou algo (o dado chegou, a decisão saiu) | move o item de §2/§3 para §1 do `ESTADO.md` |
| Achou divergência entre dois `.md` (ou `.md` × `.tex`) | corrija na hora; se não der, §4 do `ESTADO.md` |
| **Qualquer** mudança de estado | além do acima, a linha correspondente do §5 do `ESTADO.md` |

## Propagação de números

Um número vive em **um** lugar canônico (o `RESULTADOS_*`/`FASE*` que o produziu) e é
**citado** nos outros. Ao mudar:

1. Atualize o canônico, com a proveniência (script + data + fonte).
2. `grep` o valor antigo em todos os `.md` e corrija cada ocorrência.
3. Se o número já foi para o `.tex`, corrija lá também — ou sinalize explicitamente à
   Mariana que o texto está divergente. **Os dados vencem** (princípio §7 do `CLAUDE.md`).

```bash
grep -rn "1.686" --include="*.md" --include="*.tex" .
```

Nunca deixe dois `.md` afirmando coisas diferentes. Se descobrir uma divergência
enquanto trabalha em outra coisa, conserte na hora ou registre-a como ressalva.

## Convenções de escrita dos `.md` (as que a pasta já usa)

- **Cabeçalho com proveniência** logo após o título, em blockquote:
  ```markdown
  # Fase 2 — Eixo A (modularidade)

  > Gerado em **26/jul/2026** por `analise/modularidade.py` sobre
  > `snapshot_vacinas.sqlite`. Determinístico (seed 42).
  ```
- **Estado com marcador**: `✅` concluído · `⏳` em espera/bloqueado (diga *esperando o
  quê*) · `❌` descartado (diga *por quê*). Sem marcador vago tipo "em progresso".
- **Links relativos** entre docs (`[FASE1_snapshot.md](data/repl/.../FASE1_snapshot.md)`),
  nunca caminhos absolutos.
- **Tabelas** para inventários e comparações; **blocos de código** para árvores de pasta
  e comandos.
- **Datas absolutas** (`26/jul/2026`), nunca "ontem", "semana passada", "recentemente".
- **Ressalvas explícitas** junto do resultado, não escondidas no fim (ex.: "grafo de RT é
  nível-autor"; "~16% dos originais não são pt").
- Toda pasta com README começa com **"Leia primeiro"** apontando o plano e o alvo.
- Português, tom acadêmico e seco. Sem emoji além dos marcadores de estado.
- **Nunca** a palavra "claude" em nome de arquivo, pasta, branch ou commit.

## Antes de encerrar a sessão — checklist

1. Listei tudo que mudou de estado nesta sessão?
2. Cada item tem seu `.md` atualizado (não só o código)?
3. Os números novos batem com o que os outros `.md` afirmam?
4. O "Estado atual" do `README.md` do caso descreve o *agora*?
5. A tabela do lineup no `CLAUDE.md` raiz continua verdadeira?
6. Alguma pendência nova ficou registrada onde bloqueia?
7. **O `ESTADO.md` da raiz responde certo a "o que dá para avançar agora"?** — item feito
   saiu do §1, bloqueio novo entrou no §2, decisão tomada saiu do §3, divergência
   corrigida saiu do §4, §5 e a data do cabeçalho batem com a realidade.

Se algo não pôde ser atualizado (falta um dado, precisa de decisão da Mariana),
**diga isso explicitamente** no fim da resposta em vez de deixar o doc mentindo.

## Auditoria rápida (quando pedirem "o que está desatualizado?")

```bash
# .md mais antigos que o código/dados da mesma pasta
find . -name "*.md" -newer CLAUDE.md
git log --oneline --name-only -20 2>/dev/null   # se virar repo git
```

Compare cada `README.md` de caso com o que existe de fato em `data/repl/` e em
`analise/`: script que rodou sem `RESULTADOS_*` correspondente é dívida de documentação.
Reporte a lista antes de sair corrigindo tudo.

## O que NÃO fazer

- **Não sobrescrever** um `.md` existente para "reescrever melhor" — edite o trecho
  afetado. Rascunhos e histórico de decisão têm valor.
- **Não apagar** ressalvas, limitações ou apostas pré-registradas que falharam. Reportar
  honestamente quando a aposta falha é princípio do projeto.
- **Não inventar** número, data ou referência para completar uma tabela. Sem o dado,
  escreva `⏳ falta apurar`.
- **Não criar** `.md` novo quando o assunto cabe num existente. A pasta já tem muitos
  documentos; mais fragmentação piora.
- **Não documentar** o óbvio derivável do código; documente decisão, proveniência e estado.
