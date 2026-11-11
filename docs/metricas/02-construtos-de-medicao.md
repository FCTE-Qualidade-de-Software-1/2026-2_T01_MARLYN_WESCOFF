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
| Critérios de decisão | **Desvio maior que 5%** acima da linha ideal: a causa é analisada na reunião semanal seguinte. **Desvio maior que 10%**: replanejamento do escopo da entrega ou realocação de issues entre integrantes, registrado como decisão de gestão (PSM CID v2.1, Parte 2, seção 8.2) |
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
| Critérios de decisão | **Diferença maior que 5%** numa semana: a causa é investigada na reunião seguinte. **Diferença maior que 10%**: ação corretiva (reduzir o compromisso da semana seguinte ou dividir as issues grandes), registrada como decisão de gestão (PSM CID v2.1, Parte 2, seção 8.3) |
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
| Critérios de decisão | **Variação maior que 10%** na largura ou na inclinação de uma faixa entre duas semanas: análise de causa-raiz na reunião seguinte. Faixa "Em Revisão" crescendo por duas semanas seguidas: revisores redistribuídos (PSM CID v2.1, Parte 2, seção 8.4) |
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
| Critérios de decisão | **Qualquer desvio positivo** exige registro de decisão de gestão, com causa e ação para o marco seguinte (PSM CID v2.1, Parte 1, Tabela 5, linha 1) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4, a cada release |
| Procedimento de análise | Na primeira reunião depois de cada marco |

<p class="legenda">Tabela 6. Construto da medida A4, conclusão de marcos. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5.</p>

Observação: na E1, a release foi publicada em 25/10/2026 às 23h26 (horário de Brasília), antes do prazo de 26/10/2026. A tag `E1` não inclui os dois últimos commits entregues (Diagnóstico, lacuna L9); por isso a data real é a da release, e não a da tag.

## Desempenho dos Processos

### B1. Cycle time e lead time

| Campo | Definição |
|---|---|
| Identificador | B1 |
| Categoria de informação | Desempenho dos Processos |
| Necessidade de informação | Quanto tempo a equipe leva para concluir uma tarefa? O tempo de resposta é previsível? Há tarefas paradas? |
| Conceito mensurável | Eficiência do processo: velocidade (*Process Efficiency: Speed*) |
| Entidades relevantes | Issues concluídas (definição de pronto) e issues abertas |
| Atributos | Data de criação, data do primeiro movimento para "Em Progresso", data de fechamento, data da última atualização |
| Medidas básicas | `tc` = data de criação; `ti` = data do primeiro movimento para "Em Progresso" no board (na falta, `tc`); `tf` = data de fechamento; `tu` = data da última atualização |
| Método de medição | Leitura automática das datas pela API do GitHub e do histórico do board |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Inteiros maiores ou iguais a 1; razão |
| Unidade de medida | Dias corridos |
| Função de medição | `Cycle time = tf - ti + 1`; `Lead time = tf - tc + 1`; mediana, percentil 80 (P80) e percentil 90 (P90) por semana e por entrega; `Idade = hoje - tu` para issues abertas |
| Medida derivada | Cycle time e lead time de cada issue; mediana, P80 e P90; idade das issues abertas |
| Modelo de análise | Cycle time alto indica tarefa grande demais, bloqueada ou dependente de agenda externa (entrevistas, acesso a ambiente, retorno da docente). Distância grande entre lead time e cycle time indica issue que espera muito no backlog |
| Indicador | Histograma de cycle time com as linhas da mediana, do P80 e do P90; lista de issues paradas |
| Critérios de decisão | **Issue com cycle time acima da média em mais de 10%**: a causa é investigada na reunião seguinte (PSM CID v2.1, Parte 2, seção 8.5). **Mediana crescente por duas semanas seguidas**: o WIP é reduzido e as tarefas seguintes são divididas. **Mediana maior que 5 dias** numa entrega: as issues da semana seguinte são divididas. **Issue aberta sem atualização há mais de 3 dias**: o responsável informa o bloqueio na issue ou a tarefa é dividida |
| Procedimento de coleta | Extração pelos scripts da Etapa 4; a idade das issues abertas também sai no retrato semanal (`psm_coleta.py`) |
| Procedimento de análise | Na reunião semanal, pelo responsável pela gestão PSM/CID da semana |

