# Gestão do projeto

A execução do projeto é acompanhada com o **PSM** (*Practical Software and Systems Measurement*) e o guia **CID** (*Continuous Iterative Development Measurement Framework*). No PSM, cada medida existe porque responde a uma **necessidade de informação** de quem gerencia o projeto e apoia uma **decisão** (Aula 09).

A especificação do trabalho exige medidas em três categorias de informação. A equipe escolheu uma medida principal por categoria, a partir da Tabela 5 do CID (Parte 1):

| Categoria de informação | Conceito mensurável | Medida | Pergunta de gestão |
|---|---|---|---|
| Calendário e Progresso | Progresso das unidades de trabalho | Planejado vs. concluído (*Committed vs. Completed*) | Vamos entregar o que planejamos para a sprint? |
| Recursos e Custos | Esforço da equipe | Esforço estimado vs. realizado (*Estimate vs. Actual Effort*) | Nossas estimativas de horas estão corretas? Quanto custou a entrega? |
| Desempenho dos Processos | Eficiência do processo (velocidade) | Tempo de ciclo (*Cycle Time*) | Quanto tempo uma tarefa leva para ser concluída? Há tarefas paradas? |

<p class="legenda">Tabela 1. Medidas do PSM/CID adotadas. Fonte: elaboração própria a partir do PSM/CID (2021), Parte 1, Tabela 5.</p>

| Página | Conteúdo |
|---|---|
| [Plano de medição](plano-psm.md) | Instância do modelo de informação de cada medida (template da Aula 09) |
| [Registro de medições](registro-medicoes.md) | Valores medidos, interpretação e decisões de gestão |
| [Atas de reunião](atas.md) | Decisões da equipe |

## Fontes dos dados

- **Issues e milestones do GitHub:** unidade de trabalho e sprint.
- **`dados/gestao/horas.csv`:** registro de horas por integrante e por issue.
- **`scripts/psm_coleta.py`:** lê as issues pela API do GitHub e o registro de horas, calcula as três medidas e grava um retrato datado em `dados/gestao/psm-AAAA-MM-DD.csv`.
