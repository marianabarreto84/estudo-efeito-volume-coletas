"""
Importa a credencial da TikTok Research API do coletor do eTC (vm031) para o
`.env` LOCAL da pasta da dissertacao.

Por que este script existe (e por que quem roda e a Mariana)
------------------------------------------------------------
A credencial esta **hardcoded** em `~/tweetcrawler/new-tiktok/main.py` na vm031
(linhas ~332-333), nao num `.env`. Ler segredo de maquina remota e uma acao que o
modo automatico do assistente bloqueia — corretamente. Entao o script existe
pronto, e **voce** o executa uma vez.

O valor **nao aparece no terminal**: e lido por SSH e gravado direto no arquivo.
A saida imprime so um resumo mascarado (4 primeiros caracteres + tamanho).

Requisitos: VPN Cloud-DI conectada (adaptador `OpenVPN TAP-Windows6` com IP 10.8.x)
e o `.env` do caso twitter-ituassu com SSH_USERNAME / VM_031_PASSWORD.

Uso:
    cd c:/Users/maria/Documents/dissertacao/casos/tiktok
    python pipeline/importa_credencial_etc.py

Depois:
    python pipeline/testa_credencial.py
"""
import os
import pathlib
import re

import paramiko

RAIZ = pathlib.Path(__file__).resolve().parents[3]        # .../dissertacao
ENV_LOCAL = RAIZ / ".env"
ENV_SSH = RAIZ / "casos" / "twitter-ituassu" / ".env"
VM031 = "10.50.0.32"
ARQ_REMOTO = "~/tweetcrawler/new-tiktok/main.py"


def carrega(env_path):
    for linha in env_path.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))


def main():
    carrega(ENV_SSH)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("conectando na vm031 (precisa da VPN de pe)...")
    c.connect(VM031, username=os.environ["SSH_USERNAME"],
              password=os.environ["VM_031_PASSWORD"], timeout=25)
    _, o, _ = c.exec_command("grep -nE \"client_key *=|client_secret *=\" %s | head -4"
                             % ARQ_REMOTO, timeout=120)
    trecho = o.read().decode(errors="replace")
    c.close()

    key = re.search(r"client_key\s*=\s*['\"]([^'\"]+)['\"]", trecho)
    sec = re.search(r"client_secret\s*=\s*['\"]([^'\"]+)['\"]", trecho)
    if not (key and sec):
        raise SystemExit("nao achei client_key/client_secret em %s\n"
                         "(o coletor pode ter mudado; confira a mao)" % ARQ_REMOTO)
    key, sec = key.group(1), sec.group(1)

    env = ENV_LOCAL.read_text(encoding="utf-8") if ENV_LOCAL.exists() else ""
    env = re.sub(r"^TIKTOK_(CLIENT_KEY|CLIENT_SECRET)=.*\n?", "", env, flags=re.M)
    if env and not env.endswith("\n"):
        env += "\n"
    env += ("# TikTok Research API v2 - credencial do app do eTC, importada de\n"
            "# vm031:~/tweetcrawler/new-tiktok/main.py. NUNCA versionar.\n"
            "# ATENCAO: a cota e do app, compartilhada com o coletor continuo do eTC.\n"
            "TIKTOK_CLIENT_KEY=%s\nTIKTOK_CLIENT_SECRET=%s\n" % (key, sec))
    ENV_LOCAL.write_text(env, encoding="utf-8")

    print("gravado em %s" % ENV_LOCAL)
    print("  TIKTOK_CLIENT_KEY    = %s... (%d chars)" % (key[:4], len(key)))
    print("  TIKTOK_CLIENT_SECRET = %s... (%d chars)" % (sec[:3], len(sec)))
    print("\nagora rode:  python pipeline/testa_credencial.py")


if __name__ == "__main__":
    main()
