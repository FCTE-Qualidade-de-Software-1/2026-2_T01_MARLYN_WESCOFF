# Árvore GQM de resultados

<!-- Página gerada por scripts/gera_arvore_resultados.py a partir de dados/avaliacao/calculos.csv. Não editar à mão. -->

Na Fase 2 o GQM foi definido de cima para baixo: objetivo, questões e métricas ([Diagrama GQM](../fase-2/diagrama-gqm.md)). Na Fase 4 ele é **interpretado de baixo para cima**: cada métrica medida recebe uma nota pelos [níveis de pontuação](../fase-2/niveis-e-julgamento.md), a nota da questão é o mínimo das notas das suas métricas e o objetivo é julgado pelo pior caso entre as questões.

!!! info "Situação da coleta: 12 de 12 métricas"
    Gerada a partir de `dados/avaliacao/calculos.csv`. Métricas ainda sem medidas aparecem em cinza, como *pendente*, e o objetivo correspondente fica *incompleto*.

## Árvore

```mermaid
flowchart BT
    G1["<b>G1 · Adequação funcional</b><br/>Não atende"]:::n1
    Q11["<b>Q1.1</b> O núcleo dá conta das tarefas?<br/>nota 4"]:::n4
    Q11 --> G1
    Q12["<b>Q1.2</b> Notas e prazos saem certos?<br/>nota 1"]:::n1
    Q12 --> G1
    Q13["<b>Q1.3</b> As tarefas saem sem improviso?<br/>nota 4"]:::n4
    Q13 --> G1
    G2["<b>G2 · Compatibilidade</b><br/>Não atende"]:::n1
    Q21["<b>Q2.1</b> Os dados entram e saem por arquivo?<br/>nota 4"]:::n4
    Q21 --> G2
    Q22["<b>Q2.2</b> Os dados chegam como saíram?<br/>nota 1"]:::n1
    Q22 --> G2
    Q23["<b>Q2.3</b> Um sistema externo consegue usar o Moodle?<br/>nota 4"]:::n4
    Q23 --> G2
    Q24["<b>Q2.4</b> Divide o servidor sem atrapalhar?<br/>nota 2"]:::n2
    Q24 --> G2
    G3["<b>G3 · Flexibilidade</b><br/>Atende"]:::n4
    Q31["<b>Q3.1</b> Funciona nos dispositivos dos usuários?<br/>nota 4"]:::n4
    Q31 --> G3
    Q32["<b>Q3.2</b> A TI pode escolher o PHP?<br/>nota 4"]:::n4
    Q32 --> G3
    Q33["<b>Q3.3</b> Instala e atualiza pela documentação?<br/>nota 4"]:::n4
    Q33 --> G3
    Q34["<b>Q3.4</b> A atualização mantém os dados?<br/>nota 4"]:::n4
    Q34 --> G3
    M11["<b>M1.1</b> Cobertura funcional<br/>1,00 · nota 4<br/>H1.1 confirmada"]:::n4
    M12["<b>M1.2</b> Correção funcional<br/>0,95 · nota 1<br/>H1.2 refutada"]:::n1
    M13["<b>M1.3</b> Pertinência funcional<br/>1,00 · nota 4<br/>H1.3 refutada"]:::n4
    M21["<b>M2.1</b> Intercâmbio de formatos<br/>1,00 · nota 4<br/>H2.1 confirmada"]:::n4
    M22["<b>M2.2</b> Integridade<br/>0,73 · nota 1<br/>H2.2 refutada"]:::n1
    M23["<b>M2.3</b> Conectividade REST<br/>1,00 · nota 4<br/>H2.3 confirmada"]:::n4
    M24["<b>M2.4</b> Coexistência disponível<br/>0,67 · nota 2<br/>H2.4 refutada"]:::n2
    M31["<b>M3.1</b> Adaptab. acesso<br/>1,00 · nota 4<br/>H3.1 confirmada"]:::n4
    M32["<b>M3.2</b> Adaptab. PHP<br/>1,00 · nota 4<br/>H3.2 confirmada"]:::n4
    M33["<b>M3.3</b> Sucesso de instalação<br/>1,00 · nota 4<br/>H3.3 refutada"]:::n4
    M34["<b>M3.4</b> Tempo de instalação<br/>1,18 min · nota 4<br/>H3.3 confirmada"]:::n4
    M35["<b>M3.5</b> Preservação de dados<br/>1,00 · nota 4<br/>H3.4 confirmada"]:::n4
    M11 --> Q11
    M13 --> Q11
    M12 --> Q12
    M13 --> Q13
    M21 --> Q21
    M21 --> Q22
    M22 --> Q22
    M23 --> Q23
    M24 --> Q24
    M31 --> Q31
    M32 --> Q32
    M33 --> Q33
    M34 --> Q33
    M35 --> Q34
    classDef n4 fill:#c8e6c9,stroke:#2e7d32,color:#1b1b1b
    classDef n3 fill:#e6f4d7,stroke:#558b2f,color:#1b1b1b
    classDef n2 fill:#ffe0b2,stroke:#ef6c00,color:#1b1b1b
    classDef n1 fill:#ffcdd2,stroke:#c62828,color:#1b1b1b
    classDef pend fill:#eeeeee,stroke:#9e9e9e,color:#555555,stroke-dasharray:4 3
```

