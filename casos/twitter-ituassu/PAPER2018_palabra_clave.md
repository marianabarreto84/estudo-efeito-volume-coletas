# Paper 2018 (Palabra Clave) — metade do par replicado

> Doc de referência do artigo **novo**. **Não é o alvo primário:** o alvo da replicação
> é o **par 2015 + 2018** (decisão do usuário, jul/2026), rodado pelo mesmo pipeline —
> o contraste entre os dois é que carrega o argumento (efeito-de-taxonomia + a expansão
> que os próprios autores fizeram). Plano de fases em
> [REPLICACAO_CASO_COMPOS2014.md](REPLICACAO_CASO_COMPOS2014.md); eixo stance em
> [STANCE_como_o_paper_fez_e_onde_estamos.md](STANCE_como_o_paper_fez_e_onde_estamos.md).

**Ituassu, A.; Lifschitz, S.; Capone, L.; Vaz, M. B.; Mannheimer, V. (2018).**
*Compartilhamento de mídia e preferência eleitoral no Twitter: uma análise de
opinião pública durante as eleições de 2014 no Brasil.* **Palabra Clave, 21(3),
860–884.** DOI: 10.5294/pacla.2018.21.3.9. PDF:
`Compartilhamento_de_midia_e_preferencia_eleitoral_.pdf`.

**Mesmo grupo, artigo feito em cima do antigo.** Ituassu + Lifschitz assinam os
dois; 2018 acrescenta Capone, Vaz e Mannheimer (as 3 juniores que codificaram).
O 2018 cita o 2015 como *"análises preliminares no âmbito desta pesquisa"* e
*"nossos primeiros resultados"* — é literalmente o mesmo programa de pesquisa,
**expandido**. Isso é central para nós: o próprio grupo já fez uma expansão
(700 → 1.129) e **uma conclusão virou** no caminho (ver §5).

---

## 1. O que o 2018 coletou e analisou

- **Coleta:** mesma base do 2015 (Search API + Tweepy/OAuth, ~2 tweets/s), mas
  desta vez capturaram, no 2º semestre de 2016, **>200 mil tweets** de 6–26/out/2014
  com **#Eleições2014**. Campos coletados: usuário, texto, timestamp.
- **Amostra analisada (manual):** **200 tweets/dia, aleatórios, no horário de pico**,
  de **13 a 23/out** → cascata de 4 sub-amostras (Tabela 1 do paper):

| Amostra | Definição | N |
|---|---|--:|
| **A** | 200 tweets/dia aleatórios no pico, 13–23/out, #Eleições2014 | **2.200** |
| **B** | A menos contas de empresas, órgãos de imprensa e instâncias coletivas (isolar cidadãos) | **1.679** |
| **C** | tweets com **pelo menos 1 compartilhamento de mídia** (65,4% de A) | **1.439** |
| **D** | C menos tweets sem **preferência eleitoral** identificável | **1.129** |

> Análises **só de mídia** rodam sobre **C (1.439)**; análises de **mídia × preferência**
> rodam sobre **D (1.129)**. `N = 1.129` é o número-título do artigo.

**Codificação:** manual, por **3 pesquisadoras** (as juniores), divergências
resolvidas por consenso a três. Mudou de 5 revisores (2015) para 3 codificadoras.

---

## 2. A mudança de taxonomia: MV/MH → **MP/MC**

O 2015 usava **MV/MH** (mídia vertical/horizontal, de Shaw et al. 2006 — critério
de *fluxo* da informação, de cima-para-baixo × par-a-par). O 2018 **troca**
explicitamente para **MP/MC**, "buscando uma alteração metodológica que pudesse
tornar a qualificação mais precisa":

- **MP — Mídia Principal:** lista **fechada** de grandes marcas, tirada da
  **Pesquisa Brasileira de Mídia 2014** (as marcas mais lembradas em TV, rádio,
  jornal, internet, revista). O paper diz **"26 grandes mídias"** e lista (p.871–872):

  > Rede Bandeirantes · Diário Gaúcho · Época · Estado de São Paulo (Estadão) ·
  > Extra · Folha de S. Paulo · Rede Globo · O Globo · Globo.com · Hoje em Dia (R7) ·
  > iG · IstoÉ · Jornal do Brasil · Meia Hora · O Dia · O Povo · R7 · Rede Record ·
  > Rede SBT · Super Notícia · Terra · UOL · Veja · Yahoo · Zero Hora

  ⚠ **Só 25 itens são nomeados** — o texto diz 26. Lacuna de reconstrução (§7).

- **MC — Mídia Complementar:** **tudo o mais** (o paper catalogou "mais de 100
  mídias"). Inclui explicitamente **as redes sociais** (Twitter, Facebook, blogs,
  YouTube, Instagram) — tese própria do artigo: **"social media as complementary
  media"** (as redes sociais dominam o espaço das MCs). No 2015 as redes sociais
  já eram MH; aqui a diferença conceitual é o **critério**: em MP/MC é a
  *proeminência da marca* (PBM 2014), não o fluxo.

