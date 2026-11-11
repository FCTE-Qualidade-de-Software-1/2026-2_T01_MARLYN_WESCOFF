# Gestão do Projeto - Métricas PSM/CID

Esta seção explica, para um leitor externo, como a equipe acompanha o projeto de avaliação do Moodle 5.3 LTS. O modelo adotado é o **PSM** (*Practical Software and Systems Measurement*), complementado pelo **CID** (*Continuous Iterative Development Measurement Framework*). Cada medida parte de uma necessidade de informação, produz um indicador verificável e apoia uma decisão de gestão.

## 1. Objetivo da medição

O objetivo é acompanhar a execução do projeto quanto a **calendário e progresso**, **desempenho dos processos** e **recursos e custos**, permitindo identificar desvios antes dos marcos PC1, E1, E2 e Apresentação. O [diagnóstico do repositório](../metricas/01-diagnostico-repositorio.md) registra as limitações encontradas; os [construtos de medição](../metricas/02-construtos-de-medicao.md) definem previamente como cada valor é calculado e interpretado.

## 2. Medidas

| Categoria de informação | Pergunta de gestão | Medidas obrigatórias |
|---|---|---|
| Calendário e Progresso | O trabalho comprometido será concluído no prazo e está fluindo pelo quadro? | A1 Burndown; A2 Comprometido × concluído; A3 Fluxo cumulativo |
| Desempenho dos Processos | A equipe conclui tarefas em tempo previsível e com capacidade suficiente? | B1 Cycle time; B2 Velocidade |
| Recursos e Custos | O esforço está equilibrado e as estimativas são confiáveis? | C1 Esforço; C2 Contribuição; C3 Estimado × real |

<p class="legenda">Tabela 1. Medidas obrigatórias da gestão do projeto. Fonte: elaborado pelos autores a partir dos construtos PSM/CID adotados.</p>

As fórmulas, unidades, fontes, limitações e limiares de decisão estão na página de [Construtos de medição](../metricas/02-construtos-de-medicao.md). Essa especificação separa as métricas de gestão das métricas de qualidade do produto definidas na [Fase 2](../fase-2/index.md): as primeiras acompanham a execução do projeto; as segundas avaliam o Moodle.

## 3. Indicadores

O [Dashboard das métricas](../metricas/dashboard.md) apresenta o retrato mais recente das oito medidas, compara cada valor com seu limiar e reúne os gráficos nas três categorias. A página é gerada automaticamente a partir dos CSVs consolidados, evitando que números sejam copiados manualmente.

O caminho de rastreabilidade é:

1. [dados brutos](../metricas/dados/brutos/README.md), extraídos do Git, das issues, dos pull requests, do quadro e do apontamento de esforço;
2. [dados consolidados](../metricas/dados/consolidados/README.md), calculados pelos scripts;
3. [dashboard](../metricas/dashboard.md), com valores atuais, limiares e gráficos;
4. [registro de decisões](../metricas/03-registro-de-decisoes.md), que documenta a interpretação e a ação tomada.

## 4. Decisões

Um indicador fora do limiar não é tratado como nota do projeto. Ele inicia uma análise: a equipe verifica a causa, define responsável e prazo, registra a evidência e mede posteriormente o efeito. O [Registro de decisões de gestão](../metricas/03-registro-de-decisoes.md) mantém essa ligação entre medida, valor observado, decisão e resultado.

As [medições históricas](registro-medicoes.md) preservam os retratos anteriores, enquanto as [atas](atas.md) registram o contexto das reuniões. O dashboard é a fonte atual; as páginas históricas não repetem os construtos nem substituem os consolidados.

## Repositório e evidências

| Recurso | Link |
|---|---|
| Repositório | [Código e documentação](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF) |
| Releases | [Entregas publicadas](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/releases) |
| Tags | [Versões marcadas](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/tags) |
| CSVs brutos | [Diretório de dados brutos](../metricas/dados/brutos/README.md) |
| CSVs consolidados | [Diretório de dados consolidados](../metricas/dados/consolidados/README.md) |
| Scripts | [Diretório `scripts/`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/tree/main/scripts) |
| Quadro | [Marlyn Wescoff - Gestão PSM/CID](https://github.com/users/cadumotta/projects/1) |

<p class="legenda">Tabela 2. Pontos de acesso aos artefatos verificáveis da gestão. Fonte: elaborado pelos autores.</p>

## Relação com as fases da avaliação

- A [Fase 1](../fase-1/index.md) define propósito, partes interessadas, produto e escopo.
- A [Fase 2](../fase-2/index.md) especifica as métricas de qualidade do produto.
- A [Fase 3](../fase-3/plano-de-avaliacao.md) planeja a execução e os recursos necessários.
- A [Fase 4](../fases-3-4.md#fase-4-executar-a-avaliacao-prevista) obtém as medidas do produto, julga os objetivos e executa a ação de melhoria.

As métricas PSM/CID acompanham o trabalho necessário para produzir e revisar os artefatos dessas quatro fases.
