"""
Modulo de conexao ao PostgreSQL das VMs da Cloud-DI (PUC-Rio) via tunel SSH.

Uso:
    from db import conectar
    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1")

Requer a VPN da Cloud-DI conectada. Credenciais vem do .env (nenhum segredo aqui).
"""
import os
from contextlib import contextmanager
from pathlib import Path

# Shim: paramiko >=3.x removeu DSSKey usado pelo sshtunnel na init.
import paramiko
if not hasattr(paramiko, "DSSKey"):
    paramiko.DSSKey = paramiko.RSAKey
from sshtunnel import SSHTunnelForwarder
import psycopg2

# ---- Mapa das VMs (IP interno na rede da VPN + variavel de senha SSH no .env) ----
VMS = {
    "vm031": {"ip": "10.50.0.32", "senha_env": "VM_031_PASSWORD"},
    "vm067": {"ip": "10.50.0.68", "senha_env": "VM_067_PASSWORD"},
}


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


def _obrigatorio(nome):
    v = os.getenv(nome)
    if not v:
        raise SystemExit(f"[erro] variavel {nome} ausente no .env")
    return v


@contextmanager
def conectar(vm="vm067", dbname="eTC_Producao", local_port=5455):
    """Abre um tunel SSH ate a VM e devolve uma conexao psycopg2 ao Postgres."""
    carregar_env()
    if vm not in VMS:
        raise SystemExit(f"[erro] VM desconhecida: {vm} (use {list(VMS)})")
    info = VMS[vm]
    ssh_user = _obrigatorio("SSH_USERNAME")
    ssh_pass = _obrigatorio(info["senha_env"])
    pg_user = _obrigatorio("POSTGRES_USERNAME")
    pg_pass = _obrigatorio("POSTGRES_PASSWORD")

    with SSHTunnelForwarder(
        (info["ip"], 22),
        ssh_username=ssh_user,
        ssh_password=ssh_pass,
        remote_bind_address=("127.0.0.1", 5432),
        local_bind_address=("127.0.0.1", local_port),
    ) as tunnel:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            user=pg_user,
            password=pg_pass,
            dbname=dbname,
            connect_timeout=15,
        )
        try:
            yield conn
        finally:
            conn.close()
