# Construtos de medição

Este documento especifica as medidas da gestão do projeto pelo modelo de informação do PSM e da ISO/IEC/IEEE 15939, com as medidas e os limiares do *PSM Continuous Iterative Development Measurement Framework* v2.1 (PSM CID). Ele amplia as três medidas iniciais do [Plano de medição](../gestao/plano-psm.md) e parte das lacunas levantadas no [Diagnóstico do repositório](01-diagnostico-repositorio.md).

Os limiares de decisão foram **declarados antes da análise** dos dados da E2, em 10/11/2026. Uma mudança posterior de limiar vira uma decisão registrada, com justificativa, e não substitui o valor original.

## Objetivo de medição

> Acompanhar a execução do projeto de avaliação quanto a **progresso**, **eficiência de processo** e **consumo de recursos**, de modo a permitir decisões de gestão tempestivas que assegurem as entregas nos marcos da disciplina.

As três categorias de informação exigidas pela especificação do trabalho são cobertas assim:

| Categoria de informação (PSM CID) | Medidas |
|---|---|
| Calendário e Progresso (*Schedule and Progress*) | A1 Burndown da entrega; A2 Comprometido x concluído; A3 Fluxo cumulativo; A4 Conclusão de marcos |
| Desempenho dos Processos (*Process Performance*) | B1 Cycle time e lead time; B2 Velocidade e aceleração; B3 Frequência de entregas; B4 Retrabalho e não conformidades |
| Recursos e Custos (*Resources and Cost*) | C1 Esforço da equipe; C2 Distribuição de contribuição; C3 Estimado x real |

<p class="legenda">Tabela 1. Categorias de informação e medidas da gestão do projeto. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5.</p>

## Adaptação da terminologia do CID

O CID foi escrito para o desenvolvimento iterativo de software. Este projeto não desenvolve software: ele executa uma **avaliação de qualidade de produto** (ISO/IEC 25040, Fases 1 a 4), cujo resultado é um artigo, uma GitPage e uma ação de melhoria. Os termos do CID foram adaptados assim:

| Termo do CID | Equivalente neste projeto | Onde aparece no repositório |
|---|---|---|
| *Capability* / *Epic* | Fase do processo de avaliação (Fase 1 a 4) | Label `fase/N` |
| *Feature* | Produto de trabalho: plano de avaliação, instrumento de coleta, seção do artigo, página da GitPage | Arquivo ou página entregue |
| *Story* | Tarefa rastreada em uma issue | Issue com o modelo Tarefa |
| *Task* | Subtarefa da issue | Item do checklist "Critério de pronto" |
| Iteração / *Sprint* | Semana de trabalho, de segunda a domingo (semana ISO) | Campo "Iteração" do board; retrato semanal de segunda-feira |
| *Release* / *Deployment* | Entrega de um marco da disciplina | Milestone e release com tag (`E1`, `PC1`, `E2`, `Apresentação`) |
| *Backlog* | Issues abertas ainda não alocadas a uma iteração | Coluna "Backlog" do board |
| *Story points* | Tamanho relativo da issue | Label `tamanho/P` (1 ponto), `tamanho/M` (3) ou `tamanho/G` (8) |
| Defeito | Não conformidade num produto de trabalho, apontada em revisão interna (contida) ou pela docente num ponto de controle (escapada) | Comentário de revisão no PR; issue com label `retrabalho` |
| Retrabalho | Issue reaberta ou produto de trabalho revisado depois de crítica | Evento `reopened`; label `retrabalho` |

<p class="legenda">Tabela 2. Adaptação da terminologia do PSM CID ao projeto de avaliação. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1.</p>

## Definição de pronto

Uma issue só conta como **concluída** nas medidas A1, A2, B1 e B2 quando atende a todos os itens:

1. Está fechada por um pull request mergeado na `main`, com aprovação de um integrante diferente do autor. Issues sem alteração de arquivo (por exemplo, criar milestones) fecham com um comentário que descreve o que foi feito e quem conferiu.
2. Todos os itens do "Critério de pronto" da issue estão marcados.
3. A GitPage gera sem aviso (`mkdocs build --strict`) quando a issue altera `docs/`, e o artigo compila quando altera `artigo/`.
4. As horas da issue estão lançadas em `esforco.csv`.

Uma issue fechada sem esses requisitos é reaberta e conta como retrabalho (B4).

## Calendário e Progresso

### A1. Burndown da entrega

