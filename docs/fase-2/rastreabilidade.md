# Rastreabilidade Fase 1 → Fase 2

Esta página explicita que os objetivos de medição foram **derivados** da Fase 1 e não definidos isoladamente: o foco de qualidade vem das características priorizadas, o ponto de vista vem do requisitante e o contexto vem das decisões apoiadas.

## Elementos do objetivo GQM e sua origem

| Elemento do template | Valor usado em G1–G3 | Origem na Fase 1 |
|---|---|---|
| Analisar (objeto) | Moodle 5.3 LTS, núcleo, instalação de referência | [Produto avaliado](../fase-1/produto.md) e [Escopo](../fase-1/escopo.md) (objetos O1–O6) |
| Para o propósito de | Entender | [Propósito](../fase-1/proposito.md): a avaliação produz informação para uma decisão, não melhora nem controla o produto |
| Com respeito a (foco) | Adequação funcional, compatibilidade, flexibilidade | 1ª, 2ª e 3ª posições da [matriz de priorização](../fase-1/caracteristicas.md#resultado) |
| Do ponto de vista de | Coordenação de TI | [Requisitante no cenário](../fase-1/partes-interessadas.md#requisitante) |
| No contexto de | Decisões D1, D2 e D3 | [Decisões apoiadas](../fase-1/proposito.md#decisoes-apoiadas) |

<p class="legenda">Tabela 1. Origem de cada elemento dos objetivos. Fonte: elaboração própria.</p>

## Matriz de rastreabilidade completa

| Parte interessada e necessidade (Fase 1) | Decisão | Característica / subcaracterística | Questão | Métrica | Meta do ODS |
|---|---|---|---|---|---|
| Gestão acadêmica: tarefas essenciais cobertas | D1 | Adequação funcional / completude | Q1.1 | M1.1 | 4.3 |
| Docentes e tutores: notas e prazos corretos | D1 | Adequação funcional / correção | Q1.2 | M1.2 | 4.3 |
| Gestão acadêmica: sem customização para tarefas básicas | D1 | Adequação funcional / pertinência | Q1.3 | M1.3 | — |
| Integradores: importar usuários e exportar notas | D2 | Compatibilidade / interoperabilidade | Q2.1 | M2.1 | 4.4 |
| Integradores: dados sem retrabalho manual | D2 | Compatibilidade / interoperabilidade | Q2.2 | M2.2 | — |
| Integradores: consumir serviços web | D2 | Compatibilidade / interoperabilidade | Q2.3 | M2.3 | — |
| Administradores: servidor compartilhado sem interferência | D2 | Compatibilidade / coexistência | Q2.4 | M2.4 | — |
| Estudantes: acesso por navegadores e celular | D3 | Flexibilidade / adaptabilidade | Q3.1 | M3.1 | 4.a |
| Administradores: escolher a versão de PHP | D3 | Flexibilidade / adaptabilidade | Q3.2 | M3.2 | — |
| Administradores: procedimento previsível | D3 | Flexibilidade / instalabilidade | Q3.3 | M3.3, M3.4 | 4.a |
| Administradores e gestão acadêmica: nada se perde na atualização | D3 | Flexibilidade / instalabilidade | Q3.4 | M3.5 | 4.3 |

<p class="legenda">Tabela 2. Rastreabilidade entre necessidades, decisões, características, questões, métricas e ODS. Fonte: elaboração própria.</p>

## Verificação de consistência

| Verificação | Resultado |
|---|---|
| Toda característica priorizada tem um objetivo GQM | Sim (3/3) |
| Toda subcaracterística mantida no modelo adaptado tem ao menos uma questão | Sim (7/7) |
| Toda questão tem hipótese | Sim (11/11) |
| Toda métrica responde a uma questão | Sim (12/12) |
| Toda métrica tem níveis de pontuação | Sim (12/12) |
| Todo objetivo tem critério de julgamento ligado a uma decisão | Sim (3/3) |
| Nenhuma métrica mede capacidade de interação (usabilidade) | Sim |
| Toda métrica é coletável na instalação local de referência | Sim; M3.4 depende de piloto para calibrar limites |

<p class="legenda">Tabela 3. Verificação de consistência entre as Fases 1 e 2. Fonte: elaboração própria.</p>
