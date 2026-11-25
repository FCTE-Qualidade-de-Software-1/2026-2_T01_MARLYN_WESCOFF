# Fase 4: execução e resultados

A Fase 4 executou as 12 métricas planejadas na [Fase 3](../fase-3/plano-de-avaliacao.md), converteu cada valor em nota pelos [níveis da Fase 2](../fase-2/niveis-e-julgamento.md), respondeu às questões e julgou os três objetivos. Também executou e mediu uma ação de melhoria.

| Página | O que mostra |
|---|---|
| [Plano de execução](plano-de-execucao.md) | Quem coletou cada métrica, quando, com qual evidência, e como o dado vira julgamento |
| [Resultados e julgamento](resultados.md) | Valor, nota e hipótese de cada métrica, resposta às questões, julgamento de G1 a G3 com análise de sensibilidade, relações entre as características, problemas encontrados e limitações |
| [Árvore GQM de resultados](arvore-gqm-resultados.md) | O GQM lido de baixo para cima, gerado de `calculos.csv` |
| [Ação de melhoria](acao-de-melhoria.md) | Problema escolhido, prioridade, ação e medição antes e depois |

<p class="legenda">Tabela 1. Páginas da Fase 4. Fonte: elaboração própria.</p>

## Em uma frase

Pelo critério congelado, **G3 (Flexibilidade) atende**, **G2 (Compatibilidade) atende com ressalvas** (nota 2 em M2.4, pela coexistência durante a instalação) e **G1 (Adequação funcional) não atende**, por uma nota 1 em M1.2 que vem da exibição do total em soma natural (caso A-04), e não de cálculo errado. Numa análise de sensibilidade, G1 atende. A ação de melhoria eliminou a interferência da instalação em aplicações vizinhas do servidor.

## Evidências

Todos os dados brutos, logs, capturas e scripts estão no repositório, em [`dados/avaliacao/`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/), com um README por métrica que descreve o procedimento, os desvios e as tentativas descartadas. Os números consolidados estão em [`calculos.csv`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/calculos.csv) e são calculados por `scripts/calcula_julgamento.py`.
