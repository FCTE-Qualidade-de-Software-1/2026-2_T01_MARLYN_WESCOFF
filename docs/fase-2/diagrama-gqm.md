# Diagrama GQM

O diagrama mostra a hierarquia completa do plano GQM nos três níveis da Aula 08: **conceitual** (objetivos), **operacional** (questões) e **quantitativo** (métricas). A definição desce do objetivo para as métricas; a interpretação, na Fase 4, sobe das métricas para o objetivo.

## Explorador interativo

Selecione um objetivo para ver suas questões, hipóteses e métricas.

<div id="gqm-explorer" class="gqm-explorer" aria-live="polite"></div>

## Hierarquia completa

```mermaid
flowchart LR
    subgraph C["Nível conceitual"]
        G1["G1 · Adequação funcional"]
        G2["G2 · Compatibilidade"]
        G3["G3 · Flexibilidade"]
    end
    subgraph O["Nível operacional"]
        Q11["Q1.1 O núcleo dá conta das tarefas?"]
        Q12["Q1.2 Notas e prazos saem certos?"]
        Q13["Q1.3 As tarefas saem sem improviso?"]
        Q21["Q2.1 Os dados entram e saem por arquivo?"]
        Q22["Q2.2 Os dados chegam como saíram?"]
        Q23["Q2.3 Um sistema externo consegue usar o Moodle?"]
        Q24["Q2.4 Divide o servidor sem atrapalhar?"]
        Q31["Q3.1 Funciona nos dispositivos dos usuários?"]
        Q32["Q3.2 A TI pode escolher o PHP?"]
        Q33["Q3.3 Instala e atualiza pela documentação?"]
        Q34["Q3.4 A atualização mantém os dados?"]
    end
    subgraph M["Nível quantitativo"]
        M11["M1.1 Cobertura funcional"]
        M12["M1.2 Correção funcional"]
        M13["M1.3 Pertinência funcional"]
        M21["M2.1 Intercâmbio de formatos"]
        M22["M2.2 Integridade"]
        M23["M2.3 Conectividade REST"]
        M24["M2.4 Coexistência disponível"]
        M31["M3.1 Adaptab. acesso"]
        M32["M3.2 Adaptab. PHP"]
        M33["M3.3 Sucesso de instalação"]
        M34["M3.4 Tempo de instalação"]
        M35["M3.5 Preservação de dados"]
    end
    G1 --> Q11 & Q12 & Q13
    G2 --> Q21 & Q22 & Q23 & Q24
    G3 --> Q31 & Q32 & Q33 & Q34
    Q11 --> M11 & M13
    Q12 --> M12
    Q13 --> M13
    Q21 --> M21
    Q22 --> M21 & M22
    Q23 --> M23
    Q24 --> M24
    Q31 --> M31
    Q32 --> M32
    Q33 --> M33 & M34
    Q34 --> M35
```

<p class="legenda">Figura 1. Diagrama GQM com os três objetivos, 11 questões e 12 métricas, com 14 ligações entre questões e métricas, organizados pelos níveis conceitual, operacional e quantitativo. Fonte: elaboração própria.</p>

## Leitura do diagrama

- Cada objetivo corresponde a uma característica priorizada na Fase 1 e a uma decisão (G1 → D1, G2 → D2, G3 → D3).
- As questões perguntam sobre o objeto, e as métricas refinam cada questão (Aula 08). Três questões precisam de duas métricas: Q1.1 (M1.1, há função, e M1.3, serve sem contorno), Q2.2 (M2.1, o arquivo chegou, e M2.2, chegou igual) e Q3.3 (M3.3, sucesso, e M3.4, tempo).
- Duas métricas servem a duas questões: M1.3 a Q1.1 e Q1.3; M2.1 a Q2.1 e Q2.2. A nota de uma questão é o mínimo das notas das suas métricas ([Níveis e julgamento](niveis-e-julgamento.md#da-metrica-para-a-questao)).
- Não há métrica "solta": a [Rastreabilidade](rastreabilidade.md) confere a ligação de cada métrica até a necessidade da parte interessada.
