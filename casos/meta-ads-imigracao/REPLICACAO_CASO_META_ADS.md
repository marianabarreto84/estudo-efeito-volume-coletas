# Caso de replicação · Instagram/Facebook · Capozzi et al. (2020, 2021) — anúncios de imigração

> Caso **Instagram/Facebook** do lineup, a última rede sem alvo definido. Alvo:
> **Capozzi et al., CHI 2021** (29 cit.) + **SocInfo 2020** (16 cit.), sobre anúncios de
> imigração na Itália coletados da **Meta Ad Library**. Análise: **classificação**
> (pró/anti-imigração, F1 = 0,85) — o tipo que faltava. Alvo destrinchado em
> [ARTIGO_CAPOZZI_alvo.md](ARTIGO_CAPOZZI_alvo.md); viabilidade em
> [FASE0_descoberta.md](data/repl/metaads2019/FASE0_descoberta.md).

**Valor no lineup.** Três coisas que nenhum outro caso dá:

1. **Fecha a única rede vaga** da Tab. `tab:casos` com o tipo de análise que ela pede
   (`Classificação`), sem precisar concentrar um terceiro caso no Reddit.
2. **A sub-coleta é declarada pelos próprios autores**, em uma frase: *"we search for ads
   appearing only on Facebook (**not Instagram**)"*. A expansão *é* a plataforma que dá
   nome à célula. Não é preciso argumentar que houve sub-coleta — está no §3 do artigo.
3. **Tem gabarito publicado e verificado** (2.312 anúncios, [CSV baixado](data/repl/metaads2019/gabarito_capozzi2020.csv)),
   e a **lista completa das 26 palavras-chave** do filtro está no Apêndice A. A Fase 0
   é reprodutível ao pé da letra — situação melhor que a de qualquer caso anterior.

---

## 1. Afirmações testáveis

Transcritas do alvo (ver [ARTIGO_CAPOZZI_alvo.md](ARTIGO_CAPOZZI_alvo.md) §3):

| | Afirmação | Origem |
|---|---|---|
| **CA1** | Salvini é o maior anunciante sobre migração (>50 k €, ~8 M impressões) | SocInfo ✅ lido |
| **CA2** | Impressões muito desiguais: Gini **0,465** por página, **0,800** por anúncio | SocInfo ✅ |
| **CA3** | Impressões acompanham o calendário eleitoral (pico nas europeias de mai/2019) | SocInfo ✅ |
| **CA4** | Anúncios de migração atingem público **mais masculino** que os políticos gerais (~20% odds) | SocInfo ✅ |
| **CB2** | Anti = **47,6% dos anúncios** mas **65,2% das impressões** ⚠ **três denominadores** | CHI ✅ lido |
| **CB4** | Anti dos grandes partidos: **17%** mais chance de atingir homens (OR 1,17); no conjunto todo, **OR 1,69** | CHI ✅ |
| **CB5** | *Riding the wave*: notícias **causam** (Granger, δ=1 dia) as impressões dos anúncios; não o inverso | CHI ✅ |

**CB2 é o alvo-teste central.** É um **balanço entre polos medido dentro de um estrato** —
a mesma família de afirmação que já falhou **três vezes** no caso vacinas, em três
operacionalizações independentes (linhas 4b, 4c e 7 da
[tabela mestre](../RESULTADOS_tabela_mestre.md)). Se falhar aqui também, numa **rede
diferente**, com **unidade diferente** (anúncio pago, não post orgânico), vira a evidência
mais forte da leitura PP3 nº 3.

✅ **CB2 desambiguado em 7/ago/2026** — ver [DECISOES_CB2.md](data/repl/metaads2019/DECISOES_CB2.md).
O resumo do CHI contrasta duas proporções de **populações diferentes** (os 47,6% são só dos
grandes partidos; os 65,2% são das impressões dos anúncios **com posição**), e entre todos
os 2.312 os anti são **677 = 29,3%**. A decisão: medir a **razão de desproporção**
R = fatia de impressões ÷ fatia de anúncios sobre a base dos **anúncios com posição**
(R = **1,72**), reportando sempre ao lado a base de **todos** (R = **1,46**). R é a
grandeza que carrega a afirmação substantiva ("capturam atenção acima do seu peso") e é
adimensional, logo comparável entre estratos e entre plataformas.

