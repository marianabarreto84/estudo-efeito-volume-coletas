# Fase 3 / eixo B — o que muda ao descer o limiar de viralidade

> Gerado por `analise/curvas_por_limiar.py`. Todos os numeros usam o
> **mesmo** rotulador (`p4`, kappa 0,759 no stance e mediana 0,650 nas
> categorias, medidos no teste cego). Nenhuma comparacao mistura
> rotulo humano com rotulo automatico.

Corpus: 29.978 tweets originais em portugues com mais de 10 RT,
do snapshot congelado da coleta (busca 178).

> **Leia antes:** a secao 1 apresenta o MESMO corpus sob DOIS esquemas
> de anotacao. Isso nao e redundancia — e o resultado. Ver secao 3.

## 1. Stance sob os dois esquemas de anotacao

`p4` reproduz o esquema do artigo (binario forcado: todo tweet recebe
lado). `p6` usa tres classes, com `nenhum` para o tweet topicamente
relevante que nao emite juizo. Mesmo corpus, mesmo modelo, mesma
temperatura — muda so o esquema.

| Limiar | n | p4 %pro | p4 %anti | p6 %pro | p6 %anti | p6 %neutro | p4 %pro* | p6 %pro* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| >500 RT | 1.559 | 47,0% | 50,0% | 37,7% | 37,7% | **24,6%** | 48,4% | **50,0%** |
| >250 RT | 3.108 | 50,8% | 45,7% | 40,1% | 33,6% | **26,3%** | 52,6% | **54,4%** |
| >100 RT | 6.090 | 53,6% | 42,1% | 41,7% | 30,9% | **27,5%** | 56,0% | **57,5%** |
| >50 RT | 9.826 | 56,3% | 39,3% | 43,2% | 28,2% | **28,5%** | 58,9% | **60,5%** |
| >25 RT | 15.866 | 58,3% | 36,5% | 43,1% | 26,4% | **30,5%** | 61,5% | **62,0%** |
| >10 RT | 29.978 | 58,8% | 35,1% | 41,1% | 25,5% | **33,4%** | 62,6% | **61,7%** |

`%pro*` = pro entre os que receberam lado (exclui neutros).

### O que muda e o que nao muda com o esquema

**Nao muda: a direcao e a magnitude do deslocamento.** Entre os tweets
que recebem lado, a fatia pro-vacina sobe ao descer o limiar nos dois
esquemas — 14,2 pontos no binario forcado e 11,8
pontos nas tres classes. A conclusao COMPARATIVA e robusta a escolha
de anotacao.

**Muda: a descricao do corpus.** Em >10 RT o esquema do artigo diz
58,8% pro contra 35,1% anti — le-se
um debate com maioria pro-vacina clara. O esquema de tres classes diz
41,1% pro, 25,5% anti e
**33,4% sem posicao** — le-se um debate em que um
terco do material nao toma partido. Sao leituras diferentes do MESMO
corpus, produzidas pelo MESMO modelo.

**A neutralidade cresce ao descer o limiar:** de
24,6% em >500 RT para 33,4% em
>10 RT (8,8 pontos). A viralidade seleciona conteudo que
toma partido — achado proprio, so visivel sob um esquema com classe
neutra.

### Afericao no estrato com gabarito

Em >500 RT o esquema binario da 48,4% de pro entre
os decididos; o gabarito **humano** do paper da 48,4%. O instrumento
reproduz a codificacao publicada onde ela existe.

> **Confiabilidade.** O rotulador de tres classes atinge κ 0,697 contra
> codificacao humana, com teto da tarefa medido em 0,746
> (`RETESTE_intracodificador.md`). Os percentuais desta secao herdam
> essa margem; as comparacoes ENTRE limiares sao mais robustas que os
> valores absolutos, porque o erro do instrumento e o mesmo nos dois
> lados da comparacao.

## 2. Categorias tematicas — **CONVERGIRAM**

