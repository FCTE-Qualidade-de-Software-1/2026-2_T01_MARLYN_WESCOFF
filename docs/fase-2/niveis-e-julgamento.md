# Níveis de pontuação e critérios de julgamento

"Julgar a qualidade" é interpretar os resultados das medições segundo critérios estabelecidos **antes** da coleta (Aula 07). Esta página define, para todas as métricas, como o valor medido vira uma nota e como as notas viram o julgamento de cada questão e de cada objetivo.

## Escala de notas

| Nota | Nível | Significado para a Coordenação de TI |
|---|---|---|
| **4** | Excelente | Atende integralmente; nenhuma ação necessária |
| **3** | Bom | Desvio pequeno, de baixo impacto e com contorno conhecido |
| **2** | Insuficiente | Desvio que exige ação antes da migração (teste extra, ajuste de procedimento, comunicação) |
| **1** | Crítico | Desvio que impede a tarefa ou corrompe dados; bloqueia a migração até correção |

<p class="legenda">Tabela 1. Escala de notas usada em todas as métricas. Fonte: elaboração própria.</p>

## Níveis de pontuação por métrica

| Métrica | Nota 4 | Nota 3 | Nota 2 | Nota 1 |
|---|---|---|---|---|
| M1.1 Cobertura funcional | 1,00 (12/12) | ≥ 0,92 (11/12) | ≥ 0,83 (10/12) | < 0,83 |
| M1.2 Correção funcional | 1,00 | — | ≥ 0,95, com divergência só em prazo, sem alterar nota | < 0,95, ou qualquer nota final errada |
| M1.3 Pertinência funcional | 1,00 | ≥ 0,92 (1 contorno) | ≥ 0,75 (até 3) | < 0,75 |
| M2.1 Intercâmbio de formatos | 1,00 (7/7) | ≥ 0,85 (6/7) | ≥ 0,70 (5/7) | < 0,70 |
| M2.2 Integridade dos dados | 1,00 | ≥ 0,99 | ≥ 0,95 | < 0,95 |
| M2.3 Serviços web | 1,00 (6/6) | ≥ 0,83 (5/6) | ≥ 0,66 (4/6) | < 0,66 |
| M2.4 Coexistência | 1,00 (3/3) | — | 0,66 (2/3), com recuperação sem intervenção | ≤ 0,66 com intervenção, ou < 0,66 |
| M3.1 Ambiente de acesso (pior ambiente) | 1,00 | ≥ 0,875 (7/8) | ≥ 0,75 (6/8) | < 0,75 |
| M3.2 Versão de PHP (pior versão) | 1,00 | ≥ 0,92 | ≥ 0,83 | < 0,83 |
| M3.3 Sucesso de instalação | 1,00 (6/6) | ≥ 0,83 (5/6) | ≥ 0,66 (4/6) | < 0,66 |
| M3.4 Tempo de instalação (mediana) e retentativas | ≤ 15 min e R = 0 | ≤ 30 min e R ≤ 1 | ≤ 60 min e R ≤ 3 | > 60 min ou R > 3 |
| M3.5 Preservação na atualização | 1,00 | — | ≥ 0,975 (perda de 1 item não acadêmico) | qualquer perda de nota, envio ou usuário |

<p class="legenda">Tabela 2. Níveis de pontuação de todas as métricas. "—" indica que o nível não existe para aquela métrica. Fonte: elaboração própria.</p>

### Justificativa dos limites

- **Sem nota 3 em M1.2, M2.4 e M3.5:** uma nota final errada, um serviço vizinho derrubado ou um envio de estudante perdido não são "desvios pequenos"; por isso, a métrica vai direto de Excelente para Insuficiente ou Crítico.
- **M1.1, M2.1, M2.3 e M3.3** usam degraus de uma unidade (uma tarefa, um formato, uma função, uma execução), o que torna o julgamento inequívoco com populações pequenas.
- **M3.4:** os limites de tempo são **valores candidatos**. A instalação limpa pela linha de comando é esperada em poucos minutos em máquina local; os limites serão confirmados em um piloto na Fase 3 e congelados antes da coleta. Qualquer mudança será registrada em ata.
- Os limites são **decisões da equipe**, fundamentadas no impacto para o requisitante; não são valores normativos da ISO/IEC 25010 ou 25023.

## Regras de julgamento

### Da métrica para a questão

| Questão | Regra |
|---|---|
| Q1.1 | nota(M1.1) |
| Q1.2 | nota(M1.2) |
| Q1.3 | nota(M1.3) |
| Q2.1 | nota(M2.1) |
| Q2.2 | nota(M2.2) |
| Q2.3 | nota(M2.3) |
| Q2.4 | nota(M2.4) |
| Q3.1 | nota(M3.1) |
| Q3.2 | nota(M3.2) |
| Q3.3 | mínimo(nota(M3.3), nota(M3.4)) |
| Q3.4 | nota(M3.5) |

<p class="legenda">Tabela 3. Regra de julgamento de cada questão. Fonte: elaboração própria.</p>

### Da questão para o objetivo

O julgamento de cada objetivo usa o **pior caso** entre as questões, porque uma falha grave em uma subcaracterística não é compensada por bons resultados em outra (uma nota errada não é compensada por um fórum que funciona):

| Condição sobre as notas das questões do objetivo | Julgamento do objetivo | Ação para a decisão (D1, D2 ou D3) |
|---|---|---|
| Todas ≥ 3 | **Atende** | Prosseguir |
| Nenhuma = 1 e ao menos uma = 2 | **Atende com ressalvas** | Prosseguir com as ações de mitigação listadas no relatório |
| Ao menos uma = 1 | **Não atende** | Não prosseguir sem correção ou contorno documentado; a falha entra como candidata à ação de melhoria (D4) |

<p class="legenda">Tabela 4. Critério de julgamento dos objetivos e ação correspondente. Fonte: elaboração própria.</p>

### Exemplo de aplicação

Suponha que, na Fase 4, M2.1 = 6/7 = 0,86 (nota 3), M2.2 = 0,97 (nota 2, por perda de acentuação na exportação CSV), M2.3 = 1,00 (nota 4) e M2.4 = 1,00 (nota 4). As notas das questões são Q2.1 = 3, Q2.2 = 2, Q2.3 = 4 e Q2.4 = 4. Não há nota 1 e há uma nota 2, então **G2 = Atende com ressalvas**. A ação recomendada à Coordenação de TI seria documentar a codificação correta para a exportação de notas e incluir a verificação no teste de regressão da migração.

### Comparação com as hipóteses

Na Fase 4, cada valor medido também será comparado à hipótese da questão (H1.1 a H3.4). A hipótese é **confirmada** quando o valor está dentro do esperado e **refutada** quando não está; hipóteses refutadas serão explicadas usando os fatores de variação das [abstraction sheets](abstraction-sheets.md).
