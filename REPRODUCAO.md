# Como reproduzir os resultados

Este documento mapeia cada figura e cada número da dissertação *O Efeito do Volume de Coleta sobre
os Resultados de Análises: Redes Sociais Digitais como Caso de Estudo* (PUC-Rio, 2026) ao script
que o produz, ao arquivo de saída e ao dado de entrada. O objetivo é que um terceiro possa refazer
qualquer resultado, ou, quando o dado de entrada não pode ser redistribuído, refazer a coleta a
partir da fonte original.

Toda análise roda sobre um **instantâneo congelado** e local. Nenhum script de análise abre conexão
de rede; só os de `pipeline/` e `diagnostico/` o fazem.

## Figuras e tabelas da dissertação

| No texto | Produzido por | Saída | Dado de entrada |
|---|---|---|---|
| Fig. 4.1, curva do retuíte de mídia vertical | `casos/twitter-ituassu/analise/curva_midia_por_volume.py`, desenhada por `escrita/dissertacao/figuras/gerar_figuras.py` | `casos/twitter-ituassu/data/repl/compos2014/curva_midia.json` | `snapshot_hashtag.sqlite` (acervo eTC, não redistribuível) |
| Fig. 5.1, curva do eixo de rede do debate vacinal | `casos/vacinas/analise/curva_rede_por_fracao.py` | `casos/vacinas/data/repl/vacinas2022/curva_rede.json` | `snapshot_vacinas.sqlite` (acervo eTC, não redistribuível) |
| Fig. 6.1, participação multicomunidade por limiar | `casos/reddit-buntain/analise/rb3.py` | `casos/reddit-buntain/data/repl/buntain2013/curva_rb3.json` | `snapshot_buntain.sqlite`, reconstruível dos arquivos públicos (ver abaixo) |
| Fig. 8.1, conteúdo de usuário dos dois lados do filtro | `casos/youtube-agecovp/analise/fase3_efeito_filtro.py` e `fase3_no_tema.py` | `casos/youtube-agecovp/data/repl/agecovp2020/fase3_ugc_completo.json` | instantâneo próprio da API e gabarito dos autores |
| Tab. 6.1, participação por recorte de coleta | `casos/reddit-buntain/analise/rb3.py` e `rb3_recorte_artigo.py` | `curva_rb3.json`, `rb3_recorte_artigo.json`, `RB3_recorte_reconstruido.md` | `snapshot_buntain.sqlite` |
| Tab. 8.2, reprodução do ponto original do YouTube | `casos/youtube-agecovp/analise/fase2_ponto_original.py` | documentos de fase em `data/repl/agecovp2020/` | gabarito publicado pelos autores (Zenodo) |
| Tab. 9.1, taxa de deleção por data de verificação | `casos/tiktok/` (fase 2) | `casos/tiktok/data/politok_de/fase2_politok.json` | identificadores e estados publicados pelos autores do PoliTok |
| Tab. 10.1, a tabela mestre | nenhuma; cada célula vem do capítulo do caso | `casos/RESULTADOS_tabela_mestre.md` | os arquivos acima |
| §4.1 a §4.4, testes do eixo de mídia | `casos/twitter-ituassu/analise/analisa_midia.py` e `stats_midia.py` | `RESULTADOS_FASE0_midia.md`, `A_paper_reconstruida.json` | `snapshot_hashtag.sqlite`, `snapshot_full.sqlite` |
| §4.5, eixo de stance | `casos/twitter-ituassu/analise/valida_rotulador.py` e `estima_universo.py`; pré-registro em `data/repl/compos2014/stance/PRE_REGISTRO_stance.md` | `data/repl/compos2014/stance/` | amostra congelada por semente; o gabarito humano traz texto de tweet e não é redistribuído |
| §5.2 e §5.3, rede e conteúdo do debate vacinal | `casos/vacinas/analise/rede_modularidade.py`, `curvas_por_limiar.py`, `valida_rotulador.py` | `FASE2_replicacao_ponto.md`, `FASE3_eixoA_expansao.md`, `curva_rede.json` | `snapshot_vacinas.sqlite` |
| §7.1, ponto original da homofilia | `casos/reddit-massachs/analise/mh1_ponto_original.py` | `data/repl/massachs2016/` | matriz de atributos publicada pelos autores |
| §10.2, custo de infraestrutura | medição direta | [`CUSTO_infraestrutura.md`](CUSTO_infraestrutura.md) | tamanhos dos instantâneos e os JSON de curva |

