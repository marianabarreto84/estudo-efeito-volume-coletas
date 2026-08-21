# Confiabilidade intra-codificador — o teto da tarefa

n = 30 tweets re-rotulados as cegas pela mesma codificadora.

| Medida | κ |
|---|---:|
| **Mariana × Mariana** (teto da tarefa) | **0.746** |
| `p6` × Mariana, nos mesmos tweets | 0.648 |
| `p6` × Mariana, partição reservada (n=50) | 0,697 |
| Mariana × gabarito do paper (esquema binário) | 0,350 |

Acurácia da auto-concordância: 0.833

## Leitura

**Ha folga real entre o rotulador e o teto humano.** A codificadora e mais consistente consigo mesma do que o rotulador e com ela. A reprovacao da `p6` reflete limitacao do instrumento, nao do construto: ha o que ganhar com mais calibracao ou com um modelo maior.

## Ressalvas

1. **O reteste ocorreu no mesmo dia da rotulagem original.** A memória
   infla a auto-concordância, então este κ é um **limite superior
   otimista** do teto real. O viés joga contra o rotulador — faz o teto
   parecer mais alto e a máquina parecer pior —, o que torna o teste
   conservador para a decisão em questão.
2. n = 30: intervalo largo. Serve para distinguir ordens de grandeza
   (0,7 contra 0,95), não para precisão.
3. Os rótulos **originais** seguem canônicos nas validações já feitas.
   Este reteste mede consistência; não corrige nada retroativamente.
4. Confiabilidade intra-codificador é um teto mais frouxo que
   inter-codificador. O ideal seria um segundo codificador humano —
   que o artigo original teve (dois + árbitro) mas cujo κ não reportou.