**Ressalva de reprodutibilidade:** CB2 e CB4 dependem do **classificador pró/anti**, que
precisa do **texto dos anúncios**. O CSV de metadados não o traz — mas o **segundo
repositório dos autores traz o texto dos 200 anúncios anotados**, sem passar pela API
(§4.1 do ARTIGO). Para os outros 2.112, o texto depende da retenção.

---

## 2. Os eixos de expansão (separáveis)

O artigo ocupa **um ponto**: Facebook × 26 keywords × Itália × mar/2019–mar/2020. Cada
restrição é um eixo, e todas são expansíveis pelo mesmo instrumento (Ad Library API).

| Eixo | Restrição (paper) | Expansão | Isola a pergunta |
|---|---|---|---|
| **E1 · Plataforma** | só Facebook, **por escolha declarada** | **+ Instagram** (mesmo arquivo, campo `publisher_platforms`) | "a conclusão era da plataforma ou do tema?" |
| **E2 · Largura do filtro** | 26 keywords | lista mais larga; e **sem keyword** nas páginas políticas (o próprio baseline deles: **17.014** × 2.312 = **7,4×**) | "o filtro temático fabricou o balanço?" |
| **E3 · Janela** | mar/2019 – mar/2020 (12 meses) | até o fim da veiculação política na UE (**out/2025**) | "12 meses representavam o debate?" |
| **E4 · Polity** | Itália | **Brasil** (ver §3) | "a conclusão é do desenho ou do país?" |

**E1 é o eixo primário** — é ele que preenche a célula da `tab:casos` e o único que o
artigo entrega de bandeja como sub-coleta declarada.

**E2 tem um número pronto e forte:** os autores já mediram o universo não-filtrado das
páginas políticas (17.014 anúncios) e **não o usaram** para o balanço pró/anti. A razão
7,4× é a medida direta do encolhimento — comparável ao eixo E3 do caso vacinas
(largura de filtro × volume como eixos independentes, leitura PP3 nº 4).

---

## 3. O braço Brasil (E4) — o que é e o que **não** é

**Decisão de 7/ago/2026 (Mariana):** o Brasil entra como **segundo braço do mesmo caso**,
não como caso próprio.

- **Por quê:** a Ad Library brasileira é a coleta Meta mais segura que existe hoje — o
  Brasil **não** foi atingido pela proibição de anúncios políticos na UE (out/2025) e os
  anúncios de 2022 estão dentro da retenção de 7 anos (até 2029). Se o arquivo italiano
  tiver caído, o braço brasileiro **carrega o caso**.
