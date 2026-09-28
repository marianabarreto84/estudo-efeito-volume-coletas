# RETOMAR — expansão do corpus da survey

> Estado congelado em **9/set/2026**. Cole o §1 numa sessão nova; o resto é o
> contexto que ela vai precisar. A defesa é em **29/set/2026**.

---

## 1. Prompt para colar numa sessão nova

```
Estou retomando a expansão do corpus da survey, em
escrita/survey/expansao/. Leia primeiro o ESTADO.md da raiz, depois
este RETOMAR.md inteiro, e depois me diga o que dá para avançar.

Contexto curto: a survey está fechada e publicada em
escrita/survey/revisoes/survey-2.pdf (12 p.). A expansão NÃO é para
aumentar a base — é para medir se o viés de acesso movia os achados.
Existem dois braços, e os dois já têm os PDFs em disco:

  - braço ABERTO: 800 artigos sorteados (semente 20260929), extração
    rodando desde 09/set 08:47 no repo da survey.
  - braço COMERCIAL: sonda de 200 periódicos Springer, 199 baixados
    à mão pela Mariana pelo proxy da DBD. Falta reconciliar e extrair.

Não rode nada que escreva no research.db enquanto a extração dos 800
estiver rodando. Confira antes com:
    python progresso_extracao.py
```

---

## 2. Onde exatamente paramos

| Frente | Estado |
|---|---|
| **Survey (artigo)** | ✅ `revisoes/survey-2.pdf` (14/set/2026, 12 p., limpo): só terminologia, “levantamento sistemático” → “revisão”. Antes: `survey-1.pdf`, republicado **3×** em 9/set (correções de número) |
| **Varredura de acesso aberto** | ✅ **encerrada** em 23/ago: 11.093 tentados (100% da fila), **811 recuperados**, taxa final **7,7%** no estrato pago |
| **Extração dos 800 (braço aberto)** | ◐ **rodando** desde 09/set 08:47. Ver §3 |
| **Sonda Springer (braço comercial)** | ✅ **199/200 baixados**, 1 sem acesso. ⏳ falta reconciliar + extrair |
| **`corpo.tex` da dissertação** | ✅ **alinhado à survey com a extração completa em 15/set/2026** (`revisao-12.pdf`): 3.107/635/2.472, Tab. 1.1 = Tab. 3 da survey (só Gemini). Os dois estão na base 2.472, **com** a expansão e com os 198 PDFs que nunca tinham passado pelo modelo (ver `../revisoes/extracao198/LEIA.md`). Antes: base 2.322, alinhada ao survey-3 em 14/set (rodada 8) |

## 3. O que fazer, em ordem

### 3.1 Esperar a extração dos 800 acabar

```bash
cd escrita/survey/expansao
python progresso_extracao.py
```

Ele lê só o log (não toca no banco) e imprime concluídos, taxa de falha, ritmo e
**previsão de término**. Em 9/set 11:36: 365 de 789 (46%), 5,5% de falha,
2,2 artigos/min, previsão **14h48**.

⚠ **Nada mais pode escrever no `research.db` até ela terminar.**

**Se o log parar de crescer**, o script avisa em vez de deixar você supondo. E
nada se perde: o `analyze_pdfs` **persiste artigo a artigo** — verificado em
9/set, com o banco em 2.497 (2.147 + 350) enquanto a corrida ainda andava.
Relançar pula quem já tem análise, então basta refazer o comando com a lista de
ids que restarem.

### 3.2 Reconciliar a sonda e extrair os 199

```bash
cd escrita/survey/expansao
python reconcilia_pdfs.py                 # relatório
python reconcilia_pdfs.py --aplicar       # grava pdf_path dos 199
```

Depois, no repo da survey, extrair só os 199 (≈R$11):

```bash
python -c "import json;d=json.load(open(r'C:\Users\maria\Documents\GitHub\dissertacao-mestrado\escrita\survey\expansao\sonda_springer.json',encoding='utf-8'));print(' '.join(str(a['id']) for a in d['itens']))" > pdfs/.ids_sonda.txt
python -m scripts.analyze_pdfs --models gemini --workers 5 --ids $(cat pdfs/.ids_sonda.txt)
```

