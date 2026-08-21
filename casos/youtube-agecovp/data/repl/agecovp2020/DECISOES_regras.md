# Decisões de método — as duas regras que o artigo não publica

> Registrado em **18/ago/2026**. Mesmo papel do `DECISOES_ROTULADOR.md` (vacinas) e do
> `DECISOES_CB2.md` (meta-ads): toda escolha de operacionalização fica escrita, com a
> evidência que a motivou e o que foi rejeitado.
> Código: [`core/regras.py`](../../../core/regras.py) ·
> medições: [`analise/calibra_ugc.py`](../../../analise/calibra_ugc.py).

---

## D1 — `no_tema`: separar ruído de viés

**O problema.** A [Fase 3 parcial](FASE3_efeito_filtro.md) mostrou que o conjunto
descartado pelo filtro do artigo traz conteúdo genuinamente **fora do tema** (`Sport`
4,5%, `Baseball` 3,4%). Comparar "com filtro" × "sem filtro" sem separar isso mede
**ruído**, não viés — e seria uma objeção justa de banca.

**Decisão.** Teste de tema **conjuntivo e independente** da regra do artigo: o texto
(título + descrição + tags) precisa mencionar **um termo de idosos** *e* **um termo de
covid/pandemia**.

**Por que conjuntivo:** o objeto declarado do estudo é a interseção *idosos × pandemia*.
Vídeo de beisebol não menciona nenhum dos dois; vídeo só de covid, ou só de idosos, está
fora do objeto.

**Por que independente da regra do artigo:** se usasse os mesmos termos de busca, seria
**circular** — reprovaria por construção tudo o que o filtro do artigo reprova, e o teste
não teria conteúdo.

**Validação (o controle que autoriza a regra):** aplicada ao **corpus do próprio artigo**,
`no_tema` aprova **3.777 de 3.782 vídeos (99,9%)**. A regra não é severa demais: o que ela
reprova, o artigo também não teria aceitado.

**Rejeitado:** usar a lista ampla de 88 palavras-chave do artigo como teste de tema — é a
própria regra de filtro dele, logo circular.

---

## D2 — `eh_ugc`: e o achado de que **AG3 não reproduz**

**O problema.** AG3 afirma *"UGC representa menos de 7%"* — o conteúdo seria dirigido por
veículos de imprensa. O artigo **não publica** a regra que separa usuário de veículo, e o
gabarito não traz a coluna. Sem regra, AG3 não é testável.

**Regra adotada.** Canal é **institucional** se o título traz marcador de imprensa/
instituição (`news`, `tv`, `bbc`, `times`, `hospital`, `university`, …) **ou** tem
inscritos ≥ limiar. É **UGC** caso contrário. Os dois critérios são necessários: há
veículo pequeno que o limiar não pega, e criador individual enorme que o marcador não pega.

**A tentativa de calibrar, e o que ela revelou.** A intenção inicial era ajustar o limiar
para reproduzir o "<7%" sobre o corpus do artigo. Medido:

| limiar de inscritos | UGC (% dos vídeos) | UGC (% dos canais) |
|---|--:|--:|
| 0 (só o marcador decide) | 0,0% | 0,0% |
| 10 | 2,3% | 6,6% |
| **50** | **6,6%** | 14,6% |
| 100 | 9,0% | 18,7% |
| 1.000 | 22,9% | 39,2% |
| 10.000 | 32,0% | 53,9% |
| 100.000 | 41,2% | 63,8% |

⚠ **O "<7%" só aparece com o limiar em ~50 inscritos.** Isto é, seria preciso definir
"conteúdo de usuário" como *canal com menos de cinquenta inscritos* — o que exclui da
categoria qualquer pessoa física com um público mínimo. Não é uma definição defensável.

**Decisão, e é uma mudança de rumo:** **abandonar a calibragem** e adotar um limiar
**declarado e defensável — 10.000 inscritos** — reportando a sensibilidade acima ao lado.
Consequências:

