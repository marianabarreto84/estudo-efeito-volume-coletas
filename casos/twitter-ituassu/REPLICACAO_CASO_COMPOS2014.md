# Caso de replicação · Twitter/X · Ituassu et al. — #Eleições2014 (par 2015 → 2018)

> Sexto caso do lineup de replicação por expansão. Análises: **sentimento/stance**
> (preferência eleitoral EA/ED) + **classificação de conteúdo** (mídia MP/MC).
> Rede: **Twitter/X**. Preenche a lacuna do lineup — Twitter é 54,5% do
> levantamento DBLP da survey e não aparecia em nenhum caso. Valor adicional:
> fecha o ciclo com o próprio grupo (Lifschitz é coautor e orientador).
> Protocolo geral em [PROTOCOLO_REPLICACAO.md](PROTOCOLO_REPLICACAO.md).

**Alvo: o PAR de papers** (decisão do usuário, jul/2026). Não há alvo "primário" — os
dois são replicados **pelo mesmo pipeline**, e é a comparação entre eles que carrega o
argumento:

- **2015** — Ituassu & Lifschitz, *Temas e Mídia em #Eleições2014*, **E-Compós 18(2)**
  (n=700, taxonomia **MV/MH**, sem teste estatístico).
- **2018** — Ituassu, Lifschitz, Capone, Vaz & Mannheimer, *Compartilhamento de mídia e
  preferência eleitoral no Twitter*, **Palabra Clave 21(3): 860–884** (n=1.129,
  taxonomia **MP/MC**, com Qui-quadrado). Detalhe em
  [PAPER2018_palabra_clave.md](PAPER2018_palabra_clave.md).

**Por que o par, e não só o 2018:** (a) o 2018 **é** a expansão que os próprios autores
fizeram do 2015 — o par já contém uma replicação-por-expansão feita por eles, com uma
conclusão virando no caminho; (b) rodar os dois pelo mesmo pipeline mede o
**efeito-de-taxonomia** (MV/MH-fluxo × MP/MC-marca) sobre **os mesmos tweets**, separado
de volume e escopo; (c) o 2015 **não escapa** dos problemas do 2018 (mesmos tweets,
mesmos links, mesma dependência de link) — o que muda entre eles é a **fragilidade do
claim**, não a do dado. É isso que os torna comparáveis e o par informativo.

---

## 0. Por que dois papers, e o que muda

O **mesmo grupo** publicou duas vezes sobre os mesmos dados: 2015 (preliminar,
n=700) e 2018 (expandido, n=1.129). O 2018 cita o 2015 como "nossos primeiros
resultados". **Eles próprios já fizeram uma expansão** — e no caminho **uma
conclusão virou** (a hipótese "watchdog" de públicos diferenciados; ver §5 e
[PAPER2018 §5](PAPER2018_palabra_clave.md)). Isso nos dá **dois pontos medidos da
mesma curva** antes de chegarmos ao universo:

```
   n=700 (2015)  →  n=1.129 (2018)  →  UNIVERSO (nós: >200 mil / 10,7 M no banco)
   MV/MH            MP/MC + χ²           MP/MC em escala
   ED>EA            EA>ED               ?
   watchdog: SIM    watchdog: NÃO       ?
```

A pergunta da replicação fica mais forte: **não** "a amostra de 700 bastava?",
mas **"a instabilidade que os próprios autores viram entre 700 e 1.129 continua,
estabiliza ou inverte de novo no universo?"**

| Dimensão | 2015 (E-Compós) | 2018 (Palabra Clave) |
|---|---|---|
| N analisado | 700 (100/dia × 7d) | **1.129** (D); cascata 2.200→1.679→1.439→1.129 |
| Janela | 19–25/out (7d) | **13–23/out (11d)** |
| Densidade/amostragem | 100/dia, por pico | **200/dia, aleatório no pico** |
| Tipologia de mídia | MV/MH (fluxo, Shaw 2006) | **MP/MC** (marca, PBM 2014 — 26 veículos MP) |
| Stance | EA/ED/NDA | EA/ED/NDA (mesma lógica; +hashtags explícitas) |
| Teste estatístico | nenhum | **Qui-quadrado** (Tab. 7) |
| Achado dos "públicos" | H3: diferem no leque de MH | independência MP/MC (χ² p=0,021) + diferem só no conteúdo fino das MC |

---

## 1. Afirmações testáveis do 2018 (a camada substantiva)

