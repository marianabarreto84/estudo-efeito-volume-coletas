"""
Fase 2 / eixo A — AV1 formal: atribui LADO (pro/anti) a TODAS as comunidades da
particao Louvain e mede a cobertura, pareando a convencao do paper.

Por que este script existe
--------------------------
O paper reporta (Tabela 1) que "pro" e "anti" juntos sao 78% dos posts do periodo.
A Fase 2 comparou isso com as DUAS MAIORES comunidades isoladas (60,6%) — comparacao
mal pareada: o "pro"/"anti" do paper e a UNIAO dos grupos de modularidade mapeados a
cada lado (sao 7 grupos no suplemento, nao 2). Este script faz a atribuicao formal.

Regra de atribuicao (analoga a do paper)
----------------------------------------
O paper rodou Louvain, obteve grupos e rotulou cada GRUPO como pro ou anti olhando
seus membros influentes; todo usuario herda o lado do seu grupo; quem sobra e
"Unidentified". Aqui:

  1. Sementes = os 602 autores influentes publicados (aba `Authors` do suplemento),
     cada um com lado proprio — reproduz a Tabela 3 do paper (353 pro / 246 anti /
     3 sem lado, conferido em tempo de execucao).
  2. Cada comunidade recebe o lado da MAIORIA das sementes que contem.
  3. Comunidade sem semente -> nao identificada. Empate -> nao identificada.
  4. Autores fora do grafo de RT (sem RT dado nem recebido) -> nao identificados.

Decisoes registradas
--------------------
  - Reusa a particao ja congelada (`comunidades_autores`, run seed 42 de
    `rede_modularidade.py`); NAO re-roda Louvain, para o numero ser comparavel ao
    da Fase 2.
  - "Posts" = originais + RTs feitos pelo autor (mesma definicao da Tabela 1).
  - Match de autor case-insensitive e sem '@' nos dois lados.
  - Sensibilidade: exige minimo de 1/2/3/5 sementes por comunidade, para mostrar
    quanto o resultado depende de comunidades decididas por pouca evidencia.

Saidas: stdout + data/repl/vacinas2022/av1_lados.json

Uso: PYTHONIOENCODING=utf-8 python -u analise/atribui_lado_comunidades.py
"""
import collections
import json
import pathlib
import sqlite3
import time

import openpyxl

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SNAP = RAIZ / "data/repl/vacinas2022/snapshot_vacinas.sqlite"
SUPL = RAIZ / "data/repl/vacinas2022/suplementar_rotulos.xlsx"
OUT_JSON = RAIZ / "data/repl/vacinas2022/av1_lados.json"

# Tabela 1 do paper (aba `Table tweets and retweets` do suplemento)
PAPER = {
    "tweets": {"pro": 461_265, "anti": 345_688, "nao_ident": 300_271},
    "retweets": {"pro": 1_561_005, "anti": 1_632_738, "nao_ident": 848_307},
}
MINIMOS_SEMENTES = (1, 2, 3, 5)


def log(msg):
    print(msg, flush=True)


def norm(a):
    return a.strip().lstrip("@").lower() if a else None


