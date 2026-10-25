# Registro de medições

Cada medição é um retrato datado gerado por `scripts/psm_coleta.py` e guardado em `dados/gestao/`. Para cada retrato, a equipe registra a **interpretação** (comparação com os critérios do [Plano de medição](plano-psm.md)) e a **decisão de gestão** tomada.

## Como gerar uma medição

```bash
python3 scripts/psm_coleta.py --repo FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF
```

O script imprime o resumo em Markdown (para colar abaixo) e grava `dados/gestao/psm-AAAA-MM-DD.csv`.

## Medições

| Data | Sprint | Planejado vs. concluído | Razão de esforço (R/E) | Custo realizado | Tempo de ciclo (mediana) | Issues paradas | Interpretação | Decisão |
|---|---|---|---|---|---|---|---|---|
| *a registrar* | Sprint 2 | | | | | | | |

<p class="legenda">Tabela 1. Registro das medições do PSM/CID. Fonte: issues do GitHub e `dados/gestao/horas.csv`.</p>

!!! warning "Pendência da equipe"
    A primeira medição deve ser gerada depois que as issues da Entrega 1 forem cadastradas nos milestones e as horas forem lançadas em `dados/gestao/horas.csv`. Nenhum valor deve ser preenchido nesta tabela sem o arquivo de dados correspondente no repositório.
