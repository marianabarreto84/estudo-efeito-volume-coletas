"""
Teto de gasto rigido para as chamadas de LLM do eixo B.

Regra da Mariana: **nao passar de US$ 25, de forma alguma.**

Como isso e garantido aqui (tres camadas, da mais forte para a mais fraca):

  1. LIMITE NO CONSOLE (fora deste codigo, e a unica barreira de verdade):
     platform.claude.com -> Settings -> Limits -> spend limit do workspace.
     Nenhum codigo em Python pode impedir uma chamada que ja saiu; so o
     servidor pode. Configure isso — o resto e defesa em profundidade.

  2. RESERVA ANTES DE ENVIAR: cada lote so e submetido depois de estimar o
     custo MAXIMO possivel (tokens de entrada contados de verdade via
     count_tokens + max_tokens de saida como pior caso) e conferir contra o
     saldo. Se nao couber, levanta OrcamentoEstourado e nada e enviado.

  3. LIVRO-CAIXA PERSISTENTE: gastos_llm.json guarda todo lancamento entre
     execucoes. Reiniciar o script nao "zera" o gasto.

A reserva usa o pior caso (saida inteira em max_tokens), entao o gasto real
fica sempre ABAIXO do reservado — o teto nunca e furado por subestimativa.

Uso:
    from core.orcamento import Orcamento
    orc = Orcamento()
    orc.reservar(usd=0.42, descricao="lote dev 1/3")   # levanta se nao couber
    orc.lanca(entrada=120_000, saida=40_000, descricao="lote dev 1/3")
"""
import json
import pathlib
import time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
LIVRO = RAIZ / "data" / "repl" / "vacinas2022" / "gastos_llm.json"

# Teto absoluto, em dolares. Nao aumentar sem a Mariana dizer.
TETO_USD = 25.00

# Precos por milhao de tokens (Haiku 4.5, tabela publica de jul/2026).
# A Batch API cobra 50% desses valores.
PRECO_MTOK = {
    "claude-haiku-4-5-20251001": {"entrada": 1.00, "saida": 5.00},
    "claude-haiku-4-5": {"entrada": 1.00, "saida": 5.00},
}
DESCONTO_BATCH = 0.50
FATOR_CACHE_LEITURA = 0.10   # leitura de cache custa 0,1x a entrada
FATOR_CACHE_ESCRITA = 1.25   # escrita de cache custa 1,25x a entrada


class OrcamentoEstourado(RuntimeError):
    """Levantada ANTES de enviar qualquer coisa quando o lote nao cabe."""


def custo_usd(modelo, entrada=0, saida=0, cache_leitura=0, cache_escrita=0, batch=True):
    """Custo em dolares de um conjunto de tokens. Nao consulta a rede."""
    if modelo not in PRECO_MTOK:
        raise ValueError(
            f"modelo sem preco cadastrado: {modelo}. "
            f"Cadastre em core/orcamento.PRECO_MTOK antes de gastar."
        )
    p = PRECO_MTOK[modelo]
    fator = DESCONTO_BATCH if batch else 1.0
    total = (
        entrada * p["entrada"]
        + cache_leitura * p["entrada"] * FATOR_CACHE_LEITURA
        + cache_escrita * p["entrada"] * FATOR_CACHE_ESCRITA
        + saida * p["saida"]
    )
    return total / 1_000_000 * fator


