# Sondagem à DBD/PUC-Rio — direitos de TDM nas assinaturas

> Preparado em **9/set/2026**. A Mariana envia; nada aqui foi enviado por script.
> Existe porque a rota do proxy fechou por inteiro
> ([EXPANSAO_recuperacao.md §4b](../EXPANSAO_recuperacao.md)) e a rota **sancionada**
> para o mesmo fim é a API de TDM das editoras — que depende do contrato de
> assinatura, não de configuração técnica.

---

## 1. Por que perguntar isto, e não só tentar

O estrato comercial do corpus (10.230 artigos em *paywall*) ficou inalcançável por
três vias, nesta ordem:

| Via | Estado |
|---|---|
| Rotas de acesso aberto (Unpaywall, OpenAlex, S2, arXiv) | ✅ **esgotada** — censo de 11.093 tentativas, 811 recuperados (7,3%) |
| *Proxy* institucional, acesso programático | ⛔ **fechada** — todas as editoras servem desafio anti-automação; a Springer devolve HTTP 200 com 3 KB de *client challenge* no *endpoint* do PDF |
| Contorno do desafio (`curl_cffi`, Playwright) | ⛔ **recusado por decisão** — é burlar controle anti-automação, e o risco recai sobre o acesso da PUC-Rio inteira |

A quarta via é a legítima: **as editoras vendem/licenciam exatamente este uso**, sob
o nome de *Text and Data Mining* (TDM). Se o contrato da PUC-Rio já inclui direitos
de TDM para pesquisa não comercial — o que é comum —, existe uma API que entrega o
texto completo em massa, com a bênção da editora e sem desafio nenhum.

**A pergunta é contratual, não técnica.** Por isso vai para a DBD.

## 2. O que já se sabe (para não perguntar o óbvio)

- A Springer Nature tem três APIs no [dev.springernature.com](https://dev.springernature.com/):
  **Meta** (metadados e resumos) e **Open Access** (texto completo de OA), ambas com
  chave gratuita; e a **Full Text / TDM API**, que libera texto completo de conteúdo
  **assinado** e exige que a titularidade institucional esteja vinculada à chave.
- Os termos do portal dizem que assinantes institucionais podem extrair conteúdo a
  que têm acesso **"and TDM rights under their institutional license agreement"** —
  ou seja, o direito vem do contrato, e varia de instituição para instituição.
- Para pesquisa **não comercial**, a Springer declara o TDM permitido; o produto pago
  é para uso comercial.
- Elsevier e ACM têm equivalentes (`api.elsevier.com`, ACM Digital Library TDM).

## 3. A mensagem (copiar e enviar)

> **Assunto:** Direitos de *text and data mining* (TDM) nas assinaturas — pesquisa de mestrado
>
> Prezados,
>
> Sou mestranda em Informática na PUC-Rio, orientada pelo Prof. Sérgio Lifschitz, e
> estou finalizando uma revisão sistemática de literatura sobre métodos de coleta de
> dados em redes sociais digitais. O levantamento cataloga 13.395 artigos indexados
> pelo DBLP, dos quais preciso ler o texto completo para extrair, de cada um, como a
> coleta de dados foi feita.
>
> Consegui recuperar por vias de acesso aberto tudo o que era recuperável — uma
> varredura completa de 11.093 artigos, com 811 recuperações. O restante está em
> conteúdo assinado, e é aí que gostaria da orientação de vocês.
>
> Minhas perguntas são três:
>
> 1. **O contrato da PUC-Rio com a Springer Nature inclui direitos de *text and data
>    mining* para pesquisa acadêmica não comercial?** Em caso afirmativo, qual o
>    procedimento para obter uma chave da *Full Text API*
>    (dev.springernature.com) vinculada à titularidade institucional? Seriam cerca
>    de **2.000 artigos** da Springer no meu corpus.
>
> 2. **A mesma pergunta se aplica a Elsevier, ACM e IEEE?** São as demais editoras com
>    volume relevante no levantamento, e todas oferecem interfaces de TDM.
>
> 3. Caso não haja direito de TDM contratado, **qual a orientação da DBD para download
>    manual em volume** por meio do proxy institucional, feito artigo a artigo pela
>    própria pesquisadora? Pergunto porque quero manter o trabalho dentro do que os
>    contratos permitem, e prefiro reduzir o tamanho da amostra a fazer algo que
>    coloque o acesso institucional em risco.
>
> Registro que **não** tentei contornar nenhum controle técnico das editoras: onde
> encontrei verificação anti-automação, interrompi e vim perguntar.
>
> Fico à disposição para detalhar o projeto ou fornecer a lista de DOIs.
>
> Atenciosamente,
> Mariana Porto Barreto — Mestrado em Informática, PUC-Rio

## 4. Como ler a resposta

| Resposta | O que fazer |
|---|---|
| **Há TDM contratado na Springer** | Melhor desfecho. Chave da Full Text API + cliente novo; ~2.000 artigos automatizados e sancionados, sem tempo de clique. Provavelmente vale também para os outros ~1.900 da IEEE se o contrato for equivalente |
| **Não há TDM, mas o download manual é aceitável** | Vale a sonda humano-no-laço: amostra de ~200, ~1 h de clique. ⚠ com o poder declarado — n=200 detecta diferenças de ~15 p.p., **não** os 2–6 p.p. que a aposta da §6 prevê |
| **Não há TDM e o manual em volume é desaconselhado** | Fecha a questão. O artigo já está escrito para este desfecho: a ameaça à validade nº 2 trata o estrato comercial como **limite estrutural**, com a verificação de set/2026 em nota de rodapé. Nada a mudar |

⚠ **Nenhum desses desfechos bloqueia a defesa.** A survey está fechada e o
`survey-1.pdf` já reporta a situação medida. Isto é ganho marginal, não pendência.

## 5. Um ganho lateral, independente da resposta

A API **Meta** da Springer é **gratuita** e entrega **resumos**. A coluna `abstract`
do `research.db` está **vazia nos 13.395** — o que já custou uma medição descartada
(ver [DIAGNOSTICO_tipos_de_analise.md](DIAGNOSTICO_tipos_de_analise.md) §1, onde um
teste sobre título+resumo rodou de fato só sobre o título). Preencher resumos via
Crossref/OpenAlex/Meta API é gratuito, não depende de contrato nenhum e conserta essa
lacuna — mas ⛔ **não** serve para extrair campos da survey: seria um segundo
instrumento no mesmo corpus, que é o que o diagnóstico proíbe misturar.