def main():
    t0 = time.time()

    # ---------- 0. referencia do paper ----------
    p_pro = PAPER["tweets"]["pro"] + PAPER["retweets"]["pro"]
    p_anti = PAPER["tweets"]["anti"] + PAPER["retweets"]["anti"]
    p_ni = PAPER["tweets"]["nao_ident"] + PAPER["retweets"]["nao_ident"]
    p_tot = p_pro + p_anti + p_ni
    log("== 0. Referencia: Tabela 1 do paper ==")
    log(f"   posts totais {p_tot:,}  |  pro {100*p_pro/p_tot:.1f}%  "
        f"anti {100*p_anti/p_tot:.1f}%  nao ident. {100*p_ni/p_tot:.1f}%")
    log(f"   >>> cobertos (pro+anti) = {100*(p_pro+p_anti)/p_tot:.1f}%")

    # ---------- 1. sementes ----------
    log("== 1. Sementes: os 602 autores influentes do suplemento ==")
    wb = openpyxl.load_workbook(SUPL, read_only=True, data_only=True)
    lado_semente = {}
    n_pro = n_anti = n_sem = 0
    for r in list(wb["Authors"].iter_rows(values_only=True))[1:]:
        pro, anti, autor = r[0], r[1], r[2]
        a = norm(autor)
        if not a:
            continue
        if pro == 1 and anti != 1:
            lado_semente[a] = "pro"; n_pro += 1
        elif anti == 1 and pro != 1:
            lado_semente[a] = "anti"; n_anti += 1
        else:
            n_sem += 1
    log(f"   {n_pro} pro / {n_anti} anti / {n_sem} sem lado  (paper Tabela 3: 353/246)")
    assert (n_pro, n_anti) == (353, 246), "sementes divergem da Tabela 3 do paper"

    # ---------- 2. particao congelada + posts por autor ----------
    log("== 2. Particao congelada (seed 42) + posts por autor ==")
    db = sqlite3.connect(SNAP)
    cur = db.cursor()
    com_de = {}
    for autor, c in cur.execute("SELECT autor, comunidade FROM comunidades_autores"):
        com_de[norm(autor)] = c
    n_com = len(set(com_de.values()))
    log(f"   {len(com_de):,} autores em {n_com:,} comunidades")

    # Duas BASES de contagem de posts (ver secao "Qual base" no FASE2 doc):
    #   ampla  = todos os originais + todos os RTs  (6.554.705)
    #   paper  = originais em PT de autores no grafo de RT + RTs  (5.637.015),
    #            que reproduz a Tabela 1 do paper a +2% na coluna de tweets e
    #            corresponde ao criterio de inclusao declarado no PDF ("all tweets
    #            from users who retweeted or retweeted someone in the period").
    rts_por_autor = {norm(a): n for a, n in
                     cur.execute("SELECT autor, count(*) FROM rt_arestas GROUP BY 1")}

    bases = {}
    for nome, sql in (
        ("ampla", "SELECT autor, count(*) FROM originais GROUP BY 1"),
        ("paper", "SELECT o.autor, count(*) FROM originais o "
                  "WHERE o.idioma='pt' AND EXISTS (SELECT 1 FROM comunidades_autores k "
                  "WHERE k.autor = o.autor) GROUP BY 1"),
    ):
        p = collections.Counter()
        for autor, n in cur.execute(sql):
            p[norm(autor)] += n
        for autor, n in rts_por_autor.items():
            p[autor] += n
        bases[nome] = p
        log(f"   base '{nome}': {len(p):,} autores; {sum(p.values()):,} posts")

    por_com = {}          # base -> (posts_por_com, posts_fora, total)
    for nome, p in bases.items():
        ppc, fora = collections.Counter(), 0
        for autor, n in p.items():
            c = com_de.get(autor)
            if c is None:
                fora += n
            else:
                ppc[c] += n
        por_com[nome] = (ppc, fora, sum(p.values()))
        log(f"   base '{nome}': posts de autores fora do grafo {fora:,} "
            f"({100*fora/sum(p.values()):.1f}%) -> nao identificados")

    posts_por_com, posts_fora, total_posts = por_com["ampla"]

    # ---------- 3. sementes -> comunidades ----------
    log("== 3. Localizando as sementes na particao ==")
    votos = collections.defaultdict(collections.Counter)
    achadas = 0
    for a, lado in lado_semente.items():
        c = com_de.get(a)
        if c is not None:
            votos[c][lado] += 1
            achadas += 1
    log(f"   {achadas}/{len(lado_semente)} sementes localizadas, "
        f"em {len(votos)} comunidades distintas")

    mistas = {c: dict(v) for c, v in votos.items() if len(v) > 1}
    log(f"   comunidades com sementes dos DOIS lados: {len(mistas)}")
    for c, v in sorted(mistas.items(), key=lambda kv: -sum(kv[1].values()))[:5]:
        pct = 100 * posts_por_com.get(c, 0) / total_posts
        log(f"     com {c}: {v}  ({pct:.1f}% dos posts)")

    # ---------- 4. atribuicao + sensibilidade, nas duas bases ----------
    log("== 4. Atribuicao de lado por maioria das sementes ==")
    resultados = {}
    for base in ("ampla", "paper"):
        ppc, fora, total = por_com[base]
        log(f"  -- base '{base}' ({total:,} posts) --")
        cenarios, detalhe = {}, None
        for minimo in MINIMOS_SEMENTES:
            lado_com = {}
            for c, v in votos.items():
                if sum(v.values()) < minimo:
                    continue
                ordem = v.most_common()
                if len(ordem) > 1 and ordem[0][1] == ordem[1][1]:
                    continue                  # empate -> nao identificada
                lado_com[c] = ordem[0][0]

            agg = collections.Counter()
            for c, n in ppc.items():
                agg[lado_com.get(c, "nao_ident")] += n
            agg["nao_ident"] += fora

            if minimo == 1:                   # detalhe do cenario principal
                detalhe = [
                    {"comunidade": c, "lado": lado, "sementes": dict(votos[c]),
                     "posts": ppc.get(c, 0),
                     "pct_posts": round(100 * ppc.get(c, 0) / total, 2)}
                    for c, lado in sorted(lado_com.items(),
                                          key=lambda kv: -ppc.get(kv[0], 0))
                ]
                for d in detalhe:
                    log(f"     com {d['comunidade']:>5} {d['lado']:>4} | "
                        f"sementes {d['sementes']} | {d['pct_posts']:5.2f}% dos posts")

            pro, anti, ni = agg["pro"], agg["anti"], agg["nao_ident"]
            cob = 100 * (pro + anti) / total
            cenarios[minimo] = {
                "min_sementes": minimo,
                "comunidades_com_lado": len(lado_com),
                "pro_pct": round(100 * pro / total, 1),
                "anti_pct": round(100 * anti / total, 1),
                "nao_ident_pct": round(100 * ni / total, 1),
                "cobertura_pct": round(cob, 1),
                "razao_pro_anti": round(pro / anti, 3) if anti else None,
                "posts": {"pro": pro, "anti": anti, "nao_ident": ni},
            }
            marca = "  <- principal" if minimo == 1 else ""
            log(f"     >= {minimo} semente(s): {len(lado_com):>4} com lado | "
                f"pro {100*pro/total:5.1f}%  anti {100*anti/total:5.1f}%  "
                f"n/ident {100*ni/total:5.1f}%  => cobertura {cob:.1f}%{marca}")
        cenarios[1]["comunidades_detalhe"] = detalhe
        resultados[base] = {"total_posts": total, "posts_fora_grafo": fora,
                            "cenarios": cenarios}

    # ---------- 5. veredito ----------
    log("== 5. AV1 — replica x paper ==")
    log(f"   {'':<18}{'ampla':>9}{'conv. paper':>13}{'paper':>9}")
    for rot, chave, ref in (("pro", "pro_pct", 100 * p_pro / p_tot),
                            ("anti", "anti_pct", 100 * p_anti / p_tot),
                            ("nao identificados", "nao_ident_pct", 100 * p_ni / p_tot),
                            ("COBERTURA", "cobertura_pct",
                             100 * (p_pro + p_anti) / p_tot)):
        log(f"   {rot:<18}{resultados['ampla']['cenarios'][1][chave]:>8.1f}%"
            f"{resultados['paper']['cenarios'][1][chave]:>12.1f}%{ref:>8.1f}%")
    for base in ("ampla", "paper"):
        g = abs(resultados[base]["cenarios"][1]["cobertura_pct"]
                - 100 * (p_pro + p_anti) / p_tot)
        log(f"   gap de cobertura na base '{base}': {g:.1f} p.p.")

    log("== 6. O que e robusto: a RAZAO pro/anti ==")
    razoes = [resultados[b]["cenarios"][m]["razao_pro_anti"]
              for b in ("ampla", "paper") for m in MINIMOS_SEMENTES]
    log(f"   razao pro/anti nos {len(razoes)} cenarios: "
        f"min {min(razoes):.2f} · max {max(razoes):.2f}")
    log(f"   razao pro/anti do paper (Tabela 1): {p_pro/p_anti:.2f}")
    log("   -> a COBERTURA varia com a base "
        f"({min(resultados[b]['cenarios'][m]['cobertura_pct'] for b in ('ampla','paper') for m in MINIMOS_SEMENTES):.1f}"
        f"–{max(resultados[b]['cenarios'][m]['cobertura_pct'] for b in ('ampla','paper') for m in MINIMOS_SEMENTES):.1f}%); "
        "a RAZAO nao.")
    resultado_razoes = {"min": min(razoes), "max": max(razoes),
                        "paper": round(p_pro / p_anti, 3)}

    resultado = {
        "script": "analise/atribui_lado_comunidades.py",
        "executado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "particao": {"origem": "comunidades_autores (rede_modularidade.py, seed 42)",
                     "n_comunidades": n_com, "n_autores": len(com_de)},
        "sementes": {"pro": n_pro, "anti": n_anti, "sem_lado": n_sem,
                     "localizadas": achadas,
                     "comunidades_atingidas": len(votos),
                     "comunidades_mistas": mistas},
        "bases": resultados,
        "razao_pro_anti": resultado_razoes,
        "paper_tabela1": {
            "posts_total": p_tot,
            "pro_pct": round(100 * p_pro / p_tot, 1),
            "anti_pct": round(100 * p_anti / p_tot, 1),
            "nao_ident_pct": round(100 * p_ni / p_tot, 1),
            "cobertura_pct": round(100 * (p_pro + p_anti) / p_tot, 1),
        },
    }
    OUT_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    db.close()
    log(f"\nOK — concluido em {time.time()-t0:.0f}s -> {OUT_JSON.name}")


if __name__ == "__main__":
    main()
