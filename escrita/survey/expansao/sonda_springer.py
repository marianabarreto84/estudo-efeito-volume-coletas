# =====================================================================
#  Sonda do estrato comercial — Springer, humano no laco.
#
#  POR QUE HUMANO NO LACO: a Springer serve um desafio anti-automacao no
#  endpoint do PDF (HTTP 200 + 3 KB de "Client Challenge"). O controle
#  existe para verificar que ha um humano presente. Se a Mariana esta de
#  fato presente, no navegador dela, com o acesso institucional dela, o
#  controle esta sendo SATISFEITO -- nao contornado. E por isso que este
#  script nao faz requisicao nenhuma as editoras: ele prepara a fila,
#  abre as abas e depois recolhe o que o navegador baixou.
#
#  O que ele faz            | O que a Mariana faz
#  -------------------------|-------------------------------------------
#  sorteia a amostra        | configura o PAC da DBD no navegador
#  monta as URLs do PDF     | clica/salva (o navegador passa o desafio)
#  casa arquivo <-> DOI     |
#  copia para pdfs/         |
#  mede o progresso         |
#
#  NAO escreve no research.db. Os PDFs vao para pdfs/ com o nome derivado
#  do DOI, e o `reconcilia_pdfs.py --aplicar` leva ao banco depois.
#
#  Uso:
#    python sonda_springer.py --sortear 200      # 1x: congela a amostra
#    python sonda_springer.py --lote 20 --abrir  # abre 20 abas
#    python sonda_springer.py --conferir         # recolhe do Downloads
#    python sonda_springer.py --estado
# =====================================================================
import argparse
import json
import os
import random
import re
import shutil
import sqlite3
import sys
import webbrowser
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\maria\Documents\GitHub\redes-sociais-digitais-survey"
DB = os.path.join(REPO, "research.db")
PDF_DIR = os.path.join(REPO, "pdfs")
DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
ESTADO = os.path.join(AQUI, "sonda_springer.json")
PREFIXO = "10.1007"
URL_PDF = "https://link.springer.com/content/pdf/{doi}.pdf"


def nome_de(doi):
    """Nome do arquivo no pdfs/, mesma convencao do services/pdf_fetcher.py."""
    return doi.replace("/", "_").replace(":", "_") + ".pdf"


def sufixo(doi):
    """Parte do DOI depois do prefixo — e o nome com que o navegador salva."""
    return doi.split("/", 1)[1]


def fila_completa():
    con = sqlite3.connect(DB)
    out = []
    for aid, doi in con.execute(
        "select id, doi from articles "
        "where (pdf_path is null or trim(pdf_path)='') "
        "and doi is not null and lower(doi) like ?||'%' order by id",
        (PREFIXO,),
    ):
        if os.path.isfile(os.path.join(PDF_DIR, nome_de(doi))):
            continue
        out.append({"id": aid, "doi": doi})
    con.close()
    return out


def carrega():
    if not os.path.isfile(ESTADO):
        sys.exit("Amostra ainda nao sorteada. Rode: python sonda_springer.py --sortear 200")
    with open(ESTADO, encoding="utf-8") as f:
        return json.load(f)


def grava(d):
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def ja_tem(doi):
    return os.path.isfile(os.path.join(PDF_DIR, nome_de(doi)))


def cmd_sortear(n, semente):
    if os.path.isfile(ESTADO):
        sys.exit(f"ERRO: {ESTADO} ja existe. A amostra e congelada de proposito — "
                 "re-sortear depois de ver resultados invalida o desenho. "
                 "Apague o arquivo a mao se a intencao for mesmo recomecar.")
    pop = fila_completa()
    if n >= len(pop):
        amostra, modo = pop, "censo"
    else:
        amostra = random.Random(semente).sample(pop, n)
        modo = "amostra"
    amostra.sort(key=lambda a: a["id"])
    grava({
        "congelado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "modo": modo,
        "semente": semente,
        "n_alvo": n,
        "populacao": len(pop),
        "itens": amostra,
        "poder_declarado": (
            "n=200 detecta diferenca de ~15 p.p. entre estratos (z, alfa=.05, poder 80%). "
            "NAO detecta os 2-6 p.p. que a aposta A4 do PRE_REGISTRO preve: isso exigiria "
            "n~1500. A sonda responde 'o estrato comercial e categoricamente diferente?', "
            "nao 'de quanto ele difere'."
        ),
    })
    print(f"populacao Springer sem PDF ... {len(pop)}")
    print(f"{modo} congelada ............... {len(amostra)} (semente {semente})")
    print(f"gravado em {ESTADO}")


