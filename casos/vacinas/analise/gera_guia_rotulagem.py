"""
Gera o GUIA_ROTULAGEM.md — a referencia para a rotulagem MANUAL.

Por que gerado e nao escrito a mao: o guia humano tem de conter exatamente as
mesmas definicoes que o prompt do rotulador automatico recebe. Se divergirem, o
kappa medido nao compara dois rotuladores fazendo a mesma tarefa — compara
duas tarefas diferentes, e nao significa nada.

Fonte unica: `codebook_v1.json` (extraido do suplemento do paper) + as mesmas
regras de fronteira que estao no prompt `p4` (NOTAS_P2 e o tratamento por tipo
de categoria de `diagnostico_cobertura`).

Uso:
    PYTHONIOENCODING=utf-8 python -u analise/gera_guia_rotulagem.py
"""
import json
import pathlib
import sys

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from pipeline.rotula_conteudo import (NOTAS_P2, diagnostico_cobertura,
                                      gatilhos_da_categoria)

DADOS = RAIZ / "data" / "repl" / "vacinas2022"
CODEBOOK = DADOS / "codebook_v1.json"
XLSX = DADOS / "suplementar_rotulos.xlsx"
DESTINO = DADOS / "GUIA_ROTULAGEM.md"


def main():
    codebook = json.loads(CODEBOOK.read_text(encoding="utf-8"))
    diag = diagnostico_cobertura(codebook, pd.read_excel(XLSX, "Spreadsheet 1"))

    L = [
        "# Guia de rotulagem manual — caso vacinas, eixo B",
        "",
        "> **Gerado** por `analise/gera_guia_rotulagem.py` a partir do mesmo",
        "> codebook que alimenta o prompt do rotulador automatico. Nao editar a",
        "> mao: se este guia e o prompt divergirem, o κ deixa de comparar dois",
        "> rotuladores fazendo a mesma tarefa.",
        "",
        "Preencher em `VALIDACAO_HUMANA_amostra.xlsx`, aba `ROTULAR`.",
        "",
        "---",
        "",
        "## Antes de comecar: tres regras que valem para tudo",
        "",
        "1. **Julgue o autor, não quem ele cita.** Um tweet que reproduz uma",
        "   fala anti-vacina para ridicularizá-la é `pro`. Ironia e sarcasmo",
        "   são comuns neste corpus.",
        "2. **Marque o que é citado ou aludido, ainda que de passagem.** O tema",
        "   não precisa ser o assunto principal do tweet. Um tweet sobre",
        "   vacinação infantil que menciona a Anvisa de passagem é *também*",
        "   categoria 1 (Politics).",
        "3. **Não olhe os rótulos do modelo antes de terminar.** Eles estão em",
        "   `rotulos_llm/e1_lim10_pt_p4/rotulos.csv`. Ver antes de rotular",
        "   ancora o julgamento e o κ passa a medir concordância induzida.",
        "",
        "---",
        "",
        "## Parte 1 — stance (uma escolha por tweet)",
        "",
        "| valor | quando usar |",
        "|---|---|",
        "| `pro` | defende, promove ou apoia a vacinação |",
        "| `anti` | questiona, ataca ou desencoraja a vacinação |",
        "| `nenhum` | não permite decidir de lado nenhum |",
        "",
        "**`nenhum` é raro.** No gabarito humano do paper, 3 tweets em 1.525.",
        "Estes são tweets de um debate polarizado: quase todos tomam partido,",
        "ainda que de forma indireta. Se houver qualquer indício de posição,",
        "escolha `pro` ou `anti`. Não use `nenhum` como saída para o caso",
        "difícil — decida, e anote a dúvida em `observacao`.",
        "",
        "> Atenção: a amostra vem do estrato **pouco viralizado**, que pode ter",
        "> mais tweets ambíguos que o estrato viral do paper. Se você achar que",
        "> `nenhum` está sendo necessário com muito mais frequência que 1 em",
        "> 500, isso é em si um achado — anote.",
        "",
        "---",
        "",
        "## Parte 2 — categorias (zero, uma ou várias por tweet)",
        "",
        "Escreva os **números** separados por vírgula (ex.: `1,2,8`). Vazio se",
        "nenhuma se aplica.",
        "",
        "As categorias vêm em dois formatos, e a pergunta muda:",
        "",
        "- **com lista de gatilhos** → *o tweet cita ou alude a algum destes?*",
        "  Basta **um**. Quando a lista terminar em *“e qualquer outra menção",
        "  a X”*, ela é ilustrativa e não fechada.",
        "- **sem lista** (tema amplo) → *o tema aparece no tweet?* Uma menção",
        "  de passagem já conta.",
        "",
    ]

    for c in codebook["categorias"]:
        numero = c["numero"]
        tipo = diag[numero]["tipo"]
        gat = gatilhos_da_categoria(c)
        L += [f"### {numero}. {c['nome_en']} — {c['nome_pt']}", ""]
        if tipo == "exaustiva" and gat:
            L += ["**Gatilhos** (lista fechada — se não é um destes, não é "
                  "esta categoria):", ""]
            L += [f"- {g}" for g in gat]
        elif tipo == "parcial" and gat:
            itens = [g for g in gat if g != "entre outros do mesmo tipo"]
            L += ["**Gatilhos** (lista **aberta** — os exemplos abaixo **e "
                  f"qualquer outra menção a {c['nome_en']}**):", ""]
            L += [f"- {g}" for g in itens]
        elif gat:
            L += ["**Gatilhos:**", ""]
            L += [f"- {g}" for g in gat]
        else:
            L += [f"**Tema amplo.** Marque sempre que {c['nome_pt'].lower()} "
                  "aparecer, ainda que de passagem. Não há lista fechada."]
        if numero in NOTAS_P2:
            L += ["", f"> ⚠ {NOTAS_P2[numero]}"]
        n_gab = c["total_publicado"]
        L += ["", f"_No gabarito do paper: {n_gab} de 1.525 tweets "
              f"({100*n_gab/1525:.1f}%)._", ""]

    L += [
        "---",
        "",
        "## As duas fronteiras que mais confundem",
        "",
        "Foram medidas como as piores do rotulador automático (κ 0,376 e",
        "0,518). Preste atenção nelas — é onde a sua rotulagem mais informa:",
        "",
        "**7 (Advantages) × 9 (Misinformation sources).** O codebook do paper",
        "coloca *“desmentir desinformação sobre riscos da vacina”* dentro de",
        "**Advantages**, não de Misinformation. Um tweet que derruba um boato",
        "sobre efeito colateral é categoria **7**. A categoria 9 é para quando",
        "o tweet trata da desinformação *enquanto tal* (a mentira, o boato, a",
        "checagem como assunto).",
        "",
        "**9 (Misinformation sources) × 10 (Information sources).** A 10 é o",
        "veículo enquanto veículo (imprensa, TV, redes sociais, jornalistas),",
        "sem juízo sobre ser falso. Se o ponto do tweet é a falsidade, é a 9.",
        "",
        "---",
        "",
        "## Quando terminar",
        "",
        "Salve o arquivo e rode:",
        "",
        "```",
        "python -u analise/valida_estrato_baixo.py",
        "```",
        "",
        "Ele calcula o κ entre você e o rotulador nesta amostra e escreve o",
        "resultado em `VALIDACAO_ESTRATO_BAIXO.md`. O critério é o mesmo do",
        "teste cego: κ ≥ 0,70 no stance, mediana ≥ 0,60 nas categorias.",
        "",
        "- **Se passar:** o achado da Fase 3 (a inversão do stance) deixa de",
        "  ser provisório.",
        "- **Se reprovar:** o rotulador não transfere para o estrato baixo, e a",
        "  seção 1 da Fase 3 cai — o que é um resultado legítimo e publicável,",
        "  não um fracasso. Reporta-se que o instrumento validado no estrato",
        "  viral não se sustenta fora dele.",
    ]
    DESTINO.write_text("\n".join(L), encoding="utf-8")
    print(f"[ok] escrito: {DESTINO} ({len(L)} linhas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