⚠ **Passe os ids por arquivo, com caminho relativo.** Foi exatamente a
interpolação de caminho do Windows dentro de `$( )` do bash que fez a extração
encadeada falhar em 23/ago — e o laço reportou `codigo 0` por cima do erro.

### 3.3 Comparar

```bash
python compara.py --json resultado.json
```

Aplica os **dois critérios pré-registrados** e **aborta** se a base antiga deixar
de reproduzir o `baseline_agg.txt`. As apostas da §6 do
[PRE_REGISTRO](PRE_REGISTRO_expansao.md):

| # | Achado | Aposta |
|---|---|---|
| A3a | Amostragem 18,7% | **não move** (faixa 16–22%) |
| A3b | Filtragem 80,3% | **não move** (faixa 77–84%) |
| A4 | Twitter 63,7% | move, **cai** 2–6 p.p. |
| A1 | Mediana 273.290 | move, **cai** |
| A2 | 60,5% abaixo de 1 mi | move, **sobe** 2–5 p.p. |

⭐ **Se A3a ou A3b se moverem, a aposta falhou no ponto que mais importa** — e o
resultado é maior do que se ela acertasse: significaria que o achado central da
survey era artefato de acesso. Reportar na primeira linha, sem atenuação.

### 3.4 Só então decidir sobre o `corpo.tex`

Ver [ESTADO.md](../../../ESTADO.md) §3, itens 11 e 12.

## 4. As três armadilhas desta frente (todas já custaram caro)

1. **O instrumento contamina o que mede.** `pdf_inaccessible` era o rótulo de
   estrato e o `retry_pdfs` o reescrevia; o estrato estável vive em
   `estratos.json`. Mesma família: a taxa de 12,4% medida a 34% da fila não
   sobreviveu ao censo (**7,7%**), provavelmente porque 307 órfãos de disco
   entraram no numerador sem seus denominadores. ⏳ **hipótese ainda por conferir.**
2. **Log de sucesso sobre fracasso.** O `extrai_apos_varredura.sh` gravou
   `codigo 0` enquanto o `analyze_pdfs` abortava. Passou **17 dias** despercebido.
   Sempre confira o efeito no banco, não a última linha do log.
3. **A ordem da fila é um esquema de amostragem.** Sem `--shuffle`, os primeiros
   da fila são 2025–26, os menos prováveis de estar em repositório. E a amostra
   da sonda era 75% LNCS, que a assinatura não cobre — pego por um diagnóstico de
   8 cliques, antes de custar 150.

## 5. O que NÃO fazer

- ⛔ **Não mexer no `vocabulary`** (termo 22, "análise de conteúdo") antes de a
  expansão extrair — o `compara.py` passaria a medir mudança de *prompt* em vez
  de viés de acesso. Ver [DIAGNOSTICO_tipos_de_analise.md](DIAGNOSTICO_tipos_de_analise.md) §6.5.
- ⛔ **Não tentar o proxy em massa.** A rota está fechada em **todas** as
  editoras: a Springer serve `client challenge` com HTTP 200 no endpoint do PDF
  (§4b do [EXPANSAO_recuperacao.md](../EXPANSAO_recuperacao.md)). O
  `curl_cffi`/Playwright do `PROXIMAS_ETAPAS.md` **foi recusado por decisão** —
  é contornar controle anti-automação, e o risco recai sobre a PUC-Rio inteira.
- ⛔ **Não re-sortear** nenhuma amostra depois de ver resultado. Os `--sortear`
  dos dois braços se recusam a sobrescrever de propósito.
- ⛔ **Não escrever no `research.db`** com a extração rodando.

## 6. O que a sonda já provou, independente da extração

Isto é resultado, e vai ao relatório mesmo que a comparação não mova nada:

| | |
|---|---:|
| periódicos Springer baixados com acesso institucional | **199/200 (99,5%)** |
| mesmos artigos, por rotas de acesso aberto | **7,7%** |
| anais LNCS, com acesso institucional | **0/5** |
| artigos de anais LNCS no corpus, inalcançáveis | **1.492** |

⭐ Uma instituição que **assina** Springer alcança quase tudo dos periódicos e
**nada** dos anais. O estrato comercial não é um custo que se pague: é limite
estrutural para levantamento em escala — e é o que a **ameaça à validade nº 2**
do artigo já afirma, agora confirmada por dentro.