- **Por que não é caso próprio:** o alvo brasileiro candidato
  ([*Characterizing Brazilian Political Ads on Facebook*](https://sol.sbc.org.br/index.php/webmedia/article/view/22091),
  WebMedia 2022) **não passa na régua do lineup**: é análise **descritiva** (impressões,
  gasto, anunciantes), **não classificação**, e **não está indexado no Semantic Scholar** —
  o mesmo diagnóstico de "sem tração" que descartou o #207.
- **O que o braço mede:** aplica o desenho do Capozzi (keywords → classificador pró/anti)
  ao Brasil e pergunta se o **padrão** se repete. É teste de **robustez entre polities**,
  não replicação de conclusão publicada.
- **⚠ Consequência para a escrita:** o braço Brasil **não gera linha na `tab:casos`** nem
  na tabela mestre. Entra como seção de robustez do capítulo. Registrar assim, para não
  inflar o lineup.

---

## 4. Pipeline por fase

### Fase 0 — Alvo + viabilidade ◐ **quase fechada**
Feito: **os dois artigos lidos na íntegra**; os **dois** datasets públicos baixados e
conferidos; keywords transcritas; rota de coleta decidida; predições pré-registradas (§5);
e o **α de Krippendorff do CHI 2021 reproduzido** (0,763 × 0,76 nos 5 rótulos; 0,924 × 0,92
nas 2 polaridades) por `analise/reproduz_alpha_chi2021.py`.
⏳ **Falta só o que é externo:** o **teste de retenção** (§6), que depende da conta Meta.
Ver [FASE0_descoberta.md](data/repl/metaads2019/FASE0_descoberta.md).

### Fase 1 — Coletar o universo + snapshot ⏳
Com a conta verificada, consultar a Ad Library API e congelar `snapshot_metaads.sqlite`:

1. **Ponto original:** as 26 keywords × Itália × mar/2019–mar/2020 × `publisher_platforms`
   contendo Facebook → deve reproduzir os **2.312 anúncios**. Comparar com o gabarito
   `ad_id` a `ad_id`: a taxa de recuperação **é a medida da retenção** e um resultado em si.
2. **E1:** as mesmas keywords **sem** restringir a plataforma → Facebook ∪ Instagram.
3. **E2:** todos os anúncios das 208 páginas políticas, sem keyword (alvo: os 17.014).
4. **E3:** estender a janela até out/2025.
5. **E4:** repetir 1–3 para o Brasil, com lista de keywords própria (§7).

Guardar **texto e criativo** dos anúncios — sem eles não há eixo B.

### Fase 2 — Curva A(volume) ⏳
Reconstruir CB2 (fatia anti em anúncios × em impressões) em frações crescentes, do ponto
do artigo ao universo, com **≥30 réplicas bootstrap** por ponto. Uma curva por eixo, para
separar volume de largura de filtro de plataforma.

### Fase 3 — Divergência ⏳

| Afirmação | Métrica | Pode inverter/confirmar |
|---|---|---|
| **CB2** | fatia anti em anúncios e em impressões, por fração e por eixo | o gap 47,6% × 65,2% sobrevive ao Instagram? |
| **CA2** | Gini por página e por anúncio, por fração | esperado robusto (cauda extrema) |
| **CA1** | ranking de anunciantes | esperado robusto (dominância qualitativa) |
| **CA4** | odds de atingir homens, por fração e por plataforma | o Instagram borra o viés de gênero? |

### Fase 4 — Linhas da tabela mestre ⏳
Preencher as linhas *Instagram/Facebook · Classificação* em
[`../RESULTADOS_tabela_mestre.md`](../RESULTADOS_tabela_mestre.md) (linhas 13 e 14).

---

## 5. Predições pré-registradas (antes de rodar)

Ancoradas nas leituras PP3 já consolidadas na [tabela mestre](../RESULTADOS_tabela_mestre.md) §5:

- **Provável MUDA (forte) — CB2.** É balanço entre polos: a família que falhou em 4b, 4c e
  7. **Direção apostada:** a fatia **anti cai** ao incluir o Instagram. Mecanismo: o próprio
  artigo mede que os anúncios anti são mais masculinos e mais velhos (CA4), e o Instagram
  tem composição demográfica distinta — logo o estrato Facebook-only **superestima** o polo
  anti. É a aposta central e a mais falsificável.
- **Provável CONFIRMA — CA2** (Gini). Concentração de cauda extrema é estruturalmente imune
  à sub-coleta (leitura PP3 nº 3): a cauda é o que qualquer coleta captura primeiro.
- **Provável CONFIRMA — CA1** (Salvini domina) e **CA3** (picos eleitorais): dominância
  qualitativa e sazonalidade agregada convergem cedo (leitura PP3 nº 1).
- **Incerto / interessante — CA4.** Se o viés de gênero **encolher** no Instagram, o achado
  de micro-targeting do artigo era em parte propriedade da plataforma escolhida.
- **Provável NÃO CONVERGIU:** n=2.312 é pequeno para uma proporção estratificada por
  partido × plataforma.
- **Registrar humildade:** se CB2 **não** se mover, é resultado igualmente publicável — e
  seria o **primeiro** contra-exemplo à leitura PP3 nº 3, o que vale mais que uma
  confirmação. Anotar como tal.

**A terceira pergunta se aplica aqui.** Pela proposta registrada na
[tabela mestre §5.0](../RESULTADOS_tabela_mestre.md), cabe perguntar se o **esquema de
seleção** é não-viesado para a quantidade de interesse. Aqui ele declaradamente não é: o
filtro é por keyword **e** por plataforma. E2 e E1 medem exatamente esse viés.

---

## 6. Bloqueios

| O quê | Travado em | Destrava com |
|---|---|---|
| ⏳ **Toda a Fase 1** | acesso à Ad Library API | **conta Meta verificada** — documento oficial, 1-3 dias úteis. **Só a Mariana faz.** Grátis, sem porteiro institucional |
| ⏳ **Teste de retenção** | idem | com a conta, consultar um punhado de `ad_id` do gabarito. **Decide se o eixo B italiano sobrevive** |
| ✅ **CB2/CB4/CB5 conferidos** | — | **full text lido em 7/ago/2026** — e revelou a ambiguidade de denominador de CB2 (§1) |
| ◐ **Texto dos anúncios** | não está no CSV de metadados | **os 200 anotados já estão em mãos** (repo do CHI); os outros 2.112 dependem da retenção |

**Risco declarado:** a Meta parou de veicular anúncios políticos na UE em **out/2025** e a
retenção de anúncios políticos é de **7 anos** — os anúncios de mar/2019 estão no limite.
Há ainda uma nota da Meta de que anúncios da UE seriam arquivados **1 ano após a última
impressão**, que, se valer, elimina o corpus italiano. **Não foi possível verificar sem a
conta.** É por isso que o braço Brasil (§3) existe.

---

## 7. Decisões pendentes (específicas)

1. **Lista de keywords do Brasil** — traduzir a lista italiana não serve (`clandestino`,
   `extracomunitario` e `scafisti` não têm equivalente político no Brasil). Construir pelo
   mesmo método (semente + FastText) sobre qual tema? Imigração venezuelana/haitiana é o
   análogo direto; mas o debate migratório brasileiro é muito menor que o italiano.
   **Alternativa a considerar:** trocar o tema do braço BR por um de volume comparável,
   assumindo que aí ele deixa de ser réplica do desenho e vira só "mesmo método, outro tema".
2. **Janela do E3** — parar em mar/2020 (fiel), ir até out/2025 (máximo) ou até as eleições
   seguintes (2022)? A janela maior mistura efeito-temporal com efeito-volume.
3. **Unidade de análise** — o artigo alerta que "a mesma mensagem pode aparecer em vários
   anúncios, o que torna o anúncio bruto uma unidade pouco significativa" e por isso usa
   **impressões e gasto**. Fixar a unidade antes da Fase 2, e reportar CB2 nas duas
   (é literalmente o que a afirmação contrasta).
4. ~~**Reusar ou refazer o classificador**~~ — **encolheu em 7/ago/2026:** o gabarito
   pró/anti do CHI 2021 **é público** (200 anúncios × 3 anotações, com texto) e o α já
   reproduziu. O fluxo do caso vacinas transpõe direto e **não precisa de rotulagem humana
   nova para calibrar**. O que resta decidir é menor: usar a escala Likert de 5 pontos do
   artigo ou o binário pró/anti, e se vale medir o **teto da tarefa** (o α de 0,76 já é uma
   estimativa dele, publicada e agora verificada).
5. ~~**Qual CB2 medir**~~ — **fechada em 7/ago/2026**, ver
   [DECISOES_CB2.md](data/repl/metaads2019/DECISOES_CB2.md). Base primária = **só os
   anúncios com posição**; base companheira = **todos**; a dos grandes partidos fica
   reportada, não testada. A métrica levada à curva é a **razão de desproporção**
   R = fatia de impressões ÷ fatia de anúncios (**1,72** na base primária, **1,46** na
   companheira), porque R é adimensional e sobrevive à troca de população que a expansão
   para o Instagram provoca. ⚠ Descoberto no caminho: **o total de impressões do artigo não
   reproduz** a partir do CSV publicado (35 M reportados × 49,8 M pela regra que ele declara
   usar) — a Fase 2 roda as duas convenções.

---

*Docs irmãos: [ARTIGO_CAPOZZI_alvo.md](ARTIGO_CAPOZZI_alvo.md) ·
[FASE0_descoberta.md](data/repl/metaads2019/FASE0_descoberta.md).*
