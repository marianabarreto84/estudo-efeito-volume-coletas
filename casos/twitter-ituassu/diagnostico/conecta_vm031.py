"""
Conecta ao PostgreSQL da vm031 (PUC-Rio Cloud-DI) atraves de um tunel SSH.

Requer a VPN da Cloud-DI conectada (OpenVPN) antes de rodar.
Fluxo: SSH cloud-di@vm031 (10.50.0.32) -> tunela localhost:5432 da VM
       -> psycopg2 conecta em 127.0.0.1:<porta_local>.

Todas as credenciais vem do arquivo .env (nenhum segredo no codigo).
"""
import os
from pathlib import Path

# Shim: paramiko >=3.x removeu DSSKey usado pelo sshtunnel na init.
import paramiko
if not hasattr(paramiko, "DSSKey"):
    paramiko.DSSKey = paramiko.RSAKey
from sshtunnel import SSHTunnelForwarder
import psycopg2


def carregar_env(caminho=".env"):
    """Le um .env simples (CHAVE=valor) para os.environ, sem dependencias."""
    p = Path(__file__).resolve().parents[1] / caminho
    if not p.exists():
        return
    for linha in p.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


def obrigatorio(nome):
    v = os.getenv(nome)
    if not v:
        raise SystemExit(f"[erro] variavel {nome} ausente no .env")
    return v


# ---- Constantes de rede (nao sao segredo) ----
SSH_HOST = "10.50.0.32"          # vm031.cloud.inf.puc-rio.br
SSH_PORT = 22
PG_HOST_REMOTO = "127.0.0.1"     # postgres visto de dentro da VM
PG_PORT_REMOTO = 5432
LOCAL_BIND_PORT = 5433           # porta local do tunel


def main():
    carregar_env()
    ssh_user = obrigatorio("SSH_USERNAME")
    ssh_pass = obrigatorio("VM_031_PASSWORD")
    pg_user = obrigatorio("POSTGRES_USERNAME")
    pg_pass = obrigatorio("POSTGRES_PASSWORD")
    pg_db = os.getenv("POSTGRES_DATABASE", "postgres")

    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=ssh_user,
        ssh_password=ssh_pass,
        remote_bind_address=(PG_HOST_REMOTO, PG_PORT_REMOTO),
        local_bind_address=("127.0.0.1", LOCAL_BIND_PORT),
    ) as tunnel:
        print(f"[tunel] SSH ok -> 127.0.0.1:{tunnel.local_bind_port} => vm031:5432")
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            user=pg_user,
            password=pg_pass,
            dbname=pg_db,
            connect_timeout=10,
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("[pg] versao:", cur.fetchone()[0])
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY 1;")
        print("[pg] bancos:", [r[0] for r in cur.fetchall()])
        cur.close()
        conn.close()
        print("[ok] Conexao com o PostgreSQL da vm031 funcionando.")


if __name__ == "__main__":
    main()