def eh_lncs(doi):
    """Capitulo de livro / anais LNCS (DOI com ISBN) vs artigo de periodico."""
    return "978-" in doi


def cmd_diagnostico():
    """Lote misto para decidir o desenho: a assinatura cobre LNCS ou so periodico?

    Existe porque 75% da amostra e LNCS, e anais LNCS costumam ser compra
    separada da assinatura de periodicos. Se nao houver acesso a eles, a sonda
    de n=200 vira n~50 efetivo, e o desenho tem de mudar ANTES de gastar 1 h.
    """
    d = carrega()
    pend = [a for a in d["itens"] if not ja_tem(a["doi"]) and a["doi"] not in d.get("sem_acesso", [])]
    lncs = [a for a in pend if eh_lncs(a["doi"])][:5]
    per = [a for a in pend if not eh_lncs(a["doi"])][:3]
    print("DIAGNOSTICO — rode DEPOIS de o PAC da DBD estar ativo no navegador.\n")
    print("  ⚠ NAO e 'Log in via an institution' no site da Springer. O acesso e por")
    print("    IP: o PAC (dbd.puc-rio.br/proxy.pac) roteia link.springer.com pelo")
    print("    gateway 139.82.115.33:16000, e a Springer reconhece o IP da PUC-Rio.")
    print("    Se a pagina mostrar 'Log in', o proxy NAO esta ativo naquela aba.\n")
    print("A pergunta: a assinatura da PUC-Rio cobre anais LNCS, ou so periodicos?\n")
    print(f"--- {len(lncs)} capitulos/LNCS (o tipo que e 75% da amostra) ---")
    for a in lncs:
        print(URL_PDF.format(doi=a["doi"]))
    print(f"\n--- {len(per)} periodicos (controle: estes devem funcionar) ---")
    for a in per:
        print(URL_PDF.format(doi=a["doi"]))
    print("\nDepois: python sonda_springer.py --conferir")
    print("Leitura do resultado:")
    print("  LNCS baixa      -> segue a sonda de 200 como esta")
    print("  LNCS nao baixa  -> a sonda tem de ser redesenhada so com periodicos")
    print("                     (a populacao tem 521 deles); me avise antes de clicar 200x")