| Campo | Definição |
|---|---|
| Identificador | A1 |
| Categoria de informação | Calendário e Progresso |
| Necessidade de informação | O trabalho comprometido para a entrega será concluído no prazo? Quais produtos de trabalho estão em risco? |
| Conceito mensurável | Progresso das unidades de trabalho (*Work Unit Progress*) |
| Entidades relevantes | Issues do milestone da entrega (E2, PC1, Apresentação) |
| Atributos | Estado (aberta ou fechada), data de fechamento, tamanho (`tamanho/P`, `M` ou `G`) |
| Medidas básicas | `Planejado` = soma dos pontos das issues do milestone na data de corte do dia (inteiro, maior ou igual a 0); `Concluído(d)` = soma dos pontos das issues do milestone fechadas até o dia `d` (inteiro, maior ou igual a 0) |
| Método de medição | Contagem automática pela API do GitHub (issues e eventos `closed`, `reopened`, `milestoned`, `labeled`) |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Inteiros maiores ou iguais a 0; razão |
| Unidade de medida | Pontos de tamanho (P = 1, M = 3, G = 8) |
| Função de medição | `Aberto(d) = Planejado(d) - Concluído(d)`; `Ideal(d) = Planejado(d0) x (1 - (d - d0) / (dF - d0))`, com `d0` = início da entrega e `dF` = prazo do milestone; `Desvio(d) = (Aberto(d) - Ideal(d)) / Planejado(d0) x 100` |
| Medida derivada | Trabalho aberto por dia e desvio percentual em relação à linha ideal |
| Modelo de análise | Curva de trabalho aberto acima da linha ideal indica atraso; um degrau para cima indica escopo acrescentado ao milestone |
| Indicador | Gráfico de linhas: trabalho aberto x linha ideal, por milestone, com linhas verticais nos marcos |
| Critérios de decisão | **Desvio maior que 5%** acima da linha ideal: a causa é analisada na reunião semanal seguinte. **Desvio maior que 10%**: replanejamento do escopo da entrega ou realocação de issues entre integrantes, registrado como decisão de gestão (PSM CID, Parte 2, 8.2) |
| Procedimento de coleta | Extração diária ou a cada push pelos scripts da Etapa 4; fonte: GitHub Issues; responsável: scripts, sem intervenção manual |
| Procedimento de análise | Na reunião semanal (segunda-feira), pelo responsável pela gestão PSM/CID da semana, a partir do retrato semanal |

<p class="legenda">Tabela 3. Construto da medida A1, burndown da entrega. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.2.</p>

Limitação: na E1, as issues foram criadas e fechadas em lote (ver o Diagnóstico, lacuna L3). O burndown da E1 é mostrado só como registro histórico e não serve de referência.

### A2. Comprometido x concluído

| Campo | Definição |
|---|---|
| Identificador | A2 |
| Categoria de informação | Calendário e Progresso |
| Necessidade de informação | A equipe entrega o que se compromete a entregar em cada iteração? |
| Conceito mensurável | Progresso das unidades de trabalho (*Work Unit Progress*) |
| Entidades relevantes | Issues atribuídas a uma iteração (semana) no board |
| Atributos | Iteração atribuída, estado, data de fechamento, atendimento à definição de pronto |
| Medidas básicas | `Comprometidos(s)` = issues com a iteração `s` no board no retrato de segunda-feira; `Concluídos(s)` = dessas, as fechadas até domingo e que atendem à definição de pronto |
| Método de medição | Leitura automática do campo "Iteração" do board e do estado das issues pela API do GitHub |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Inteiros maiores ou iguais a 0; razão |
| Unidade de medida | Issues |
| Função de medição | `PC(s) = Concluídos(s) / Comprometidos(s) x 100`; `Diferença(s) = 100 - PC(s)`; `PC acumulado = soma dos concluídos / soma dos comprometidos x 100` |
| Medida derivada | Percentual concluído por semana e acumulado |
| Modelo de análise | Diferença persistente indica que a equipe se compromete com mais do que consegue fazer, ou que as issues são grandes demais para uma semana |
| Indicador | Gráfico de colunas comprometido x concluído por semana, com a linha do percentual acumulado |
| Critérios de decisão | **Diferença maior que 5%** numa semana: a causa é investigada na reunião seguinte. **Diferença maior que 10%**: ação corretiva (reduzir o compromisso da semana seguinte ou dividir as issues grandes), registrada como decisão de gestão (PSM CID, Parte 2, 8.3) |
| Procedimento de coleta | Retrato automático toda segunda-feira (`psm-coleta.yml`) e extração pelos scripts da Etapa 4 |
| Procedimento de análise | Na reunião semanal, comparando a semana encerrada com o compromisso registrado no retrato anterior |