Cada caso tem um `README.md` próprio em `casos/<caso>/` com a ordem das fases e os comandos.

## A revisão da literatura (artigo companion)

O sistema que cataloga a literatura e produz o `research.db` é um projeto separado. Neste
repositório ficam os scripts de figura e de validação (`escrita/survey/figuras.py`,
`escrita/survey/validacao.py`), os números consolidados (`escrita/survey/numeros.json`) e o braço de
expansão da base (`escrita/survey/expansao/`), com o pré-registro que fixou a condição de parada
antes da medição.

## O que não é redistribuído, e por quê

1. **Tweets (casos de 2014 e de 2021–22).** Os instantâneos trazem texto, autor e métricas de
   publicações de pessoas identificáveis. Redistribuir o conteúdo contraria os termos da plataforma
   e é dado pessoal de terceiros. O que se publica são os agregados: as curvas, as contagens por
   dia, as tabelas de resultado. Os acervos originais estão preservados no laboratório eTC da
   PUC-Rio e o acesso é institucional.
2. **Rotulagem humana e reconstruções de amostra.** Seis arquivos de gabarito de *stance*
   (`casos/twitter-ituassu/data/repl/compos2014/stance/gold_stance_*.csv`, 1.005 linhas) e três JSON
   de reconstrução de amostra trazem o texto da publicação, o identificador do autor e a contagem de
   seguidores. Eles **fazem parte deste repositório**, porque é deles que sai a rotulagem que o
   Capítulo 4 usa e sem eles a etapa mais cara do caso não é verificável. O que os números do texto
   usam são os agregados, e é por eles que o mapa acima aponta.
   > ⚠ Quem reusar esses arquivos está reusando dado pessoal de terceiros publicado numa plataforma
   > que hoje proíbe a redistribuição do conteúdo. O depósito de artefatos que acompanha este
   > trabalho **não os inclui**: ele traz só scripts, pré-registros e agregados, verificados por
   > conteúdo, e o `MANIFESTO.md` de lá lista o que ficou de fora e por quê.
3. **Metadados de vídeo e de canal do YouTube.** Obtidos pela Data API v3, cujos termos restringem
   o armazenamento e a redistribuição. A coleta é refazível: as oitenta e cinco buscas estão
   declaradas no caso, e a chave da API é gratuita.
4. **Gabaritos de outros autores.** O do YouTube (AGECovP) e o do PoliTok são públicos na fonte
   original, e o caso aponta para lá em vez de copiar. O mesmo vale para a matriz de atributos do
   caso de homofilia, publicada pelos autores em `github.com/JoanMassachs/reddit-data`.
5. **Reddit.** É o único caso em que a população completa é pública. Os arquivos históricos são
   distribuídos via Academic Torrents, e o instantâneo de 43.479 submissões e 1.015.247 comentários
   é reconstruível a partir deles com o `pipeline/` do caso. Por tamanho, o arquivo não é
   versionado aqui.

## Estrutura

```
casos/<caso>/
  core/        conexão e utilidades (credenciais vêm de .env, nunca versionado)
  pipeline/    coleta e congelamento do instantâneo (usa rede)
  analise/     análises sobre o instantâneo (sem rede)
  data/        instantâneos e resultados; os .sqlite não são versionados
escrita/       fonte LaTeX da dissertação e do artigo da revisão
```

---

*Os números do texto foram conferidos contra estes arquivos. Onde o texto entregue à banca diverge
do que os dados mostram, a divergência está registrada na errata do projeto.*
