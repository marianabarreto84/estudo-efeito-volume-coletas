# twitter-ituassu — caso #Eleições2014 do lineup da dissertação

Replicação por expansão de **dois** alvos da mesma linhagem, sobre a mesma coleta:

- **Ituassu & Lifschitz (2015)**, *E-Compós* — eixo **MV/MH** (mídia vertical ×
  horizontal), H1 e H2;
- **Ituassu, Lifschitz, Capone, Vaz & Mannheimer (2018)**, *Palabra Clave* — eixo
  **MP/MC** (mídia principal × complementar), Tabelas 2–7.

Acervo histórico do eTC (Twitter/X não permite coleta nova). Primeiro caso executado
do lineup.

## Leia primeiro

- [REPLICACAO_CASO_COMPOS2014.md](REPLICACAO_CASO_COMPOS2014.md) — plano de fases (o mapa).
- [PAPER2018_palabra_clave.md](PAPER2018_palabra_clave.md) — o alvo de 2018, taxonomia MP/MC, crosswalk.
- [RESULTADOS_analise_midia_MV_MH.md](RESULTADOS_analise_midia_MV_MH.md) — **canônico do eixo MV/MH**.
- [STANCE_como_o_paper_fez_e_onde_estamos.md](STANCE_como_o_paper_fez_e_onde_estamos.md) — o eixo stance (contexto).
- [CODEBOOK_stance.md](CODEBOOK_stance.md) — guia de rotulagem, pronto para uso (18/ago/2026).

## Estrutura

```
twitter-ituassu/
├── core/         db.py · extrai_links.py (1º link efetivo) · resolve_midia.py
│                 midia_dominios.py (MV/MH) · midia_mp_mc.py + resolve_mp_mc.py (MP/MC)
├── pipeline/     extrai_snapshot.py · expandir_links.py · expandir_links_texto.py
│                 expandir_branded.py   (expansão de encurtadores → expand_cache.sqlite)
├── diagnostico/  exploração do banco e planilhas de curadoria (top_indefinidos.py,
│                 blogs_em_portal.py — ambas SUPERADAS, ver abaixo)
├── analise/      EIXO MV/MH
│                   analisa_midia.py · stats_midia.py · compara_escopo.py · intra_autor.py
│                   curva_midia_por_volume.py   curva A(volume) de H1 e da dominância MV
│                   curva_h2_por_dia.py         curva de H2, que é afirmação sobre UM DIA
│                 EIXO MP/MC
│                   analisa_midia_mp_mc.py      ponto original (Fase 0)
│                   cura_indefinidos.py         curadoria do resíduo `indefinido`
│                   sensibilidade_mp_mc.py      as 3 alavancas de classificação
│                   cdx_links_mortos.py         link rot via Internet Archive
│                   proxy_link_rot.py           link rot via encurtados sobreviventes
├── vpn/          perfis OpenVPN da Cloud-DI (vpn-fixed.ovpn) — só para re-extrair
└── data/repl/compos2014/   snapshots + RESULTADOS_*.md (nunca versionar dados crus)
```

