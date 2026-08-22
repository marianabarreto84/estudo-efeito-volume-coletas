# Caso de replicação · Instagram/Facebook · Capozzi et al. (2020, 2021) — anúncios de imigração

> ⛔ **FORA DO ESCOPO DA DISSERTAÇÃO desde 21/ago/2026.** Na 2ª rodada de revisão do
> texto, a Mariana decidiu tratar a dissertação sem Instagram e Facebook. O
> `corpo.tex` passou a apresentar as plataformas da Meta na §2.4 como **rota de coleta
> fechada** (CrowdTangle desligado, Content Library paga e sem exportação, Ad Library
> restrita a conteúdo publicitário), e não mais como caso pendente; o conjunto de casos
> ficou em **6 casos / 4 redes**. As linhas 13 e 14 da
> [tabela mestre](../RESULTADOS_tabela_mestre.md) estão marcadas como fora do escopo.
>
> **Nada aqui foi apagado, e nada aqui está errado.** Este caso permanece por inteiro
> — Fase 0, gabaritos baixados e conferidos, α reproduzido, CB2 desambiguado — para
> poder ser retomado sem refazer nada, caso uma rota de coleta compatível com o
> protocolo volte a existir. Os “próximos passos” da dissertação preveem essa
> reabertura explicitamente. **O que muda é só o escopo do texto**; o registro abaixo
> continua válido como estado do trabalho.

**Leia primeiro:** o plano em [REPLICACAO_CASO_META_ADS.md](REPLICACAO_CASO_META_ADS.md) e
o alvo em [ARTIGO_CAPOZZI_alvo.md](ARTIGO_CAPOZZI_alvo.md).

Caso **Instagram/Facebook** do lineup — a última rede que estava sem alvo definido. Alvo:
**Capozzi et al., CHI 2021** (29 cit.) + **SocInfo 2020** (16 cit.), sobre anúncios de
imigração na Itália coletados da **Meta Ad Library**. Traz a análise de **classificação**
(pró/anti-imigração, F1 = 0,85) que faltava, sem concentrar um terceiro caso no Reddit.

## Estado atual (7/ago/2026)

- ◐ **Fase 0 quase fechada** — **os dois artigos lidos na íntegra**, keywords transcritas,
  rota decidida, predições pré-registradas. Ver
  [data/repl/metaads2019/FASE0_descoberta.md](data/repl/metaads2019/FASE0_descoberta.md).
- ✅ **Dois gabaritos publicados e verificados** — o [CSV de metadados](data/repl/metaads2019/gabarito_capozzi2020.csv)
  com **2.312 anúncios** (bate exatamente com o paper; 731 páginas contra as 733 declaradas)
  e as [anotações do CHI 2021](data/repl/metaads2019/anotacoes_chi2021/) — **200 anúncios ×
  3 anotadores, com o texto dos anúncios**.
- ✅ **α de Krippendorff reproduzido** (`analise/reproduz_alpha_chi2021.py`): **0,763** ×
  0,76 nos 5 rótulos (n=174, exato) e **0,924** × 0,92 nas 2 polaridades — ⚠ mas sobre
  **141** anúncios, não os 150 do artigo. Primeiro número publicado reproduzido no caso,
  inteiramente offline.
- ✅ **CB2 desambiguado** ([DECISOES_CB2.md](data/repl/metaads2019/DECISOES_CB2.md)): o
  resumo do alvo contrasta proporções de **populações diferentes**. Decidido medir a
  **razão de desproporção** R = fatia de impressões ÷ fatia de anúncios, na base dos
  anúncios **com posição** (**R = 1,72**), com a base de **todos** ao lado (**R = 1,46**).
- ⚠ **As impressões do alvo não reproduzem.** O CHI reporta ~35 M; o CSV publicado dá
  **49,8 M** pela regra que o próprio artigo declara usar (média dos extremos) e 36,5 M
  somando os mínimos. Hipótese "só impressões na Itália" testada e **descartada**. A Fase 2
  roda as duas convenções.
- ✅ **Rota: Ad Library API** — grátis e exportável, a **única** coleta Meta viva. A Meta
  Content Library foi descartada: virou paga em jan/2026 e os dados **não saem do ambiente
  seguro**, o que quebra a Fase 1 do protocolo.
- ✅ **Full text do CHI 2021 lido** em 7/ago/2026 — fechou a pendência de proveniência e
  revelou a ambiguidade de CB2 acima.
- ⏳ **Fase 1** — travada na **conta Meta verificada**. 📌 **Ação pendente da Mariana**,
  adiada em 07/ago/2026. O **passo a passo está pronto** em
  [FASE0 §5.1](data/repl/metaads2019/FASE0_descoberta.md) (4 passos, só o 1º espera 1-3
  dias úteis) e o **primeiro comando a rodar** — o teste de retenção, não a coleta — em
  [§5.2](data/repl/metaads2019/FASE0_descoberta.md).

**Alvo-teste central (CB2):** anti-imigração são **47,6% dos anúncios** mas **65,2% das
impressões**. É um balanço entre polos medido num estrato — a família que já falhou três
vezes no caso vacinas (linhas 4b, 4c e 7 da [tabela mestre](../RESULTADOS_tabela_mestre.md)).

**O que funda o caso:** os autores declaram a sub-coleta em uma frase — *"we search for ads
appearing only on Facebook (**not Instagram**)"*. A expansão **é** a plataforma que dá nome
à célula da `tab:casos`.

⚠ **Risco aberto:** a Meta parou de veicular anúncios políticos na UE em out/2025 e a
retenção é de 7 anos — o corpus italiano de mar/2019 está no limite. Mitigação: o **braço
Brasil** (não atingido pela UE, retenção até 2029), que entra como segundo braço **sem
alvo próprio** e **não gera linha** na `tab:casos`. Ver [REPLICACAO §3](REPLICACAO_CASO_META_ADS.md).

## Estrutura

```
meta-ads-imigracao/
├── README.md                      <- este arquivo
├── REPLICACAO_CASO_META_ADS.md    <- plano de fases (4 eixos de expansão + braço BR)
├── ARTIGO_CAPOZZI_alvo.md         <- os dois artigos destrinchados
├── analise/
│   └── reproduz_alpha_chi2021.py  <- reproduz o α publicado (offline, sem dependências)
└── data/repl/metaads2019/
    ├── FASE0_descoberta.md        <- viabilidade + predições + reprodução do α
    ├── DECISOES_CB2.md            <- qual CB2 medir, e por quê (decisão de método)
    ├── gabarito_capozzi2020.csv   <- metadados dos 2.312 anúncios (SocInfo 2020, 42 colunas)
    └── anotacoes_chi2021/         <- 12 CSVs, 200 anúncios × 3 anotadores, COM texto
```

Sem `core/`/`pipeline/` ainda — entram na Fase 1.
