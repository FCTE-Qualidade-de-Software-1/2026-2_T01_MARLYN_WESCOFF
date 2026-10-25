# Dados

| Pasta | Conteúdo |
|---|---|
| `gestao/` | Dados da gestão do projeto (PSM/CID) |
| `gestao/horas.csv` | Registro de horas: uma linha por sessão de trabalho |
| `gestao/psm-AAAA-MM-DD.csv` | Retratos gerados por `scripts/psm_coleta.py` |
| `avaliacao/` | Dados brutos das medições da Fase 4, uma subpasta por métrica (`M1.1/`, `M2.3/`, ...) |

## Formato de `gestao/horas.csv`

| Coluna | Formato | Exemplo |
|---|---|---|
| `data` | AAAA-MM-DD | 2026-10-24 |
| `membro` | Nome como em `docs/sobre/equipe.md` | Pedro Goncalves Rocha |
| `issue` | Número da issue, sem `#` (vazio se não houver) | 12 |
| `atividade` | Texto curto, **sem vírgulas** | Revisão das métricas de G2 |
| `horas` | Número com ponto decimal | 1.5 |

## Como preencher as horas da Entrega 1

O arquivo já lista as atividades de cada integrante, com `data` e `horas` em branco. Cada um:

1. preenche a **data** (AAAA-MM-DD) e as **horas reais** das próprias linhas;
2. apaga as linhas de atividades que não fez e acrescenta linhas para o que faltou;
3. divide em várias linhas a atividade feita em dias diferentes.

Linhas sem horas são ignoradas por `scripts/psm_coleta.py`.

## Dados de participantes

Se houver entrevistas ou testes com pessoas, os nomes são substituídos por códigos (P1, P2, ...). Gravações e termos de consentimento assinados não são versionados em repositório público; a forma de acesso é combinada com a docente.
