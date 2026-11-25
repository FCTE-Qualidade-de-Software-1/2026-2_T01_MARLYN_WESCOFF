# Objetivos, questões e hipóteses

Cada característica priorizada na [Fase 1](../fase-1/caracteristicas.md) gera um objetivo de medição no template da Aula 08. Os três objetivos compartilham o **objeto** (Moodle 5.3 LTS na instalação de referência), o **propósito** (entender o nível de qualidade para apoiar uma decisão) e o **ponto de vista** (Coordenação de TI, requisitante no cenário). O **foco de qualidade** vem da característica e de suas subcaracterísticas no [modelo adaptado](../fase-1/modelo-de-qualidade.md).

As questões caracterizam o objeto em relação ao foco de qualidade (Aula 08): perguntam sobre o Moodle, e não sobre a métrica. Cada questão é refinada por uma ou mais métricas, e uma métrica pode servir a mais de uma questão (coluna **Métricas**).

As hipóteses vêm das [abstraction sheets](abstraction-sheets.md) e são a **resposta que a equipe espera** para cada questão (o *baseline*), com o valor esperado. Elas não são o critério de aceitação: a régua que diz se o resultado é aceitável são os [níveis de pontuação e o critério de julgamento](niveis-e-julgamento.md), definidos à parte. Por isso, uma hipótese pode ser refutada sem que a nota caia, e o contrário também. H3.3, por exemplo, espera que uma atualização falhe na primeira tentativa: se as 6 execuções derem certo, a hipótese é refutada e M3.3 ainda recebe nota 4.

## G1 – Adequação funcional

| Template GQM | G1 |
|---|---|
| **Analisar** | o núcleo do Moodle 5.3 LTS |
| **para o propósito de** | entender |
| **com respeito à** | adequação funcional (completude, correção e pertinência funcional) das tarefas acadêmicas essenciais |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | decisão de adoção/atualização para a 5.3 LTS (D1), em instalação local de referência com dados fictícios |

| Questão | Métricas | Hipótese (resposta esperada) |
|---|---|---|
| **Q1.1** (completude) O núcleo do Moodle, sem plugins, dá conta das tarefas acadêmicas essenciais da instituição? | M1.1, M1.3 | **H1.1** Sim. Esperamos que o núcleo tenha função para as 12 tarefas do catálogo (12 de 12) e que só uma delas peça contorno (ver H1.3). |
| **Q1.2** (correção) O Moodle calcula notas e controla prazos como a instituição espera? | M1.2 | **H1.2** Sim. Esperamos que todos os casos de teste deem o resultado do oráculo, sem nenhuma divergência em notas ou prazos. |
| **Q1.3** (pertinência) Docentes e gestão conseguem fazer as tarefas pelo caminho previsto, sem improvisar passos? | M1.3 | **H1.3** Quase sempre. Esperamos que só a restauração de backup como novo curso exija contorno (11 de 12 tarefas sem contorno). |

<p class="legenda">Tabela 1. Objetivo, questões e hipóteses de G1. Fonte: elaboração própria.</p>

## G2 – Compatibilidade

| Template GQM | G2 |
|---|---|
| **Analisar** | o núcleo do Moodle 5.3 LTS e suas interfaces de troca de dados |
| **para o propósito de** | entender |
| **com respeito à** | compatibilidade (interoperabilidade por arquivos e serviços web; coexistência em servidor compartilhado) |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | decisão sobre manter ou adaptar as integrações antes da migração (D2), com sistemas externos simulados |

| Questão | Métricas | Hipótese (resposta esperada) |
|---|---|---|
| **Q2.1** (interoperabilidade) A instituição consegue levar dados para o Moodle e tirá-los dele nos arquivos que os outros sistemas usam? | M2.1 | **H2.1** Sim, com no máximo uma exceção. Esperamos que 6 ou 7 dos 7 formatos sejam trocados sem erro. |
| **Q2.2** (interoperabilidade) Os dados que passam entre o Moodle e os outros sistemas chegam ao destino como saíram? | M2.1, M2.2 | **H2.2** Sim. Esperamos todos os registros idênticos à referência; o risco conhecido é a acentuação no CSV. |
| **Q2.3** (interoperabilidade) Um sistema externo consegue consultar e alterar dados do Moodle pelos serviços web, sem intervenção manual? | M2.3 | **H2.3** Sim. Esperamos que as 6 funções respondam sem erro e com dados coerentes (6 de 6). |
| **Q2.4** (coexistência) O Moodle pode dividir o servidor com outras aplicações sem atrapalhá-las? | M2.4 | **H2.4** Sim. Esperamos que nenhuma das 3 entidades vizinhas seja afetada (3 de 3). |

<p class="legenda">Tabela 2. Objetivo, questões e hipóteses de G2. Fonte: elaboração própria.</p>

## G3 – Flexibilidade

| Template GQM | G3 |
|---|---|
| **Analisar** | o Moodle 5.3 LTS e seus procedimentos oficiais de instalação e atualização |
| **para o propósito de** | entender |
| **com respeito à** | flexibilidade (adaptabilidade a ambientes de acesso e de servidor; instalabilidade) |
| **do ponto de vista da** | Coordenação de TI da instituição |
| **no contexto da** | definição do procedimento de migração e dos ambientes suportados (D3), em máquina virtual de referência |

| Questão | Métricas | Hipótese (resposta esperada) |
|---|---|---|
| **Q3.1** (adaptabilidade) Estudantes e docentes conseguem usar o Moodle a partir dos computadores e celulares que já têm? | M3.1 | **H3.1** Quase todos. Esperamos que os 3 ambientes de desktop concluam as 8 tarefas e que o Android falhe em no máximo uma (7 ou 8 de 8 no pior ambiente). |
| **Q3.2** (adaptabilidade) A TI pode escolher entre as versões de PHP suportadas sem que o Moodle mude de comportamento? | M3.2 | **H3.2** Sim. Esperamos o mesmo resultado nas 12 tarefas com PHP 8.3 e com PHP 8.4. |
| **Q3.3** (instalabilidade) A TI consegue instalar e atualizar o Moodle seguindo só a documentação oficial, em tempo previsível? | M3.3, M3.4 | **H3.3** Sim, com um tropeço. Esperamos que as 3 instalações limpas concluam e que uma atualização falhe na primeira tentativa por causa da nova raiz web `public/` (5 de 6); a instalação limpa deve levar menos de 15 min. |
| **Q3.4** (instalabilidade) A atualização da 4.5 para a 5.3 mantém os dados acadêmicos que já existem? | M3.5 | **H3.4** Sim. Esperamos os 40 itens de verificação iguais antes e depois da atualização (40 de 40). |

<p class="legenda">Tabela 3. Objetivo, questões e hipóteses de G3. Fonte: elaboração própria.</p>

## Revisão das questões

Seguindo a Aula 08 ("respondendo esta questão vou poder concluir algo sobre o meu objetivo?"), a equipe conferiu que:

- cada subcaracterística do modelo adaptado tem pelo menos uma questão;
- nenhuma questão é a própria métrica reescrita nem cita o nome dela: as questões perguntam sobre o **Moodle visto pela Coordenação de TI**, e as métricas definem **como contar**;
- onde uma contagem só não responde à questão, ela tem mais de uma métrica: Q1.1 usa M1.1 (há função?) e M1.3 (a função serve sem contorno?); Q2.2 usa M2.1 (o arquivo chegou?) e M2.2 (chegou igual?); Q3.3 usa M3.3 (concluiu?) e M3.4 (em quanto tempo?);
- todas as questões têm hipótese com valor esperado, o que permite comparar o esperado com o observado na Fase 4.
