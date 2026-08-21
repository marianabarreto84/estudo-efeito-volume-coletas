# Guia de rotulagem manual — caso vacinas, eixo B

> **Gerado** por `analise/gera_guia_rotulagem.py` a partir do mesmo
> codebook que alimenta o prompt do rotulador automatico. Nao editar a
> mao: se este guia e o prompt divergirem, o κ deixa de comparar dois
> rotuladores fazendo a mesma tarefa.

Preencher em `VALIDACAO_HUMANA_amostra.xlsx`, aba `ROTULAR`.

---

## Antes de comecar: tres regras que valem para tudo

1. **Julgue o autor, não quem ele cita.** Um tweet que reproduz uma
   fala anti-vacina para ridicularizá-la é `pro`. Ironia e sarcasmo
   são comuns neste corpus.
2. **Marque o que é citado ou aludido, ainda que de passagem.** O tema
   não precisa ser o assunto principal do tweet. Um tweet sobre
   vacinação infantil que menciona a Anvisa de passagem é *também*
   categoria 1 (Politics).
3. **Não olhe os rótulos do modelo antes de terminar.** Eles estão em
   `rotulos_llm/e1_lim10_pt_p4/rotulos.csv`. Ver antes de rotular
   ancora o julgamento e o κ passa a medir concordância induzida.

---

## Parte 1 — stance (uma escolha por tweet)

| valor | quando usar |
|---|---|
| `pro` | defende, promove ou apoia a vacinação |
| `anti` | questiona, ataca ou desencoraja a vacinação |
| `nenhum` | não permite decidir de lado nenhum |

**`nenhum` é raro.** No gabarito humano do paper, 3 tweets em 1.525.
Estes são tweets de um debate polarizado: quase todos tomam partido,
ainda que de forma indireta. Se houver qualquer indício de posição,
escolha `pro` ou `anti`. Não use `nenhum` como saída para o caso
difícil — decida, e anote a dúvida em `observacao`.

> Atenção: a amostra vem do estrato **pouco viralizado**, que pode ter
> mais tweets ambíguos que o estrato viral do paper. Se você achar que
> `nenhum` está sendo necessário com muito mais frequência que 1 em
> 500, isso é em si um achado — anote.

---

## Parte 2 — categorias (zero, uma ou várias por tweet)

Escreva os **números** separados por vírgula (ex.: `1,2,8`). Vazio se
nenhuma se aplica.

As categorias vêm em dois formatos, e a pergunta muda:

- **com lista de gatilhos** → *o tweet cita ou alude a algum destes?*
  Basta **um**. Quando a lista terminar em *“e qualquer outra menção
  a X”*, ela é ilustrativa e não fechada.
- **sem lista** (tema amplo) → *o tema aparece no tweet?* Uma menção
  de passagem já conta.

### 1. Politics — Politica

**Gatilhos** (lista **aberta** — os exemplos abaixo **e qualquer outra menção a Politics**):

- Bolsonaro
- GovernmentNotRegional
- Pro-government politicians
- senators deputies councilors
- Regional Governments
- Lula
- PT
- other Left politicians
- Paes
- Dória
- Anti-vacine policies
- Vaccination delay
- Public Consultation on COVID-19 child immunization
- Minister of National Health Services
- Ministry of National Health Services
- Public National Health Services
- National Health Surveillance Agency
- Corruption
- Lobby
- Political supporters
- Judiciary

_No gabarito do paper: 719 de 1.525 tweets (47.1%)._

### 2. Children — Criancas

**Gatilhos** (lista **aberta** — os exemplos abaixo **e qualquer outra menção a Children**):

- Pro need of vaccine prescription for children
- Against need of vaccine prescription for children

_No gabarito do paper: 592 de 1.525 tweets (38.8%)._

### 3. Restrictive policies — Politicas restritivas

**Gatilhos** (lista **aberta** — os exemplos abaixo **e qualquer outra menção a Restrictive policies**):

- Pro freedom for the vaccinees
- Against freedom for the anti-vaccine
- Pro mandatory vaccination
- Pro vaccination but against its obligation
- Pro freedom for the anti-vaccine
- Against mandatory vaccination
- Pro vaccine to university enrollment
- Pro vaccine to school / University enrollment
- Against vaccine to university enrollment
- Against vaccine to school / University enrollment

_No gabarito do paper: 531 de 1.525 tweets (34.8%)._

### 4. Disadvantages of vaccines — Desvantagens das vacinas

**Gatilhos** (lista fechada — se não é um destes, não é esta categoria):

- Non-severity of covid in children
- Non-severity of covid
- Natural immunity is better than vaccine
- Ineffectiveness of vaccines
- Vaccine risks

_No gabarito do paper: 378 de 1.525 tweets (24.8%)._

### 5. Anti-vaccine people — Pessoas anti-vacina

**Gatilhos** (lista **aberta** — os exemplos abaixo **e qualquer outra menção a Anti-vaccine people**):

