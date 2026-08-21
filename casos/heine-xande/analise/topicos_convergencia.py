"""
Eixo A — curva de convergência de tópicos (replica os parâmetros exatos do Heine).

Fonte dos dados (uma das duas):
  - CSV do Heine com coluna `content_text` (ex.: 1st_turn_day.csv), ou
  - snapshot SQLite local (tabela tweets, coluna de texto configurável).

Ideia (ver EIXO_TOPICOS.md): treina um BERTopic no dataset completo (o dia 2/out),
depois mede o quanto a distribuição de tópicos de FRAÇÕES crescentes se aproxima da do
todo — ≥R réplicas bootstrap por fração. Sobrepõe o n=16.367 da fórmula de proporção do
Heine para mostrar onde a curva REALMENTE estabiliza (a tese: muito acima do n da fórmula).

Parâmetros do BERTopic copiados do repo do Heine (Maxteralex/representative-dataset-
problem, bertopic_use_case_1st_turn_day): embeddings paraphrase-multilingual-MiniLM-L12-v2;
UMAP n_neighbors=15, n_components=5, min_dist=0.0, cosine, random_state=42; HDBSCAN
min_cluster_size=15, euclidean, eom; CountVectorizer stopwords PT, min_df=2, ngram(1,2).

Usa CPU por padrão (umap-learn/hdbscan). Se houver GPU + cuML, é análogo ao do Heine.
Requer: pandas, sentence-transformers, bertopic, umap-learn, hdbscan, scikit-learn,
nltk (stopwords pt), numpy.

Uso:
  python analise/topicos_convergencia.py --csv 1st_turn_day.csv
  python analise/topicos_convergencia.py --sqlite data/repl/heine2022/snapshot_dia_2022-10-02.sqlite --texto-col texto
  (opcional) --fracoes 0.01,0.05,0.1,0.25,0.5,1.0 --replicas 30
"""
import argparse, sqlite3
from pathlib import Path

EMB_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # igual ao Heine
N_FORMULA_HEINE = 16367  # n da fórmula de proporção (99% conf., ±1%) p/ N=1.291.891


def carregar_textos(args):
    if args.csv:
        import pandas as pd
        df = pd.read_csv(args.csv)
        col = args.texto_col if args.texto_col in df.columns else "content_text"
        return [t for t in df[col].tolist() if isinstance(t, str) and t.strip()]
    con = sqlite3.connect(args.sqlite)
    cur = con.execute(f'SELECT "{args.texto_col}" FROM tweets WHERE "{args.texto_col}" IS NOT NULL;')
    txts = [r[0] for r in cur.fetchall() if r[0] and str(r[0]).strip()]
    con.close()
    return txts


def build_bertopic(embedding_model):
    """BERTopic com os mesmos hiperparâmetros do Heine (CPU: umap-learn + hdbscan)."""
    from bertopic import BERTopic
    from umap import UMAP
    from hdbscan import HDBSCAN
    from sklearn.feature_extraction.text import CountVectorizer
    import nltk
    try:
        stop = nltk.corpus.stopwords.words("portuguese")
    except LookupError:
        nltk.download("stopwords"); stop = nltk.corpus.stopwords.words("portuguese")
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42)
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric="euclidean",
                            cluster_selection_method="eom", prediction_data=True)
    vectorizer = CountVectorizer(stop_words=stop, min_df=2, ngram_range=(1, 2))
    return BERTopic(embedding_model=embedding_model, umap_model=umap_model,
                    hdbscan_model=hdbscan_model, vectorizer_model=vectorizer,
                    calculate_probabilities=False, verbose=False)


def js_divergence(p, q):
    import numpy as np
    p = np.asarray(p, float); q = np.asarray(q, float)
    p = p / p.sum() if p.sum() else p; q = q / q.sum() if q.sum() else q
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = a > 0
        return float((a[mask] * np.log2(a[mask] / b[mask])).sum())
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def dist_topicos(topics, n_topicos):
    import numpy as np
    v = np.zeros(n_topicos + 2)  # +1 outliers(-1), +1 folga
    for t in topics:
        v[t + 1] += 1
    return v


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--csv", help="CSV do Heine (coluna content_text)")
    g.add_argument("--sqlite", help="snapshot SQLite (tabela tweets)")
    ap.add_argument("--texto-col", default="content_text")
    ap.add_argument("--fracoes", default="0.01,0.05,0.1,0.25,0.5,1.0")
    ap.add_argument("--replicas", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    import numpy as np
    from sentence_transformers import SentenceTransformer

    textos = carregar_textos(args)
    N = len(textos)
    print(f"[dados] {N:,} textos")
    print(f"[nota] n da fórmula do Heine = {N_FORMULA_HEINE:,} ({100*N_FORMULA_HEINE/max(N,1):.2f}% de N)")

    print(f"[emb] {EMB_MODEL} ...")
    emb_model = SentenceTransformer(EMB_MODEL)
    emb = emb_model.encode(textos, show_progress_bar=True, batch_size=256)

    print("[todo] BERTopic no dataset completo (referência)...")
    modelo = build_bertopic(emb_model)
    topics_todo, _ = modelo.fit_transform(textos, embeddings=emb)
    n_top = max(topics_todo) if topics_todo else 0
    dist_ref = dist_topicos(topics_todo, n_top)
    print(f"[todo] {n_top+1} tópicos (+outliers).")

    rng = np.random.default_rng(args.seed)
    fracoes = [float(x) for x in args.fracoes.split(",")]
    linhas = ["# Curva de convergência de tópicos (caso Heine 2022)\n",
              f"N={N:,} · modelo={EMB_MODEL} · réplicas={args.replicas}",
              f"n_fórmula_Heine={N_FORMULA_HEINE:,} ({100*N_FORMULA_HEINE/max(N,1):.2f}% de N)\n",
              "| fração | n | JS média (frac × todo) | JS desvio |", "|---|--:|--:|--:|"]
    for f in fracoes:
        n = max(1, int(round(f * N))); js_vals = []
        for _ in range(args.replicas if f < 1.0 else 1):
            idx = rng.choice(N, size=n, replace=False)
            topics_frac = modelo.transform([textos[i] for i in idx], embeddings=emb[idx])[0]
            js_vals.append(js_divergence(dist_topicos(topics_frac, n_top), dist_ref))
        media, desvio = float(np.mean(js_vals)), float(np.std(js_vals))
        marca = "  <-- ~n da fórmula" if abs(n - N_FORMULA_HEINE) / N_FORMULA_HEINE < 0.25 else ""
        print(f"  fração={f:<5} n={n:>9,}  JS={media:.4f} ±{desvio:.4f}{marca}")
        linhas.append(f"| {f} | {n:,} | {media:.4f} | {desvio:.4f} |")

    out = Path("data/repl/heine2022/RESULTADOS_topicos_convergencia.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\n[ok] -> {out}")
    print("[leitura] JS↓ conforme fração↑; a tese é que na fração ~n_fórmula o JS ainda é")
    print("          ALTO, achatando só muito acima — a fórmula de proporção é inadequada p/ tópicos.")


if __name__ == "__main__":
    main()