**Crosswalk MV/MH (nosso código atual) → MP/MC (2018):** ver §6. O ponto prático:
MP é uma lista **mais restrita** que a nossa MV — veículos como **Valor, A Tarde,
CartaCapital, BBC, WSJ** estão na nossa MV mas **não** entram nas 26 marcas, logo
"cairiam" para MC. Isso importa porque **Valor e A Tarde aparecem no topo** das
tabelas de mais-compartilhados do próprio 2018 (Tab. 3 e 5) — tensão a resolver (§7).

---

## 3. Resultados PP1 — que mídia foi compartilhada (Amostra C, n=1.439)

**Predomínio da mídia principal**, mas com 40% de complementar:

| | N | % |
|---|--:|--:|
| **MP** | 851 | **59%** |
| **MC** | 588 | **41%** |
| Total (C) | 1.439 | 100% |

- **65,4%** dos 2.200 tweets tinham compartilhamento de mídia.
- **Top-10 mídias = 60%** dos compartilhamentos (Tab. 3): G1 15%, UOL 15%, Folha 5%,
  Estadão 5%, Valor 5%, JB 4%, O Dia 3%, O Globo 3%, R7 3%, A Tarde 2%.
- Reclassificando as 20 mais-compartilhadas em (a) old media na web, (b) agregadores
  digitais, (c) redes sociais → **~2/3 são mainstream** (old media + agregadores,
  seguindo Foster 2012).