| # | Categoria | >500 RT | >100 RT | >10 RT | delta | humano >500 |
|---|---|---:|---:|---:|---:|---:|
| 3 | Restrictive policies | 31,8% | 27,4% | 23,4% | −8,4 | 34,8% |
| 4 | Disadvantages of vaccines | 16,2% | 14,3% | 12,5% | −3,7 | 24,8% |
| 6 | International | 11,0% | 9,9% | 8,2% | −2,9 | 16,6% |
| 10 | Information sources | 5,1% | 4,5% | 3,7% | −1,4 | 11,7% |
| 1 | Politics | 39,6% | 41,6% | 38,2% | −1,4 | 47,1% |
| 2 | Children | 31,8% | 30,8% | 30,6% | −1,2 | 38,8% |
| 11 | Science | 9,5% | 10,1% | 10,4% | +0,9 | 6,2% |
| 7 | Advantages of vaccines | 10,5% | 11,8% | 11,3% | +0,8 | 15,9% |
| 12 | Vaccines type or laboratories | 6,7% | 6,7% | 7,4% | +0,7 | 5,6% |
| 5 | Anti-vaccine people | 14,4% | 14,4% | 13,8% | −0,6 | 24,6% |
| 9 | Misinformation sources | 6,2% | 6,5% | 5,8% | −0,4 | 13,2% |
| 14 | Other drugs | 1,3% | 1,6% | 1,4% | +0,1 | 2,1% |
| 8 | COVID risks | 13,1% | 13,2% | 13,1% | −0,0 | 15,8% |
| 13 | Religion | 0,6% | 0,7% | 0,7% | +0,0 | 3,0% |

**A composicao tematica e estavel.** O maior deslocamento em 14
categorias e -8,4 pontos (Restrictive policies); a maioria fica dentro de ±2 pontos. Descer o
limiar de 500 para 10 RT multiplica o corpus por 19x e **nao** reordena os temas.

## 3. Leitura

Os dois eixos do mesmo experimento respondem de forma **oposta** a
sub-coleta, e e esse contraste que interessa a tese:

- **Analise de composicao tematica: convergiu.** O estrato viral ja
  representava bem a distribuicao de temas do corpus amplo. Coletar
  30x mais nao teria mudado essa conclusao do paper.
- **Analise de stance: mudou, e inverteu o sinal.** A leitura de que o
  polo anti-vacina tem presenca equivalente ou superior vale para o
  material que viralizou, nao para o debate. O proprio titulo do paper
  ('Political quarrel overshadows vaccination advocacy') se apoia numa
  leitura do estrato viral.

Ou seja: **nao e o trabalho que esta sub-coletado, e o tipo de analise
que tem sensibilidade diferente a sub-coleta.** Uma tabela de
prevalencia tematica aguenta o estrato viral; uma afirmacao sobre o
equilibrio de forcas do debate, nao.

## 4. Limitacoes

1. **O instrumento foi validado APENAS no estrato viral.** O kappa de
   0,759 foi medido contra o gabarito, que so existe para >500 RT.
   Tweets pouco viralizados podem ser sistematicamente diferentes
   (mais curtos, mais dependentes de contexto, mais respostas), e o
   desempenho do rotulador ali e **desconhecido**. Como a conclusao
   da secao 1 depende exatamente desse estrato nao validado, ela e
   provisoria ate que se meça o kappa la. **Proposta: rotular a mao
   uma amostra aleatoria de ~100 tweets do estrato <100 RT e medir.**
   E o unico teste que pode derrubar o achado principal.
2. Sinal a favor (nao substitui o teste acima): se o rotulador
   estivesse a deriva no estrato baixo, seria de esperar deriva
   tambem nas categorias. Elas ficam estaveis; so o stance se move.
3. O rotulador sub-marca categorias em relacao aos humanos (medido no
   teste cego). O vies **atenua** diferencas entre estratos, ou seja,
   joga contra a deteccao de mudanca — o lado seguro para a secao 2,
   mas nao neutraliza a limitacao 1.
4. `Advantages of vaccines` (kappa 0,376) e `Misinformation sources`
   (0,518) sao as categorias fracas do rotulador; leituras que
   dependam so delas precisam de ressalva.
5. O corpus e a re-coleta de mai/2022, com contagens de RT posteriores
   as do paper — os limiares nao sao exatamente os mesmos objetos.

---

## 5. E3 — a conclusão é do recorte de **termos** ou do fenômeno? (07/ago/2026)

