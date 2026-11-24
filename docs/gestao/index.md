# Gestão do projeto (PSM/CID)

Esta seção explica, para um leitor externo, como a equipe acompanha o projeto de avaliação do Moodle 5.3 LTS. O modelo adotado é o **PSM** (*Practical Software and Systems Measurement*), complementado pelo **CID** (*Continuous Iterative Development Measurement Framework*). Cada medida parte de uma necessidade de informação, produz um indicador verificável e apoia uma decisão de gestão.

## 1. Necessidades de informação

No PSM, a medição não começa por um objetivo nem por uma pergunta: começa pelas **necessidades de informação** do projeto, isto é, os riscos, os problemas e a falta de informação que a gestão precisa acompanhar. Cada necessidade abaixo nasceu de uma evidência do [diagnóstico do repositório](../metricas/01-diagnostico-repositorio.md) e levou a uma das três categorias de informação exigidas pela especificação do trabalho.

| Necessidade de informação | Tipo | Origem | Categoria de informação |
|---|---|---|---|
| **N1.** O trabalho comprometido para cada marco (PC2 e E2) será concluído no prazo? Quais produtos de trabalho estão em risco? | Risco | Todo o conteúdo da E1 entrou na `main` na véspera do prazo, e o PC1 não foi apresentado | Calendário e Progresso |
| **N2.** Quanto tempo uma tarefa leva, o ritmo da equipe basta para o escopo que falta e a revisão interna encontra os problemas antes da docente? | Problema | As issues da E1 foram abertas e fechadas em lote, sem revisão registrada, e houve duas semanas sem progresso entre a E1 e a E2 | Desempenho dos Processos |
| **N3.** Quanto esforço o projeto consome, como ele se distribui entre os integrantes e as estimativas servem para planejar? | Falta de informação | Nenhuma hora foi registrada na E1 | Recursos e Custos |

<p class="legenda">Tabela 1. Necessidades de informação da gestão do projeto, com o tipo, a origem e a categoria. Fonte: elaborado pelos autores a partir do diagnóstico do repositório e da Aula 09.</p>

Esta seção trata da **gestão do projeto**. A avaliação da qualidade do Moodle segue outro modelo, o GQM da [Fase 2](../fase-2/index.md), que parte de objetivos e questões sobre o produto. Os dois não se misturam.

## 2. Do modelo de informação à decisão

Cada necessidade segue a ordem do modelo de informação do PSM: necessidade de informação → categoria → conceito mensurável → medidas → indicador → critério de decisão → decisão.

| Necessidade de informação | Categoria | Conceito mensurável | Medidas | Indicador | Critério de decisão (exemplo) |
|---|---|---|---|---|---|
| N1 | Calendário e Progresso | Progresso das unidades de trabalho; conclusão de marcos | A1 Burndown; A2 Comprometido × concluído; A3 Fluxo cumulativo; A4 Conclusão de marcos | Burndown por marco e colunas comprometido × concluído por semana | Diferença maior que 10% entre comprometido e concluído: replanejar a semana seguinte |
| N2 | Desempenho dos Processos | Eficiência do processo (velocidade) e efetividade da revisão | B1 Cycle time; B2 Velocidade; B3 Frequência de entregas; B4 Retrabalho | Histograma de cycle time e velocidade com projeção | Projeção de semanas restantes maior que o prazo: decisão de escopo |
| N3 | Recursos e Custos | Esforço de pessoal e acurácia da estimativa | C1 Esforço; C2 Contribuição; C3 Estimado × real | Horas por integrante e por fase; custo estimado × realizado | Acurácia fora de 0,85 a 1,25: recalibrar as estimativas |

<p class="legenda">Tabela 2. Ligação entre necessidade de informação, medidas, indicador e critério de decisão. Fonte: elaborado pelos autores a partir dos construtos de medição.</p>

As fórmulas, unidades, fontes, limitações e limiares de decisão estão na página de [Construtos de medição](../metricas/02-construtos-de-medicao.md). Essa especificação separa as medidas de gestão do projeto das métricas de qualidade do produto definidas na [Fase 2](../fase-2/index.md): as primeiras acompanham a execução do projeto; as segundas avaliam o Moodle.

## 3. Indicadores

O [Dashboard dos indicadores de gestão](../metricas/dashboard.md) apresenta o retrato mais recente das oito medidas, compara cada valor com seu limiar e reúne os gráficos nas três categorias. A página é gerada automaticamente a partir dos CSVs consolidados, evitando que números sejam copiados manualmente.

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
| Quadro | [Marlyn Wescoff - Gestão do projeto (PSM/CID)](https://github.com/orgs/FCTE-Qualidade-de-Software-1/projects/54), na organização da disciplina; o [quadro anterior](https://github.com/users/cadumotta/projects/1) guarda as movimentações de 10 a 24/11 |

<p class="legenda">Tabela 3. Pontos de acesso aos artefatos verificáveis da gestão. Fonte: elaborado pelos autores.</p>

## Relação com as fases da avaliação

- A [Fase 1](../fase-1/index.md) define propósito, partes interessadas, produto e escopo.
- A [Fase 2](../fase-2/index.md) especifica as métricas de qualidade do produto.
- A [Fase 3](../fase-3/plano-de-avaliacao.md) planeja a execução e os recursos necessários.
- A [Fase 4](../fase-4/plano-de-execucao.md) obtém as medidas do produto, julga os objetivos e executa a ação de melhoria.

As medidas e os indicadores do PSM/CID acompanham o trabalho necessário para produzir e revisar os artefatos dessas quatro fases.
