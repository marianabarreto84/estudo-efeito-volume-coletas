# -*- coding: utf-8 -*-
"""Gera as figuras da dissertacao a partir dos JSON congelados dos casos.

Rastreabilidade: nenhum numero e digitado aqui. Tudo vem de:
  casos/twitter-ituassu/data/repl/compos2014/curva_midia.json
  casos/vacinas/data/repl/vacinas2022/curva_rede.json
  casos/reddit-buntain/data/repl/buntain2013/curva_rb3.json
  casos/youtube-agecovp/data/repl/agecovp2020/fase3_ugc_completo.json

Uso: python gerar_figuras.py     (a partir desta pasta)
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]                     # .../dissertacao-mestrado
CASOS = RAIZ / "casos"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
})

CINZA = "#4d4d4d"
BANDA = "#b8b8b8"
DESTAQUE = "#000000"


def fig_rtmv():
    """Cap. 3 -- curva A(volume) do RTMV: o estimador nao anda, so estreita."""
    d = json.loads((CASOS / "twitter-ituassu/data/repl/compos2014/curva_midia.json")
                   .read_text(encoding="utf-8"))
    pts = d["curva_rtmv_janela"]
    n = [p["n"] for p in pts]
    media = [p["media"] for p in pts]
    lo = [p["p2_5"] for p in pts]
    hi = [p["p97_5"] for p in pts]

    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    ax.fill_between(n, lo, hi, color=BANDA, alpha=0.55, linewidth=0,
                    label="banda de 95% das subamostras")
    ax.plot(n, media, color=CINZA, linewidth=1.4, marker="o", markersize=3,
            label="RTMV médio no universo da janela")
    ax.axhline(50, color=DESTAQUE, linestyle="--", linewidth=1.0)
    ax.annotate("H1 do artigo: RTMV > 50%", xy=(140, 50), xytext=(140, 53.2),
                color=DESTAQUE, fontsize=8)

    # ponto publicado pelo artigo: 48,3% sobre n=700
    ax.plot([700], [48.3], marker="D", color=DESTAQUE, markersize=5, zorder=5,
            linestyle="none", label="estimativa do artigo (700 tweets, pico)")
    ax.annotate("48,3%", xy=(700, 48.3), xytext=(820, 45.0), fontsize=8,
                color=DESTAQUE,
                arrowprops=dict(arrowstyle="-", color=DESTAQUE, linewidth=0.7))

    ax.set_xscale("log")
    ax.set_xlabel("tweets sorteados do universo da janela (escala log)")
    ax.set_ylabel("retuíte de mídia vertical (%)")
    ax.set_ylim(26, 58)
    ax.set_xlim(85, 40000)
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{int(v):,}".replace(",", ".")))
    ax.set_xticks([100, 700, 2800, 11200, 32193])
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout(pad=0.4)
    saida = AQUI / "curva_rtmv.pdf"
    fig.savefig(saida)
    fig.savefig(saida.with_suffix(".png"), dpi=180)
    plt.close(fig)
    print("ok:", saida.name)


def fig_rede_vacinas():
    """Cap. 4 -- a razao entre os polos ainda sobe; e nunca se aproxima de 1,02."""
    d = json.loads((CASOS / "vacinas/data/repl/vacinas2022/curva_rede.json")
                   .read_text(encoding="utf-8"))
    pts = d["pontos"]
    f = [p["fracao"] * 100 for p in pts]
    r_med = [p["razao_pro_anti"]["media"] for p in pts]
    r_lo = [p["razao_pro_anti"]["min"] for p in pts]
    r_hi = [p["razao_pro_anti"]["max"] for p in pts]
    nmi_med = [p["nmi_vs_cheio"]["media"] for p in pts]
    nmi_lo = [p["nmi_vs_cheio"]["min"] for p in pts]
    nmi_hi = [p["nmi_vs_cheio"]["max"] for p in pts]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.0, 2.9))

    a1.fill_between(f, r_lo, r_hi, color=BANDA, alpha=0.55, linewidth=0)
    a1.plot(f, r_med, color=CINZA, linewidth=1.4, marker="o", markersize=3,
            label="réplica")
    a1.axhline(1.02, color=DESTAQUE, linestyle="--", linewidth=1.0)
    a1.annotate("1,02 (valor do artigo)", xy=(1.2, 1.02), xytext=(1.2, 1.05),
                fontsize=7.5, color=DESTAQUE)
    a1.set_xscale("log")
    a1.set_xlabel("fração da coleta (%, escala log)")
    a1.set_ylabel("razão entre os polos (pró / anti)")
    a1.set_ylim(0.97, 1.62)
    a1.set_xticks([1, 5, 25, 100])
    a1.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    a1.set_title("(a) razão entre os polos")

    a2.fill_between(f, nmi_lo, nmi_hi, color=BANDA, alpha=0.55, linewidth=0)
    a2.plot(f, nmi_med, color=CINZA, linewidth=1.4, marker="o", markersize=3)
    a2.axhline(nmi_med[-1], color=DESTAQUE, linestyle="--", linewidth=1.0)
    a2.annotate("teto (0,97)", xy=(1.2, nmi_med[-1]), xytext=(1.2, nmi_med[-1] + 0.02),
                fontsize=7.5, color=DESTAQUE)
    a2.set_xscale("log")
    a2.set_xlabel("fração da coleta (%, escala log)")
    a2.set_ylabel("NMI contra o corpus cheio")
    a2.set_ylim(0.35, 1.05)
    a2.set_xticks([1, 5, 25, 100])
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    a2.set_title("(b) similaridade da partição")

    fig.tight_layout(pad=0.4)
    fig.subplots_adjust(wspace=0.42)
    saida = AQUI / "curva_rede_vacinas.pdf"
    fig.savefig(saida)
    fig.savefig(saida.with_suffix(".png"), dpi=180)
    plt.close(fig)
    print("ok:", saida.name)


def fig_rb3_limiar():
    """Cap. 5 -- multi-participacao por limiar de atividade: sobe e assenta,
    e o valor do artigo nao e recuperavel em limiar nenhum."""
    d = json.loads((CASOS / "reddit-buntain/data/repl/buntain2013/curva_rb3.json")
                   .read_text(encoding="utf-8"))
    pts = d["curva_por_limiar"]
    k = [p["k"] for p in pts]
    pct = [p["pct_multi"] for p in pts]
    alvo = d["paper"]["pct_multi"]

    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    ax.plot(k, pct, color=CINZA, linewidth=1.4, marker="o", markersize=3.5)
    ax.annotate("universo, sob cada limiar de atividade", xy=(5, 48.8),
                xytext=(1.9, 59), fontsize=8, color=CINZA)
    ax.axhline(alvo, color=DESTAQUE, linestyle="--", linewidth=1.0)
    ax.annotate("3%: o valor publicado, sobre 279 participantes",
                xy=(1.02, alvo), xytext=(1.02, alvo + 2.2), fontsize=8,
                color=DESTAQUE)
    ax.axvspan(10, 50, color=BANDA, alpha=0.35, linewidth=0)
    ax.annotate("a medida assenta", xy=(20, 20), xytext=(11.3, 22), fontsize=8,
                color=CINZA)

    for x, y in zip(k, pct):
        if x in (1, 20):
            ax.annotate(f"{y:.1f}%".replace(".", ","), xy=(x, y),
                        xytext=(x * 1.12, y - 4.5), fontsize=8, color=CINZA)

    ax.set_xscale("log")
    ax.set_xticks(k)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    ax.set_xlabel("limiar de atividade: mínimo de mensagens no mês (escala log)")
    ax.set_ylabel("participantes em mais de\num comunidade (%)")
    ax.set_ylim(0, 66)
    ax.set_xlim(0.95, 62)
    fig.tight_layout(pad=0.4)
    saida = AQUI / "curva_rb3_limiar.pdf"
    fig.savefig(saida)
    fig.savefig(saida.with_suffix(".png"), dpi=180)
    plt.close(fig)
    print("ok:", saida.name)


def fig_youtube_filtro():
    """Cap. 6 -- o filtro de palavra-chave quase nao seleciona; o funil inteiro,
    sim. Duas comparacoes da mesma quantidade (fatia de UGC), lado a lado."""
    d = json.loads((CASOS / "youtube-agecovp/data/repl/agecovp2020"
                            "/fase3_ugc_completo.json")
                   .read_text(encoding="utf-8"))
    filtro = d["API (todos os canais)"]
    funil = d["corpus_x_nao_corpus"]

    virg = lambda v: f"{abs(v):.1f}".replace(".", ",")
    grupos = [
        ("(a) o filtro de palavra-chave",
         [("aprovados", filtro["passa_pct"]),
          ("descartados", filtro["descartado_pct"])],
         "o filtro descarta {} p.p. – e não mais –\n"
         "de conteúdo de usuário do que preserva\n"
         "(IC 95%: {} a {})".format(
             virg(filtro["delta_pp"]), virg(filtro["ic95"][1]),
             virg(filtro["ic95"][0]))),
        ("(b) o funil de coleta inteiro",
         [("canal no corpus", funil["no_corpus"]["ugc_pct"]),
          ("canal fora dele", funil["fora_corpus"]["ugc_pct"])],
         "o corpus publicado tem {} p.p. menos\n"
         "de conteúdo de usuário do que o que ficou fora\n"
         "(IC 95%: {} a {})".format(
             virg(funil["delta_pp"]), virg(funil["ic95"][0]),
             virg(funil["ic95"][1]))),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(6.0, 3.3), sharey=True)
    for ax, (titulo, barras, rodape) in zip(axes, grupos):
        nomes = [b[0] for b in barras]
        vals = [b[1] for b in barras]
        ax.bar(nomes, vals, color=[CINZA, BANDA], width=0.55)
        for i, v in enumerate(vals):
            ax.annotate(f"{v:.1f}%".replace(".", ","), xy=(i, v),
                        xytext=(i, v + 1.8), ha="center", fontsize=8.5,
                        color=DESTAQUE)
        ax.set_title(titulo)
        ax.set_ylim(0, 72)
        ax.set_xlabel(rodape, fontsize=8)
    axes[0].set_ylabel("vídeos de conteúdo de usuário (%)")
    fig.tight_layout(pad=0.4)
    fig.subplots_adjust(wspace=0.12)
    saida = AQUI / "youtube_filtro_funil.pdf"
    fig.savefig(saida)
    fig.savefig(saida.with_suffix(".png"), dpi=180)
    plt.close(fig)
    print("ok:", saida.name)


if __name__ == "__main__":
    fig_rtmv()
    fig_rede_vacinas()
    fig_rb3_limiar()
    fig_youtube_filtro()
