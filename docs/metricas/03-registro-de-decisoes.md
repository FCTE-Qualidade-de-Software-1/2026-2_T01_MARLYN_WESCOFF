# Registro de decisões de gestão

Este documento registra as decisões de gestão tomadas a partir das medidas do PSM CID: a medida que disparou cada decisão, o valor observado comparado com o critério, a interpretação da causa, a ação, o responsável, a evidência e o efeito observado depois. As medidas e os critérios estão nos [Construtos de medição](02-construtos-de-medicao.md), e as lacunas citadas (L1 a L12), no [Diagnóstico do repositório](01-diagnostico-repositorio.md).

**Data de corte dos valores:** 10/11/2026. Todo número deste registro sai dos arquivos de [`dados/consolidados/`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/tree/main/docs/metricas/dados/consolidados), gerados por `scripts/consolidar_metricas.py --data-ref 2026-11-10`, ou dos retratos semanais de `dados/gestao/`. Uma decisão com efeito ainda não observável fica marcada como "a verificar", com a medida e a data da verificação.

## Resumo

| Nº | Data | Categoria | Medida que disparou | Decisão | Efeito |
|---|---|---|---|---|---|
| DG-01 | 26/10/2026 | Recursos e Custos | C1 e C3 | Lançar as horas ao fechar cada issue | Verificado: não cumprida (0 h em 02/11 e 09/11) |
| DG-02 | 10/11/2026 | Recursos e Custos | C1 e C3 | Apontamento `esforco.csv` com registro no dia e reconstrução da E1 em faixa | A verificar em 17/11/2026 |
| DG-03 | 26/10/2026 | Desempenho dos Processos | B1 | Abrir as issues no planejamento, e não no fim | Verificado: parcial (mediana de 1 dia na E2) |
| DG-04 | 10/11/2026 | Calendário e Progresso | A2 e B2 | Criar as issues #15 a #32 e dividi-las em três blocos sequenciais | Verificado: 13 pontos na W46, contra 0 na W44 e na W45 |
| DG-05 | 10/11/2026 | Desempenho dos Processos | B4 e C2 | Toda mudança entra por pull request revisado por outro integrante | Verificado: 6 PRs aprovados e 1 não conformidade contida |
| DG-06 | 10/11/2026 | Recursos e Custos | Retrospectiva da E1, tópico C2 | Bernardo como líder da E2 | A verificar no review deste registro |
| DG-07 | 10/11/2026 | Calendário e Progresso | Retrospectiva da E1, tópico C3; A2 | Iteração semanal no quadro e blocos com milestone | A verificar em 17/11/2026 |
| DG-08 | 10/11/2026 | Desempenho dos Processos | B3 e A4 | Congelamento interno 3 dias antes de cada marco | A verificar na entrega da E2 |

<p class="legenda">Tabela 1. Resumo das decisões de gestão. Fonte: elaborado pelos autores a partir de <code>dados/consolidados/</code>, dos retratos de <code>dados/gestao/</code> e da retrospectiva da E1.</p>

As três categorias têm decisões, e quatro delas (DG-01, DG-03, DG-04 e DG-05) já têm efeito verificado por dado. A DG-01 mostra um efeito negativo: a decisão não foi cumprida, e isso gerou a DG-02.

## Recursos e Custos

### DG-01 - Lançar as horas ao fechar cada issue

- **Data:** 2026-10-26
- **Medida que disparou:** C1 Esforço da equipe e C3 Estimado x real, no fechamento da E1.
- **Valor observado x critério:** 20,5 h estimadas nas issues da E1 e 0,0 h realizadas; razão R/E de 0,00 ([`psm-2026-10-26-2.csv`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/gestao/psm-2026-10-26-2.csv)). O critério do plano da E1 era R/E acima de 1,3, e ele não pôde ser avaliado.
- **Interpretação:** o valor 0 não mede esforço; mede a falta de registro. O arquivo `horas.csv` existia, mas ninguém tinha o hábito nem um momento definido para preenchê-lo (lacuna L1).
- **Decisão tomada:** na E2, cada integrante lança as horas ao fechar cada issue, e a razão R/E passa a ser medida na metade e no fim de cada sprint.
- **Responsável e prazo:** todos os integrantes, a partir de 26/10/2026.
- **Evidência da execução:** [Registro de medições](../gestao/registro-medicoes.md), medição de 26/10/2026.
- **Efeito observado posteriormente:** **não cumprida.** Os retratos de [02/11](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/gestao/psm-2026-11-02.csv) e [09/11](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/gestao/psm-2026-11-09.csv) continuam com 0,0 h realizadas. Até 10/11/2026, nenhuma linha do `esforco.csv` tinha horas (aviso de `validar_dados.py`: 28 linhas sem horas). A causa foi a falta de um responsável por verificar o cumprimento. Gerou a DG-02.

