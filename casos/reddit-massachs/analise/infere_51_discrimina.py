"""
Engenharia reversa da lista dos 51 — usando quem esta DENTRO e quem esta FORA do grupo.

Regra do artigo: membro <=> >=10 comentarios em 2012 E >=10 em 2016, somados na lista S.
Temos contagens por subreddit para:
  P = amostra sorteada do grupo publicado (contagem_por_usuario.jsonl)
  N = amostra de quem comentou em r/politics em 2012 e NAO esta no grupo
      (contagem_fora_do_grupo.jsonl)
Para uma lista candidata S, contamos:
  perde  = membros de P que a regra com S deixaria de fora (deveria ser 0)
  sobra  = nao-membros de N que a regra com S poria dentro (deveria ser 0)
So os nao-membros ATIVOS em 2016 informam alguma coisa: quem sumiu em 2016 fica fora
com qualquer S.

Passos
1. S = os 34 nomes conhecidos.
2. Cada um dos 34 retirado por vez: quanto muda "sobra" e "perde".
3. Busca gulosa a partir de {politics}: acrescenta o subreddit que mais melhora
   (acertos = membros dentro + nao-membros fora), ate 60 subreddits, e registra a trajetoria.

Uso: PYTHONIOENCODING=utf-8 python -u analise/infere_51_discrimina.py
"""
import collections
import json
import pathlib

D = pathlib.Path("data/repl/massachs2016")
LIMIAR = 10

import importlib.util
_spec = importlib.util.spec_from_file_location("i51", pathlib.Path(__file__).with_name("infere_51.py"))
_i51 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_i51)
CONHECIDOS = _i51.CONHECIDOS


def carrega(nome):
    regs = [json.loads(l) for l in (D / nome).read_text(encoding="utf-8").splitlines()]
    return [r for r in regs if r.get("2012") is not None and r.get("2016") is not None]


def dentro(r, S):
    return all(sum(r[a].get(s, 0) for s in S) >= LIMIAR for a in ("2012", "2016"))


def placar(P, N, S):
    perde = sum(1 for r in P if not dentro(r, S))
    sobra = sum(1 for r in N if dentro(r, S))
    return perde, sobra


def main():
    P = carrega("contagem_por_usuario.jsonl")
    N_todos = carrega("contagem_fora_do_grupo.jsonl")
    ativo16 = [r for r in N_todos if sum(r["2016"].values()) >= LIMIAR]
    print(f"dentro do grupo: {len(P)}; fora do grupo: {len(N_todos)}, "
          f"dos quais ativos (>=10) em 2016 no Reddit todo: {len(ativo16)}")
    N = ativo16

    out = {"n_P": len(P), "n_N": len(N_todos), "n_N_ativos_2016": len(N)}

    perde, sobra = placar(P, N, CONHECIDOS)
    print(f"\n1) S = 34 conhecidos: perde {perde}/{len(P)} membros; "
          f"poe dentro {sobra}/{len(N)} nao-membros ativos")
    out["34"] = {"perde": perde, "sobra": sobra}

    print("\n2) retirando um dos 34 por vez (so os que mudam algo):")
    efeito = []
    for s in CONHECIDOS:
        S = [x for x in CONHECIDOS if x != s]
        p, n = placar(P, N, S)
        if (p, n) != (perde, sobra):
            efeito.append((s, p, n))
            print(f"   sem {s:22s} perde {p:3d}  sobra {n:3d}")
    out["retirando_um"] = efeito

    print("\n3) busca gulosa a partir de {politics}:")
    freq = collections.Counter(s for r in P for a in ("2012", "2016") for s in r[a])
    cands = [s for s, c in freq.items() if c >= 5]
    S = ["politics"]
    traj = []
    for _ in range(60):
        base = placar(P, N, S)
        melhor, mel = None, base
        for s in cands:
            if s in S:
                continue
            p, n = placar(P, N, S + [s])
            if (p + n) < (mel[0] + mel[1]):
                melhor, mel = s, (p, n)
        if melhor is None:
            break
        S.append(melhor)
        tag = "(conhecido)" if melhor in CONHECIDOS else ""
        traj.append((melhor, mel[0], mel[1]))
        print(f"   + {melhor:24s} perde {mel[0]:3d}  sobra {mel[1]:3d} {tag}")
    out["guloso"] = traj
    no34 = [s for s in S if s in CONHECIDOS]
    print(f"\n   lista gulosa: {len(S)} subreddits, {len(no34)} deles entre os 34 conhecidos")
    (D / "infere_51_discrimina.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")


if __name__ == "__main__":
    main()
