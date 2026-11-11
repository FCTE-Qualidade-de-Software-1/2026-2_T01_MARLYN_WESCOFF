# Dados

| Pasta | Conteúdo |
|---|---|
| `gestao/` | Dados da gestão do projeto (PSM/CID) |
| `gestao/horas.csv` | Registro de horas da E1, **descontinuado** (as atividades foram migradas para `esforco.csv`) |
| `gestao/psm-AAAA-MM-DD.csv` | Retratos gerados por `scripts/psm_coleta.py` |
| `avaliacao/` | Dados brutos das medições da Fase 4, uma subpasta por métrica (`M1.1/`, `M2.3/`, ...) |

## Apontamento de esforço

Desde a E2, as horas ficam em [`docs/metricas/dados/brutos/esforco.csv`](../docs/metricas/dados/brutos/esforco.csv), o único arquivo de preenchimento manual da gestão PSM/CID. Uma linha por sessão de trabalho.

| Coluna | Formato | Exemplo |
|---|---|---|
| `data` | AAAA-MM-DD | 2026-11-12 |
| `membro` | Nome como em `docs/sobre/equipe.md` | Pedro Goncalves Rocha |
| `fase` | `1` a `4`, ou vazio para trabalho transversal (artigo, gestão) | 3 |
| `tipo_atividade` | `reuniao`, `pesquisa`, `documentacao`, `coleta`, `analise`, `artigo`, `gestao` ou `revisao` | documentacao |
| `issue` | Número da issue com `#` (vazio se não houver) | #21 |
| `horas` | Número com ponto decimal | 1.5 |
| `tipo_registro` | `registrado` (anotado no dia) ou `reconstruido` (estimado depois, em consenso da equipe) | registrado |
| `observacao` | Texto curto, **sem vírgulas** | Construtos de Calendário e Progresso |

Regras:

- Registrar no mesmo dia, ao terminar a sessão, com `tipo_registro = registrado`.
- Nunca apagar nem alterar linhas de outra pessoa. Uma correção vira uma nova linha, explicada em `observacao`.
- Linhas sem horas são ignoradas por `scripts/psm_coleta.py`.

### Horas da Entrega 1 (reconstrução)

A E1 não teve registro de horas no dia. As atividades listadas antes em `gestao/horas.csv` foram migradas para `esforco.csv` com `data` e `horas` em branco e `tipo_registro = reconstruido`. Cada integrante, na reunião de reconstrução:

1. preenche a **data** e as **horas** das próprias linhas, pela melhor estimativa;
2. apaga as linhas de atividades que não fez e acrescenta as que faltaram, também como `reconstruido`;
3. divide em várias linhas a atividade feita em dias diferentes.

Essas horas são estimativas feitas depois. A limitação é declarada nas ameaças à validade do artigo e não pode ser apresentada como medição.

## Dados de participantes

Se houver entrevistas ou testes com pessoas, os nomes são substituídos por códigos (P1, P2, ...). Gravações e termos de consentimento assinados não são versionados em repositório público; a forma de acesso é combinada com a docente.
