"""
Fase 3, controle de DATA: o material que nos temos e o artigo nao tem existia quando
eles coletaram?

Por que existe
--------------
Duvida da Mariana em 28/set/2026, vespera da defesa: os 38,3 p.p. do funil e o residuo
no tema podem ser artefato de os videos terem sido publicados DEPOIS da coleta original.
Se for isso, a objecao "os videos nao existiam" derruba o capitulo.

O teste: refazer as duas comparacoes centrais cortando a coleta por data de publicacao,
cada vez mais para tras. Se o sinal nao se move, a data nao explica nada.

O corte critico e 2022-08-21, que e a data do video MAIS RECENTE do corpus publicado:
qualquer video publicado antes disso ja existia quando eles coletaram, seja quando for
que eles tenham coletado.

Uso: PYTHONIOENCODING=utf-8 python -u analise/fase3_data_publicacao.py
Saida: stdout + data/repl/agecovp2020/fase3_data_publicacao.json
"""
import csv
import json
import math
import pathlib
import sqlite3
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.regras import no_tema, eh_ugc, LIMIAR_INSCRITOS

csv.field_size_limit(10 ** 8)
D = pathlib.Path("data/repl/agecovp2020")
G = D / "gabarito_zenodo"
OUT = D / "fase3_data_publicacao.json"
Z = 1.959964
CORTES = [None, "2022-08-21", "2022-06-30", "2022-01-01", "2021-06-30"]