class Orcamento:
    def __init__(self, caminho=LIVRO, teto=TETO_USD):
        self.caminho = pathlib.Path(caminho)
        self.teto = float(teto)
        self._carrega()

    # ---- persistencia ----
    def _carrega(self):
        if self.caminho.exists():
            d = json.loads(self.caminho.read_text(encoding="utf-8"))
            self.lancamentos = d.get("lancamentos", [])
            teto_gravado = float(d.get("teto_usd", self.teto))
            if teto_gravado != self.teto:
                raise OrcamentoEstourado(
                    f"teto do livro-caixa ({teto_gravado}) difere do teto do codigo "
                    f"({self.teto}). Alguem mexeu — pare e confira {self.caminho}."
                )
        else:
            self.lancamentos = []
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            self._grava()

    def _grava(self):
        self.caminho.write_text(json.dumps({
            "teto_usd": self.teto,
            "gasto_usd": round(self.gasto, 6),
            "reservado_usd": round(self.reservado, 6),
            "saldo_usd": round(self.saldo, 6),
            "lancamentos": self.lancamentos,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- saldos ----
    @property
    def gasto(self):
        """Gasto realizado (lancamentos confirmados)."""
        return sum(l["usd"] for l in self.lancamentos if l["tipo"] == "gasto")

    @property
    def reservado(self):
        """Reservas ainda em aberto (lote enviado, resultado nao conciliado)."""
        return sum(l["usd"] for l in self.lancamentos if l["tipo"] == "reserva")

    @property
    def saldo(self):
        """Quanto ainda pode ser comprometido sem furar o teto."""
        return self.teto - self.gasto - self.reservado

    # ---- operacoes ----
    def reservar(self, usd, descricao, detalhe=None):
        """
        Compromete `usd` do teto ANTES de enviar o lote. Levanta
        OrcamentoEstourado (sem gastar nada) se nao couber.
        Devolve o id da reserva, para conciliar depois.
        """
        usd = float(usd)
        if usd < 0:
            raise ValueError("reserva negativa")
        if usd > self.saldo:
            raise OrcamentoEstourado(
                f"lote bloqueado: custo maximo estimado US$ {usd:.4f} > "
                f"saldo US$ {self.saldo:.4f} "
                f"(teto US$ {self.teto:.2f}, gasto US$ {self.gasto:.4f}, "
                f"reservado US$ {self.reservado:.4f}). Nada foi enviado."
            )
        ident = f"r{len(self.lancamentos):04d}"
        self.lancamentos.append({
            "id": ident, "tipo": "reserva", "usd": usd,
            "descricao": descricao, "detalhe": detalhe or {},
            "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        self._grava()
        return ident

    def concilia(self, ident, modelo, entrada=0, saida=0,
                 cache_leitura=0, cache_escrita=0, batch=True, descricao=None):
        """
        Troca uma reserva pelo gasto real (uso devolvido pela API). O gasto real
        e sempre <= reserva, porque a reserva assume saida cheia em max_tokens.
        """
        reserva = next((l for l in self.lancamentos
                        if l["id"] == ident and l["tipo"] == "reserva"), None)
        if reserva is None:
            raise ValueError(f"reserva {ident} inexistente ou ja conciliada")
        usd = custo_usd(modelo, entrada, saida, cache_leitura, cache_escrita, batch)
        reserva["tipo"] = "reserva_baixada"
        reserva["usd"] = 0.0
        self.lancamentos.append({
            "id": f"g{len(self.lancamentos):04d}", "tipo": "gasto", "usd": usd,
            "descricao": descricao or reserva["descricao"],
            "detalhe": {
                "modelo": modelo, "batch": batch, "reserva": ident,
                "tokens_entrada": entrada, "tokens_saida": saida,
                "tokens_cache_leitura": cache_leitura,
                "tokens_cache_escrita": cache_escrita,
            },
            "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        self._grava()
        return usd

    def libera(self, ident, motivo="lote falhou"):
        """Devolve uma reserva ao saldo (lote nao chegou a ser cobrado)."""
        for l in self.lancamentos:
            if l["id"] == ident and l["tipo"] == "reserva":
                l["tipo"] = "reserva_liberada"
                l["usd"] = 0.0
                l["motivo"] = motivo
                self._grava()
                return
        raise ValueError(f"reserva {ident} inexistente")

    def resumo(self):
        return (f"teto US$ {self.teto:.2f} | gasto US$ {self.gasto:.4f} | "
                f"reservado US$ {self.reservado:.4f} | saldo US$ {self.saldo:.4f}")