1. **AG3 passa a "não reproduz".** Sob a regra declarada, UGC é **32,0%** dos vídeos do
   corpus do artigo, contra os "<7%" publicados. A divergência pode ser **definicional**
   (a regra deles é desconhecida e pode não ser sobre tamanho de canal), e é assim que
   deve ser reportada — como o caso das impressões do Capozzi, que também não reproduzem
   a partir dos dados publicados.
2. **A comparação continua válida.** O que a Fase 3 mede é a **diferença** entre os dois
   lados do filtro sob a **mesma** regra. Essa diferença não depende de onde o limiar
   está — e é ela, não o valor absoluto, que responde à pergunta da tese.

**Por que não calibrar assim mesmo:** calibrar produziria um número bonito (≈7%) por
construção, e o capítulo passaria a afirmar que "AG3 replica" quando o que houve foi
ajuste de parâmetro até bater. É o oposto do que o projeto faz — e a mesma armadilha que o
`PRE_REGISTRO_stance.md` §4 proíbe ("nunca olhar o teste para escolher o parâmetro").

---

## D2b — ⚠ **AG3 é irreproduzível porque o artigo se contradiz** (achado de 19/ago/2026)

A pergunta "como descobrir a regra deles?" levou à leitura integral do trecho, e o que
apareceu não foi a regra: foi **uma contradição interna**. O artigo afirma as duas coisas
opostas, duas vezes cada uma.

| onde | frase (literal) | implica |
|---|---|---|
| §4, após a rotulagem | *"Results of this labeling process showed that **less than 7% of the videos were UCC and not UGC**"* | **>93% é UGC** |
| §4, frase **seguinte** | *"This indicates that the dataset is dominated by videos originally aired on television by news sources... and **very few videos were originally created by YouTube users**"* | ~7% é UGC |
| §*Sentiment analysis* | *"many of which are from news outlets rather than user-generated content (**UGC accounts for less than 7%**)"* | ~7% é UGC |
| §*Channel statistics* | *"**most videos come from channels with smaller subscriber counts**... o dataset pende para criadores menos promovidos"* | UGC dominante |
| §*Toxicity* | *"**most videos come from news media** and informative outlets, which typically employ moderated, neutral language"* | imprensa dominante |

**A frase da 2ª linha contradiz o número da 1ª, no parágrafo seguinte.** E a leitura
"imprensa dominante" é **carregadora**: ela é usada para explicar **dois** resultados
distintos — o sentimento positivo dos vídeos (59%/72%) e a toxicidade baixa (>90% ≤ 0,3).
Se a leitura correta for a outra (>93% UGC), as duas explicações caem.

**Não é adjudicável de fora.** Os rótulos UGC/UCC foram feitos **à mão, vídeo a vídeo**
(dois autores codificaram 10% em duplicata; um autor rotulou o resto) e **não estão
publicados** — não há coluna correspondente em `videos.csv`. Ou seja: a única evidência
que resolveria a contradição é justamente a que ficou de fora do gabarito.

**O que a nossa medição independente diz.** Pela regra declarada (marcador de imprensa
**ou** ≥10.000 inscritos), o corpus tem **32,0% de UGC** e 68% institucional — **nenhum**
dos dois extremos. Não resolve a contradição, mas mostra que os dois valores publicados
são implausíveis como descrição do corpus.

**Consequência para o caso.** AG3 sai da lista de alvos-teste replicáveis e entra como
**achado sobre reprodutibilidade**: não é que a réplica falhou; é que a afirmação, como
publicada, não tem valor de verdade determinado. Junta-se aos irmãos:

- vacinas: corpo do texto diz 11 categorias, o material suplementar numera 14;
- meta-ads: as impressões (~35 M) não reproduzem do CSV publicado (49,8 M);
- **AGECovP: UGC é <7% e >93% no mesmo artigo.**

⚠ Isto **substitui** a pendência "perguntar a regra aos autores": não há regra a pedir —
há uma inconsistência a reportar. Se houver contato com os autores, a pergunta certa passa
a ser *qual das duas frases está correta*.