def ic(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    return 100 * d, 100 * (d - Z * se), 100 * (d + Z * se)


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def main():
    t = json.loads((D / "termos_agecovp.json").read_text(encoding="utf-8"))
    lista = [norm(x) for x in t["filtro_palavras_chave"]["termos"]]

    def filtro_corrigido(tit, desc, termo):
        campo = norm(tit) + " " + norm(desc)
        if all(w in campo for w in norm(termo).split()):
            return 1
        return 1 if any(k in campo for k in lista) else 0

    cx = sqlite3.connect(D / "snapshot_agecovp.sqlite")
    cx.row_factory = sqlite3.Row
    vids = [dict(r) for r in cx.execute(
        "SELECT video_id, channel_id, title, description, description_full,"
        " published_at, termo_busca, passa_filtro FROM videos")]
    canais = {r["channel_id"]: dict(r) for r in cx.execute("SELECT * FROM canais")}
    cx.close()

    gab_ch, gab_vid, datas_gab = set(), set(), []
    with open(G / "channels.csv", encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            gab_ch.add(r["Channel_id"])
    with open(G / "videos.csv", encoding="utf-8-sig", errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            v = (r.get("Video_id") or "").strip()
            d = (r.get("Published_date") or "").strip()
            if v:
                gab_vid.add(v)
            if d:
                datas_gab.append(d)
    datas_gab.sort()

    # limite inferior para a data em que ELES coletaram: o comentario mais recente do
    # gabarito deles. Nao se coleta um comentario antes de ele existir.
    ult_com = ""
    with open(G / "comments.csv", encoding="utf-8-sig", errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            d = (r.get("PublishedAt") or "").strip()
            if d > ult_com:
                ult_com = d
    mais_novo_nosso = max(v["published_at"] for v in vids)
    print("A COLETA DELES e POSTERIOR a %s (comentario mais recente do gabarito)." % ult_com[:10])
    print("O video mais novo do NOSSO instantaneo e de %s." % mais_novo_nosso[:10])
    print("=> os %d videos nossos ja existiam quando eles coletaram." % len(vids))
    print()
    print("janela de publicacao do CORPUS PUBLICADO : %s .. %s" % (datas_gab[0][:10], datas_gab[-1][:10]))
    print("janela de publicacao da NOSSA COLETA     : %s .. %s"
          % (min(v["published_at"] for v in vids)[:10], max(v["published_at"] for v in vids)[:10]))
    tail = [v for v in vids if v["published_at"] >= datas_gab[-1]]
    print("videos nossos publicados DEPOIS do mais recente deles: %d de %d (%.1f%%)"
          % (len(tail), len(vids), 100 * len(tail) / len(vids)))
    print()

    def ugc(v):
        r = canais.get(v["channel_id"])
        if not r:
            return None
        return 1 if eh_ugc(r.get("title"), r.get("inscritos"), LIMIAR_INSCRITOS) else 0

    res = {"coleta_deles_posterior_a": ult_com,
           "video_mais_novo_nosso": mais_novo_nosso,
           "todos_ja_existiam": ult_com > mais_novo_nosso,
           "corpus_publicado": {"min": datas_gab[0], "max": datas_gab[-1]},
           "nossa_coleta": {"min": min(v["published_at"] for v in vids),
                            "max": max(v["published_at"] for v in vids)},
           "publicados_depois_do_mais_recente_deles": len(tail),
           "limiar_inscritos": LIMIAR_INSCRITOS, "cortes": {}}

    cab = ("%-14s %6s | %-28s | %-28s | %s"
           % ("corte", "n", "filtro: UGC passa x descarta", "funil: UGC dentro x fora", "residuo"))
    print(cab)
    print("-" * len(cab))

    for conv, campo, refaz in (("como publicado (descricao truncada)", "description", False),
                               ("corrigido (descricao completa)", "description_full", True)):
      print()
      print("convencao do texto: %s" % conv)
      res["cortes"][conv] = {}
      for corte in CORTES:
        sub = [v for v in vids if corte is None or v["published_at"] < corte]
        tema = [v for v in sub if no_tema(v["title"], v[campo])]
        linha = {"n_coletados": len(sub), "n_tema": len(tema)}

        # (a) o filtro, entre os videos no tema. `refaz` = recalcular o filtro sobre a
        # descricao completa; sem ele usa-se a coluna do capitulo (descricao truncada).
        def aprova(v):
            return (filtro_corrigido(v["title"], v[campo], v["termo_busca"])
                    if refaz else v["passa_filtro"])
        p = [v for v in tema if aprova(v)]
        b = [v for v in tema if not aprova(v)]
        up, tp = sum(1 for v in p if ugc(v) == 1), sum(1 for v in p if ugc(v) is not None)
        ub, tb = sum(1 for v in b if ugc(v) == 1), sum(1 for v in b if ugc(v) is not None)
        df, lof, hif = ic(up, tp, ub, tb)
        linha["filtro"] = {"ugc_passa_pct": round(100 * up / tp, 1),
                           "ugc_descarta_pct": round(100 * ub / tb, 1),
                           "delta_pp": round(df, 1), "ic95": [round(lof, 1), round(hif, 1)]}

        # (b) o funil inteiro: canal dentro x fora do corpus publicado
        dentro = [v for v in tema if v["channel_id"] in gab_ch]
        fora = [v for v in tema if v["channel_id"] not in gab_ch]
        ud, td = sum(1 for v in dentro if ugc(v) == 1), sum(1 for v in dentro if ugc(v) is not None)
        uf, tf = sum(1 for v in fora if ugc(v) == 1), sum(1 for v in fora if ugc(v) is not None)
        dn, lon, hin = ic(ud, td, uf, tf)
        linha["funil"] = {"ugc_dentro_pct": round(100 * ud / td, 1), "n_dentro": td,
                          "ugc_fora_pct": round(100 * uf / tf, 1), "n_fora": tf,
                          "delta_pp": round(dn, 1), "ic95": [round(lon, 1), round(hin, 1)]}

        # (c) o residuo: quanto do descarte esta no tema
        desc_tot = [v for v in sub if not filtro_corrigido(v["title"], v[campo], v["termo_busca"])]
        desc_tema = [v for v in desc_tot if no_tema(v["title"], v[campo])]
        linha["residuo_no_tema_pct"] = round(100 * len(desc_tema) / len(desc_tot), 1)

        print("%-14s %6d | %5.1f%% x %5.1f%%  %+6.1f p.p. | %5.1f%% x %5.1f%%  %+6.1f p.p. | %5.1f%%"
              % (corte or "sem corte", len(sub),
                 linha["filtro"]["ugc_passa_pct"], linha["filtro"]["ugc_descarta_pct"], df,
                 linha["funil"]["ugc_dentro_pct"], linha["funil"]["ugc_fora_pct"], dn,
                 linha["residuo_no_tema_pct"]))
        res["cortes"][conv][corte or "sem corte"] = linha

    # quem e mais novo: o material dentro ou fora do corpus publicado?
    tema_all = [v for v in vids if no_tema(v["title"], v["description"])]
    def med_data(grupo):
        xs = sorted(v["published_at"] for v in grupo)
        return xs[len(xs) // 2][:10] if xs else None
    dentro = [v for v in tema_all if v["channel_id"] in gab_ch]
    fora = [v for v in tema_all if v["channel_id"] not in gab_ch]
    res["data_mediana"] = {"dentro_do_corpus": med_data(dentro), "fora_do_corpus": med_data(fora)}
    print()
    print("data de publicacao MEDIANA, videos no tema:")
    print("  canal dentro do corpus publicado: %s (n=%d)" % (med_data(dentro), len(dentro)))
    print("  canal fora do corpus publicado  : %s (n=%d)" % (med_data(fora), len(fora)))

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n-> %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
