"""
MH1 — reproducao do PONTO ORIGINAL do Massachs et al. (2020), sobre o gabarito
publicado pelos proprios autores (`reddit-politics-12-16`, 44.924 usuarios).

A afirmacao testada
-------------------
MH1 e uma ORDENACAO entre tres familias de features de 2012, prevendo quem
participa de r/The_Donald em 2016:

    participacao (homofilia) F1 34,8%  ~=  scores (feedback) 33,7%  >>
    interacoes (influencia direta) 26,7%        [baseline aleatorio 15,2%]

Metodo do artigo (§4-5) e o que fazemos aqui
--------------------------------------------
  - regressao logistica, 5-fold CV, F1 da classe positiva;
  - remocao de features esparsas (<500 usuarios), como o artigo declara;
  - o artigo tambem cita Pearson p<0,05 e VIF; NAO reproduzimos essa parte
    (nao ha limiar publicado para o VIF) — logo o nosso F1 e o do MESMO modelo
    com MENOS selecao. Divergencia declarada, direcao desconhecida.
  - `class_weight='balanced'`: o artigo reporta precisao 0,27 e recall 0,56 no
    melhor modelo, perfil que so sai com rebalanceamento. Rodamos as DUAS
    variantes e reportamos as duas.

Por que isto importa para a dissertacao
---------------------------------------
E a Fase 2 do caso: fixa o ponto de partida ANTES da expansao. Se a ordenacao
nao reproduz aqui, nao ha o que expandir — e isso seria, ele mesmo, um achado
sobre reprodutibilidade. A Fase 3 (baixar dumps 2012/2016 e refazer o focus
group com limiar de atividade menor) so faz sentido depois deste numero.

Uso: PYTHONIOENCODING=utf-8 python -u analise/mh1_ponto_original.py
Saida: stdout + data/repl/massachs2016/mh1_ponto_original.json
"""
import json
import pathlib
import sys
import time
import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

warnings.filterwarnings("ignore")

D = pathlib.Path("data/repl/massachs2016")
CSV = D / "reddit-politics-12-16.csv.bz2"
OUT = D / "mh1_ponto_original.json"

MIN_USUARIOS = 500      # o artigo remove features presentes em <500 usuarios
N_FOLDS = 5
SEED = 20260818

# familias de features, na nomenclatura do README dos autores
FAMILIAS = {
    "participacao (homofilia)": ["participation_12"],
    "scores (feedback social)": ["pos_scores_12", "neg_scores_12"],
    "interacoes (influencia)": ["dist_int_12", "pos_int_12", "num_int_12"],
    "participacao + scores": ["participation_12", "pos_scores_12", "neg_scores_12"],
    "TODAS": ["participation_12", "pos_scores_12", "neg_scores_12",
              "dist_int_12", "pos_int_12", "num_int_12"],
}

# numeros publicados (Tab. 1-2 do artigo), para comparacao lado a lado
ALVO_F1 = {
    "participacao (homofilia)": 34.8,
    "scores (feedback social)": 33.7,
    "interacoes (influencia)": 26.7,
    "participacao + scores": 35.3,
}


def log(m):
    print(m, flush=True)


def avalia(X, y, balanced):
    """5-fold CV; devolve medias de F1/AUC/precisao/recall da classe positiva."""
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    f1s, aucs, precs, recs = [], [], [], []
    for tr, te in skf.split(X, y):
        clf = make_pipeline(
            StandardScaler(with_mean=False),
            LogisticRegression(max_iter=2000, solver="liblinear",
                               class_weight="balanced" if balanced else None))
        clf.fit(X[tr], y[tr])
        p = clf.predict(X[te])
        f1s.append(f1_score(y[te], p))
        precs.append(precision_score(y[te], p, zero_division=0))
        recs.append(recall_score(y[te], p))
        aucs.append(roc_auc_score(y[te], clf.predict_proba(X[te])[:, 1]))
    return (float(np.mean(f1s)), float(np.std(f1s)), float(np.mean(aucs)),
            float(np.mean(precs)), float(np.mean(recs)))


