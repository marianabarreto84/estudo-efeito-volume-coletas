"""
Fase 0 sob a taxonomia MP/MC — replicacao do paper de 2018 (Palabra Clave).
Alvo primario. Deterministico (nao depende de stance). Convencao ESTRITA das 26
marcas (ver core/midia_mp_mc.py e PAPER2018_palabra_clave.md).

Reproduz a parte DETERMINISTICA da cascata A->B->C->D do 2018:
  A  = amostra 200 tweets/dia (aleatorio, horario de pico noturno), 13-23/out,
       so #Eleicoes2014.                                 [alvo do paper: 2.200]
  C  = subconjunto de A com compartilhamento de midia (1o link classificado
       MP ou MC).                                        [alvo: 1.439 = 65,4% de A]
  Tab.2 = split MP/MC entre os tweets de C.              [alvo: MP 59% / MC 41%]
  Tab.3 = midias mais compartilhadas (todas).            [alvo: G1 15, UOL 15...]
  Tab.4 = midias mais compartilhadas entre as MCs.       [alvo: Twitter 29...]

  B  (filtro cidadao) e D (preferencia EA/ED) + Tab.5/6/7 dependem de rotulo
     manual (cidadao? / stance) => STUB, marcados abaixo. Fase 0.5.

Cascata "ao pe da letra" (decisao do usuario): a Tab.1 do 2018 diz que a analise
so-de-midia roda sobre C, e o texto deriva 1.439 = 65,4% de A (2.200) — ou seja,
C sai de A, o filtro-cidadao (B) NAO precede a analise de midia. Reproduzimos isso.

Uso: python analise/analisa_midia_mp_mc.py
"""
import json, random, sqlite3
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.resolve_mp_mc import classe_mp_mc_do_primeiro_link, carrega_cache_mp_mc
from core.extrai_links import links_efetivos
from core.midia_mp_mc import MP_POR_MARCA, classificar_host_mp_mc, MAINSTREAM_REBAIXADA_PARA_MC

DB_PATH = Path("data/repl/compos2014/snapshot_hashtag.sqlite")
CACHE_PATH = Path("data/repl/compos2014/expand_cache.sqlite")
OUT_MD = Path("data/repl/compos2014/RESULTADOS_FASE0_mp_mc.md")

# --- Parametros da amostragem do 2018 ---
JANELA = [date(2014, 10, 13) + timedelta(days=i) for i in range(11)]  # 13..23/out (11 dias)
N_POR_DIA = 200
# "postados a noite, obedecendo aos horarios de pico" (2018, p.870). O paper nao da
# a hora exata (o de 2015 dava; ver analisa_midia.py). Operacionalizamos pico noturno
# como 19h-23h59 BRT. Parametrizavel; documentado como escolha de reproducao.
PICO_INI, PICO_FIM = "19:00:00", "23:59:59"
SEED = 20141026  # semente fixa -> amostra reprodutivel (o sorteio original e irrecuperavel)

CACHE = carrega_cache_mp_mc(CACHE_PATH)  # traz final_url -> permite a regra de path

# host -> nome de marca MP (para rotular Tab.3); senao, o proprio host
_HOST2MARCA = {}
for marca, doms in MP_POR_MARCA.items():
    for d in doms:
        _HOST2MARCA[d] = marca
# o 2018 lista "G1" a parte de "Globo.com" na Tab.3; rotulamos os dominios do G1 assim
_HOST2MARCA["g1.globo.com"] = "G1"
_HOST2MARCA["g1.com.br"] = "G1"


def rotulo_host(host):
    if not host:
        return "(sem host)"
    for dom, marca in _HOST2MARCA.items():
        if host == dom or host.endswith("." + dom):
            return marca
    return host


def carrega():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def classe_e_host(links_json, texto=None):
    # 1o link efetivo: campo `links`; se vazio, cai para a 1a URL do texto.
    links = links_efetivos(links_json, texto)
    return classe_mp_mc_do_primeiro_link(links, CACHE)


def secao(t):
    print(f"\n{'='*66}\n{t}\n{'='*66}")


def reconstroi_amostra_A(con):
    """A = N_POR_DIA tweets/dia sorteados no pico noturno, 13-23/out."""
    rng = random.Random(SEED)
    A = []
    for dia in JANELA:
        ini = f"{dia.isoformat()}T{PICO_INI}"
        fim = f"{dia.isoformat()}T{PICO_FIM}"
        rows = con.execute(
            "SELECT * FROM tweets WHERE data_brt >= ? AND data_brt <= ?",
            (ini, fim)).fetchall()
        rows = [dict(r) for r in rows]
        escolhidos = rows if len(rows) <= N_POR_DIA else rng.sample(rows, N_POR_DIA)
        for r in escolhidos:
            r["_dia"] = dia.isoformat()
        A.extend(escolhidos)
    return A


def classifica(tweets):
    for t in tweets:
        cl, host = classe_e_host(t["links"], t.get("texto"))
        t["_classe"] = cl
        t["_host"] = host
    return tweets