def cmd_redesenhar(n, semente):
    """Restringe a sonda a PERIODICOS, preservando o trabalho ja feito.

    POR QUE: medido em 9/set/2026, a assinatura da PUC-Rio cobre periodicos
    Springer e NAO cobre anais LNCS -- 3/3 periodicos baixaram, 0/5 LNCS.
    A amostra original era 75% LNCS, entao teria n~50 efetivo.

    O DESENHO CONTINUA VALIDO: o sorteio original foi uma amostra aleatoria
    simples (AAS) de 2.013; o subconjunto de periodicos dela e, portanto, uma
    AAS dos 521 periodicos da populacao. Completar essa parte com um sorteio
    aleatorio entre os 471 restantes produz exatamente uma AAS de tamanho n
    dos 521 -- sortear em duas etapas sem reposicao equivale a sortear de uma
    vez. Nada do que a Mariana ja baixou e descartado.
    """
    d = carrega()
    antigos = [a for a in d["itens"] if not eh_lncs(a["doi"])]
    pop = [a for a in fila_completa() if not eh_lncs(a["doi"])]
    # a populacao de periodicos inclui os ja baixados; recompoe pelo id
    ids_pop = {a["id"] for a in pop} | {a["id"] for a in antigos}
    todos = {a["id"]: a for a in pop}
    for a in antigos:
        todos.setdefault(a["id"], a)
    universo = [todos[i] for i in sorted(ids_pop)]

    ja = {a["id"] for a in antigos}
    resto = [a for a in universo if a["id"] not in ja]
    falta = max(0, n - len(antigos))
    extra = random.Random(semente).sample(resto, min(falta, len(resto)))
    novos = sorted(antigos + extra, key=lambda a: a["id"])

    hist = d.get("historico", [])
    hist.append({
        "em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "o_que": "restricao a periodicos",
        "motivo": ("assinatura PUC-Rio nao cobre anais LNCS: no diagnostico de "
                   "9/set/2026, 3/3 periodicos baixaram e 0/5 LNCS. A amostra "
                   "original (150 LNCS + 50 periodicos) teria n~50 efetivo."),
        "amostra_anterior": {"n": len(d["itens"]), "lncs": len(d["itens"]) - len(antigos),
                             "periodico": len(antigos)},
        "preservados": len(antigos),
        "sorteados_agora": len(extra),
        "semente_complemento": semente,
    })
    d.update({
        "modo": "amostra (periodicos Springer)",
        "populacao": len(universo),
        "n_alvo": len(novos),
        "itens": novos,
        "historico": hist,
        "poder_declarado": (
            f"n={len(novos)} de uma populacao de {len(universo)} periodicos Springer sem PDF. "
            f"Com correcao de populacao finita, margem ~±4,4 p.p. numa proporcao de 20%. "
            "ESCOPO: a sonda mede o estrato comercial DE PERIODICO Springer -- nao o estrato "
            "comercial inteiro. Anais LNCS ficam fora por nao serem assinados, e isso e "
            "resultado a reportar, nao ruido."
        ),
    })
    grava(d)
    print(f"populacao de periodicos ... {len(universo)}")
    print(f"preservados do sorteio antigo {len(antigos)}  (nada do que ja baixou se perde)")
    print(f"sorteados agora ........... {len(extra)}  (semente {semente})")
    print(f"amostra final ............. {len(novos)}")
    tem = sum(1 for a in novos if ja_tem(a["doi"]))
    print(f"ja em disco ............... {tem}  -> faltam {len(novos)-tem} cliques")


def cmd_sem_acesso(dois):
    """Registra DOIs sem acesso mesmo autenticada (nao assinados).

    Sem isto o --lote devolveria eternamente os mesmos artigos, e o
    denominador da sonda ficaria desonesto: 'nao baixado' misturaria
    'ainda nao tentei' com 'a instituicao nao assina'.
    """
    d = carrega()
    sa = set(d.get("sem_acesso", []))
    conhecidos = {a["doi"] for a in d["itens"]}
    novos, fora = [], []
    for x in dois:
        x = x.strip()
        # aceita DOI puro ou a URL do PDF
        m = re.search(r"(10\.1007/\S+?)(?:\.pdf)?$", x)
        doi = m.group(1) if m else x
        (novos if doi in conhecidos else fora).append(doi)
    sa.update(novos)
    d["sem_acesso"] = sorted(sa)
    grava(d)
    print(f"marcados sem acesso: {len(novos)} (total acumulado: {len(sa)})")
    if fora:
        print(f"⚠ ignorados por nao estarem na amostra: {', '.join(fora[:5])}")


