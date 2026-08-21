# Fase 0 — Alvo e viabilidade do dado (caso Instagram/Facebook / Capozzi 2020-2021)

> Gerado em **7/ago/2026** por análise documental **offline** + consultas de rede sem
> autenticação (GitHub API, download dos dois datasets dos autores, PDFs dos dois artigos).
> Sem VPN, sem banco, sem gasto de LLM. Números do gabarito apurados por leitura direta dos
> CSVs; números do alvo com a seção do paper como proveniência (ver
> [ARTIGO_CAPOZZI_alvo.md](../../../ARTIGO_CAPOZZI_alvo.md)).
>
> **Estado: ◐ quase fechada.** Ambos os artigos lidos na íntegra, os **dois** datasets
> públicos baixados e conferidos, e o α de Krippendorff do CHI 2021 **reproduzido** (§4.2).
> Resta **uma** pendência, e é externa: a conta Meta verificada (§5.1).

## 1. O que o alvo é (resumo operacional)

- **Capozzi et al.**, ISI Foundation. Dois artigos sobre o mesmo corpus: **SocInfo 2020**
  (16 cit., caracterização) e **CHI 2021** (**29 cit.**, classificação pró/anti, F1 = 0,85).
- Coleta = **Meta Ad Library API**, consulta única em 30/mar/2020, anúncios da Itália,
  filtrados por **26 palavras-chave** de migração → **2.312 anúncios de 733 páginas**.
- **A sub-coleta é declarada pelos autores**: *"we search for ads appearing only on
  Facebook (**not Instagram**)"* (SocInfo §3). O Instagram estava no mesmo arquivo, sob a
  mesma consulta, e foi descartado por escolha.
- Afirmação-alvo central (**CB2**): anti-imigração são **47,6% dos anúncios** mas
  **65,2% das impressões**.

## 2. O que "coletar mais" exige (o universo-alvo)

O universo *on-theme* = os mesmos anúncios de migração na Itália, **sem** o corte de
plataforma (Facebook ∪ Instagram), **sem** o estreitamento por keyword (o baseline dos
próprios autores já mostra **17.014** anúncios nas páginas políticas contra 2.312 filtrados
= **7,4×**) e, opcionalmente, com janela maior. O tema é preservado; os 2.312 são um
subconjunto materializado do que a mesma API entrega.

**Tamanho esperado (a confirmar na Fase 1):** dezenas de milhares de anúncios — ordem de
grandeza muito menor que qualquer caso de Twitter/Reddit do lineup. Trivial em SQLite local.
O gargalo aqui **não é volume, é acesso**.

## 3. Viabilidade — rota de coleta

Varridas as quatro rotas de coleta Meta existentes em ago/2026:

| Rota | Estado |
|---|---|
| **Ad Library API** | ✅ **rota escolhida** — grátis, exportável, viva. Exige só conta Meta pessoal + verificação de documento (1-3 dias úteis). Cobre **Facebook e Instagram**. Retenção de **7 anos** para anúncios políticos |
| **Meta Content Library** | ❌ **descartada.** Passou a cobrar **US$ 371/mês + US$ 1.000** de entrada em jan/2026, exige aprovação do CASD, e **os dados não saem do ambiente seguro** — incompatível com a Fase 1 do protocolo (snapshot congelado local). O impeditivo é o ambiente fechado, não o preço |
| **CrowdTangle** | ❌ desligado em ago/2024 |
| **API pública do Instagram** | ❌ morta desde 2018-2020. É o que inviabiliza os papers de Instagram mais citados (ex.: Hosseinmardi 2015, 189+222 cit., com sub-coleta de desenho ideal — rotulou 2.218 de ~25 k sessões por limiar de ≥15 comentários — mas **sem como coletar mais**) |

**Consequência para o lineup:** a célula Instagram/Facebook só fecha por Ad Library. Isso
restringe o objeto a **anúncio pago**, não post orgânico — e essa restrição deve ser
declarada no capítulo, não escondida.

## 4. Gabarito do paper ✅ — publicado, baixado e conferido

