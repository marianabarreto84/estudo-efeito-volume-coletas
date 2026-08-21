"""
Teste de fumaca da credencial da TikTok Research API — o menor gasto de cota possivel.

Faz exatamente duas coisas:
  1. pede o token (nao consome cota de consulta);
  2. UMA consulta minima (1 dia, max_count baixo) so para provar que a chave
     tem acesso a Research API e ver o formato do retorno.

Nao grava nada. Nao pagina. Use antes de qualquer coleta de verdade.

Uso:  PYTHONIOENCODING=utf-8 python -u pipeline/testa_credencial.py
      python -u pipeline/testa_credencial.py --hashtag eleicoes2026 --regiao BR \
             --inicio 20260801 --fim 20260801
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.tiktok_api import TikTokAPI, MAX_COUNT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hashtag", default="brasil")
    ap.add_argument("--regiao", default="BR")
    ap.add_argument("--inicio", default="20260801")
    ap.add_argument("--fim", default="20260801")
    a = ap.parse_args()

    api = TikTokAPI()
    print("1) autenticando...")
    api.token()
    print("   OK — a credencial vale para client_credentials\n")

    print("2) uma consulta minima: #%s, regiao %s, %s..%s (max %d videos)"
          % (a.hashtag, a.regiao, a.inicio, a.fim, MAX_COUNT))
    try:
        lote = next(api.busca_videos(inicio=a.inicio, fim=a.fim,
                                     hashtags=[a.hashtag], regiao=a.regiao,
                                     max_paginas=1))
    except StopIteration:
        print("   consulta OK, mas 0 videos — a credencial funciona; o filtro e que "
              "nao casou (tente outra hashtag/data/regiao).")
        return 0

    print("   OK — %d videos no primeiro lote\n" % len(lote))
    print("3) exemplo de registro (campos disponiveis):")
    print(json.dumps(lote[0], ensure_ascii=False, indent=1)[:1200])
    print("\nchamadas de API gastas neste teste: %d" % api.chamadas)
    print("\nSe chegou ate aqui, a coleta local esta viavel. ⚠ Antes de coletar em "
          "escala, ver o aviso de COTA COMPARTILHADA em core/tiktok_api.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