<p class="legenda">Figura 1. Árvore GQM de resultados, das métricas (embaixo) aos objetivos (em cima). Verde: nota 4 ou 3; laranja: nota 2; vermelho: nota 1; cinza tracejado: pendente. Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>

## Por objetivo

### G1 – Adequação funcional

**Julgamento: Não atende.** Decisão D1: Não prosseguir sem correção ou contorno documentado; candidata à ação de melhoria (D4).

| Questão | Métricas (valor · nota) | Nota da questão | Hipóteses |
|---|---|---|---|
| **Q1.1** O núcleo dá conta das tarefas? | M1.1 1,00 · 4<br>M1.3 1,00 · 4 | 4 (Excelente) | H1.1: confirmada<br>H1.3: refutada |
| **Q1.2** Notas e prazos saem certos? | M1.2 0,95 · 1 | 1 (Crítico) | H1.2: refutada |
| **Q1.3** As tarefas saem sem improviso? | M1.3 1,00 · 4 | 4 (Excelente) | H1.3: refutada |

<p class="legenda">Tabela 1. Notas das questões de G1: mínimo das notas das métricas. Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>

### G2 – Compatibilidade

**Julgamento: Não atende.** Decisão D2: Não prosseguir sem correção ou contorno documentado; candidata à ação de melhoria (D4).

| Questão | Métricas (valor · nota) | Nota da questão | Hipóteses |
|---|---|---|---|
| **Q2.1** Os dados entram e saem por arquivo? | M2.1 1,00 · 4 | 4 (Excelente) | H2.1: confirmada |
| **Q2.2** Os dados chegam como saíram? | M2.1 1,00 · 4<br>M2.2 0,73 · 1 | 1 (Crítico) | H2.1: confirmada<br>H2.2: refutada |
| **Q2.3** Um sistema externo consegue usar o Moodle? | M2.3 1,00 · 4 | 4 (Excelente) | H2.3: confirmada |
| **Q2.4** Divide o servidor sem atrapalhar? | M2.4 0,67 · 2 | 2 (Insuficiente) | H2.4: refutada |

<p class="legenda">Tabela 2. Notas das questões de G2: mínimo das notas das métricas. Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>

### G3 – Flexibilidade

**Julgamento: Atende.** Decisão D3: Prosseguir.

| Questão | Métricas (valor · nota) | Nota da questão | Hipóteses |
|---|---|---|---|
| **Q3.1** Funciona nos dispositivos dos usuários? | M3.1 1,00 · 4 | 4 (Excelente) | H3.1: confirmada |
| **Q3.2** A TI pode escolher o PHP? | M3.2 1,00 · 4 | 4 (Excelente) | H3.2: confirmada |
| **Q3.3** Instala e atualiza pela documentação? | M3.3 1,00 · 4<br>M3.4 1,18 min · 4 | 4 (Excelente) | H3.3: confirmada<br>H3.3: refutada |
| **Q3.4** A atualização mantém os dados? | M3.5 1,00 · 4 | 4 (Excelente) | H3.4: confirmada |

<p class="legenda">Tabela 3. Notas das questões de G3: mínimo das notas das métricas. Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>

As evidências de cada métrica estão em `dados/avaliacao/<métrica>/` no repositório, e as hipóteses refutadas são explicadas pelas [medidas de contexto](../fase-2/abstraction-sheets.md) de cada coleta.