<p class="legenda">Tabela 4. Construto da medida A2, comprometido x concluído. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.3.</p>

Até o board estar em uso (issue #19), o compromisso de cada semana é registrado em ata ou no comentário do retrato semanal. Sem esse registro, a semana fica sem medida.

### A3. Fluxo cumulativo

| Campo | Definição |
|---|---|
| Identificador | A3 |
| Categoria de informação | Calendário e Progresso |
| Necessidade de informação | O trabalho flui pelos estados do processo ou se acumula em filas e gargalos? |
| Conceito mensurável | Progresso das unidades de trabalho e efetividade do processo |
| Entidades relevantes | Todas as issues do repositório |
| Atributos | Estado no board (Backlog, A Fazer, Em Progresso, Em Revisão, Concluído) em cada dia |
| Medidas básicas | `N(e, d)` = número de issues no estado `e` no fim do dia `d` (inteiro, maior ou igual a 0) |
| Método de medição | Reconstrução diária do estado de cada issue a partir do histórico de transições do board e dos eventos de issue |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Inteiros maiores ou iguais a 0; razão |
| Unidade de medida | Issues; issues por dia (throughput); dias (tempo de ciclo aproximado) |
| Função de medição | `WIP(d) = N(Em Progresso, d) + N(Em Revisão, d)`; `TH` = issues que entram em Concluído por dia, média do período; `CT aproximado = WIP médio / TH` (Lei de Little) |
| Medida derivada | WIP médio, throughput e tempo de ciclo aproximado |
| Modelo de análise | Faixa que se alarga de forma sustentada indica fila naquele estado; faixa de Concluído que não sobe indica parada do fluxo |
| Indicador | Diagrama de áreas empilhadas por estado ao longo do tempo, com linhas verticais nos marcos |
| Critérios de decisão | **Variação maior que 10%** na largura ou na inclinação de uma faixa entre duas semanas: análise de causa-raiz na reunião seguinte. Faixa "Em Revisão" crescendo por duas semanas seguidas: revisores redistribuídos (PSM CID, Parte 2, 8.4) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4 a partir do board e de `issue_events.jsonl` |
| Procedimento de análise | Na reunião semanal, junto com A1 e A2 |

<p class="legenda">Tabela 5. Construto da medida A3, fluxo cumulativo. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.4.</p>

Limitação: antes da criação do board (Diagnóstico, lacuna L4) não há histórico de estados intermediários. Nesse período, o fluxo cumulativo tem só duas faixas, "aberta" e "fechada", e a limitação é declarada no gráfico.

### A4. Conclusão de marcos

| Campo | Definição |
|---|---|
| Identificador | A4 |
| Categoria de informação | Calendário e Progresso |
| Necessidade de informação | Os marcos da disciplina foram atingidos nas datas previstas? |
| Conceito mensurável | Conclusão de marcos (*Milestone Completion*) |
| Entidades relevantes | Marcos da disciplina: E1, PC1, E2 e Apresentação |
| Atributos | Data planejada e data de conclusão |
| Medidas básicas | `Data planejada` = prazo do milestone no GitHub, igual ao cronograma da disciplina; `Data real` = data de publicação da release da entrega (horário de Brasília) |
| Método de medição | Leitura automática dos milestones e das releases pela API do GitHub |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Datas; intervalo (o desvio em dias é de razão) |
| Unidade de medida | Dias |
| Função de medição | `Desvio = Data real - Data planejada` |
| Medida derivada | Desvio do marco, em dias (negativo: antes do prazo) |
| Modelo de análise | Desvio positivo indica entrega atrasada; desvio próximo de zero em todos os marcos, com A1 concentrado no último dia, indica entrega de véspera |
| Indicador | Tabela planejado x real por marco, com o desvio |
| Critérios de decisão | **Qualquer desvio positivo** exige registro de decisão de gestão, com causa e ação para o marco seguinte (PSM CID, Parte 1, Tabela 5, linha 1) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4, a cada release |
| Procedimento de análise | Na primeira reunião depois de cada marco |

<p class="legenda">Tabela 6. Construto da medida A4, conclusão de marcos. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5.</p>

Observação: na E1, a release foi publicada em 25/10/2026 às 23h26 (horário de Brasília), antes do prazo de 26/10/2026. A tag `E1` não inclui os dois últimos commits entregues (Diagnóstico, lacuna L9); por isso a data real é a da release, e não a da tag.

## Desempenho dos Processos

Seção preenchida na issue #22 (medidas B1 a B4).

## Recursos e Custos

Seção preenchida na issue #23 (medidas C1 a C3).