- Unvaccinated do not risk others
- Unvaccinated risk others
- Anti- only COVID-19 vaccine
- Oneself anti-vaccine
- Someone specific anti-vaccine
- Pointing someone not vaccinated
- Anti-vax movement
- Anti-vaccination people who get vaccinated

> ⚠ conta tambem mencao generica a pessoas antivacina ('os negacionistas', 'quem nao se vacina'), nao so a pessoa nomeada

_No gabarito do paper: 375 de 1.525 tweets (24.6%)._

### 6. International — Internacional

**Gatilhos** (lista **aberta** — os exemplos abaixo **e qualquer outra menção a International**):

- USA
- World
- Australia
- England UK
- Canada
- Germany
- Austria
- France
- Italy
- Sweden
- China
- Europe
- Israel
- Mexico
- Czech republic
- Norway
- South Africa
- Cuba
- Argentina
- Denmark
- New Zeland
- Portugal
- Serbia
- South Korea

_No gabarito do paper: 253 de 1.525 tweets (16.6%)._

### 7. Advantages of vaccines — Vantagens das vacinas

**Gatilhos** (lista fechada — se não é um destes, não é esta categoria):

- Effectiveness of vaccines
- Vaccine safety
- Misinformation on vaccine risks

> ⚠ ATENCAO: o codebook do paper coloca 'desmentir desinformacao sobre riscos da vacina' DENTRO desta categoria, e nao na 9

_No gabarito do paper: 242 de 1.525 tweets (15.9%)._

### 8. COVID risks — Riscos da COVID

**Tema amplo.** Marque sempre que riscos da covid aparecer, ainda que de passagem. Não há lista fechada.

_No gabarito do paper: 241 de 1.525 tweets (15.8%)._

### 9. Misinformation sources — Fontes de desinformacao

**Gatilhos:**

- Misinformation

> ⚠ use so quando o tweet trata da desinformacao ENQUANTO TAL: mentira, boato, fake news, checagem, desmentido

_No gabarito do paper: 201 de 1.525 tweets (13.2%)._

### 10. Information sources — Fontes de informacao

**Gatilhos** (lista fechada — se não é um destes, não é esta categoria):

- Social media
- Official media

> ⚠ use quando o tweet trata de veiculos e canais de informacao enquanto tais (imprensa, TV, redes sociais, jornalistas), sem juizo sobre serem falsos; se o ponto e a falsidade, use a 9

_No gabarito do paper: 179 de 1.525 tweets (11.7%)._

### 11. Science — Ciencia

**Tema amplo.** Marque sempre que ciencia aparecer, ainda que de passagem. Não há lista fechada.

_No gabarito do paper: 94 de 1.525 tweets (6.2%)._

### 12. Vaccines type or laboratories — Tipos de vacina / laboratorios

**Gatilhos** (lista fechada — se não é um destes, não é esta categoria):

- VaccineLab generally
- BioCuba Pharma
- Moderna
- Butantan
- Sinovac
- Sputnik
- AstraZenecaOxford
- Vaccine types
- Pfizer
- CEO Pfizer

_No gabarito do paper: 86 de 1.525 tweets (5.6%)._

### 13. Religion — Religiao

**Tema amplo.** Marque sempre que religiao aparecer, ainda que de passagem. Não há lista fechada.

_No gabarito do paper: 46 de 1.525 tweets (3.0%)._

### 14. Other drugs — Outras drogas

**Gatilhos:**

- OtherDrugs Cloroquina
- Ivermectna

_No gabarito do paper: 32 de 1.525 tweets (2.1%)._

---

## As duas fronteiras que mais confundem

Foram medidas como as piores do rotulador automático (κ 0,376 e
0,518). Preste atenção nelas — é onde a sua rotulagem mais informa:

**7 (Advantages) × 9 (Misinformation sources).** O codebook do paper
coloca *“desmentir desinformação sobre riscos da vacina”* dentro de
**Advantages**, não de Misinformation. Um tweet que derruba um boato
sobre efeito colateral é categoria **7**. A categoria 9 é para quando
o tweet trata da desinformação *enquanto tal* (a mentira, o boato, a
checagem como assunto).

**9 (Misinformation sources) × 10 (Information sources).** A 10 é o
veículo enquanto veículo (imprensa, TV, redes sociais, jornalistas),
sem juízo sobre ser falso. Se o ponto do tweet é a falsidade, é a 9.

---

## Quando terminar

Salve o arquivo e rode:

```
python -u analise/valida_estrato_baixo.py
```

Ele calcula o κ entre você e o rotulador nesta amostra e escreve o
resultado em `VALIDACAO_ESTRATO_BAIXO.md`. O critério é o mesmo do
teste cego: κ ≥ 0,70 no stance, mediana ≥ 0,60 nas categorias.

- **Se passar:** o achado da Fase 3 (a inversão do stance) deixa de
  ser provisório.
- **Se reprovar:** o rotulador não transfere para o estrato baixo, e a
  seção 1 da Fase 3 cai — o que é um resultado legítimo e publicável,
  não um fracasso. Reporta-se que o instrumento validado no estrato
  viral não se sustenta fora dele.