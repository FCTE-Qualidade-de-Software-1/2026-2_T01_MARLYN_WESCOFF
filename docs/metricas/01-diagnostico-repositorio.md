# Diagnóstico do repositório

Este documento levanta a evidência que o repositório já tem e a que falta, **antes** de definir as medidas da gestão PSM/CID. Ele é a Etapa 1 do plano de gestão (issue #17) e serve de base para os construtos de medição e para as decisões de instrumentação.

**Data de corte:** 10/11/2026, por volta das 22h (horário de Brasília). Todos os números vêm dos arquivos de [`dados/brutos/`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/tree/main/docs/metricas/dados/brutos), extraídos nessa data, com o comando de cada um descrito no README da pasta. As ações de instrumentação feitas depois da extração estão na última seção.

## 1. Retrato numérico

| Item | Valor na data de corte |
|---|---|
| Período do histórico da `main` | 25/10/2026 (primeiro commit) a 09/11/2026 (último commit) |
| Commits na `main` | 18: 13 de Maykon (incluindo o commit inicial), 1 de João Pedro e 4 do robô de coleta do PSM. Detalhes na Tabela 2 |
| Issues | 32: 14 da E1 (todas fechadas) e 18 da gestão PSM/CID (#15 a #32, abertas em 10/11/2026) |
| Milestones | 2: `Sprint 2 - Entrega 1` (prazo 26/10/2026, ainda aberto, 14 issues fechadas) e `Gestão PSM/CID - Entrega 2` (sem prazo) |
| Pull requests | 0 |
| Branches além da `main` | Só `gh-pages`, gerado pelo deploy da GitPage |
| Releases e tags | 1 release (`E1`, publicada em 26/10/2026 às 02:26 UTC) e 1 tag leve (`E1`, no commit `172e1af`) |
| Project board | Nenhum |
| Eventos de issues | 158: 63 de label, 35 de atribuição, 31 de milestone, 14 de fechamento, 9 de desatribuição, nenhum de reabertura |
| Apontamento de horas | `dados/gestao/horas.csv`, com 26 atividades e **todas as horas e datas em branco** |
| Atas | 1 (ata 01, data aproximada, registrada depois) e a retrospectiva da E1 em PDF, na raiz |

<p class="legenda">Tabela 1. Retrato numérico do repositório na data de corte. Fonte: elaborado pelos autores a partir de <code>issues.json</code>, <code>issue_events.jsonl</code>, <code>prs.json</code>, <code>milestones.json</code>, <code>releases.json</code>, <code>tags.csv</code> e <code>commits.csv</code>, extraídos em 10/11/2026.</p>

## 2. Histórico de commits

| Autor (consolidado pelo `.mailmap`) | Commits | Linhas adicionadas | Semana ISO dos commits |
|---|---:|---:|---|
| Maykon Junio dos Santos Soares | 13 | 5.960 (5.448 no commit de migração) | 2026-W43, todos em 25/10/2026 |
| João Pedro Sampaio Maciel | 1 | 0 (PDF da retrospectiva, enviado pela interface web) | 2026-W44 (28/10/2026) |
| github-actions (coleta semanal do PSM) | 4 | 7 | 2026-W44 a 2026-W46 |
| Bernardo, Carlos e Pedro | 0 | 0 | — |

<p class="legenda">Tabela 2. Commits na <code>main</code> por autor. Fonte: elaborado pelos autores a partir de <code>commits.csv</code>, extraído em 10/11/2026.</p>

Observações:

- **Todo o conteúdo da E1 entrou na `main` em um único dia** (25/10/2026, entre 10h34 e 23h34), na véspera do prazo. Desde então, os únicos commits são o PDF da retrospectiva e os retratos automáticos.
- A primeira versão da Fase 1 foi escrita no repositório original da equipe ([Bercacos/Qualidade-de-Software---Marlyn-Wescoff](https://github.com/Bercacos/Qualidade-de-Software---Marlyn-Wescoff)), que tem 3 commits de Bernardo, de 19/10/2026. Esse conteúdo foi migrado para o repositório da disciplina no commit `d64b70e`, de Maykon, com 5.448 linhas. Por isso, **commits e linhas não mostram quem escreveu o quê na E1**.
- Os diretórios mais alterados pelos integrantes foram `docs/` (12 commits), a raiz (9), `artigo/` (8) e `dados/` (6).
- Os commits têm mensagem no imperativo e em português, como pede o `CONTRIBUTING.md`, mas nenhum cita uma issue.

## 3. Issues e milestones

- **As 14 issues da E1 foram criadas em 27 segundos** (25/10/2026, 14h26 UTC) e **fechadas em 12 minutos** (26/10/2026, entre 02h14 e 02h26 UTC), todas pela mesma conta. A mediana de 0,5 dia de tempo de ciclo registrada em 26/10 mede o intervalo administrativo, e não a duração do trabalho.
- As 31 mensagens nas issues da E1 são da mesma conta: as sugestões de responsável, as atualizações e os registros de "revisão concluída, sem alterações pedidas". **Não há registro, em issue ou PR, de uma não conformidade encontrada em revisão.**
- Das 14 issues da E1, 9 não tinham responsável atribuído. As 5 restantes estavam com Maykon (4), Bernardo (2), João Pedro (1) e Pedro (1); algumas tinham mais de um responsável.
- Labels existentes até a data de corte: `entrega-1`, `revisão`, `pendência-da-equipe` e as padrão do GitHub. Não havia labels de fase, tipo, tamanho ou prioridade.
- O plano de medição (`docs/gestao/plano-psm.md`) cita uma `Sprint 1` (13/10 a 19/10/2026) que **não existe como milestone**. A `Sprint 2 - Entrega 1` continuava aberta 15 dias depois do prazo.
- Os retratos `psm-2026-10-26-2.csv`, `psm-2026-10-26-3.csv`, `psm-2026-11-02.csv` e `psm-2026-11-09.csv` são idênticos: **não houve issue nova nem fechada entre 26/10 e 09/11/2026**.

## 4. Pull requests, releases, board e esforço

- **Fluxo de integração:** trunk, com commits direto na `main` e nenhum pull request. O artigo da E1 (`artigo/main.tex`, Seção 3.2) diz que "a integração na main é feita por pull request revisado por outro integrante", o que não corresponde ao histórico.
- **Release E1:** a tag leve `E1` aponta para `172e1af` (25/10/2026, 23h25). Os commits `a35c79e` (mapa dos critérios, termo de consentimento, coleta semanal, CONTRIBUTING) e `b1097fb` (separação das medições do PSM) foram feitos 7 e 9 minutos depois, antes do prazo, mas **ficaram fora da tag**.
- **Board:** não existe, então não há histórico de transição de estado (A Fazer, Em Progresso, Em Revisão).
- **Esforço:** não há nenhuma hora registrada. As atas não registram duração das reuniões. A retrospectiva de 28/10/2026 lista apenas 2 dos 5 integrantes e deixa em branco o link para o commit.

## 5. Fontes de dados e medidas que elas habilitam

| Fonte | Disponibilidade na data de corte | Medidas habilitadas |
|---|---|---|
| Commits da `main` (`commits.csv`) | Completa desde 25/10; não cobre a primeira versão, feita em outro repositório | B3 (cadência), C2 (dimensão commits e linhas), linhas verticais de marcos |
| Issues (`issues.json`) | Completa, mas as datas da E1 não refletem o trabalho (criação e fechamento em lote) | A1, A2, A4, B1, B2 a partir da E2 |
| Eventos de issues (`issue_events.jsonl`) | Completa; nenhuma reabertura registrada | A3 (só criada e fechada), B4 (reaberturas), C2 (issues fechadas por membro) |
| Milestones (`milestones.json`) | Parcial: só a sprint da E1, sem os marcos PC1, E2 e Apresentação | A1, A2, A4 |
| Pull requests (`prs.json`) | Inexistente | C2 (revisões de PR), B4 (não conformidades contidas), B1 (tempo de revisão) |
| Releases e tags | Parcial: só E1, com a tag antes dos últimos commits | A4, B3 |
| Project board | Inexistente | A3 completo (estados intermediários), B1 com início real |
| Apontamento de horas | Arquivo existe, sem nenhum valor | C1, C2 (dimensão horas), C3 |
| Atas e retrospectiva | 1 ata aproximada e 1 retrospectiva fora da pasta de atas | Evidência das decisões de gestão (Etapa 6) |

<p class="legenda">Tabela 3. Fontes de dados, disponibilidade e medidas que elas habilitam. Os identificadores A1 a C3 são as medidas definidas em <a href="../02-construtos-de-medicao/">Construtos de medição</a>. Fonte: elaborado pelos autores a partir dos arquivos de <code>dados/brutos/</code>, extraídos em 10/11/2026.</p>

## 6. Lacunas e decisões

Para cada lacuna, a decisão é uma de três: **(a)** corrigir via retrofit, **(b)** usar medida substituta ou **(c)** declarar a limitação. Lacuna é resultado: nenhuma delas é preenchida com estimativa apresentada como medição.

| Nº | Lacuna | Decisão | Como |
|---|---|---|---|
| L1 | Nenhuma hora registrada na E1 | (a) e (c) | Novo apontamento `esforco.csv` (#20). As horas da E1 são reconstruídas em reunião, marcadas como `reconstruido` e declaradas nas ameaças à validade |
| L2 | Nenhum pull request; não há evidência de revisão por pares | (a) a partir da E2; (c) para a E1 | Toda mudança entra por PR revisado por outro integrante, desde as issues #16, #18 e #20. Para a E1, C2 não usa a dimensão "revisões de PR" |
| L3 | Datas de criação e fechamento das issues da E1 não refletem o trabalho | (c) | A1, A2 e B1 da E1 são apresentados só como registro histórico e não entram em média, mediana ou referência de velocidade |
| L4 | Não há board nem histórico de estados | (a) e (b) | Board criado na Etapa 2 (#19). Antes dele, o fluxo cumulativo usa só "criada" e "fechada" |
| L5 | Milestones não correspondem aos marcos da disciplina | (a) | Milestones E1, PC1, E2 e Apresentação (#18) |
| L6 | Issues sem classificação de fase, tipo ou tamanho | (a) | Labels `fase/`, `tipo/`, `tamanho/`, `prioridade/` e `retrabalho`, aplicadas às 32 issues (#18) |
| L7 | Commits não mostram a autoria do conteúdo da E1 (migração de outro repositório) | (b) e (c) | C2 usa a visão multidimensional (horas, issues, revisões); o repositório original entra como fonte complementar da primeira versão da Fase 1 |
| L8 | Nenhuma não conformidade registrada em revisão interna | (c) para a E1; (a) para a E2 | Taxa de escape da E1 é calculada só com as escapadas (apontamentos da docente). Na E2, cada não conformidade vira comentário de revisão no PR ou issue com label `retrabalho` |
| L9 | Tag `E1` não inclui os dois últimos commits entregues | (c) | A tag não é movida, para não reescrever o que foi entregue. A4 e B3 usam a data da release |
| L10 | Retratos semanais idênticos entre 26/10 e 09/11 | (c) | É um resultado: duas semanas sem progresso registrado. Vai para o registro de decisões (Etapa 6) |
| L11 | Retrospectiva fora da pasta de atas e sem referência no site | (a) | Movida para `atas/` e citada no registro de decisões (#28) |
| L12 | Identidades no Git sem nome completo e sem padrão | (a) | `.mailmap` com o nome de `docs/sobre/equipe.md` (#18) |

<p class="legenda">Tabela 4. Lacunas encontradas e decisão para cada uma. Fonte: elaborado pelos autores.</p>

## 7. Ações de instrumentação

Registro das ações feitas para tornar o repositório mensurável, sem reescrever a história.

| Data | Ação | Issue e PR | Lacunas |
|---|---|---|---|
| 10/11/2026 | Extração dos dados brutos para `docs/metricas/dados/brutos/`, com fonte e comando de cada arquivo | #16, PR #33 | Base de todas |
| 10/11/2026 | Labels de fase, tipo, tamanho, prioridade e retrabalho criadas e aplicadas às issues #1 a #32 | #18, PR #34 | L6 |
| 10/11/2026 | Milestone `Sprint 2 - Entrega 1` renomeado para `E1 - 26/10/2026` e fechado; `Gestão PSM/CID - Entrega 2` renomeado para `E2`; `PC1` e `Apresentação` criados (prazos a preencher) | #18, PR #34 | L5 |
| 10/11/2026 | `.mailmap` criado e convenção de labels e milestones documentada no `CONTRIBUTING.md` | #18, PR #34 | L12 |
| 10/11/2026 | Apontamento `esforco.csv` criado, com as atividades da E1 migradas e as horas em branco, à espera da reconstrução | #20, PR #35 | L1 |
| 10/11/2026 | Fluxo por branch e pull request revisado adotado a partir das issues da gestão PSM/CID | PRs #33 em diante | L2 |
| Pendente | Project board com os estados do fluxo | #19 | L4 |

<p class="legenda">Tabela 5. Ações de instrumentação do repositório. Fonte: elaborado pelos autores.</p>