<p class="legenda">Tabela 7. Construto da medida B1, cycle time e lead time. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.5, e do <a href="../../gestao/plano-psm/">Plano de medição</a> da E1.</p>

Os dois últimos critérios vêm do plano de medição da E1 e foram mantidos para preservar a comparação entre as entregas. Na E1, o cycle time não é calculado, porque as datas das issues não refletem o trabalho (Diagnóstico, lacuna L3).

### B2. Velocidade e aceleração

| Campo | Definição |
|---|---|
| Identificador | B2 |
| Categoria de informação | Desempenho dos Processos |
| Necessidade de informação | A capacidade de produção da equipe é estável e suficiente para concluir o escopo restante até o próximo marco? |
| Conceito mensurável | Eficiência do processo: velocidade (*Process Efficiency: Speed*) |
| Entidades relevantes | Iterações (semanas) e issues concluídas em cada uma |
| Atributos | Pontos de tamanho das issues concluídas; semana de conclusão |
| Medidas básicas | `P(s)` = soma dos pontos das issues concluídas na semana `s`; `B` = soma dos pontos das issues abertas do milestone; `S` = semanas inteiras até o prazo do milestone |
| Método de medição | Contagem automática a partir das issues fechadas e das labels `tamanho/` |
| Tipo de método | Objetivo, sobre um tamanho atribuído de forma subjetiva |
| Escala e tipo de escala | Reais maiores ou iguais a 0; razão |
| Unidade de medida | Pontos por semana |
| Função de medição | `V(s)` = média móvel de `P` nas últimas 3 semanas (ou nas disponíveis, se forem menos); `Aceleração(s) = (V(s) - V(s - 1)) / V(s - 1)`, não calculada quando `V(s - 1) = 0`; `Semanas restantes = B / V(s)`, registrada como "sem projeção" quando `V(s) = 0` |
| Medida derivada | Velocidade média, aceleração e projeção de semanas restantes |
| Modelo de análise | Projeção de semanas restantes maior que `S` indica que o escopo não cabe no prazo com o ritmo atual |
| Indicador | Gráfico de colunas de pontos concluídos por semana, com a linha da média móvel e a projeção |
| Critérios de decisão | **Variação da velocidade maior que 10%**, para mais ou para menos: analisada na reunião semanal ou na retrospectiva (PSM CID v2.1, Parte 2, seção 8.10). **Semanas restantes maior que `S`**: decisão de escopo (cortar, simplificar ou redistribuir issues), justificada com a projeção |
| Procedimento de coleta | Extração pelos scripts da Etapa 4, a cada semana |
| Procedimento de análise | Na reunião semanal; a projeção é revista em cada decisão de escopo |

<p class="legenda">Tabela 8. Construto da medida B2, velocidade e aceleração. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.10.</p>

Limitação: a disciplina tem poucas semanas até a E2, então a média móvel usa no máximo 3 semanas e a série é curta. Os pontos de tamanho são atribuídos pela estimativa de horas da issue (P até 2 h, M até 5 h, G acima de 5 h), e não por consenso da equipe.

### B3. Frequência de entregas