def distribui(tweets):
    return Counter(t["_classe"] for t in tweets)


def tabela_por_dia(tweets, rotulo):
    secao(f"{rotulo}  (n={len(tweets)})")
    por_dia = defaultdict(Counter)
    for t in tweets:
        por_dia[t.get("_dia") or t["data_brt"][:10]][t["_classe"]] += 1
    hdr = f"{'dia':<12}{'n':>5}{'MP':>6}{'MC':>6}{'NDA':>6}{'n/res':>7}{'ind':>5}{'%comMidia':>11}{'MP%C':>7}"
    print(hdr)
    tot = Counter()
    linhas = []
    for dia in sorted(por_dia):
        c = por_dia[dia]
        n = sum(c.values())
        for k in c:
            tot[k] += c[k]
        tot["n"] += n
        comidia = c["MP"] + c["MC"]
        mp_c = 100 * c["MP"] / comidia if comidia else 0
        pct_midia = 100 * comidia / n if n else 0
        linhas.append((dia, n, c["MP"], c["MC"], c["NDA"], c["nao_resolvido"],
                       c["indefinido"], pct_midia, mp_c))
        print(f"{dia:<12}{n:>5}{c['MP']:>6}{c['MC']:>6}{c['NDA']:>6}{c['nao_resolvido']:>7}"
              f"{c['indefinido']:>5}{pct_midia:>10.1f}%{mp_c:>6.1f}%")
    n = tot["n"]
    comidia = tot["MP"] + tot["MC"]
    ag = dict(rotulo=rotulo, n=n, MP=tot["MP"], MC=tot["MC"], NDA=tot["NDA"],
              nao_res=tot["nao_resolvido"], ind=tot["indefinido"], comidia=comidia,
              pct_midia=100 * comidia / n if n else 0,
              mp_pct_C=100 * tot["MP"] / comidia if comidia else 0,
              mc_pct_C=100 * tot["MC"] / comidia if comidia else 0,
              linhas=linhas)
    print(f"{'TOTAL':<12}{n:>5}{tot['MP']:>6}{tot['MC']:>6}{tot['NDA']:>6}{tot['nao_resolvido']:>7}"
          f"{tot['indefinido']:>5}{ag['pct_midia']:>10.1f}%{ag['mp_pct_C']:>6.1f}%")
    print(f"\n  [Amostra C = tweets com midia] n={comidia}  ->  MP {ag['mp_pct_C']:.1f}%  |  "
          f"MC {ag['mc_pct_C']:.1f}%   (alvo 2018: 59% / 41%)")
    print(f"  [% com compartilhamento de midia] {ag['pct_midia']:.1f}%   (alvo 2018: 65,4%)")
    return ag


def top_midias(tweets, apenas_mc=False, k=15):
    cont = Counter()
    base = 0
    for t in tweets:
        if t["_classe"] not in ("MP", "MC"):
            continue
        if apenas_mc and t["_classe"] != "MC":
            continue
        cont[rotulo_host(t["_host"])] += 1
        base += 1
    linhas = []
    for nome, c in cont.most_common(k):
        linhas.append((nome, c, 100 * c / base if base else 0))
    return linhas, base


def bloco_top(titulo, linhas, base, alvo):
    secao(titulo + f"  (base={base})")
    print(f"  alvo 2018: {alvo}")
    for nome, c, pct in linhas:
        print(f"  {nome:<34}{c:>5}{pct:>7.1f}%")
    return linhas, base