- **PP1 — predomínio da mídia principal.** MP = 59% × MC = 41% (Amostra C);
  ~2/3 mainstream somando agregadores. **Confirmada no paper.**
- **PP2a — leque MP/MC independe da preferência.** EA 61% MP / ED 67% MP; os
  autores leem como "mesmo padrão" (χ², p=0,021). *← ver a ressalva estatística §5.*
- **PP2b — mas o conteúdo fino das MCs difere por lado** (Tab. 6): blogs de direita
  para EA, de esquerda para ED. **É a tese central sobrevivente** ("social media as
  complementary media", mais partidarizada e alinhada a cada público).
- **Composição:** EA 581 / ED 548 (Amostra D). *Maioria Aécio — invertida vs 2015.*

> Do 2015 herdamos ainda, como pontos de comparação da âncora: **H1** (RTMV>50%),
> **H2** (MH rivaliza com MV em ≥1 dia), composição 226 EA / 284 ED / 156 NDA.
> O eixo mídia já testou H1/H2 sob MV/MH (ver §6); serão **retestados sob MP/MC**.

---

## 2. A ressalva metodológica honesta (vale para os dois papers)

O banco do **eTC** tem coleta de 2014, mesma janela, porém **não é o universo exato**
de onde as amostras saíram — é coleta *vizinha*, mais larga no escopo temático. Logo
`A_mais` **não é estritamente um superconjunto** de nenhuma das amostras. A
divergência medida mistura, em princípio, **efeito-de-volume** com
**efeito-de-escopo-de-coleta**. O desenho abaixo **separa** essas fontes (§3), e a
separação vira contribuição, não defeito.

---

## 3. Os três eixos de expansão (separáveis)

Cada paper ocupa um ponto restrito em **três** eixos ao mesmo tempo. Expandimos um
de cada vez, fixando os outros no valor do paper, para atribuir a mudança a uma causa.

| Eixo | Restrição (2018) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Densidade intra-janela** | 200 tweets/dia | todos os tweets/dia de #Eleições2014 | "a amostra de 200/dia bastava?" |
| **E2 · Escopo temático** | só #Eleições2014 | todas as hashtags eleitorais on-theme | "a hashtag única representa o debate?" |
| **E3 · Extensão temporal** | 13–23/out (11d) | 6–26/out (21d, turno inteiro) | "a janela central representa o turno?" |

E1×E3 fixando E2 (só #Eleições2014) é a comparação **mais limpa** de volume/janela.
E2 entra como eixo adicional, reportado à parte, para não contaminar o teste de
volume puro. **Novidade do par:** o ponto n=700 (2015) e o ponto n=1.129 (2018)
já são duas medições de E1×E3 — dá para **calibrar a curva** com dados reais antes
de extrapolar para o universo.

---

## 4. Taxonomia de mídia — as duas convenções, sobre os mesmos tweets

Rodamos **as duas**: **MV/MH** (2015, critério de *fluxo*) e **MP/MC** (2018, critério de
*marca*). A diferença entre elas, medida sobre os mesmos tweets, **é** o eixo
**efeito-de-taxonomia** — quanto a conclusão muda só por trocar o rótulo, separado de
volume (E1) e escopo (E2). Nenhuma é "a" convenção; o contraste é o dado. O dicionário
determinístico passa a ser a **lista fechada de 26 marcas MP** da Pesquisa Brasileira
de Mídia 2014 (ver [PAPER2018 §2 e crosswalk](PAPER2018_palabra_clave.md)); tudo o
mais identificável = MC; sem link = NDA; encurtador morto = não_resolvido; domínio
fora do dicionário = indefinido.

- **Vantagem:** resolve a antiga "decisão pendente nº1" (reconstruir o dicionário) —
  o 2018 **dá a lista**, mais reproduzível que o MV/MH exemplificado do 2015.
- **Cuidado:** MP é mais restrita que a nossa MV. Valor, A Tarde, CartaCapital, BBC,
  WSJ saem de MV e, pela regra estrita, viram MC — mas Valor/A Tarde estão no topo
  das tabelas do 2018. ✅ **Rodado nas duas convenções em 07/ago/2026** — ver
  [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md).
  Resultado: a conceitual **piora** o ajuste ao paper (+4,9 p.p.), porque alargar MP
  só aumenta MP%. A estrita já é o mínimo possível.
- **Eixo MV/MH (2015): refeito e corrigido em jul/2026** — os scripts liam só o campo
  `links` e contavam ~9% de tweets como NDA quando eram link (t.co só no texto, hoje
  morto). Corrigido com `core/extrai_links.py`. Sobreviveram: dominância MV (83,4%),
  H1 refutada, ΔMV do escopo (h=1,20). Encolheu: tudo apoiado no NDA — intra-autor
  OR **4,47→2,91**. Ver `RESULTADOS_analise_midia_MV_MH.md` §0.
- **Divergência em aberto:** sob MP/MC nossa medição dá MP ~75% contra 59% do paper.
  Causa **não estabelecida**. Candidatos: blogs-em-portal (nós MP, eles MC — ≥5,6% nos
  encurtados), coleta eTC ≠ coleta deles, link rot (hipótese não testada, ~2 p.p.).
  Teste pendente: CDX do Internet Archive nos `t.co` mortos.

---

## 5. Onde apostar + a ressalva estatística do 2018

**Predições pré-registradas (antes de rodar no universo):**

- **Provável MUDA:**
  - *Conteúdo fino das MCs (Tab. 6) e ranking de mais-compartilhados (Tab. 3–5).*
    Percentuais de 1–5% em n~1.400 são frágeis — fortes candidatos a reordenar.
  - *Composição EA/ED.* Já inverteu entre 2015 (ED) e 2018 (EA); a magnitude deve
    se mexer muito no universo.
- **Provável NÃO MUDA:** *PP1 — predomínio agregado de MP.* Efeito grande e
  estrutural. **Contraponto honesto:** no eixo MV/MH essa mesma aposta ("H1 robusto")
  **foi refutada** — o RTMV caiu de ~48% (amostra) para 36% (universo). Então o
  "predomínio" pode ser mais frágil do que parece; ver §6.
- **Incerto / mais interessante:** *PP2a — independência MP/MC.* Ver ressalva abaixo.

> ⚠ **Ressalva estatística sobre o 2018 (achado de replicação já no paper).**
> A Tabela 7 imprime χ²=369, mas o valor real (soma das células deles, e recálculo
> por scipy) é **χ² = 5,29, df=1, p=0,0214** — o "369" é erro de tabela. Como
> 5,29 > 3,84 (crítico 5%), o teste **rejeita** a independência: EA e ED **diferem**
> no mix MP/MC (ED 67% MP > EA 61% MP). Mas **Cramér's V = 0,068** (efeito trivial).
> Ou seja: o 2018 trocou "efeito pequeno" por "independência". No universo, com N
> gigante, **qualquer** diferença fica hiper-significativa — então o teste correto
> deixa de ser "há diferença?" e passa a ser **tamanho de efeito** (V, Cohen's h,
> ICs da diferença). Fixar isso no protocolo desde já.

---

## 6. Pipeline por fase (instanciando o PROTOCOLO)

### Fase 0 — Reproduzir o 2018 (sanity check agregado)
Os rótulos manuais originais (nem 700 nem 1.129) são recuperáveis. Reprodução é
**agregada**: reconstruir a amostra pela regra do 2018 (**200/dia aleatório no pico,
13–23/out, só #Eleições2014**, cascata A→B→C→D) e verificar se as **proporções**
batem: 65,4% com mídia, **MP 59% / MC 41%**, EA 581 / ED 548, χ² e a Tab. 6.
Fazer o **mesmo para o 2015** (100/dia por pico, 19–25/out) como ponto-âncora.

> Se as proporções reconstruídas não baterem, já é achado: a amostra é instável a
> ponto de nem reamostrar a mesma regra a reproduzir.

### Fase 0.5 — Validar os classificadores (contribuição metodológica própria)
1. **Mídia MP/MC:** lookup determinístico por domínio do 1º link. Reescrever
   `core/midia_dominios.py` com as 26 marcas MP (§4); rodar nas duas convenções.
   Quase não precisa de ML — mas precisa fixar a lista (decisões em
   [PAPER2018 §7](PAPER2018_palabra_clave.md)).
2. **Stance EA/ED/NDA:** ◐ **kit montado em 18/ago/2026** — amostra de **320** tweets
   sorteada e congelada (seed `20260818`, split 110 dev / 210 teste cego, reteste de 40),
   codebook operacional em [CODEBOOK_stance.md](CODEBOOK_stance.md) e pré-registro
   (apostas + critério κ ≥ 0,70, escrito antes de medir) em
   [PRE_REGISTRO_stance.md](data/repl/compos2014/stance/PRE_REGISTRO_stance.md).
   **Falta só a rotulagem humana** (~3–4 h); a validação e a aplicação em escala
   espelham o fluxo já validado no caso vacinas.
3. **Temas (só herdado do 2015):** o 2018 **abandonou** o eixo temas. Fica como
   análise exploratória opcional (topic modeling), não teste estrito.

### Fase 1 — A_mais (snapshot congelado) — **já feito**
`data/repl/compos2014/`: `snapshot_hashtag.sqlite` (140.909, só #Eleições2014) e
`snapshot_full.sqlite` (214.393, qualquer hashtag eleitoral) + `expand_cache.sqlite`.

### Fase 2 — Curva A(volume) com dois pontos ancorados
Frações crescentes de N até N_máx, **≥30 réplicas bootstrap/ponto**, três curvas
(uma por eixo). **Ancorar a curva nos pontos reais 700 e 1.129** e ver se a
tendência 2015→2018 continua até o universo.

### Fase 3 — Divergência (métricas do protocolo)

| Análise | Métrica | Afirmação que pode inverter |
|---|---|---|
| **Mídia MP/MC** | JS dos histogramas; MP% agregada; **tamanho de efeito** EA×ED (V, h) ao longo do N | PP1 (MP domina) se mantém? PP2a (independência) — o efeito trivial vira relevante ou some? |
| **Stance EA/ED** | JS das distribuições; classe majoritária; série temporal | EA>ED (2018) sobrevive, ou volta a ED (2015), ou some? |
| **Conteúdo fino MC** | RBO / Kendall-τ entre rankings (Tab. 3–6) | PP2b: o alinhamento MC-por-lado sobrevive? |

### Fase 4 — Tabela mestre + recomendação
Linha do caso: *as amostras (700/1.129) bastavam? × a conclusão mudou? × fração
mínima que estabiliza cada conclusão* — agora com **dois pontos empíricos** na curva.

---

## 7. Decisões pendentes (específicas deste caso)

1. ~~**Fechar a lista MP** (26 vs 25 nomeadas) e o tratamento das mainstream fora das
   26 — convenção estrita × conceitual.~~ ✅ **RESOLVIDO em 07/ago/2026, por medição.**
   Não é decisão a tomar: as duas convenções foram rodadas e a **estrita é a certa**
   por ser o mínimo de MP — a conceitual afasta ainda mais do paper. E a divergência
   MP 72,2% × 59% **não vem daí**: as quatro explicações do nosso lado (lista,
   blog-em-portal, resíduo `indefinido`, link rot) foram testadas e descartadas. Ver
   [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md) e
   [link rot](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md). O que resta é do
   lado do artigo e **não é resolúvel com o material publicado**.
2. **Reconstruir a cascata do 2018** (A→B→C→D) — decidir se replicamos a
   não-nidificação (C sai de A, não de B: análise de mídia inclui não-cidadãos) ou
   se aplicamos o filtro-cidadão antes.
3. ~~**Tamanho da amostra de rotulagem manual** (stance, Fase 0.5)~~ — **fixado em
   18/ago/2026: 320 tweets** (110 dev / 210 teste cego), com justificativa no
   [pré-registro](data/repl/compos2014/stance/PRE_REGISTRO_stance.md) §1. **Resta**
   decidir **quem** rotula: com 1 pessoa mede-se só o teto intracodificador (reteste de
   40); com 2, sai também o κ humano×humano — a 2ª pessoa preenche uma **cópia** do
   mesmo CSV.
4. **Schema rico como análise nova ou controle?** RT/likes/seguidores/verificação
   permitem centralidade/influência que nenhum dos papers fez. Bônus possível, sem
   fugir do escopo "efeito de volume".
5. **Reportar a inconsistência da Tab. 7 do 2018** como achado (χ²=369 impresso vs
   5,29 real; independência vs efeito trivial) — parte do confronto, não só nota.

---

*Docs irmãos: [PAPER2018_palabra_clave.md](PAPER2018_palabra_clave.md) (alvo
primário, taxonomia MP/MC, crosswalk) · [STANCE_...md](STANCE_como_o_paper_fez_e_onde_estamos.md)
(eixo stance) · `RESULTADOS_analise_midia_MV_MH.md` + `data/repl/compos2014/RESULTADOS_*.md`
(resultados do eixo mídia sob a convenção-âncora 2015).*