### DG-02 - Apontamento no dia e reconstrução das horas da E1 em faixa

- **Data:** 2026-11-10
- **Medida que disparou:** C1 e C3, pelo não cumprimento da DG-01.
- **Valor observado x critério:** 0 h registradas em duas semanas depois da decisão de 26/10. C1 e C3 exigem horas por integrante, por fase e por issue.
- **Interpretação:** lançar as horas só "ao fechar a issue" deixa o registro para o fim, quando a memória já falhou. A E1 não tem como ser medida depois do fato com precisão por integrante.
- **Decisão tomada:**
    1. Novo apontamento `docs/metricas/dados/brutos/esforco.csv`, com uma linha por sessão de trabalho, registrada no mesmo dia (`tipo_registro = registrado`). A verificação passa a ser automática: `validar_dados.py` roda todo dia no workflow e aponta linha sem tipo, sem data ou com formato inválido.
    2. As horas da E1 foram reconstruídas em consulta à equipe em 10/11/2026: **cada integrante estimou ter dedicado entre 9 e 12 horas à E1, de 45 a 60 horas na equipe.** A equipe não conseguiu estimar as horas por atividade nem por integrante com mais precisão. Por isso, a faixa é registrada como faixa, e não convertida em valores individuais.
- **Responsável e prazo:** Carlos (apontamento, issue #20, PR #35); Pedro (verificação automática, issue #25); todos os integrantes, no dia de cada sessão, a partir de 10/11/2026.
- **Evidência da execução:** [PR #35](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/pull/35), [`esforco.csv`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/docs/metricas/dados/brutos/esforco.csv) e [`dados/README.md`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/README.md).
- **Efeito observado posteriormente:** a verificar em 17/11/2026, pelo número de linhas `registrado` em `esforco.csv` com data entre 10/11 e 16/11 e por integrante (C1, `esforco_consolidado.csv`).

Consequência para as medidas da E1: C1 é apresentado como a faixa de 45 a 60 h, com custo de R$ 675,00 a R$ 900,00 (R$ 15,00 por hora); a dimensão "horas" de C2 não diferencia os integrantes na E1, porque todos informaram a mesma faixa; e C3 da E1 não é calculado por issue. Essa limitação entra nas ameaças à validade do artigo.

### DG-06 - Liderança da E2

- **Data:** 2026-11-10
- **Medida que disparou:** retrospectiva da E1, de 28/10/2026, tópico C2 "ausência de liderança", priorizado com 2 votos. A ação definida foi "definiremos um integrante responsável por liderar e delegar responsabilidades", sem nome registrado.
- **Valor observado x critério:** a retrospectiva não registrou quem seria o líder. Duas semanas depois, não havia responsável pela verificação das decisões de 26/10 (DG-01 e DG-03).
- **Interpretação:** sem um responsável nomeado, as decisões da E1 ficaram sem acompanhamento: a DG-01 não foi cumprida, e os retratos de 02/11 e 09/11 não geraram nenhuma ação.
- **Decisão tomada:** Bernardo Broetto Brun é o líder da E2. Ele acompanha o quadro na reunião semanal, verifica o cumprimento das decisões deste registro na data de cada verificação e abre uma issue com as labels `retrabalho` e `apontamento-docente` para cada apontamento da docente (B4).
- **Responsável e prazo:** Bernardo, até a Apresentação.
- **Evidência da execução:** [retrospectiva da E1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-10-28-retrospectiva-e1.pdf), página 4; a indicação é confirmada pelo Bernardo na revisão do pull request deste registro.
- **Efeito observado posteriormente:** a verificar no review deste registro (confirmação) e em 17/11/2026, pela coluna "Efeito" das decisões com verificação marcada até essa data.

## Calendário e Progresso

### DG-04 - Duas semanas sem progresso: issues da gestão em três blocos sequenciais

- **Data:** 2026-11-10
- **Medida que disparou:** A2 Comprometido x concluído e B2 Velocidade, nos retratos semanais.
- **Valor observado x critério:** os retratos de 26/10, 02/11 e 09/11 são idênticos (14 de 14 issues, todas da E1). Na `velocidade.csv`, as semanas 2026-W44 e 2026-W45 têm 0 issues e 0 pontos concluídos. A velocidade média caiu para 0, e a projeção de semanas restantes ficou "sem projeção". O critério de B2 é variação da velocidade maior que 10%.
- **Interpretação:** não havia trabalho da E2 planejado no repositório: nenhuma issue aberta, nenhum responsável e nenhum marco com as tarefas da gestão PSM/CID. Sem tarefas definidas, ninguém começou.
- **Decisão tomada:** criar as issues #15 a #32 da gestão PSM/CID, com estimativa, labels de tipo e tamanho e o milestone E2, e dividi-las em três blocos sequenciais com responsáveis: bloco 1 (Carlos, #16 a #22), bloco 2 (Pedro, #23 a #25 e #28) e bloco 3 (Bernardo, #26, #27 e #29 a #32). Cada bloco só começa depois do merge do anterior.
- **Responsável e prazo:** Carlos (criação das issues e bloco 1), em 10/11/2026.
- **Evidência da execução:** [issue #15](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/issues/15) e [milestone E2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/milestone/2).
- **Efeito observado posteriormente:** **verificado.** Na semana 2026-W46, até 10/11, foram concluídas 8 issues, com 13 pontos, contra 0 na W44 e na W45. A velocidade média de 3 semanas passou de 0 para 4,33 pontos por semana. O milestone E2 tem 35 pontos planejados e 22 abertos (`progresso_diario.csv`). Ressalva: as 8 issues foram criadas e fechadas no mesmo dia, então o aumento mostra a retomada, e não ainda um ritmo estável. O ritmo é verificado de novo na W47.

### DG-07 - Iterações semanais no quadro

- **Data:** 2026-11-10
- **Medida que disparou:** retrospectiva da E1, tópico C3 "pouca atenção aos prazos", priorizado com 2 votos, com a ação "dividir as responsabilidades em sprints" e a métrica "demandas planejadas / demandas cumpridas" (A2).
- **Valor observado x critério:** na E1, o plano citava uma Sprint 1 que não existia como milestone (lacuna L5), e não havia registro de compromisso por semana. A2 não pode ser calculado para nenhuma semana até 10/11 (`comprometido_concluido.csv`: "sem registro de compromisso").
- **Interpretação:** sem um compromisso registrado no início da semana, não há como comparar o planejado com o cumprido. A retrospectiva pediu exatamente essa comparação.
- **Decisão tomada:** iteração = semana ISO, de segunda a domingo. O compromisso da semana é o campo "Iteração" do quadro no retrato de segunda-feira. Os marcos da disciplina viram milestones (E1, PC1, E2 e Apresentação). A issue vai para "Em Progresso" quando o trabalho começa, e não quando termina.
- **Responsável e prazo:** Carlos (quadro, issue #19; milestones, issue #18); Bernardo (acompanhamento semanal, DG-06), a partir da W47 (16/11/2026).
- **Evidência da execução:** [quadro do projeto](https://github.com/users/cadumotta/projects/1), [PR #34](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/pull/34) e [Construtos de medição](02-construtos-de-medicao.md), Tabela 2.
- **Efeito observado posteriormente:** a verificar em 17/11/2026, pelo percentual concluído da W47 em `comprometido_concluido.csv`. Depende do retrato diário do quadro, que precisa do token `PSM_PROJECT_TOKEN` no workflow.

## Desempenho dos Processos

### DG-03 - Abrir as issues no planejamento

- **Data:** 2026-10-26
- **Medida que disparou:** B1 Tempo de ciclo, no fechamento da E1.
- **Valor observado x critério:** mediana de 0,5 dia ([`psm-2026-10-26-2.csv`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/gestao/psm-2026-10-26-2.csv)), dentro do critério do plano da E1 (mediana até 5 dias). O valor estava dentro do limite, mas sem significado: as 14 issues foram criadas em 27 segundos e fechadas em 12 minutos (lacuna L3).
- **Interpretação:** as issues foram abertas depois do trabalho, só para registrá-lo. O tempo de ciclo mediu o intervalo administrativo, e não a duração das tarefas.
- **Decisão tomada:** na E2, abrir as issues no planejamento da sprint, antes de começar o trabalho.
- **Responsável e prazo:** todos os integrantes, a partir de 26/10/2026.
- **Evidência da execução:** [Registro de medições](../gestao/registro-medicoes.md), medição de 26/10/2026; issues #15 a #32, abertas em 10/11/2026.
- **Efeito observado posteriormente:** **parcial.** As issues da E2 foram abertas antes de cada bloco, mas as 8 issues do bloco 1 foram abertas e fechadas no mesmo dia: cycle time de 1 dia em todas e mediana de 1 dia na E2 (`cycle_time.csv`). Para os blocos 2 e 3, a data de início passa a vir do primeiro movimento para "Em Progresso" no quadro (DG-07). A verificação é refeita no fechamento do bloco 2.

### DG-05 - Revisão por pares em pull request

- **Data:** 2026-11-10
- **Medida que disparou:** B4 Retrabalho e não conformidades e C2, dimensão "revisões".
- **Valor observado x critério:** na E1, nenhum pull request e nenhuma revisão registrada (lacunas L2 e L8), embora o artigo da E1 diga que a integração era feita por PR revisado. Sem revisão registrada, a taxa de escape (B4) não tem não conformidades contidas para comparar.
- **Interpretação:** a revisão existia como combinado, mas não deixava rastro. Sem registro, não há como mostrar que a revisão interna encontra problemas antes da docente.
- **Decisão tomada:** toda mudança entra na `main` por pull request, com a aprovação de um integrante diferente do autor, a partir do PR #33. Um problema encontrado na revisão é registrado como "Request changes", que conta como não conformidade contida em B4.
- **Responsável e prazo:** todos os integrantes; o autor de cada PR pede a revisão. A partir de 10/11/2026.
- **Evidência da execução:** PRs [#33](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/pull/33) a [#38](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/pull/38), abertos por Carlos e revisados por Pedro.
- **Efeito observado posteriormente:** **verificado.** Os 6 PRs do bloco 1 foram mergeados em 10/11/2026, todos com aprovação de outro integrante (`prs.json`). No PR #35, a revisão encontrou duas não conformidades (um trecho solto no `dados/README.md` e o papel errado de um integrante na retrospectiva) e pediu mudanças antes de aprovar. Em `retrabalho.csv`, a E2 tem 1 não conformidade contida em revisão, contra 0 na E1. Em `contribuicao.csv`, a dimensão "revisões" passa a ter dado na E2.

### DG-08 - Congelamento interno antes de cada marco

- **Data:** 2026-11-10
- **Medida que disparou:** B3 Frequência de entregas (concentração de véspera) e A4 Conclusão de marcos.
- **Valor observado x critério:** na E1, a concentração de véspera foi de 100%: as 5.962 linhas alteradas na `main` até a release entraram nas 48 horas anteriores à publicação (`entregas.csv`). O critério de B3 é concentração acima de 50%. A release saiu 1 dia antes do prazo (desvio de -1 dia em A4), então o marco foi cumprido, mas no limite.
- **Interpretação:** parte do valor vem da migração do conteúdo de outro repositório num único commit (lacuna L7), mas o histórico também mostra 13 commits da equipe em 25/10/2026, entre 10h34 e 23h34. Os dois tópicos priorizados na retrospectiva (C2 e C3) apontam a mesma causa: trabalho concentrado no fim, sem acompanhamento.
- **Decisão tomada:** cada marco passa a ter um congelamento interno 3 dias antes do prazo. Depois dessa data, só entram correções que vierem de revisão. O conteúdo novo precisa estar em PR aberto até o congelamento.
- **Responsável e prazo:** Bernardo (líder, DG-06), assim que os prazos de PC1, E2 e Apresentação forem preenchidos nos milestones.
- **Evidência da execução:** a registrar na issue #15 com as datas de congelamento, depois do preenchimento dos prazos dos milestones.
- **Efeito observado posteriormente:** a verificar na entrega da E2, pela concentração de véspera e pelo desvio do marco em `entregas.csv`. A meta é concentração abaixo de 50%.

## Situação das verificações

| Data | Verificação | Medida e arquivo |
|---|---|---|
| 17/11/2026 | Horas registradas no dia, por integrante (DG-02) | C1, `esforco_consolidado.csv` |
| 17/11/2026 | Primeira semana com compromisso no quadro (DG-07) | A2, `comprometido_concluido.csv` |
| 17/11/2026 | Ritmo da W47 (DG-04) | B2, `velocidade.csv` |
| Fechamento do bloco 2 | Cycle time com início pelo quadro (DG-03) | B1, `cycle_time.csv` |
| Entrega da E2 | Concentração de véspera e desvio do marco (DG-08) | B3 e A4, `entregas.csv` |

<p class="legenda">Tabela 2. Próximas verificações de efeito. Fonte: elaborado pelos autores.</p>