[github.com/PotenteOpossum/Facebook-Ads-Politics-of-Migration-in-Italy](https://github.com/PotenteOpossum/Facebook-Ads-Politics-of-Migration-in-Italy)
— repositório público, existência verificada pela API do GitHub em 7/ago/2026 (id
282867703). Dois arquivos: o README com a citação e o CSV. Baixado para
[`gabarito_capozzi2020.csv`](gabarito_capozzi2020.csv) (945.780 bytes).

Conferência do CSV contra o artigo:

| | apurado | paper | |
|---|--:|--:|---|
| anúncios (`ad_id` únicos) | **2.312** | 2.312 | ✅ bate exatamente |
| páginas (`page_id` únicos) | **731** | 733 | ⚠ diverge em 2 (0,3%) |
| colunas | 42 | — | 14 de gênero×idade, 20 de região |
| início de veiculação | 17/nov/2017 → 28/mar/2020 | arquivo "desde mar/2019" | ⚠ **6 anúncios** anteriores a mar/2019 |

Meses de maior volume: **jul/2019** (284), **mai/2019** (277 — eleições europeias de
23-26/mai), set/2019 (245), jan/2020 (207). Coerente com CA3.

**Situação melhor que a de todos os casos anteriores:** aqui há gabarito real (no
`reddit-buntain` os 279 usuários rotulados não foram publicados; no #207 o repo nem
existia). Some-se a isso que o **Apêndice A publica as 26 keywords e os nomes dos
anunciantes excluídos** — a Fase 0 "reproduzir o artigo tal-como-publicado" é executável
ao pé da letra.

⚠ Este CSV **não traz texto nem criativo** — só metadados. Mas há um **segundo** gabarito.

### 4.1 Os dados anotados do CHI 2021 ✅ — e eles trazem o texto

Nota de rodapé 10 do CHI 2021, verificada em 7/ago/2026:
[Clandestino-or-Rifugiato-…](https://github.com/PotenteOpossum/Clandestino-or-Rifugiato-Anti-immigration-Facebook-Ad-Targeting-in-Italy)
— público, 12 CSVs, baixados para [`anotacoes_chi2021/`](anotacoes_chi2021/).

**600 anotações = 200 anúncios × 3 anotadores**, com `ad_url`, **`ad_creative_body`**,
`ad_creative_link_title`, `ad_creative_link_description` e `Label` (Likert 1–5 +
`irrelevant`). Nenhum texto vazio. Distribuição: `1`=108, `2`=106, `3`=107, `4`=94, `5`=92,
`irrelevant`=93.

**Duas consequências que mudam o plano:**

1. **O gabarito pró/anti é público.** A decisão nº 4 do [REPLICACAO §7](../../../REPLICACAO_CASO_META_ADS.md)
   ("rotular quanto?") encolhe: há 200 anúncios com 3 anotações humanas cada para calibrar
   e medir o teto da tarefa, como se fez no caso vacinas.
2. **O texto existe para esses 200 anúncios, sem passar pela API** — logo **sem depender da
   retenção**. Para os outros 2.112 o texto continua exigindo re-consulta por `ad_id`.

### 4.2 ✅ Reprodução do α de Krippendorff (feita em 7/ago/2026)

Por `analise/reproduz_alpha_chi2021.py` (determinístico, offline, só biblioteca padrão),
sobre os 12 CSVs acima:

| medida | réplica | paper | |
|---|--:|--:|---|
| anúncios removidos por irrelevância (≥2 anotadores) | **26 (13%)** | 26 (13%) | ✅ exato |
| **α ordinal**, 5 rótulos | **0,763** em n = **174** | 0,76 em n = 174 | ✅ valor e n |
| **α**, 2 polaridades ({1,2} × {4,5}) | **0,924** em n = **141** | 0,92 em n = **150** | ✅ valor · ⚠ **n diverge** |

**O que isso entrega:** é a **primeira reprodução bem-sucedida de um número publicado neste
caso**, feita inteiramente offline e antes de qualquer coleta — valida de uma vez o
gabarito, o esquema de rotulagem e a nossa leitura dele.

⚠ **A divergência de `n` (141 × 150) não foi explicada.** Testadas cinco convenções
alternativas de filtragem sobre os mesmos dados: ≥2 rótulos em {1,2,4,5} → **141**; ≥1 →
163; os 3 → 89; sem remover os irrelevantes → 141 ou 170; maioria caindo num polo → 138.
**Nenhuma devolve 150.** Como o α reproduz, a divergência está na **contagem de unidades
reportada**, não na concordância. Registrado, não corrigido.

## 5. Bloqueios e o que destrava

1. ⏳ **Conta Meta verificada** — bloqueia **toda** a Fase 1. Grátis e sem porteiro
   institucional, mas exige documento oficial e 1-3 dias úteis. **Só a Mariana faz** —
   procedimento completo em §5.1, para não se perder.
2. ⏳ **Teste de retenção** — depende de (1). Rodar a consulta de §5.2 e cruzar os `ad_id`
   devolvidos com os 2.312 do gabarito. **É o que decide se o eixo italiano sobrevive**, e
   é um resultado em si (uma medida de quanto do arquivo público some com o tempo).

### 5.1 Como abrir a conta verificada (⏳ **pendente da Mariana**, 07/ago/2026)

Levantado das páginas oficiais em 7/ago/2026. Quatro passos; só o primeiro tem espera.

| # | Passo | Onde | Prazo |
|---|---|---|---|
| 1 | Confirmar identidade: subir **documento oficial com foto** (passaporte, RG ou CNH) e confirmar o país | [facebook.com/ID](https://www.facebook.com/ID/), com a conta pessoal logada | **1-3 dias úteis** |
| 2 | Criar conta de desenvolvedor (*Get started*, aceitar a Platform Policy) | [developers.facebook.com](https://developers.facebook.com) | instantâneo |
| 3 | Criar o app (*Access the API*, ou My Apps → Create App). **Sem App Review, sem tier pago** | [facebook.com/ads/library/api](https://www.facebook.com/ads/library/api) | instantâneo |
| 4 | Gerar *user access token* no Graph API Explorer e guardar como `META_ADLIB_TOKEN` no `.env` da raiz (**nunca versionado**, mesma convenção da `ANTHROPIC_VACINAS_API_KEY`) | Graph API Explorer | instantâneo; token **expira em 60 dias** |

⚠ **Incerteza não resolvida:** algumas fontes descrevem, para *anunciantes* políticos, um
passo extra de confirmação de endereço por **código enviado em carta física** (semanas).
Para o **acesso à API** a exigência documentada é apenas documento + país. **Se a tela do
passo 1 pedir endereço postal, o cronograma do caso muda** e o braço Brasil (§6) passa a
principal — registrar aqui o que aparecer.

### 5.2 O primeiro comando (teste de retenção, não coleta)

```bash
curl -sG "https://graph.facebook.com/v21.0/ads_archive" \
  --data-urlencode "access_token=$META_ADLIB_TOKEN" \
  --data-urlencode "ad_reached_countries=['IT']" \
  --data-urlencode "ad_type=POLITICAL_AND_ISSUE_ADS" \
  --data-urlencode "search_terms=clandestini" \
  --data-urlencode "ad_delivery_date_min=2019-03-01" \
  --data-urlencode "ad_delivery_date_max=2020-03-30" \
  --data-urlencode "fields=id,ad_delivery_start_time,page_name,ad_creative_bodies" \
  --data-urlencode "limit=25"
```

| Desfecho | Leitura |
|---|---|
| volta com anúncios de 2019 | eixo italiano **vivo**; `ad_creative_bodies` traz o **texto** que falta no CSV (§4) |
| volta vazio, sem erro | retenção caiu (ou vale a regra de 1 ano para anúncios da UE) → **braço Brasil vira o principal**, e o sumiço do arquivo público **vira achado do capítulo** |
| erro de permissão | a verificação do passo 1 ainda não propagou; esperar e repetir |

Notas: `ad_type=POLITICAL_AND_ISSUE_ADS` é o que libera os campos de impressão e demografia
(o que o caso usa); a API tem teto de **~200 chamadas/hora por app** — suficiente para as
26 keywords, não para tentativa e erro.
3. ✅ **Full text do CHI 2021 — lido em 7/ago/2026.** Fechou a pendência de proveniência.
   Achado principal: **o denominador de CB2 no resumo não é o do corpo** (47,6% é dos
   anúncios de *grandes partidos*, não de todos; entre todos, os anti são **29,3%**). Ver
   [ARTIGO §5.1](../../../ARTIGO_CAPOZZI_alvo.md).
4. ✅ **Qual CB2 medir — decidido em 7/ago/2026.** Base primária = anúncios **com posição**;
   métrica = **razão de desproporção** R (fatia de impressões ÷ fatia de anúncios), R = 1,72;
   base companheira = todos, R = 1,46. Ver [DECISOES_CB2.md](DECISOES_CB2.md). ⚠ De quebra,
   descobriu-se que **o total de impressões do artigo não reproduz** a partir do CSV
   publicado (35 M × 49,8 M pela regra declarada) — §4 daquele documento.

**Risco declarado (não verificável sem a conta):** a Meta parou de veicular anúncios
políticos na UE em **out/2025**; a retenção de anúncios políticos é de **7 anos**, o que
põe mar/2019 no limite em 2026; e há uma nota da Meta de que anúncios da UE seriam
arquivados **1 ano após a última impressão** — se essa regra valer, o corpus italiano já
não existe. Tentou-se sondar a Ad Library sem autenticação em 7/ago/2026: **inconclusivo**,
a interface é SPA e exige login. Mitigação = o braço Brasil.

## 6. O braço Brasil (mitigação de risco)

O Brasil **não** foi atingido pela proibição da UE e os anúncios de 2022 estão dentro da
retenção (até 2029). Entra como **segundo braço do mesmo caso**, sem alvo publicado próprio
— o candidato brasileiro (*Characterizing Brazilian Political Ads on Facebook*, WebMedia
2022) é descritivo, não classifica, e não está indexado no Semantic Scholar. Detalhe e
consequências em [REPLICACAO §3](../../../REPLICACAO_CASO_META_ADS.md).

## 7. Predições pré-registradas

(Detalhe e mecanismo em [REPLICACAO §5](../../../REPLICACAO_CASO_META_ADS.md).)

- **Muda (forte):** **CB2** — a fatia **anti cai** ao incluir o Instagram. Mecanismo, agora
  quantificado pelo full text: os anúncios anti têm **OR = 1,69** de atingir homens em vez
  de mulheres (69% mais prováveis) e sua audiência é mais velha; o Instagram tem composição
  demográfica distinta, logo o estrato Facebook-only **superestima** o polo anti. Mesma
  família de afirmação que falhou em 4b, 4c e 7.
  ⚠ **Qual CB2 medir precisa ser decidido antes** (§5.3 do ARTIGO): 29,3% (todos os
  anúncios), 47,6% (só grandes partidos) ou 65,2% (impressões entre os com posição). A
  aposta acima vale para as três, mas o **ponto de partida** muda.
- **Muda (moderado) — CB5** (*riding the wave*): o teste de Granger foi rodado sobre um
  corpus filtrado por 26 keywords **e** truncado em dez/2019. Ampliar a janela e a largura
  do filtro é exatamente o tipo de mudança a que uma série temporal curta é sensível.
- **Confirma:** **CA2** (Gini — cauda extrema), **CA1** (Salvini domina) e **CA3** (picos
  eleitorais).
- **Incerto:** **CA4** — se o viés de gênero encolher no Instagram, o micro-targeting
  medido era em parte propriedade da plataforma escolhida.
- **Não convergiu:** n=2.312 é pequeno para uma proporção estratificada por partido ×
  plataforma.
- **Humildade registrada:** se CB2 não se mover, é o **primeiro contra-exemplo** à leitura
  PP3 nº 3 — vale mais que uma confirmação.
