# Resultados da expansão — braço de acesso aberto

> Gerado em **9/set/2026** por `compara.py` sobre o `research.db`, com os números
> crus em `resultado_braco_aberto.json`. Determinístico (2.000 reamostragens).
> O script **aborta** se a base antiga deixar de reproduzir o `baseline_agg.txt`,
> e a guarda passou.
>
> As apostas foram registradas em [PRE_REGISTRO_expansao.md](PRE_REGISTRO_expansao.md)
> §6, **antes** de qualquer extração. Duas acertaram e três falharam — todas as três
> na direção oposta à prevista. Está tudo reportado abaixo, sem atenuação.
>
> ⚠ **Atualização de 15/set/2026 (extração completa).** Dos 800 sorteados, 28 estavam
> entre os 198 PDFs que nunca tinham passado pelo modelo. Com eles extraídos (27; 1 PDF
> corrompido), o `compara.py --so-amostra` foi refeito, e o estrato novo passou a **624**
> na base (175 descartados): A3a **19,6%** (*p* = 0,64), A3b **83,3%** (*p* = 0,09), A4
> **68,9%** (*p* = 0,020), A1 mediana **778.576**, A2 **51,8%** (*p* = 0,0004) e B3
> **2,6%**. Nenhuma leitura abaixo muda. As tabelas deste arquivo seguem com os números
> de 9/set. A base do artigo é agora **2.472**, isto é, a combinada daqui (1.718 + 624)
> mais os 130 artigos da coleta primária e de fora do sorteio que também nunca tinham
> sido extraídos. Números crus em `../revisoes/extracao198/compara_depois.json` (os de
> antes, em `compara_antes.json`).
>
> ⚠ **Desvio declarado do pré-registro (15/set/2026, survey-6-v4, pedido da Mariana).**
> O §3 previa amostra de 800 porque a população (811) passava do teto de gasto. Com os 11
> de fora também extraídos, a survey passou a reportar o teste sobre os **811**, sem o
> sorteio (`compara.py --recuperados`, números em
> `../revisoes/extracao198/compara_811.json`): estrato novo **633** na base (177
> descartados, 1 PDF corrompido), A3a **19,6%** (*p* = 0,62), A3b **83,6%**
> (*p* = 0,07), A4 **69,0%** (*p* = 0,017), A1 mediana **766.105**, A2 **52,3%**.
> Nenhuma leitura muda. O teste sobre os 800 continua sendo o pré-registrado.

---

## 1. O que foi feito

| | |
|---|---:|
| base antiga (baseline congelado, pós-descarte) | **1.718** |
| estrato novo extraído (pós-descarte) | **604** |
| **base combinada** | **2.322** |
| artigos extraídos nesta corrida | 789 |
| falhas de extração | 28 (3,5%) |
| descartados por não coletarem RSD | 168 do estrato novo |

Custo real ≈ R$43, dentro do teto. Nenhuma condição de parada de custo disparou.

## 2. A aposta central ACERTOU — e é o que mais importa

> **Aposta global (§6):** *"Os dois achados centrais não se movem; a descrição do
> corpus se move."*

| # | Achado | antiga | estrato novo | combinada | crit.1 | crit.2 | *p* |
|---|---|---:|---:|---:|:---:|:---:|---:|
| **A3a** | amostragem | 18,7% | 19,7% | **18,9%** | não | não | 0,583 |
| **A3b** | filtragem | 80,3% | 83,6% | **81,1%** | não | não | 0,071 |

✅ **Os dois achados centrais não se movem.** A amostragem segue rara e a filtragem
segue a norma, e o estrato que estava inacessível **não é diferente** nesse ponto
(nenhum dos dois critérios dispara). Os valores caem dentro das faixas apostadas
(16–22% e 77–84%).

⭐ **Consequência para o artigo:** o achado central da survey **não era artefato de
viés de acesso**. Isso não é um resultado nulo — é a resposta a uma ameaça à
validade que o próprio artigo declara, obtida por medição em vez de argumento.

## 3. As três apostas de direção FALHARAM — e falharam juntas