def cmd_lote(k, abrir):
    d = carrega()
    sa = set(d.get("sem_acesso", []))
    pend = [a for a in d["itens"] if not ja_tem(a["doi"]) and a["doi"] not in sa]
    print(f"pendentes: {len(pend)} de {len(d['itens'])}"
          + (f"  (excluidos {len(sa)} sem acesso)" if sa else ""))
    if not pend:
        print("nada a fazer — tudo baixado.")
        return
    lote = pend[:k]
    print(f"\nlote de {len(lote)}:\n")
    for a in lote:
        print(URL_PDF.format(doi=a["doi"]))
    if abrir:
        print(f"\nabrindo {len(lote)} abas...")
        for a in lote:
            webbrowser.open_new_tab(URL_PDF.format(doi=a["doi"]))
        print("quando terminarem de baixar: python sonda_springer.py --conferir")
    else:
        print("\n(use --abrir para abrir no navegador)")


def cmd_conferir(pasta):
    d = carrega()
    por_sufixo = {sufixo(a["doi"]).lower(): a["doi"] for a in d["itens"]}
    if not os.path.isdir(pasta):
        sys.exit(f"pasta nao encontrada: {pasta}")

    achados, lixo, ja = 0, [], 0
    for f in os.listdir(pasta):
        if not f.lower().endswith(".pdf"):
            continue
        # o navegador desambigua duplicatas com " (1)"; o stem e o sufixo do DOI
        stem = re.sub(r"\s*\(\d+\)$", "", f[:-4]).strip().lower()
        doi = por_sufixo.get(stem)
        if not doi:
            continue
        origem = os.path.join(pasta, f)
        if ja_tem(doi):
            ja += 1
            continue
        with open(origem, "rb") as fh:
            cab = fh.read(4)
        if cab != b"%PDF" or os.path.getsize(origem) < 1024:
            lixo.append(f)      # pagina de desafio salva como .pdf, ou truncado
            continue
        shutil.copy2(origem, os.path.join(PDF_DIR, nome_de(doi)))
        achados += 1

    total = len(d["itens"])
    tem = sum(1 for a in d["itens"] if ja_tem(a["doi"]))
    print(f"copiados agora ............ {achados}")
    if ja:
        print(f"ja estavam em pdfs/ ....... {ja}")
    if lixo:
        print(f"⚠ descartados (nao sao PDF) {len(lixo)}: {', '.join(lixo[:5])}")
        print("  isso costuma ser a pagina de desafio salva como .pdf — reabra esses.")
    print(f"\nprogresso da sonda ........ {tem}/{total} ({100*tem/total:.0f}%)")
    if tem == total:
        print("\nsonda completa. Para levar ao banco:")
        print("    python reconcilia_pdfs.py --aplicar")


def cmd_limpar(pasta, aplicar):
    """Apaga do Downloads o que ja esta salvo em pdfs/, e so isso.

    Regra unica e conservadora: so apaga arquivo cujo conteudo e IDENTICO
    (md5) ao que ja esta em pdfs/. Qualquer duvida -- nao copiado ainda,
    conteudo diferente, alheio a sonda -- fica. Abrir mao de espaco e
    barato; apagar um download que nao foi preservado, nao.

    Existe porque `--lote --abrir` reabre os mesmos pendentes se rodado sem
    `--conferir` no meio, e o navegador acumula "(1)", "(2)", "(3)"...
    """
    import hashlib

    def md5(p):
        h = hashlib.md5()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()

    d = carrega()
    por_suf = {sufixo(a["doi"]).lower(): a["doi"] for a in d["itens"]}
    for extra in ("sonda_springer_v1_lncs.json",):
        p = os.path.join(AQUI, extra)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                for a in json.load(f)["itens"]:
                    por_suf.setdefault(sufixo(a["doi"]).lower(), a["doi"])

    apagar, manter, alheios = [], [], 0
    for f in sorted(os.listdir(pasta)):
        if not f.lower().endswith(".pdf"):
            continue
        stem = re.sub(r"\s*\(\d+\)$", "", f[:-4]).strip().lower()
        doi = por_suf.get(stem)
        if not doi:
            alheios += 1
            continue
        origem = os.path.join(pasta, f)
        dest = os.path.join(PDF_DIR, nome_de(doi))
        if not os.path.isfile(dest):
            manter.append((f, "ainda nao esta em pdfs/ — rode --conferir antes"))
        elif md5(origem) != md5(dest):
            manter.append((f, "conteudo difere do preservado"))
        else:
            apagar.append((f, os.path.getsize(origem)))

    mb = sum(t for _, t in apagar) / 1048576
    print(f"identicos ao preservado (apagaveis) . {len(apagar)}  ({mb:.1f} MB)")
    print(f"da sonda, mas NAO apagaveis .......... {len(manter)}")
    for f, m in manter:
        print(f"     {f}  -> {m}")
    print(f"alheios a sonda, intocados ........... {alheios}")

    if not aplicar:
        print("\n(simulacao; nada foi apagado. Rode com --aplicar para valer)")
        return
    n = 0
    for f, _ in apagar:
        os.remove(os.path.join(pasta, f))
        n += 1
    print(f"\napagados {n} arquivos de {pasta} ({mb:.1f} MB liberados).")


