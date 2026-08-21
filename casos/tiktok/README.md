# TikTok — infraestrutura de coleta (a célula ainda **sem alvo definido**)

> Criado em **18/ago/2026**. ⚠ **Isto ainda não é um caso de replicação** — é a
> infraestrutura de coleta, que independe de qual artigo virá a ocupar a célula
> TikTok da `tab:casos`. Quando o alvo for escolhido, nasce `casos/tiktok-<alvo>/`
> e reaproveita este `core/`.

---

## 1. O que se descobriu (18/ago/2026)

Levantando o terreno na **vm031**, apareceu algo que não estava em nenhum `.md`:

- o eTC tem um **coletor de TikTok pela API oficial** — `~/tweetcrawler/new-tiktok/`,
  mexido pela última vez em **jun/2025**, rodando em **loop contínuo**
  (`execute_tiktok.sh`), gravando em `eTC_Producao` no Postgres **local da vm031**;
- ele usa a **TikTok Research API v2** — `open.tiktokapis.com/v2/oauth/token/` +
  `/v2/research/video/query/`, com 14 campos por vídeo;
- a credencial (`client_key` / `client_secret`) está **hardcoded** no `main.py`
  (linhas ~332-333), não num `.env`;
- há também um coletor **antigo por scraping** (`~/tweetcrawler/tiktok/`, 2023, com
  automação de mouse e rotação de user-agent) — **superado** pelo da API oficial.

**A Mariana confirmou que não há nada coletado** — a decisão é usar a chave para
coletar **localmente**, no padrão dos outros casos (Fase 1 → snapshot congelado →
análise offline).

---

## 2. Como pôr para funcionar (2 comandos, 1 é seu)

**Passo 1 — importar a credencial** (precisa da VPN Cloud-DI de pé):

```
cd c:/Users/maria/Documents/dissertacao/casos/tiktok
python pipeline/importa_credencial_etc.py
```

Lê o `main.py` da vm031 e grava `TIKTOK_CLIENT_KEY` / `TIKTOK_CLIENT_SECRET` no
`.env` da raiz da dissertação. **O valor não aparece no terminal.**

> Por que este passo é seu e não do assistente: ler segredo de máquina remota é
> exatamente o que o modo automático bloqueia — e faz bem em bloquear. O script
> está pronto; só a execução é sua.

**Passo 2 — teste de fumaça** (gasta 1 chamada de cota):

```
python pipeline/testa_credencial.py
```

Autentica e faz **uma** consulta mínima. Se imprimir um vídeo de exemplo, a coleta
local está viável.

**Depois — coletar de verdade:**

```
python -u pipeline/coleta.py --hashtag <tag> --regiao BR \
       --inicio 20260101 --fim 20260331 --limite-chamadas 200
```

Sempre com `--dry-run` antes para ver o plano de janelas.

---

## 2b. ⚠ A credencial do eTC está MORTA — diagnóstico de 18/ago/2026

A Mariana importou a chave e o teste de fumaça falhou no **primeiro passo**, a
autenticação:

```
{'error': 'invalid_client',
 'error_description': 'Client info is illegal or malformed.'}
```

**Não é erro de cópia nem de código.** Verificado, nesta ordem:

| verificação | resultado |
|---|---|
| a chave no nosso `.env` é a mesma do `tweetcrawler`? | ✅ **sim** — `sha256` idêntico (comparado por hash, sem expor o valor) |
| os dois deployments (`tweetcrawler` e `tweetcrawler_teste`) usam chaves diferentes? | ❌ **não** — é a **mesma** credencial nos dois |
| formato | 16 chars (key) / 32 (secret) — o formato certo da Research API |
| a credencial **já funcionou**? | ✅ **sim** — o log de **19/jun/2025** registra `Access token acquired: clt.2.…` e uma coleta completa (`All pages collected. Inserting into database…`) |
| há erro de autenticação nos logs do eTC? | `invalid_client` aparece **0×** — quando parou de funcionar, ninguém estava olhando |

**Conclusão:** a credencial da Research API do eTC **foi revogada ou expirou** entre
jun/2025 e ago/2026. Aprovações da TikTok Research API são **por projeto e com prazo**;
sem renovação, o cliente morre silenciosamente.

