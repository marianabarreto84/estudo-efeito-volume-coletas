# Fase 0 — Alvo e viabilidade do dado (caso Reddit / Massachs 2020)

> Gerado em **7/ago/2026**, **offline**, agora **completo** (full text lido — arXiv
> 2005.01790). Alvo em [ARTIGO_MASSACHS_alvo.md](../../../ARTIGO_MASSACHS_alvo.md).

## O que o alvo é (resumo operacional)

- **Massachs et al. 2020** (WebSci, 29 cit.). Prevê apoio a Trump (participação em
  **r/The_Donald** em 2016) a partir de features de **2012**, testando **homofilia ×
  feedback social × influência direta**. Achado (**MH1**): homofilia (F1 34,8%) e feedback
  (33,7%) preveem; influência (26,7%) quase não.
- **Estrato sub-coletado:** focus group de **44.924 usuários** com ≥10 comentários em 2012
  **e** 2016 em subreddits políticos (r/politics + 50 similares). Rótulo: 7.083 (15,8%)
  apoiadores.

## O que "coletar mais" exige (o universo-alvo)

O universo *on-theme* = **relaxar o filtro do focus group**: incluir usuários **menos
ativos** (limiar <10 comentários/ano) e/ou uma semente política mais larga, mantendo o
tema (discussão política no Reddit 2012→2016) e a mesma tarefa preditiva. O n=44.924 é um
**subconjunto por critério de atividade** do universo de usuários políticos.

**Tamanho:** o focus group é 44.924 usuários; o universo ao relaxar o limiar sobe para
**centenas de milhares a milhões** de usuários × dumps de 2012 e 2016. Grande, mas os dumps
mensais são filtráveis offline; as features são agregados por usuário (cabe em Parquet/DB).

## Viabilidade — rota de coleta ✅

- ✅ **Gabarito existe:** os autores publicaram o dataset `reddit-politics-12-16`
  (`github.com/JoanMG/reddit-data`) — o ponto original (44.924 usuários + features + rótulo)
  é reproduzível direto, sem reconstruir.
- ✅ **Expansão:** dumps de **2012 e 2016** (Pushshift/Arctic Shift/**Academic Torrents**)
  cobrem o período; r/The_Donald (2015–16) arquivado apesar do ban de jun/2020.
- ❌ API oficial não serve (2012 fora de alcance; r/The_Donald banido).

## Bloqueios e o que destrava (tudo offline, sem VPN)

Nenhum bloqueio de dado. Fase 0 fechada. Fase 1 = (a) baixar o dataset dos autores (ponto
original), (b) baixar dos dumps 2012+2016 e reconstruir features com **limiar de atividade
menor** (o eixo de expansão), (c) congelar snapshot.

## Predições pré-registradas

(Detalhe em [REPLICACAO §4](../../../REPLICACAO_CASO_MASSACHS.md).)

- **Provável CONFIRMA (comparativo):** a **ordenação** homofilia/feedback > influência
  sobrevive — é efeito forte e é uma ordem, não uma magnitude.
- **Provável MUDA (magnitude/mecanismo):** ao incluir usuários menos ativos, as features de
  **homofilia (participação) ficam mais esparsas** → o F1 da homofilia pode **cair** e
  encostar no do feedback ou da influência. Se a vantagem da homofilia **depende** do
  estrato hiperativo, é o achado forte ("a conclusão era do recorte de usuários ativos").
- **Persona (MH2):** os subreddits-âncora (r/Conservative, r/conspiracy, r/guns…) tendem a
  ser robustos; a lista fina pode reordenar.
- Segue o padrão cross-case (comparativo robusto, magnitude/descrição não) — a confirmar.