def escreve_relatorio(cob, ag_A, ag_uni, top_all, base_all, top_mc, base_mc):
    def tab_dia(ag):
        L = ["| dia | n | MP | MC | NDA | n/res | ind | % com mídia | MP% (de C) |",
             "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
        for (dia, n, mp, mc, nda, nr, ind, pm, mpc) in ag["linhas"]:
            L.append(f"| {dia} | {n} | {mp} | {mc} | {nda} | {nr} | {ind} | {pm:.1f}% | {mpc:.1f}% |")
        L.append(f"| **TOTAL** | **{ag['n']}** | {ag['MP']} | {ag['MC']} | {ag['NDA']} | "
                 f"{ag['nao_res']} | {ag['ind']} | **{ag['pct_midia']:.1f}%** | **{ag['mp_pct_C']:.1f}%** |")
        return "\n".join(L)

    def tab_top(linhas):
        L = ["| mídia | n | % |", "|---|--:|--:|"]
        for nome, c, pct in linhas:
            L.append(f"| {nome} | {c} | {pct:.1f}% |")
        return "\n".join(L)

    md = f"""# Fase 0 sob MP/MC — replicação do paper de 2018 (Palabra Clave)

> Gerado por `analise/analisa_midia_mp_mc.py` sobre `snapshot_hashtag.sqlite` +
> `expand_cache.sqlite`. Convenção **estrita** das 26 marcas (25 nomeadas) —
> `core/midia_mp_mc.py`. Determinístico (não usa stance). Ver
> `PAPER2018_palabra_clave.md` e `REPLICACAO_CASO_COMPOS2014.md`.

## Método (o que reproduz e o que é stub)
- **Amostra A:** {N_POR_DIA} tweets/dia sorteados (semente {SEED}) no pico noturno
  ({PICO_INI[:5]}–{PICO_FIM[:5]} BRT), 13–23/out (11 dias), só #Eleições2014.
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
{cob}
```

## Amostra A reconstruída (≈2.200; alvo do paper)
{tab_dia(ag_A)}

- **Amostra C** (com mídia) = **{ag_A['comidia']}** de {ag_A['n']} → **{ag_A['pct_midia']:.1f}%**
  compartilharam mídia *(alvo 2018: 65,4%; 1.439/2.200)*.
- **Tabela 2** (split entre os de C): **MP {ag_A['mp_pct_C']:.1f}% · MC {ag_A['mc_pct_C']:.1f}%**
  *(alvo 2018: 59% / 41%)*.

## Universo on-hashtag na mesma janela (13–23/out) — efeito de volume
{tab_dia(ag_uni)}

## Tabela 3 — mídias mais compartilhadas (amostra A, base = tweets com mídia)
{tab_top(top_all)}

## Tabela 4 — mídias mais compartilhadas entre as MCs (amostra A)
{tab_top(top_mc)}

## Ressalvas desta reprodução
- **% com mídia pode vir abaixo de 65,4%**: `indefinido` (domínio real fora do
  dicionário) e `nao_resolvido` (encurtador morto) são links que *podem* ser mídia
  mas não classificamos — o paper (manual) reconhecia "100+ mídias". Resíduo a curar.
- **Marcas rebaixadas para MC** pela regra estrita das 26 (aparecem no topo do 2018,
  mas fora da lista): {", ".join(MAINSTREAM_REBAIXADA_PARA_MC) or "(nenhuma no dicionário)"}.
- **Amostragem aleatória**: números variam com a semente; é reprodução *agregada*
  (Fase 0), não recuperação dos tweets originais.
- **B/D e Tab. 5–7**: dependem de stance (Fase 0.5, adiada).
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"\n[ok] relatorio -> {OUT_MD}")


def cobertura_universo(con):
    secao("COBERTURA MP/MC — universo on-hashtag (janela 13-23/out)")
    dist = Counter()
    tot = 0
    for lj, tx in con.execute(
            "SELECT links, texto FROM tweets WHERE data_brt >= '2014-10-13' AND data_brt < '2014-10-24'"):
        cl, _ = classe_e_host(lj, tx)
        dist[cl] += 1
        tot += 1
    linhas = [f"total: {tot}"]
    for cl, c in dist.most_common():
        linhas.append(f"  {cl:<14}{c:>8}  {100*c/tot:>5.1f}%")
    resolvido = tot - dist["nao_resolvido"]
    linhas.append(f"cobertura (classe definida): {100*resolvido/tot:.1f}%")
    txt = "\n".join(linhas)
    print(txt)
    return txt


def main():
    if not DB_PATH.exists():
        raise SystemExit("snapshot ausente — rode pipeline/extrai_snapshot.py hashtag")
    if not CACHE:
        print("[aviso] cache de expansao vazio — links curtos ficam 'nao_resolvido'")
    con = carrega()

    cob = cobertura_universo(con)

    A = classifica(reconstroi_amostra_A(con))
    ag_A = tabela_por_dia(A, "AMOSTRA A reconstruida (200/dia, pico noturno)")

    uni = classifica([dict(r) for r in con.execute(
        "SELECT * FROM tweets WHERE data_brt >= '2014-10-13' AND data_brt < '2014-10-24'")])
    ag_uni = tabela_por_dia(uni, "UNIVERSO on-hashtag 13-23/out")

    top_all, base_all = top_midias(A, apenas_mc=False)
    bloco_top("TABELA 3 — mídias mais compartilhadas (amostra A)", top_all, base_all,
              "G1 15, UOL 15, Folha 5, Estadão 5, Valor 5, JB 4, O Dia 3, O Globo 3, R7 3, A Tarde 2")
    top_mc, base_mc = top_midias(A, apenas_mc=True)
    bloco_top("TABELA 4 — mais compartilhadas entre as MCs (amostra A)", top_mc, base_mc,
              "Twitter 29, Facebook 20, Blogs 12, Instagram 8, YouTube 7")

    # dump da amostra A para auditoria
    outA = Path("data/repl/compos2014/A2018_reconstruida.json")
    outA.write_text(json.dumps(
        [{k: t[k] for k in ("id_tweet", "_dia", "data_brt", "autor", "texto",
                            "status_retweet", "status_verificado")}
         | {"host": t["_host"], "classe_mp_mc": t["_classe"]} for t in A],
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n[ok] amostra A -> {outA}  ({len(A)} tweets)")

    escreve_relatorio(cob, ag_A, ag_uni, top_all, base_all, top_mc, base_mc)


if __name__ == "__main__":
    main()