| Campo | Definição |
|---|---|
| Identificador | B3 |
| Categoria de informação | Desempenho dos Processos |
| Necessidade de informação | Com que cadência a equipe consolida produtos de trabalho na `main`? O trabalho se concentra na véspera dos marcos? |
| Conceito mensurável | Eficiência do processo: velocidade (*Process Efficiency: Speed*) |
| Entidades relevantes | Releases (marcos) e pull requests mergeados na `main` |
| Atributos | Data de publicação da release; data de merge de cada pull request; linhas alteradas |
| Medidas básicas | `R` = número de releases no período; `D(r)` = dias entre a release `r - 1` (ou o início da disciplina) e a release `r`; `M(d)` = pull requests mergeados na `main` no dia `d`; `L(d)` = linhas alteradas na `main` no dia `d` |
| Método de medição | Leitura automática das releases, dos pull requests e do `git log` |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Inteiros maiores ou iguais a 0; razão |
| Unidade de medida | Releases; dias; pull requests por semana; percentual |
| Função de medição | `Duração da release = D(r)`; `Frequência = R / semanas do período`; `Concentração(r)` = linhas alteradas nas 48 horas anteriores à publicação da release `r`, divididas pelas linhas alteradas desde a release anterior (ou desde o início da disciplina), vezes 100 |
| Medida derivada | Duração e frequência das releases; merges por semana; concentração de véspera |
| Modelo de análise | Semanas sem merge seguidas de concentração alta na véspera indicam o "pico de véspera": risco de qualidade e de revisão insuficiente |
| Indicador | Linha do tempo das releases e dos merges por semana, com os marcos da disciplina; tabela de concentração por entrega |
| Critérios de decisão | **Semana sem nenhum merge na `main`** antes de um marco: a causa é registrada na reunião seguinte. **Concentração maior que 50%** numa entrega: decisão de gestão para a entrega seguinte (por exemplo, prazo interno de congelamento 3 dias antes do marco) (PSM CID v2.1, Parte 2, seção 8.9) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4 |
| Procedimento de análise | Na primeira reunião depois de cada marco |

<p class="legenda">Tabela 9. Construto da medida B3, frequência de entregas. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.9.</p>

A "concentração" é uma medida derivada acrescentada pela equipe, porque o projeto tem poucas releases (uma por marco) e a frequência sozinha não mostra a distribuição do trabalho. Na E1, todo o conteúdo entrou na `main` em 25/10/2026, véspera do prazo (Diagnóstico, seção 2); como o conteúdo foi migrado de outro repositório, esse valor mede a consolidação, e não a produção.

### B4. Retrabalho e não conformidades

| Campo | Definição |
|---|---|
| Identificador | B4 |
| Categoria de informação | Desempenho dos Processos |
| Necessidade de informação | Quanto esforço vai para corrigir trabalho já dado como pronto? A revisão interna encontra os problemas antes da entrega? |
| Conceito mensurável | Efetividade do processo, adaptada do conceito de defeito contido e escapado do PSM CID (*Functional Correctness*) |
| Entidades relevantes | Pull requests, issues e apontamentos da docente em cada entrega e ponto de controle |
| Atributos | Revisões de PR, eventos de reabertura, labels `retrabalho` e `apontamento-docente` |
| Medidas básicas | `Reabertas` = issues com evento `reopened`; `Contidas` = não conformidades encontradas em revisão interna: revisões de PR com estado "Changes requested" mais issues com `retrabalho` e sem `apontamento-docente`; `Escapadas` = não conformidades apontadas pela docente, uma issue por apontamento, com as labels `retrabalho` e `apontamento-docente` |
| Método de medição | Contagem automática das revisões de PR, dos eventos e das labels pela API do GitHub; o registro das escapadas é manual (uma issue por apontamento, aberta na semana do retorno da docente) |
| Tipo de método | Objetivo (contagem), sobre uma classificação feita pela equipe |
| Escala e tipo de escala | Inteiros maiores ou iguais a 0; razão |
| Unidade de medida | Não conformidades; percentual |
| Função de medição | `Taxa de escape = Escapadas / (Contidas + Escapadas) x 100`, por entrega |
| Medida derivada | Taxa de escape por entrega; número de issues reabertas |
| Modelo de análise | Taxa de escape alta indica que a revisão interna não está encontrando os problemas que a docente encontra |
| Indicador | Gráfico de colunas contidas x escapadas por entrega, com a taxa de escape |
| Critérios de decisão | **A taxa de escape deve cair da E1 para a E2.** Se não cair, os PRs da entrega seguinte passam a exigir dois revisores e um checklist da rubrica da fase. **Issue reaberta**: a causa é registrada na própria issue (PSM CID v2.1, Parte 2, seção 8.6) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4; issues de apontamento abertas pelo responsável pela gestão PSM/CID ao receber o retorno da docente |
| Procedimento de análise | Na primeira reunião depois de cada retorno da docente |

