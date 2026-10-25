# Plano de medição (PSM/CID)

Cada medida é descrita no template de instância do modelo de informação (*measurement construct*) da Aula 09: necessidade de informação, entidades, atributos, medidas básicas e derivadas, indicador, modelo de análise e critérios de decisão.

## Custo da hora

Para a categoria Recursos e Custos, a equipe adota um **custo de referência de R$ 15,00 por hora** de integrante, valor aproximado da hora de um estágio de 30 h semanais em desenvolvimento de software. O valor é uma convenção do projeto para comparar entregas e não representa pagamento real; se a equipe adotar outra fonte, o valor será corrigido aqui e em `scripts/psm_coleta.py`.

## 1. Planejado vs. concluído (Calendário e Progresso)

| Campo do template | Definição |
|---|---|
| Necessidade de informação | As tarefas planejadas para a sprint estão sendo concluídas? A entrega está em risco? |
| Conceito mensurável | Progresso das unidades de trabalho |
| Entidades | Issues de cada milestone (sprint) |
| Atributos | Situação da issue (aberta/fechada) |
| Medidas básicas | P = issues planejadas na sprint; C = issues fechadas da sprint |
| Método de medição | Contagem automática pela API do GitHub (`scripts/psm_coleta.py`) |
| Tipo de método | Objetivo |
| Escala e unidade | Inteiros ≥ 0; issue |
| Medida derivada | Percentual concluído |
| Função de medição | `PC = C / P × 100` |
| Indicador | Tabela por sprint e gráfico de barras (planejado × concluído) |
| Modelo de análise | Quanto maior a diferença entre planejado e concluído, maior o risco de não cumprir o marco da sprint |
| Critérios de decisão | Na metade da sprint, **PC < 50%**: redistribuir tarefas na reunião seguinte. No fim da sprint, **diferença > 10%**: registrar a causa em ata e replanejar o que ficou aberto (adaptado do CID, Parte 2, seção 8.3) |

<p class="legenda">Tabela 1. Instância do modelo de informação de Planejado vs. concluído. Fonte: elaboração própria a partir da Aula 09 e do PSM/CID (2021).</p>

## 2. Esforço estimado vs. realizado (Recursos e Custos)

| Campo do template | Definição |
|---|---|
| Necessidade de informação | As estimativas de esforço estão corretas? Qual o custo de cada entrega? |
| Conceito mensurável | Esforço da equipe / desempenho financeiro |
| Entidades | Issues de cada sprint |
| Atributos | Horas estimadas e horas realizadas |
| Medidas básicas | E = soma das horas estimadas (campo "Estimativa (horas)" da issue); R = soma das horas registradas em `dados/gestao/horas.csv` |
| Método de medição | 1. Estimativa feita pelo responsável ao abrir a issue. 2. Registro de horas pelo responsável ao concluir cada sessão de trabalho |
| Tipo de método | E: subjetivo; R: objetivo (registro) |
| Escala e unidade | Reais ≥ 0; hora |
| Medidas derivadas | Razão de esforço; custo realizado |
| Função de medição | `RE = R / E`; `Custo = R × R$ 15,00` |
| Indicador | Tabela por sprint e por integrante; gráfico estimado × realizado |
| Modelo de análise | RE > 1: a equipe subestimou; RE < 1: superestimou |
| Critérios de decisão | **RE > 1,3** em uma sprint: revisar as estimativas das issues restantes e dividir tarefas grandes. **Integrante com menos de 10% das horas da sprint**: discutir a distribuição na reunião seguinte |

<p class="legenda">Tabela 2. Instância do modelo de informação de Esforço estimado vs. realizado. Fonte: elaboração própria a partir da Aula 09 e do PSM/CID (2021).</p>

## 3. Tempo de ciclo (Desempenho dos Processos)

| Campo do template | Definição |
|---|---|
| Necessidade de informação | Quanto tempo uma tarefa leva entre ser aberta e ser concluída? Há tarefas paradas? |
| Conceito mensurável | Eficiência do processo (velocidade) |
| Entidades | Issues fechadas e abertas |
| Atributos | Data de criação, data de fechamento, data da última atualização |
| Medidas básicas | `tc` = data de criação; `tf` = data de fechamento; `tu` = última atualização |
| Método de medição | Leitura automática das datas pela API do GitHub |
| Tipo de método | Objetivo |
| Escala e unidade | Reais ≥ 0; dia |
| Medida derivada | Tempo de ciclo; idade sem atualização |
| Função de medição | `TC = tf − tc` (média e mediana por sprint); `Idade = hoje − tu` para issues abertas |
| Indicador | Tabela por sprint e lista de issues paradas |
| Modelo de análise | Tempo de ciclo alto indica tarefas grandes demais ou bloqueadas |
| Critérios de decisão | **Issue aberta sem atualização há mais de 3 dias**: o responsável informa o bloqueio ou a tarefa é dividida. **Mediana do tempo de ciclo > 5 dias** em uma sprint de 7 dias: dividir as tarefas da sprint seguinte |

<p class="legenda">Tabela 3. Instância do modelo de informação de Tempo de ciclo. Fonte: elaboração própria a partir da Aula 09 e do PSM/CID (2021), Parte 2, seção 8.5.</p>

## Sprints da Entrega 1

| Sprint (milestone) | Período | Objetivo |
|---|---|---|
| Sprint 1 | 13/10 a 19/10/2026 | Primeira versão da Fase 1 |
| Sprint 2 | 20/10 a 26/10/2026 | Revisão da Fase 1, Fase 2, artigo, GitPage e release E1 |

<p class="legenda">Tabela 4. Sprints da Entrega 1. Fonte: elaboração própria.</p>