**Snapshots** (locais, congelados — a análise não precisa de VPN):
`snapshot_hashtag.sqlite` (140.909 tweets com #Eleições2014) ·
`snapshot_full.sqlite` (214.393, escopo amplo) · `expand_cache.sqlite` (21.452 links
expandidos).

⚠ **A coluna `classe_midia` gravada no snapshot é PRÉ-correção de jul/2026** (MV
50.040 lá contra 66.370 no canônico). Todo script recomputa a classe pelo 1º link
efetivo. Não use a coluna.

## Estado atual

### Eixo MV/MH (alvo 2015) — ✅ **fechado**

- ✅ Ponto original + universo, **corrigidos em jul/2026** (os scripts liam só o campo
  `links` e contavam ~9% de tweets como NDA quando eram link com `t.co` só no texto).
- ✅ **Curvas `A(volume)`** (07/ago/2026, 300 réplicas/ponto) —
  [RESULTADOS_FASE3_curva_midia.md](data/repl/compos2014/RESULTADOS_FASE3_curva_midia.md):
  - **dominância MV** converge já em n=100;
  - **H1** converge em **n≈200** — e os 48,3% do artigo **não cabem** na banda de
    n=700 aleatório, o que mostra que a falha dele é **viés do esquema de amostragem,
    não falta de volume**. Bastariam 200 tweets sorteados para refutar H1 com 99,7%
    de poder; o artigo coletou 700;
  - **H2** não reproduz **em recorte nenhum** — taxa de rivalidade 0% em todos os
    dias a partir de n=50, e a amostra reconstruída do próprio artigo também não
    mostra rivalidade em 23/out.

### Eixo MP/MC (alvo 2018) — ✅ **fechado, com divergência declarada irresolúvel**

- ✅ Ponto original (Fase 0): MP **70,3%** na amostra e **72,2%** no universo, contra
  **59%** do artigo.
- ✅ **Resíduo `indefinido` curado** (692 hosts, `indefinidos_curados.csv`).
- ✅ **As 4 explicações do nosso lado testadas e descartadas** —
  [sensibilidade](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_sensibilidade.md) e
  [link rot](data/repl/compos2014/RESULTADOS_FASE0_mp_mc_cdx.md): convenção de lista
  (alargar MP **piora**), blog-em-portal (efeito ausente por path **e** por
  subdomínio), resíduo não curado (−1,3 p.p.) e link rot (−0,1 p.p.; o CDX não
  alcança — o Archive não guarda redirecionadores).
- ⚠ **A divergência é do lado do artigo** — corpus diferente ou critério não
  explicitado — e **não é resolúvel com o material publicado** (o alvo não publica a
  lista de domínios por classe nem o gabarito dos 2.200 sorteados). Registrada como
  **limite de reprodutibilidade**, não como pendência.
- 📋 As planilhas de curadoria manual `INDEFINIDOS_candidatos_MC.md` e
  `BLOGS_EM_PORTAL_candidatos.md` ficaram **superadas**: esperavam marcação à mão que
  nunca aconteceu, e as perguntas foram respondidas por medição.

### Eixo stance (H3) — ◐ **dev fechado; falta o teste cego de 210**

O kit foi montado e congelado em **18/ago/2026**; em **22/ago/2026** a rotulagem começou
e o conjunto de **calibragem (dev, 110)** fechou, em duas rodadas.

| artefato | onde |
|---|---|
| codebook operacional (14 casos-limite decididos) | [CODEBOOK_stance.md](CODEBOOK_stance.md) |
| **página de rotulagem — teste cego, 210 tweets, ~5–6 h** ← *o que falta* | `data/repl/compos2014/stance/rotulagem_teste.html` |
| gabarito do dev: `v1` cego e `v2` revisto | `.../stance/gold_stance_dev_MARIANA.csv` · `.../stance/gold_stance_dev_v2.csv` |
| diário de decisões (desenho, números, 3 regras novas) | [.../stance/DECISOES_ROTULADOR.md](data/repl/compos2014/stance/DECISOES_ROTULADOR.md) |
| reteste intracodificador (40 itens, ≥ 29/ago) | `.../stance/gold_stance_RETESTE.csv` |
| pré-registro: split 110/210, apostas, critério κ ≥ 0,70 | [.../stance/PRE_REGISTRO_stance.md](data/repl/compos2014/stance/PRE_REGISTRO_stance.md) |
| planilha completa (320) — alternativa em Excel à página | `.../stance/gold_stance_para_rotular.csv` |
| sorteador (seed `20260818`, sha `dc8ee39ff69b`) | `analise/amostra_stance_humana.py` |
| geradores das páginas de rotulagem e de revisão | `analise/gera_pagina_rotulagem.py` · `analise/gera_pagina_revisao.py` |
| lado medido das hashtags (contexto, não regra) | `analise/lean_hashtags.py` |

**Dois achados já saíram do dev** (n = 110), e nenhum depende do teste:

- **zero divergência de polo.** Entre o gabarito humano e uma pré-anotação automática,
  nunca um leu EA onde o outro leu ED. **Toda** a discordância é sobre *haver ou não*
  lado — a fronteira frágil do rótulo do artigo é `lado × NDA`, e é ela que decide o
  23,4% de NDA que ele reporta;
- **NDA em 61%** do dev contra **23,4%** do artigo, nas duas leituras — a aposta P1
  (≥ 35%) se confirma com folga e **não depende de quem rotula**.

★ E o dev produziu um terceiro número, sobre método: a rodada de revisão das divergências
levou o mesmo anotador, nos mesmos itens, de **κ 0,699 para 0,916** depois de ver os
rótulos da máquina — **+0,22 de ancoragem medida dentro do próprio caso**. É por isso que
o teste de 210 é cego, e o `v2` do dev fica registrado como gabarito **de consenso**, não
independente.

O fluxo seguinte (validação κ → aplicação em escala → curva `A(volume)`) espelha o caso
irmão `vacinas` (κ 0,759) e é automático. Ver
[STANCE_...md](STANCE_como_o_paper_fez_e_onde_estamos.md) §9.

⚠ De passagem, o kit **corrigiu um erro nosso**: `#AecioNever` é pró-Dilma (**ED**), não
EA como o `STANCE_...md` afirmava — medido em 84×0 co-ocorrências (`CODEBOOK_stance.md` §2).

## Linhas na tabela mestre

Este caso preenche as linhas **1, 2, 3** (eixo MV/MH), **3b** (eixo MP/MC) e **10**
(stance, ⏳) de [`casos/RESULTADOS_tabela_mestre.md`](../RESULTADOS_tabela_mestre.md).

## Pré-requisitos

Só para **re-extrair** do banco (a análise roda offline sobre os snapshots):
VPN Cloud-DI conectada + `.env` na raiz com credenciais SSH/Postgres.
⚠ Túnel de pé = adaptador `OpenVPN TAP-Windows6` em `Up` **e** rota `10.x` — o ícone
na bandeja engana. O caso 2014 vive na **vm067** (`eTC_Producao`, tabela
`ituassu_2014`).