**Isso explica o resto do quadro.** O coletor está **vivo mas ocioso** desde
24/jun/2025 — os últimos logs repetem *"Nenhuma busca agendada"*, e a única coleta
registrada foi um teste com o termo `lesma`. Bate exatamente com o que a Mariana já
sabia: **não há nada coletado**.

### O que destrava

1. **Renovar a aprovação do eTC** — quem gerencia a conta de desenvolvedor (o
   `execute_tiktok.sh` cita o **Tomaz**) precisa checar o status do app no portal da
   TikTok e renovar. Caminho mais curto se a conta ainda existir.
2. **Pedir credencial própria** — o **Brasil é região elegível** à Research API (a
   única fora de EUA/Europa; ver [BALANCO §7](../../BALANCO_2026-08-07.md)). É o caminho
   mais lento, e o melhor para a tese: credencial própria é o que torna a Fase 1
   **reproduzível por terceiros** — o mesmo critério que descartou a Meta Content
   Library no caso `meta-ads-imigracao`.

Enquanto nenhum dos dois acontecer, **a célula TikTok não coleta** — e o código deste
caso fica pronto e testado a seco, esperando uma chave viva.

---

## 3. ⚠ A cota é compartilhada — quando a chave voltar a funcionar

A credencial é **do app do eTC**, e o coletor da vm031 **roda em loop contínuo com
ela**. A cota da Research API é **por aplicação**, não por máquina: tudo o que for
gasto aqui **sai da mesma cota** da coleta contínua do grupo — e o inverso também.

Por isso `coleta.py` tem `--limite-chamadas` (default **200**) como teto rígido por
execução, no mesmo espírito do teto de gasto de LLM do caso vacinas. Antes de
qualquer coleta grande:

1. combinar com quem opera o crawler (os comentários do `execute_tiktok.sh` citam
   o **Tomaz**), **ou**
2. pedir credencial própria à TikTok (o Brasil **é** região elegível — é a única
   fora de EUA/Europa; registrado no [BALANCO de 07/ago](../../BALANCO_2026-08-07.md) §7).

A opção 2 é a que deixa o caso **auto-contido**, e tem um efeito colateral bom para
a tese: credencial própria é condição para que a Fase 1 seja **reproduzível por
terceiros** — o mesmo critério que fez a Meta Content Library ser descartada no caso
`meta-ads-imigracao` (dados que não saem do ambiente seguro quebram a Fase 1).

---

## 4. Limites da API que o cliente já respeita

| limite | como é tratado |
|---|---|
| `max_count` ≤ 100 por chamada | fixo em 100 |
| janela de uma query ≤ **30 dias** | `fatia_janela()` quebra o período automaticamente |
| paginação por `cursor` + `search_id` | laço até `has_more` = falso |
| token expira em ~2 h | renovado sozinho |
| HTTP 429 (cota/ritmo) | espera exponencial, com teto de tentativas |
| coleta interrompida | `collect_log` no SQLite — reexecutar **retoma** |

---

## 5. O que **falta decidir** (não é técnico)

O alvo. A `tab:casos` pede um artigo **publicado e com tração** para a célula TikTok,
e o candidato previsto (**#299, EDTok**) tem **2 citações e é só arXiv** — o mesmo
perfil que motivou o descarte do #207. Ter a coleta resolvida **não** resolve isso:
sem alvo, não há "ponto original" a replicar, e a linha da tabela mestre não fecha.

Duas saídas possíveis, ambas da Mariana:
1. **outro alvo de TikTok** publicado e citado (buscar no corpus da survey);
2. manter o EDTok assumindo a fraqueza de tração, e declarar isso no capítulo.

---

## 6. Estrutura

```
tiktok/
├── README.md                        <- este arquivo
├── core/
│   └── tiktok_api.py                <- cliente da Research API v2 (token, query, cota)
└── pipeline/
    ├── importa_credencial_etc.py    <- traz a chave da vm031 para o .env  ← rode você
    ├── testa_credencial.py          <- teste de fumaça (1 chamada)
    └── coleta.py                    <- Fase 1: snapshot SQLite resumível
```