> `analise/e3_por_termo.py` → `e3_por_termo.json`. Esquema `p6` (três classes).
> Casamento por regex sobre `originais.texto` (a coluna `hashtags` está vazia na
> fonte — ver [FASE1](FASE1_snapshot.md) Achado 1; o `texto` não está).
>
> ⚠ Os subconjuntos **se sobrepõem de propósito** — "vacina" é prefixo de quase
> todos os outros termos. Cada linha é "tweets que contêm o termo X", não "tweets
> trazidos exclusivamente por X".

### 5.1 O balanço pró × anti sobrevive a todos os termos

| termo-índice | n | %pró | %anti | %neutro | razão pró/anti |
|---|--:|--:|--:|--:|--:|
| vacina (genérico) | 16.980 | 41,4% | 29,4% | 29,2% | **1,41** |
| vacinação | 9.573 | 39,8% | 19,5% | 40,7% | 2,04 |
| vacinar | 4.083 | 48,8% | 28,8% | 22,5% | 1,70 |
| anti-vacinação | **7** | 57,1% | 28,6% | 14,3% | 2,00 |
| anti-vax | 796 | 75,5% | 10,2% | 14,3% | **7,42** |
| vacinação infantil | 1.022 | 54,0% | 10,8% | 35,2% | 5,02 |
| **corpus inteiro** | 29.978 | 41,1% | 25,5% | 33,4% | **1,61** |

**Em nenhum termo o lado anti é majoritário.** A magnitude varia muito (1,41 a
7,42), mas a **direção não se inverte em nenhum recorte** — é a evidência mais
forte até aqui de que a conclusão de AV6 não é artefato do recorte de termos.

**Dois achados de passagem:**

1. **Os termos "anti-*" não capturam discurso anti-vacina — capturam gente pró
   falando sobre anti-vaxxers.** Em `anti-vax`, 75,5% dos tweets são **pró** e
   83,9% caem na categoria *Anti-vaccine people*. O termo pensado para pegar um
   lado entrega o outro lado comentando sobre ele.
2. **Um dos seis termos-índice do artigo é inerte:** `anti-vacinação` traz
   **7 tweets** em 29.978. A lista de termos não é seis, na prática — é quatro.

### 5.2 Mas a composição **temática** é fortemente dependente do termo

Top-5 categorias por termo:

| termo | top-5 |
|---|---|
| vacina (genérico) | Politics 32,8% · Children 22,5% · Restrictive policies 20,5% · Disadvantages 17,7% · Advantages 16,5% |
| vacinação | Politics 51,2% · Children 44,8% · Restrictive policies 29,5% · COVID risks 11,4% · Science 10,6% |
| vacinar | **Children 53,4%** · Politics 34,2% · Restrictive policies 28,9% · Anti-vaccine people 14,4% |
| anti-vax | **Anti-vaccine people 83,9%** · Politics 20,0% · Restrictive policies 13,1% |
| vacinação infantil | **Children 88,4%** · Politics 64,9% · Restrictive policies 11,3% |

⚠ **Parte disso é tautológico** e precisa ser dito: selecionar por "vacinação
infantil" seleciona tweets sobre crianças. O ponto **não** é que a variação
surpreenda — é que **o ranking de enquadramentos publicado é função direta da lista
de termos**, e o artigo o apresenta como descrição do "debate vacinal". Como os
termos são desiguais em produtividade (16.980 × 796 × 7), o ranking publicado é, na
prática, o ranking dos termos genéricos.

### 5.3 O contraste que interessa à tese

A mesma afirmação (AV5, o ranking de enquadramentos) responde de forma **oposta** a
dois eixos de expansão:

| eixo | AV5 (enquadramento) | AV6 (balanço pró/anti) |
|---|---|---|
| **volume** (E1, descer o limiar) | ✅ **converge** (máx. −8,4 p.p.) | ✘ **muda** (48,4% → 62,6%) |
| **largura do filtro** (E3, por termo) | ✘ **muda muito** (Politics 32,8% × Anti-vaccine people 83,9%) | ✅ **não inverte** em nenhum termo |

Ou seja: **coletar mais do mesmo** não mexe no enquadramento, mas **mudar o filtro**
mexe — e o inverso vale para o balanço entre polos. Volume e largura de filtro são
eixos independentes, e uma conclusão robusta a um pode ser frágil ao outro.