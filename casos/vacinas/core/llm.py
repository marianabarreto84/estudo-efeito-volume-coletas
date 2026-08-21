"""
Cliente Anthropic para o rotulador do eixo B.

So resolve credencial e devolve o cliente. Todo controle de gasto vive em
core/orcamento.py; nada aqui gasta dinheiro sozinho.

Ordem de busca da chave (a primeira que existir vence):
    1. variavel de ambiente ANTHROPIC_VACINAS_API_KEY
    2. variavel de ambiente ANTHROPIC_API_KEY
    3. casos/vacinas/.env
    4. dissertacao/.env            <- e onde a Mariana pos

O nome dedicado (ANTHROPIC_VACINAS_API_KEY) e preferido de proposito: uma
ANTHROPIC_API_KEY solta no ambiente e capturada por qualquer outra ferramenta
que fale com a Anthropic. Esta chave e do orcamento do caso vacinas e so dele.
"""
import os
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]          # casos/vacinas
RAIZ_PROJETO = RAIZ.parents[1]                              # dissertacao/

NOMES = ("ANTHROPIC_VACINAS_API_KEY", "ANTHROPIC_API_KEY")
ENVS = (RAIZ / ".env", RAIZ_PROJETO / ".env")

# Modelo pinado para reprodutibilidade (a opcao A do EIXO_CONTEUDO.md).
# Trocar de modelo invalida o kappa ja medido — refazer a validacao.
MODELO_PADRAO = "claude-haiku-4-5-20251001"


def _le_env(caminho):
    """Le um .env simples (CHAVE=valor) sem dependencias. Nao sobrescreve."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


def carrega_chave():
    """Devolve a chave da API. Levanta SystemExit com instrucao se faltar."""
    for nome in NOMES:
        if os.getenv(nome):
            return os.environ[nome]
    for env in ENVS:
        _le_env(env)
    for nome in NOMES:
        if os.getenv(nome):
            return os.environ[nome]
    raise SystemExit(
        "[erro] chave da API nao encontrada.\n"
        f"       Procurei em {NOMES} e em {[str(e) for e in ENVS]}.\n"
        "       Ponha uma linha ANTHROPIC_VACINAS_API_KEY=sk-ant-... num .env\n"
        "       (nunca versionado)."
    )


def cliente():
    """Cliente Anthropic ja autenticado."""
    import anthropic
    return anthropic.Anthropic(api_key=carrega_chave())
