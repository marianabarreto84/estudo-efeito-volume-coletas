# Fase 0 sob MP/MC — replicação do paper de 2018 (Palabra Clave)

> Gerado por `analise/analisa_midia_mp_mc.py` sobre `snapshot_hashtag.sqlite` +
> `expand_cache.sqlite`. Convenção **estrita** das 26 marcas (25 nomeadas) —
> `core/midia_mp_mc.py`. Determinístico (não usa stance). Ver
> `PAPER2018_palabra_clave.md` e `REPLICACAO_CASO_COMPOS2014.md`.

## Método (o que reproduz e o que é stub)
- **Amostra A:** 200 tweets/dia sorteados (semente 20141026) no pico noturno
  (19:00–23:59 BRT), 13–23/out (11 dias), só #Eleições2014.
  *(O 2018 diz "200/dia à noite no pico"; a hora exata não é dada — pico noturno é
  escolha de reprodução documentada. O sorteio original é irrecuperável → semente fixa.)*
- **Amostra C:** tweets de A com 1º link classificado **MP ou MC** (compartilhou mídia).
  Cascata ao pé da letra: **C sai de A**, não do filtro-cidadão B (ver cabeçalho do script).
- **MP/MC:** 1º link; MP = 26 marcas (PBM 2014, lista fechada); MC = demais mídias
  (incl. redes sociais). Domínio fora do dicionário = `indefinido` (resíduo p/ curadoria,
  não vira MC automático). Encurtador morto = `nao_resolvido`.
- **STUB (Fase 0.5, precisa de rótulo humano):** B (filtro cidadão), D (preferência
  EA/ED), Tab. 5/6/7 (leque por público + Qui-quadrado). Não calculados aqui.

## Cobertura MP/MC no universo on-hashtag (janela 13–23/out)
```
total: 37068
  MP               15852   42.8%
  NDA               9423   25.4%
  MC                6096   16.4%
  nao_resolvido     4926   13.3%
  indefinido         515    1.4%
  nao_midia          256    0.7%
cobertura (classe definida): 86.7%
```

## Amostra A reconstruída (≈2.200; alvo do paper)
| dia | n | MP | MC | NDA | n/res | ind | % com mídia | MP% (de C) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| 2014-10-13 | 200 | 81 | 52 | 42 | 22 | 2 | 66.5% | 60.9% |
| 2014-10-14 | 200 | 27 | 12 | 140 | 19 | 2 | 19.5% | 69.2% |
| 2014-10-15 | 200 | 127 | 12 | 32 | 27 | 0 | 69.5% | 91.4% |
| 2014-10-16 | 200 | 59 | 15 | 112 | 11 | 2 | 37.0% | 79.7% |
| 2014-10-17 | 200 | 100 | 42 | 30 | 23 | 4 | 71.0% | 70.4% |
| 2014-10-18 | 200 | 31 | 54 | 64 | 37 | 6 | 42.5% | 36.5% |
| 2014-10-19 | 200 | 67 | 17 | 105 | 10 | 1 | 42.0% | 79.8% |
| 2014-10-20 | 200 | 127 | 30 | 36 | 6 | 1 | 78.5% | 80.9% |
| 2014-10-21 | 200 | 80 | 29 | 49 | 40 | 1 | 54.5% | 73.4% |
| 2014-10-22 | 200 | 55 | 35 | 79 | 25 | 6 | 45.0% | 61.1% |
| 2014-10-23 | 200 | 80 | 55 | 33 | 29 | 3 | 67.5% | 59.3% |
| **TOTAL** | **2200** | 834 | 353 | 722 | 249 | 28 | **54.0%** | **70.3%** |

- **Amostra C** (com mídia) = **1187** de 2200 → **54.0%**
  compartilharam mídia *(alvo 2018: 65,4%; 1.439/2.200)*.
- **Tabela 2** (split entre os de C): **MP 70.3% · MC 29.7%**
  *(alvo 2018: 59% / 41%)*.

