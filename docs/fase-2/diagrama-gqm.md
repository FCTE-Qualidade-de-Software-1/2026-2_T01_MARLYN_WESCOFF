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
        Q11["Q1.1 Cobertura das tarefas"]
        Q12["Q1.2 Correção dos resultados"]
        Q13["Q1.3 Conclusão sem contorno"]
        Q21["Q2.1 Formatos trocados"]
        Q22["Q2.2 Integridade dos dados"]
        Q23["Q2.3 Serviços web"]
        Q24["Q2.4 Coexistência"]
        Q31["Q3.1 Ambientes de acesso"]
        Q32["Q3.2 Versões de PHP"]
        Q33["Q3.3 Instalação e atualização"]
        Q34["Q3.4 Preservação na atualização"]
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
    Q11 --> M11
    Q12 --> M12
    Q13 --> M13
    Q21 --> M21
    Q22 --> M22
    Q23 --> M23
    Q24 --> M24
    Q31 --> M31
    Q32 --> M32
    Q33 --> M33 & M34
    Q34 --> M35
```

<p class="legenda">Figura 1. Diagrama GQM com os três objetivos, 11 questões e 12 métricas, organizados pelos níveis conceitual, operacional e quantitativo. Fonte: elaboração própria.</p>

## Leitura do diagrama

- Cada objetivo corresponde a uma característica priorizada na Fase 1 e a uma decisão (G1 → D1, G2 → D2, G3 → D3).
- Toda métrica responde a exatamente uma questão; Q3.3 é respondida por duas métricas complementares (sucesso e tempo).
- Não há métrica "solta": a [Rastreabilidade](rastreabilidade.md) confere a ligação de cada métrica até a necessidade da parte interessada.