<p class="legenda">Tabela 10. Construto da medida B4, retrabalho e não conformidades. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 2, seção 8.6.</p>

Limitação: na E1 não houve nenhum registro de não conformidade em revisão interna (Diagnóstico, lacuna L8). A taxa de escape da E1 fica em 100% sempre que houver qualquer apontamento da docente. Esse valor é o ponto de partida da comparação, e não uma medição da qualidade das revisões.

## Recursos e Custos

O custo é medido em **homem-hora**, a medida primária desta categoria. A monetização é complementar e usa a premissa do [Plano de medição](../gestao/plano-psm.md#custo-da-hora): R$ 15,00 por hora de integrante, uma convenção do projeto para comparar entregas, e não pagamento real. A fonte das três medidas é o apontamento `esforco.csv`, triangulado com os commits, as issues e as revisões de pull request.

### C1. Esforço da equipe

| Campo | Definição |
|---|---|
| Identificador | C1 |
| Categoria de informação | Recursos e Custos |
| Necessidade de informação | Quanto esforço a equipe está gastando, em que fases e tipos de atividade? O esforço está distribuído entre os integrantes? |
| Conceito mensurável | Esforço da equipe (*Effort*) |
| Entidades relevantes | Sessões de trabalho registradas em `esforco.csv`; integrantes de `docs/sobre/equipe.md`; fases e entregas |
| Atributos | Data, integrante, fase, tipo de atividade, issue, horas e tipo de registro (`registrado` ou `reconstruido`) |
| Medidas básicas | `h(m, f, t)` = horas da linha do integrante `m`, na fase `f` (1 a 4, ou transversal), no tipo de atividade `t` (real, maior que 0); `Prev(f)` = soma das estimativas, em horas, das issues com a label `fase/f` no milestone da entrega |
| Método de medição | Registro manual de cada sessão em `esforco.csv`, no mesmo dia, pelo próprio integrante; soma automática pelos scripts da Etapa 4. Linhas sem horas são ignoradas |
| Tipo de método | Subjetivo no registro (cada integrante anota as próprias horas); objetivo na agregação |
| Escala e tipo de escala | Reais maiores ou iguais a 0; razão |
| Unidade de medida | Horas (homem-hora); reais (R$) no custo |
| Função de medição | `H(m)` = soma de `h(m, f, t)` por integrante; `H(f)` = soma de `h(m, f, t)` por fase; `Total` = soma de `H(m)`; `%H(m) = H(m) / Total x 100`; `Média = Total / número de integrantes`; `Desvio(m) = (H(m) - Média) / Média x 100`; `Desvio(f) = (H(f) - Prev(f)) / Prev(f) x 100`; `Custo = Total x R$ 15,00` |
| Medida derivada | Esforço total, por fase, por tipo e por integrante; percentual por integrante; desvio em relação à média e ao previsto da fase; custo da entrega |
| Modelo de análise | Integrante muito acima da média indica concentração de trabalho e risco de dependência de uma pessoa; muito abaixo indica sub-alocação ou falta de registro. Fase acima do previsto indica escopo subestimado, que tende a comprimir as fases seguintes |
| Indicador | Gráfico de barras empilhadas de horas por fase e tipo de atividade, por entrega; gráfico de barras das horas por integrante, com a linha da média e a faixa de +/-30% |
| Critérios de decisão | **Integrante com desvio maior que +/-30% da média** na entrega: a distribuição das issues da semana seguinte é revista e o trabalho é redistribuído, registrado como decisão de gestão. **Fase com esforço mais de 20% acima do previsto**: o escopo das fases seguintes é reavaliado (cortar, simplificar ou redistribuir), com justificativa |
| Procedimento de coleta | Cada integrante registra as horas ao fim de cada sessão de trabalho, com `tipo_registro = registrado`; os scripts da Etapa 4 consolidam o arquivo a cada execução |
| Procedimento de análise | Na reunião semanal, pelo responsável pela gestão PSM/CID da semana, e no fechamento de cada entrega |

<p class="legenda">Tabela 11. Construto da medida C1, esforço da equipe. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5, e do <a href="../../gestao/plano-psm/">Plano de medição</a> da E1.</p>

Limitação: a E1 não teve nenhuma hora registrada (Diagnóstico, lacuna L1). As horas da E1 são reconstruídas em consenso, depois do fato, e ficam marcadas como `reconstruido`. Elas aparecem separadas das horas `registrado` em todos os indicadores, não entram na média usada como referência e são declaradas nas ameaças à validade do artigo. O registro depende da disciplina de cada integrante: hora não anotada aparece como esforço menor, e não como falta de registro.

### C2. Distribuição de contribuição

| Campo | Definição |
|---|---|
| Identificador | C2 |
| Categoria de informação | Recursos e Custos |
| Necessidade de informação | Como o trabalho de cada entrega se distribui entre os integrantes? A Tabela de Contribuição do artigo (Apêndice A) é sustentada pelos dados do repositório? |
| Conceito mensurável | Esforço da equipe, distribuído por integrante (*Effort*) |
| Entidades relevantes | Integrantes; commits da `main`; issues concluídas; revisões de pull request; sessões de `esforco.csv` |
| Atributos | Autor canônico do commit (via `.mailmap`), linhas adicionadas e removidas, responsáveis pela issue, autor da revisão, horas |
| Medidas básicas | Por integrante `m` e por entrega: `Cm` = commits na `main`; `Lm` = linhas adicionadas mais removidas; `Im` = issues concluídas em que `m` é responsável (uma issue com `k` responsáveis vale `1/k` para cada um); `Rm` = revisões de pull request submetidas por `m` em PRs de outra pessoa; `Hm` = horas em `esforco.csv` |
| Método de medição | Contagem automática pelo `git log` e pela API do GitHub; horas somadas de `esforco.csv`. Commits do robô de coleta (`github-actions`) são excluídos |
| Tipo de método | Objetivo |
| Escala e tipo de escala | Reais maiores ou iguais a 0; razão |
| Unidade de medida | Commits, linhas, issues, revisões e horas; percentual por dimensão |
| Função de medição | Para cada dimensão `X` em {C, L, I, R, H}: `%X(m) = Xm / soma de X x 100`, de modo que cada dimensão soma 100%; `Divergência(m)` = maior `%X(m)` menos menor `%X(m)`, entre as dimensões com dado |
| Medida derivada | Percentual de cada integrante em cada uma das cinco dimensões; divergência entre dimensões |
| Modelo de análise | Nenhuma dimensão sozinha mede contribuição: commits e linhas favorecem quem integra e migra conteúdo; horas dependem do registro; issues dependem da atribuição. Percentuais parecidos nas cinco dimensões indicam distribuição consistente. Divergência alta indica um papel específico (por exemplo, quem integra ou quem revisa) ou falha de registro, e precisa ser explicada |
| Indicador | Tabela multidimensional integrante x dimensão, com os percentuais; gráfico de barras agrupadas por integrante. A mesma tabela alimenta a Tabela de Contribuição do artigo, com a dimensão horas como principal |
| Critérios de decisão | **Divergência maior que 30 pontos percentuais** para um integrante: a causa é explicada por escrito na Tabela de Contribuição, e não escondida. **Dimensão cujos percentuais não somam 100%**: a tabela não é publicada até o erro ser corrigido (`validar_dados.py`) |
| Procedimento de coleta | Extração pelos scripts da Etapa 4 (`extrair_git.py` e `extrair_issues.py`) e consolidação por `consolidar_metricas.py` |
| Procedimento de análise | No fechamento de cada entrega, antes de montar o Apêndice A do artigo, por toda a equipe |

<p class="legenda">Tabela 12. Construto da medida C2, distribuição de contribuição. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5.</p>

Limitação: o número de commits, sozinho, é uma medida ruim de contribuição. Na E1, o conteúdo foi escrito em outro repositório e migrado em um único commit (Diagnóstico, lacuna L7), então commits e linhas da E1 mostram quem integrou, e não quem escreveu. A E1 também não teve pull request (lacuna L2), e a dimensão revisões fica vazia nessa entrega. Por isso a E1 é apresentada só com as dimensões disponíveis, com essas lacunas citadas na tabela, e a dimensão horas da E1 é reconstruída (lacuna L1).

### C3. Estimado x real

| Campo | Definição |
|---|---|
| Identificador | C3 |
| Categoria de informação | Recursos e Custos |
| Necessidade de informação | As estimativas de esforço da equipe são precisas o bastante para planejar as próximas fases e entregas? |
| Conceito mensurável | Acurácia da estimativa (*Estimation Accuracy*) |
| Entidades relevantes | Issues concluídas com estimativa; fases e entregas |
| Atributos | Estimativa de horas da issue e horas reais lançadas para a issue |
| Medidas básicas | `E(i)` = valor do campo "Estimativa (horas)" da issue `i`, preenchido ao abrir a issue; `R(i)` = soma das horas de `esforco.csv` com a issue `i` |
| Método de medição | Leitura automática do corpo das issues pela API do GitHub e soma das horas de `esforco.csv` por issue |
| Tipo de método | `E`: subjetivo (estimativa do responsável); `R`: subjetivo no registro, objetivo na agregação |
| Escala e tipo de escala | Reais maiores que 0; razão |
| Unidade de medida | Horas; razão adimensional; percentual |
| Função de medição | `Acurácia(i) = R(i) / E(i)`; `Acurácia(f)` = soma de `R` dividida pela soma de `E` das issues da fase ou da entrega; `EPM` = média, entre as issues, do valor absoluto de `(R(i) - E(i)) / E(i)`, vezes 100 (erro percentual médio); `Fator` = `Acurácia(f)` da fase anterior |
| Medida derivada | Acurácia por issue, por fase e por entrega; erro percentual médio; fator de recalibração |
| Modelo de análise | Acurácia acima de 1 indica subestimativa; abaixo de 1, superestimativa. EPM alto com acurácia agregada perto de 1 indica erros que se compensam: a estimativa da entrega acerta, mas a de cada issue não serve para planejar a semana |
| Indicador | Gráfico de dispersão estimado x real por issue, com a linha de 45 graus; barras pareadas estimado x real por fase |
| Critérios de decisão | **Acurácia da fase fora da faixa de 0,85 a 1,25**: as estimativas das issues das fases seguintes são multiplicadas pelo fator observado, e a recalibração é registrada como decisão de gestão (PSM CID v2.1, Parte 2, seção 9.2) |
| Procedimento de coleta | Estimativa no campo da issue, obrigatório no modelo Tarefa; horas em `esforco.csv` com o número da issue; extração e consolidação pelos scripts da Etapa 4 |
| Procedimento de análise | No fechamento de cada fase e de cada entrega, pelo responsável pela gestão PSM/CID, antes de estimar as issues da fase seguinte |

<p class="legenda">Tabela 13. Construto da medida C3, estimado x real. Fonte: elaborado pelos autores a partir do PSM CID v2.1, Parte 1, Tabela 5, e Parte 2, seção 9.2.</p>

Limitação: a estimativa vem do campo da issue, e o real, do `esforco.csv`. Issues sem estimativa numérica ou sem horas lançadas com o número da issue ficam fora do cálculo e são listadas à parte, para não distorcer a acurácia. Na E1, as issues somam 20,5 h estimadas (retratos de 26/10/2026), mas as horas reais são reconstruídas (Diagnóstico, lacuna L1) e várias atividades da E1 não têm issue, como a primeira versão da Fase 1. A acurácia da E1 é apresentada só como registro histórico e não é usada como fator de recalibração.
