# Objetivos, questões e hipóteses

Cada característica priorizada na [Fase 1](../fase-1/caracteristicas.md) gera um objetivo de medição no template da Aula 08. Os três objetivos compartilham o **objeto** (Moodle 5.3 LTS na instalação de referência), o **propósito** (entender o nível de qualidade para apoiar uma decisão) e o **ponto de vista** (Coordenação de TI, requisitante no cenário). O **foco de qualidade** vem da característica e de suas subcaracterísticas no [modelo adaptado](../fase-1/modelo-de-qualidade.md).

As hipóteses vêm das [abstraction sheets](abstraction-sheets.md) e são escritas como valores esperados das métricas, para que possam ser confirmadas ou refutadas na Fase 4.

## G1 – Adequação funcional

| Template GQM | G1 |
|---|---|
| **Analisar** | o núcleo do Moodle 5.3 LTS |
| **para o propósito de** | entender |
| **com respeito à** | adequação funcional (completude, correção e pertinência funcional) das tarefas acadêmicas essenciais |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | decisão de adoção/atualização para a 5.3 LTS (D1), em instalação local de referência com dados fictícios |

| Questão | Hipótese |
|---|---|
| **Q1.1** (completude) Em que medida as funções do núcleo cobrem as tarefas acadêmicas essenciais do catálogo? | **H1.1** O núcleo oferece função para as 12 tarefas do catálogo (M1.1 = 1,00). |
| **Q1.2** (correção) Os resultados calculados pelo Moodle (notas automáticas, agregação do livro de notas e controle de prazos) correspondem aos resultados esperados? | **H1.2** Todos os casos de teste produzem o resultado do oráculo (M1.2 = 1,00). |
| **Q1.3** (pertinência) As funções disponíveis permitem concluir as tarefas sem recorrer a contornos? | **H1.3** No máximo uma tarefa exige contorno (M1.3 ≥ 0,92). |

<p class="legenda">Tabela 1. Objetivo, questões e hipóteses de G1. Fonte: elaboração própria.</p>

## G2 – Compatibilidade

| Template GQM | G2 |
|---|---|
| **Analisar** | o núcleo do Moodle 5.3 LTS e suas interfaces de troca de dados |
| **para o propósito de** | entender |
| **com respeito à** | compatibilidade (interoperabilidade por arquivos e serviços web; coexistência em servidor compartilhado) |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | decisão sobre manter ou adaptar as integrações antes da migração (D2), com sistemas externos simulados |

| Questão | Hipótese |
|---|---|
| **Q2.1** (interoperabilidade) Em que medida os formatos de arquivo oferecidos pelo núcleo são exportados e importados com sucesso entre o Moodle e outro sistema? | **H2.1** Pelo menos 6 dos 7 formatos são trocados com sucesso (M2.1 ≥ 0,85). |
| **Q2.2** (interoperabilidade) Os dados trocados chegam íntegros ao outro lado, sem perda nem alteração? | **H2.2** Todos os registros chegam íntegros (M2.2 = 1,00). |
| **Q2.3** (interoperabilidade) As funções de serviço web REST selecionadas atendem corretamente a um cliente externo? | **H2.3** As 6 funções respondem sem erro e com dados coerentes (M2.3 = 1,00). |
| **Q2.4** (coexistência) O Moodle opera no mesmo servidor que outras aplicações sem prejudicá-las? | **H2.4** Nenhuma das 3 entidades vizinhas é afetada (M2.4 = 1,00). |

<p class="legenda">Tabela 2. Objetivo, questões e hipóteses de G2. Fonte: elaboração própria.</p>

## G3 – Flexibilidade

| Template GQM | G3 |
|---|---|
| **Analisar** | o Moodle 5.3 LTS e seus procedimentos oficiais de instalação e atualização |
| **para o propósito de** | entender |
| **com respeito à** | flexibilidade (adaptabilidade a ambientes de acesso e de servidor; instalabilidade) |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | definição do procedimento de migração e dos ambientes suportados (D3), em máquina virtual de referência |

| Questão | Hipótese |
|---|---|
| **Q3.1** (adaptabilidade) Os fluxos essenciais funcionam em todos os ambientes de acesso previstos? | **H3.1** Os 3 ambientes de desktop concluem todas as tarefas; o Android falha em no máximo uma (M3.1 ≥ 0,875 no pior ambiente). |
| **Q3.2** (adaptabilidade) O Moodle se comporta da mesma forma nas versões de PHP suportadas? | **H3.2** Não há diferença entre PHP 8.3 e 8.4 (M3.2 = 1,00 nas duas). |
| **Q3.3** (instalabilidade) A instalação limpa e a atualização, seguindo a documentação oficial, concluem com êxito e em tempo razoável? | **H3.3** As 3 instalações limpas concluem; ao menos uma atualização falha na primeira tentativa por causa da raiz web `public/` (M3.3 ≥ 0,83); a instalação limpa leva até 15 min (M3.4). |
| **Q3.4** (instalabilidade) A atualização 4.5 → 5.3 preserva os dados acadêmicos existentes? | **H3.4** Todos os itens de verificação são preservados (M3.5 = 1,00). |

<p class="legenda">Tabela 3. Objetivo, questões e hipóteses de G3. Fonte: elaboração própria.</p>

## Revisão das questões

Seguindo a Aula 08 ("respondendo esta questão vou poder concluir algo sobre o meu objetivo?"), a equipe conferiu que:

- cada subcaracterística do modelo adaptado tem pelo menos uma questão;
- nenhuma questão é a própria métrica reescrita: as questões perguntam sobre a **característica do objeto** (cobertura, correção, integridade, preservação), e as métricas definem **como contar**;
- todas as questões têm hipótese numérica, o que permite comparar o esperado com o observado na Fase 4.