| # | Achado | antiga | estrato novo | combinada | aposta | deu |
|---|---|---:|---:|---:|---|---|
| **A4** | Twitter | 63,7% | **68,7%** | 65,0% | cai 2–6 p.p. | ⬆ **sobe 5,0** |
| **A1** | mediana de itens | 273.290 | **769.584** | 386.670 | cai, talvez <200 mil | ⬆ **2,8×** |
| **A2** | < 1 milhão | 60,5% | **51,9%** | 58,3% | sobe 2–5 p.p. | ⬇ **cai 8,6** |

Todas com o **critério 2** disparado (A4 *p*=0,028; A2 *p*=0,0005; A1 com IC95% da
diferença em [170.942; 958.056], que não cruza zero). Ou seja: **o estrato antes
inacessível é de fato diferente** — só que ao contrário do que se apostou.

**Por que a aposta errou.** O raciocínio registrado era: *"a base extraída foi montada
com o que era grátis na hora do download, e isso é dominado por arXiv — a fatia mais
concentrada em Twitter que existe. O estrato pago tem mais periódico de comunicação e
ciências sociais, onde Facebook e YouTube pesam mais."*

Os dados dizem o contrário, e as três falhas são **coerentes entre si**: o estrato
recuperado tem **mais** Twitter, coletas **maiores** e **menos** coleta pequena. A1 e
A2 são espelhos aritméticos, então na prática são dois fenômenos, não três — mais
Twitter, e mais escala.

⏳ **A explicação fica em aberto.** Uma hipótese compatível com os três: o que estava
atrás de *paywall* é mais concentrado em periódico técnico de larga escala, e não em
ciências sociais como se supôs. Não foi testada, e **não deve ser escrita como se
tivesse sido**.

## 4. O que muda no artigo: um número, e só um

| # | Achado | antiga | novo | **combinada** | crit.1 | *p* |
|---|---|---:|---:|---:|:---:|---:|
| **B3** | DOI persistente | 8,3% | **2,6%** | **6,8%** | ⭐ **SIM** | <0,0001 |
| B1 | coleta via API | 69,7% | 67,4% | 69,1% | não | 0,283 |

**B3 é o único que dispara o critério 1** — o único cuja mudança sai do IC95% da base
antiga e portanto **muda o número publicável**: a adesão a repositórios com DOI
persistente cai de **8,3% para 6,8%**.

E a direção faz sentido: artigo que estava em acesso aberto tem mais propensão a
publicar dados em repositório com DOI. O estrato que estava fechado publica **três
vezes menos** (2,6%). ⭐ Isso **reforça** o argumento de reprodutibilidade do artigo,
que já era o mais duro da seção de persistência.

## 5. Leitura de conjunto

1. ✅ **O achado central da survey sobrevive à correção do viés de acesso.** É o
   desfecho que a aposta previu, e o mais importante dos três.
2. ❌ **A descrição do corpus muda, mas não como se apostou.** Reportar a falha é
   obrigação do pré-registro, e o erro é informativo: a intuição sobre *quem* está
   atrás do paywall estava invertida.
3. ⭐ **Um número do artigo muda de fato** (DOI persistente 8,3% → 6,8%), e na
   direção que fortalece o argumento.
4. Isto repete a forma de desfecho do **caso vacinas** (`CLAUDE.md` §3): *conclusão
   comparativa robusta ao instrumento, descrição do corpus não*. Num objeto
   completamente diferente — o que faz dela um achado transversal da dissertação,
   como o pré-registro §6 antecipou.

## 6. ⏳ O que ainda não entrou aqui

- **O braço comercial** (sonda Springer): 199 PDFs reconciliados no banco em
  9/set, **ainda não extraídos** (≈R$11). É população e pergunta diferentes — o
  estrato *pago*, não o *recuperável em aberto* —, e por isso vai num relatório
  separado, não misturado a estes números.
- **A propagação para o `.tex`**: nada foi alterado no `survey.tex` nem no
  `corpo.tex`. A base combinada de **2.322** e o B3 de **6,8%** são decisão da
  Mariana — ver [ESTADO.md](../../../ESTADO.md) §3.
- **A hipótese dos 307 órfãos** (§3c do [EXPANSAO_recuperacao.md](../EXPANSAO_recuperacao.md)),
  que explicaria a taxa de 12,4% não ter sobrevivido ao censo, segue por conferir.
