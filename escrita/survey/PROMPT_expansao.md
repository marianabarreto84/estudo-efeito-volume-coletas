# Prompt — expansão do corpus da survey

> Escrito em **21/ago/2026**. Cole o bloco abaixo numa sessão nova para retomar
> este trabalho do zero, sem depender do histórico da conversa. Ele é
> auto-contido de propósito: diz o objetivo, o estado, as travas e as condições
> de parada.

---

```
Trabalhe na expansão do corpus da survey da dissertação. Leia primeiro o
ESTADO.md da raiz e o escrita/survey/STATUS.md.

CONTEXTO
A survey cataloga 13.395 artigos mas só extraiu 2.139, porque 10.075 estavam
marcados como inacessíveis por paywall. Isso é a maior limitação declarada do
trabalho, e a dissertação hoje a admite em vez de medi-la (decisão em aberto nº 1
do STATUS.md, e comentário [9] da 1ª rodada de revisão).

Em 21/ago/2026 apurou-se que a marcação está DESATUALIZADA: numa amostra de 70
DOIs do estrato pago, 18,6% estão em acesso aberto (IC95% Wilson 11,2%–29,2%),
em repositórios ou na própria editora. Extrapolando, 1.127 a 2.944 artigos são
recuperáveis sem credencial nenhuma.

OBJETIVO
Aplicar à própria survey o protocolo que a dissertação propõe: coletar mais e
medir se a conclusão muda. Não é "melhorar a survey" — é medir se o viés de
acesso alterava os achados.

O QUE FAZER, NESTA ORDEM
1. Recuperar os PDFs em acesso aberto da fila inteira:
   cd redes-sociais-digitais-survey
   python -u -m scripts.retry_pdfs --workers 4
   Usa Unpaywall, OpenAlex, Semantic Scholar e arXiv. NÃO usa o proxy.
   Acompanhe por pdfs/.progress.txt. É lento; rode em background.

2. Antes de extrair qualquer coisa, PRÉ-REGISTRAR num .md versionado:
   - a semente do sorteio e o tamanho da amostra;
   - quais achados serão testados e o que contaria como mudança. No mínimo:
     mediana de itens coletados (hoje ~273 mil), fração que não chega a 1 milhão
     (hoje seis em cada dez), taxa de amostragem × filtragem (hoje 18,7% × 80,3%)
     e a fatia de Twitter (hoje 54,5%);
   - a aposta: mudam ou não mudam, e em que direção.
   Isso não é burocracia: é a mesma exigência que o protocolo faz a todo caso, e
   sem ela o resultado não vale.

3. Extrair a amostra com o pipeline existente
   (python -m scripts.analyze_pdfs), respeitando o orçamento (ver TRAVAS).

4. Recomputar os agregados com escrita/survey/agg_results.py e comparar contra os
   números de hoje, com banda de reamostragem. Reportar movido/não movido por
   achado, não um veredito único.

5. Se algum número da survey mudar, ele muda também no resumo, no Cap. 1 e na
   conclusão da dissertação. Rode escrita/dissertacao/audita_numeros.py e
   audita_contas.py ANTES e DEPOIS, e propague com verificação, não à mão.

TRAVAS — não contorne nenhuma sem falar com a Mariana
- NÃO use o proxy institucional (PUCRIO_PROXY*) para volume. Ele autentica e
  funciona, mas as editoras bloqueiam automação: ACM 403, IEEE 202 com corpo
  vazio, Elsevier 403 na ScienceDirect, SAGE 403, T&F 403. Só a Springer
  devolveu 200. Rodar volume por ali arrisca o acesso da PUC-Rio INTEIRA, não só
  o da Mariana. Se ela autorizar a Springer, vá devagar e pare ao primeiro 403.
- ORÇAMENTO: a extração usa Gemini e OpenAI, com chaves no .env do repo da
  survey. O teto de US$ 25 do ANTHROPIC_VACINAS_API_KEY é do rotulador do stance
  e está em US$ 9,58 — NÃO gaste nele. Pergunte o teto antes de extrair em
  escala; recuperar PDFs é barato, extrair não é.
- Dimensione a amostra pelo orçamento, não o contrário. Uma amostra aleatória de
  algumas centenas responde a pergunta; extrair milhares não é necessário.

CONDIÇÕES DE PARADA
- Taxa de recuperação muito abaixo de 11% (o piso do IC): pare e reporte — a
  amostra de 70 era otimista e a extrapolação não vale.
- Qualquer sinal de bloqueio ou captcha: pare, não tente contornar.
- Se a extração ficar acima do orçamento: pare e reporte o custo por artigo.

O QUE NÃO FAZER
- Não mexa no corpo.tex enquanto a Mariana não tiver lido o revisao-3.pdf; o PDF
  que ela comenta tem de bater com a fonte.
- Não trate "aumentar a base" como o objetivo. O objetivo é o veredito
  mudou/não mudou. Uma base maior com os mesmos achados é um resultado ótimo, e
  fecha a decisão em aberto nº 1 do STATUS.md.
```

---

## Por que este é o trabalho recomendado

Ele é o único item grande que **não depende da Mariana**, e resolve com medida uma
limitação que hoje é só declarada. Se os achados não se moverem, o viés de editora
fica quantificado e a limitação encolhe; se se moverem, é resultado. Os dois
desfechos são publicáveis, que é a marca de uma boa pergunta.

⚠️ **A prioridade da Mariana continua sendo outra** e não muda por causa disto:
ler o `revisao-3.pdf` (cadeia de dependência mais longa) e rotular as 320 linhas
do stance (fecham três linhas da tabela mestre). Esta expansão roda em paralelo,
do lado do assistente.