def cmd_estado():
    d = carrega()
    itens = d["itens"]
    sa = set(d.get("sem_acesso", []))
    tem = [a for a in itens if ja_tem(a["doi"])]
    n = len(itens)
    print(f"congelado em .. {d['congelado_em']}  ({d['modo']}, semente {d['semente']})")
    print(f"populacao ..... {d['populacao']}")
    print(f"baixados ...... {len(tem)}/{n} ({100*len(tem)/n:.0f}%)")
    if sa:
        print(f"sem acesso .... {len(sa)}  (nao assinados; saem do denominador util)")
    falta = n - len(tem) - len(sa)
    print(f"faltam ........ {falta}")

    def quebra(rot, sel):
        c = sum(1 for a in sel if eh_lncs(a["doi"]))
        print(f"  {rot:14s} LNCS {c:4d} | periodico {len(sel)-c:4d}")
    print("\ncomposicao:")
    quebra("amostra", itens)
    quebra("baixados", tem)
    print(f"\npoder: {d['poder_declarado']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortear", type=int, metavar="N", help="congela a amostra (rodar 1x)")
    ap.add_argument("--semente", type=int, default=20260929, help="semente do sorteio (default: %(default)s)")
    ap.add_argument("--lote", type=int, metavar="K", help="mostra as proximas K URLs")
    ap.add_argument("--abrir", action="store_true", help="abre o lote em abas do navegador")
    ap.add_argument("--conferir", action="store_true", help="recolhe os PDFs baixados")
    ap.add_argument("--pasta", default=DOWNLOADS, help="pasta de downloads (default: %(default)s)")
    ap.add_argument("--estado", action="store_true", help="progresso da sonda")
    ap.add_argument("--diagnostico", action="store_true",
                    help="lote misto LNCS+periodico para testar a cobertura da assinatura")
    ap.add_argument("--sem-acesso", nargs="+", metavar="DOI", dest="sem_acesso",
                    help="marca DOIs (ou URLs) sem acesso mesmo autenticada")
    ap.add_argument("--redesenhar-periodicos", type=int, metavar="N", dest="redesenhar",
                    help="restringe a sonda a periodicos, preservando o ja baixado")
    ap.add_argument("--limpar-downloads", action="store_true", dest="limpar",
                    help="apaga do Downloads so o que ja esta salvo em pdfs/ (simula por padrao)")
    ap.add_argument("--aplicar", action="store_true", help="com --limpar-downloads: apaga de verdade")
    a = ap.parse_args()

    if a.sortear:
        cmd_sortear(a.sortear, a.semente)
    elif a.diagnostico:
        cmd_diagnostico()
    elif a.sem_acesso:
        cmd_sem_acesso(a.sem_acesso)
    elif a.redesenhar:
        cmd_redesenhar(a.redesenhar, a.semente + 1)
    elif a.limpar:
        cmd_limpar(a.pasta, a.aplicar)
    elif a.lote:
        cmd_lote(a.lote, a.abrir)
    elif a.conferir:
        cmd_conferir(a.pasta)
    elif a.estado:
        cmd_estado()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