- **Dentro das MCs** (Tab. 4), as 6 primeiras são redes sociais: Twitter 29%,
  Facebook 20%, Blogs 12%, Instagram 8%, YouTube 7% (→ "social media as
  complementary media").

---

## 4. Resultados PP2 — públicos diferentes têm leques diferentes? (Amostra D, n=1.129)

**Composição por preferência** (deduzida da Tab. 7): **EA = 581 · ED = 548**
(entre quem compartilhou mídia **e** tinha preferência identificável).

> 🔀 **A maioria inverteu entre os dois papers.** 2015: ED 284 > EA 226 (maioria
> Dilma). 2018: **EA 581 > ED 548** (maioria Aécio). Amostras são definidas de
> formas diferentes (D é condicionada a ter mídia), então não é comparação limpa —
> mas é mais um sinal de instabilidade da composição fina.

**Achado 1 — leque MP/MC é "igual" entre os públicos** (Tab. 7, Gráfico 1):

| público | MP | MC |
|---|--:|--:|
| **EA** (Aécio) | 60,8% (353) | 39,2% (228) |
| **ED** (Dilma) | 67,3% (369) | 32,7% (179) |

**Achado 2 — mas o *conteúdo fino* das MCs difere por lado** (Tab. 6): cada público
compartilha MCs politicamente alinhadas —
- **EA:** blogs do Reinaldo Azevedo, Miriam Leitão, Noblat, Ricardo Setti, Rodrigo
  Constantino, Pastor Everaldo, Congresso em foco, Twitter do Olavo de Carvalho.
- **ED:** Brasil 247, Conversa Afiada (Paulo H. Amorim), Blog do Miro, José Roberto
  de Toledo, Julia Duailibi, Laura Capriglione, Pragmatismo Político.

Conclusão dos autores: os públicos compartilham **a mesma proporção** de MP/MC,
diferindo **só no conteúdo detalhado** das MCs.

---

## 5. A conclusão que os próprios autores VIRARAM (700 → 1.129)

No **2015**, eles levantaram a hipótese: **eleitores da oposição (Aécio)**
determinariam mais o compartilhamento de **mainstream**, e **eleitores da
incumbente (Dilma)** o de **redes sociais/complementares** — efeito "cão de guarda"
(*watchdog*) do jornalismo (Azevedo, 2010).

No **2018**, com amostra maior e um **teste estatístico**, eles escrevem:
> *"Com uma amostra maior e um teste estatístico, no entanto, essa suposição não
> se confirmou."*

Isto é: **a hipótese diferencial de 2015 morreu na expansão do próprio grupo.**
É o argumento-mãe da nossa replicação, entregue pelos próprios autores — só que
eles pararam em 1.129, e nós temos o universo (>200 mil / 10,7 M no banco).

---

## 6. ⚠ Achado estatístico — a Tabela 7 não sustenta a manchete do 2018

A Tabela 7 imprime **"Qui-quadrado = 369,000"**, mas as **contribuições das próprias
células** somam **χ² = 5,294** (0,926 + 1,643 + 0,982 + 1,742). Recalculado do zero
(scipy, `chi2_contingency`):

- **χ² = 5,294** (sem Yates; 5,012 com Yates), **df = 1**, **p = 0,0214** ✓ (bate com o
  p=0,021 que eles reportam → confirma que o "369" impresso é **erro de tabela**;
  o valor real do teste deles é 5,29).
- Crítico a 5%: **3,841**. Como **5,29 > 3,84**, o teste **REJEITA a independência**
  → pelos próprios dados, EA e ED **diferem** significativamente no mix MP/MC
  (ED = 67% MP vs EA = 61% MP).
- **Porém o efeito é minúsculo: Cramér's V = 0,068.** Associação estatisticamente
  significativa (por causa do n), mas de magnitude desprezível.

**Leitura honesta:** o 2018 conflou "efeito pequeno" com "independência". A frase
*"os públicos apresentaram praticamente o mesmo padrão... (p=0,021)"* é imprecisa —
p=0,021 formalmente **rejeita** o "mesmo padrão" a 5%. O correto seria: *associação
significativa porém trivial em tamanho*. **Isto é um achado de replicação sobre o
próprio artigo** (antes mesmo de escalar): a inferência-título não está sustentada
pelo teste que ele mesmo roda. (Recalculado em §Nota; guardar para o confronto.)

---

## 7. Diferenças que a replicação precisa fixar (decisões pendentes deste paper)

1. **Fechar a lista MP (26 vs 25).** O texto diz 26 marcas; só 25 são nomeadas.
   Decidir a 26ª (candidatos: CBN, Globo News — citados no corpo) ou registrar
   "25 nomeadas" e seguir.
2. **Marcas mainstream fora das 26.** Valor, A Tarde, CartaCapital, imprensa
   internacional (BBC, WSJ) são MV no nosso código mas **não** estão nas 26 → pela
   regra estrita seriam MC. Mas **Valor e A Tarde estão no topo** das tabelas do
   próprio 2018. Decidir: (a) seguir a lista fechada ao pé da letra, ou (b) usar a
   regra conceitual "old media na web + agregadores = MP" (que reincluiria Valor etc.).
   As duas dão números diferentes de MP% — reportar a sensibilidade.
3. **Cascata não-aninhada.** C (1.439) é 65,4% de **A (2.200)**, não de B (1.679, o
   filtro "cidadão"). Ou seja, a análise de mídia do 2018 **inclui contas não-cidadãs**.
   Ao reconstruir, decidir se replicamos isso ou se aplicamos o filtro-cidadão antes.
4. **Janela/densidade.** 2018 = **200/dia aleatório, 13–23/out (11 dias)**; 2015 =
   100/dia por pico, 19–25/out (7 dias). A Tab. 1 do 2018 diz "dez dias", mas
   2.200 = 200 × **11** → a janela é 11 dias (inconsistência menor do paper).
5. **Sinais de stance.** 2018 cita hashtags explícitas (#Aécionever, #ForaDilma)
   como 1ª camada, depois análise de sentimento do texto+link. Mesma lógica EA/ED/NDA
   do 2015 — o codebook de stance vale para os dois.

---

## Crosswalk operacional MV/MH → MP/MC (para o `core/midia_dominios.py`)

| Veículo (domínio) | Hoje (MV/MH) | 2018 (MP/MC) | Nota |
|---|:--:|:--:|---|
| G1, Globo.com, O Globo, Extra, Época | MV | **MP** | nas 26 |
| Folha, UOL, Estadão, R7, Terra, iG, Yahoo | MV | **MP** | nas 26 |
| Veja, IstoÉ, Band, Zero Hora, O Dia, JB | MV | **MP** | nas 26 |
| **Valor** | MV | **MC?** | ⚠ fora das 26, mas top-5 na Tab. 3 |
| **A Tarde** | MV | **MC?** | ⚠ fora das 26 |
| **CartaCapital, BBC, WSJ** | MV | **MC** | fora das 26 (e não-BR) |
| Facebook, Twitter, YouTube, Instagram, blogs | MH | **MC** | "social media as complementary" |
| Brasil 247, Congresso em foco, Conversa Afiada, etc. | MH | **MC** | blogs/nicho partidário (Tab. 6) |

> ~~Ação (fase seguinte): reescrever `core/midia_dominios.py` com `MP = {26 marcas}`
> e `MC = resto identificável`, parametrizado para rodar nas duas convenções
> (estrita × conceitual) e comparar.~~
>
> ✅ **FEITO.** O dicionário virou `core/midia_mp_mc.py` (convenção estrita) e as
> duas convenções foram comparadas em 07/ago/2026 por
> `analise/sensibilidade_mp_mc.py`. **A conceitual piora o ajuste ao paper** (+4,9
> p.p.): alargar MP só aumenta MP%, e a estrita já é o mínimo possível. Ver
> [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md).