def main():
    t = time.time()
    log("lendo %s ..." % CSV)
    df = pd.read_csv(CSV, header=[0, 1], index_col=0)
    log("  %d usuarios x %d colunas (%.0fs)" % (df.shape[0], df.shape[1], time.time() - t))

    y = df[("y", "The_Donald")].astype(int).values
    log("  apoiadores de Trump: %d (%.2f%%)" % (y.sum(), 100 * y.mean()))

    # baseline aleatorio: predizer positivo com prob = taxa base
    rng = np.random.default_rng(SEED)
    base = float(np.mean([f1_score(y, rng.random(len(y)) < y.mean()) for _ in range(20)]))
    log("  baseline aleatorio F1 = %.1f%% (artigo: 15,2%%)" % (100 * base))

    resultados = {}
    for nome, prefixos in FAMILIAS.items():
        cols = [c for c in df.columns if c[0] in prefixos]
        sub = df[cols].fillna(0)
        # remocao de esparsas: feature com <500 usuarios com valor != 0
        nz = (sub != 0).sum(axis=0)
        mantidas = nz[nz >= MIN_USUARIOS].index
        X = sub[mantidas].values.astype(np.float32)
        log("\n%s" % nome)
        log("  features: %d -> %d apos corte de esparsidade (<%d usuarios)"
            % (len(cols), X.shape[1], MIN_USUARIOS))
        if X.shape[1] == 0:
            log("  (sem features) pulando")
            continue
        linha = {"n_features_bruto": len(cols), "n_features": int(X.shape[1])}
        for bal in (True, False):
            f1, sd, auc, prec, rec = avalia(X, y, bal)
            tag = "balanced" if bal else "sem peso"
            log("  [%-8s] F1 %.1f%% (+-%.1f)  AUC %.3f  prec %.2f  rec %.2f"
                % (tag, 100 * f1, 100 * sd, auc, prec, rec))
            linha[tag] = {"f1": round(100 * f1, 2), "f1_dp": round(100 * sd, 2),
                          "auc": round(auc, 4), "precisao": round(prec, 4),
                          "recall": round(rec, 4)}
        if nome in ALVO_F1:
            alvo = ALVO_F1[nome]
            melhor = max(linha["balanced"]["f1"], linha["sem peso"]["f1"])
            linha["f1_artigo"] = alvo
            linha["delta_pp"] = round(melhor - alvo, 2)
            log("  artigo: %.1f%%  ->  delta %+.1f p.p." % (alvo, melhor - alvo))
        resultados[nome] = linha

    # o teste de MH1 e a ORDENACAO, nao os valores
    def melhor_f1(k):
        return max(resultados[k]["balanced"]["f1"], resultados[k]["sem peso"]["f1"])

    ordem = sorted([k for k in ALVO_F1 if k in resultados], key=melhor_f1, reverse=True)
    log("\n=== ordenacao reproduzida ===")
    for i, k in enumerate(ordem, 1):
        log("  %d. %-28s F1 %.1f%%   (artigo %.1f%%)" % (i, k, melhor_f1(k), ALVO_F1[k]))

    homo, infl = "participacao (homofilia)", "interacoes (influencia)"
    mh1_ok = melhor_f1(homo) > melhor_f1(infl)
    log("\nMH1 (homofilia >> influencia): %s  [%.1f%% x %.1f%%]"
        % ("REPRODUZ" if mh1_ok else "NAO REPRODUZ", melhor_f1(homo), melhor_f1(infl)))

    OUT.write_text(json.dumps(
        {"fonte": str(CSV), "n_usuarios": int(df.shape[0]),
         "taxa_positiva": round(float(y.mean()), 4),
         "baseline_aleatorio_f1": round(100 * base, 2),
         "min_usuarios_feature": MIN_USUARIOS, "n_folds": N_FOLDS, "seed": SEED,
         "resultados": resultados, "ordenacao": ordem, "mh1_reproduz": bool(mh1_ok)},
        ensure_ascii=False, indent=1), encoding="utf-8")
    log("\nescrito em %s  (%.0fs no total)" % (OUT, time.time() - t))


if __name__ == "__main__":
    sys.exit(main())