## Universo on-hashtag na mesma janela (13–23/out) — efeito de volume
| dia | n | MP | MC | NDA | n/res | ind | % com mídia | MP% (de C) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| 2014-10-13 | 2380 | 1123 | 470 | 362 | 386 | 29 | 66.9% | 70.5% |
| 2014-10-14 | 4207 | 736 | 528 | 2337 | 529 | 55 | 30.0% | 58.2% |
| 2014-10-15 | 3308 | 1413 | 366 | 990 | 486 | 39 | 53.8% | 79.4% |
| 2014-10-16 | 4890 | 1937 | 692 | 1246 | 934 | 53 | 53.8% | 73.7% |
| 2014-10-17 | 2766 | 1553 | 407 | 431 | 303 | 55 | 70.9% | 79.2% |
| 2014-10-18 | 1191 | 356 | 323 | 248 | 221 | 24 | 57.0% | 52.4% |
| 2014-10-19 | 3063 | 1099 | 345 | 1303 | 270 | 29 | 47.1% | 76.1% |
| 2014-10-20 | 2992 | 1617 | 505 | 516 | 276 | 48 | 70.9% | 76.2% |
| 2014-10-21 | 3257 | 1504 | 704 | 522 | 435 | 66 | 67.8% | 68.1% |
| 2014-10-22 | 2908 | 1327 | 566 | 590 | 321 | 61 | 65.1% | 70.1% |
| 2014-10-23 | 6106 | 3187 | 1190 | 878 | 765 | 56 | 71.7% | 72.8% |
| **TOTAL** | **37068** | 15852 | 6096 | 9423 | 4926 | 515 | **59.2%** | **72.2%** |

## Tabela 3 — mídias mais compartilhadas (amostra A, base = tweets com mídia)
| mídia | n | % |
|---|--:|--:|
| UOL (portal) | 344 | 29.0% |
| G1 | 219 | 18.4% |
| facebook.com | 102 | 8.6% |
| Terra (portal) | 61 | 5.1% |
| Epoca | 52 | 4.4% |
| atarde.com.br | 50 | 4.2% |
| Globo.com | 48 | 4.0% |
| O Estado de S.Paulo (Estadao) | 40 | 3.4% |
| Jornal do Brasil | 33 | 2.8% |
| Folha de S.Paulo | 29 | 2.4% |
| instagram.com | 27 | 2.3% |
| bbc.com | 26 | 2.2% |
| Hoje em Dia (R7) | 19 | 1.6% |
| youtube.com | 17 | 1.4% |
| congressoemfoco.com.br | 13 | 1.1% |

## Tabela 4 — mídias mais compartilhadas entre as MCs (amostra A)
| mídia | n | % |
|---|--:|--:|
| facebook.com | 102 | 28.9% |
| atarde.com.br | 50 | 14.2% |
| instagram.com | 27 | 7.6% |
| bbc.com | 26 | 7.4% |
| youtube.com | 17 | 4.8% |
| UOL (portal) | 16 | 4.5% |
| congressoemfoco.com.br | 13 | 3.7% |
| dia-da-terra.blogspot.com | 10 | 2.8% |
| huff.to | 10 | 2.8% |
| agenciabrasil.ebc.com.br | 8 | 2.3% |
| G1 | 8 | 2.3% |
| Yahoo | 8 | 2.3% |
| x.com | 6 | 1.7% |
| ebcnare.de | 4 | 1.1% |
| m.facebook.com | 4 | 1.1% |

> ⚠ **Atualização de 07/ago/2026 — as ressalvas abaixo foram trabalhadas.** O resíduo
> `indefinido` foi **curado** (692 hosts, `indefinidos_curados.csv`) e a divergência
> MP 70,3% × 59% foi investigada até o fim: as quatro explicações que dependiam da
> nossa classificação estão **descartadas por medição**. Ver
> [sensibilidade](RESULTADOS_FASE0_mp_mc_sensibilidade.md) e
> [link rot / CDX](RESULTADOS_FASE0_mp_mc_cdx.md).

## Ressalvas desta reprodução
- **% com mídia pode vir abaixo de 65,4%**: `indefinido` (domínio real fora do
  dicionário) e `nao_resolvido` (encurtador morto) são links que *podem* ser mídia
  mas não classificamos — o paper (manual) reconhecia "100+ mídias". Resíduo a curar.
- **Marcas rebaixadas para MC** pela regra estrita das 26 (aparecem no topo do 2018,
  mas fora da lista): abril.com.br, atarde.com.br, bbc.co.uk, bbc.com, cartacapital.com.br, on.wsj.com, terranews.com.br, valor.com.br, valoreconomico.com.br, wsj.com.
- **Amostragem aleatória**: números variam com a semente; é reprodução *agregada*
  (Fase 0), não recuperação dos tweets originais.
- **B/D e Tab. 5–7**: dependem de stance (Fase 0.5, adiada).
