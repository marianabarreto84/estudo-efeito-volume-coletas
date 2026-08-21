"""
Modulo de conexao ao PostgreSQL das VMs da Cloud-DI (PUC-Rio) via tunel SSH.

Identico ao usado nos casos irmaos (twitter-ituassu, heine-xande): o banco
eTC_Producao na vm067 guarda a coleta continua da plataforma eTC — candidato
natural para a coleta vacinas (dez/2021-mar/2022) do preprint Verjovsky et al.
Requer a VPN da Cloud-DI conectada.

Uso:
    from core.db import conectar
    with conectar(vm="vm067", dbname="eTC_Producao") as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1")

Credenciais vem do .env na raiz do projeto (nenhum segredo aqui).
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
    "vm037": {"ip": "10.50.0.38", "senha_env": "VM_037_PASSWORD"},
    "vm067": {"ip": "10.50.0.68", "senha_env": "VM_067_PASSWORD"},
}


def carregar_env(caminho=".env"):
    """
    Le um .env simples (CHAVE=valor) para os.environ, sem dependencias.
    Procura, nesta ordem: .env deste caso -> .env dos casos irmaos, para REUSAR
    as credenciais sem copiar o segredo. O primeiro que existir vence
    (setdefault nao sobrescreve).
    """
    raiz = Path(__file__).resolve().parents[1]
    candidatos = [
        raiz / caminho,
        raiz.parent / "twitter-ituassu" / ".env",           # casos irmaos (Documents/dissertacao/casos)
        raiz.parent / "heine-xande" / ".env",
        raiz.parent.parent.parent.parent / "Downloads" / "pesquisa-twitter-refeita" / ".env",  # layout Downloads
    ]
    for p in candidatos:
        if not p.exists():
            continue
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


def conectar_auto(dbname=None, vm="vm067"):
    """
    Escolhe a conexao automaticamente:
      - se env PGTUNNEL_PORT estiver setada (ex.: 5001) -> usa o SEU tunel ssh -L
        (conectar_porta_local); nao abre VPN/SSH em python;
      - senao -> abre o tunel SSH em python ate a VM (precisa VPN + .env com SSH_*).
    Devolve um context manager (use com 'with').
    """
    carregar_env()
    porta = os.getenv("PGTUNNEL_PORT")
    if porta:
        return conectar_porta_local(local_port=int(porta), dbname=dbname)
    return conectar(vm=vm, dbname=dbname or "eTC_Producao")


@contextmanager
def conectar_porta_local(local_port=5001, dbname=None):
    """
    Conecta ao Postgres por um tunel SSH que VOCE ja abriu (o jeito da Mariana):
        ssh -L 5001:localhost:5432 cloud-di@vm067   # deixe essa janela aberta
    Aqui so falamos com 127.0.0.1:<local_port>. Nao abre VPN nem SSH em python —
    piggyback no tunel manual. dbname vem do .env (POSTGRES_DATABASE) se nao dado.
    """
    carregar_env()
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=local_port,
        user=_obrigatorio("POSTGRES_USERNAME"),
        password=_obrigatorio("POSTGRES_PASSWORD"),
        dbname=dbname or os.getenv("POSTGRES_DATABASE") or "eTC_Producao",
        connect_timeout=15,
    )
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def conectar(vm="vm067", dbname="eTC_Producao", local_port=5457):
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
