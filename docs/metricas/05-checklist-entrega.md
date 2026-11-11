# Checklist de conformidade da gestão PSM/CID

**Data da verificação:** 11/11/2026  
**Escopo:** artefatos da gestão PSM/CID disponíveis na branch da issue #32, incluindo as dependências #29, #30 e #31.

Somente itens comprovados por arquivo versionado ou por uma verificação reexecutável estão marcados. A conferência foi feita sobre os dados com data de corte de 11/11/2026.

## Requisito da especificação — Seção 2

- [x] **As três categorias têm ao menos uma medida especificada e medida.** Os [construtos](02-construtos-de-medicao.md) especificam A1–A4, B1–B4 e C1–C3; o [dashboard](dashboard.md) apresenta indicadores das três categorias a partir dos consolidados.
- [x] **As evidências estão no repositório.** Commits, issues, pull requests, milestones, releases, tags e histórico do quadro estão em [`dados/brutos`](dados/brutos/README.md), e os indicadores estão no [dashboard](dashboard.md).
- [x] **Medições, interpretação e decisões de gestão estão registradas.** Os valores estão em [`dados/consolidados`](dados/consolidados/README.md), a interpretação está no [dashboard](dashboard.md) e as decisões, no [registro de decisões](03-registro-de-decisoes.md).

## Conformidade PSM

- [x] **Cada medida tem o construto completo.** As fichas A1–A4, B1–B4 e C1–C3 registram necessidade de informação, entidade, atributo, medidas básicas e derivadas, fórmula, unidade, fonte, coleta, critérios e análise nos [construtos de medição](02-construtos-de-medicao.md).
- [x] **Os critérios de decisão foram definidos antes da análise.** Os commits dos construtos (`c3e7976`, `768ef2f`, `bf6f402` e `9665cf3`) antecedem o commit do registro de decisões (`67fc374`); os limiares permanecem nas fichas das medidas.
- [x] **Há ao menos uma medida derivada por categoria.** A2 deriva percentual concluído; B1 deriva cycle time, lead time e percentis; C2 deriva participações percentuais e o índice multidimensional.
- [x] **A terminologia CID foi adaptada e documentada.** A equivalência entre capability/epic, feature, story, task, iteração e release está na seção [Adaptação da terminologia do CID](02-construtos-de-medicao.md#adaptacao-da-terminologia-do-cid).

## Rastreabilidade

- [x] **Todo gráfico rastreia até um CSV versionado.** As figuras A1, A2, A3, B1, B2, C1, C2 e C3 informam o arquivo-fonte e o [dashboard](dashboard.md) oferece links para os CSVs.
- [x] **Todo CSV consolidado é gerado por script reexecutável.** O mapeamento está no [catálogo dos consolidados](dados/consolidados/README.md); a geração é feita por `scripts/consolidar_metricas.py`, seguida por `scripts/gerar_graficos.py` e `scripts/gerar_dashboard.py`.
- [x] **Os dados reconstruídos estão marcados como tal.** O campo `tipo_registro` de [`esforco.csv`](dados/brutos/esforco.csv) distingue `reconstruido` de `registrado`, e essa distinção é preservada nos consolidados.
- [x] **`validar_dados.py` roda sem erros.** Execução em 11/11/2026: zero erros e quatro avisos conhecidos de revisor automatizado fora da lista da equipe nos PRs #40–#43.

## Rubrica

- [x] **GitPage atualizada, com versão, data e links funcionais (F2-C10, AG-C4).** O rodapé informa `Entrega 2 | Versão 2.0 · 11/11/2026`; `mkdocs build --strict` concluiu com sucesso em 11/11/2026.
- [x] **Figuras e tabelas numeradas, com legenda e fonte, citadas no texto (AG-C2).** O [dashboard](dashboard.md) numera as oito figuras e o [texto do artigo](04-texto-artigo.md) cita A2, B1 e C2; o PDF foi compilado e inspecionado.
- [x] **Tabela de Contribuição totalizando 100% e detalhando responsabilidades (AG-C5).** A tabela C2 consta no [texto do artigo](04-texto-artigo.md) e no Apêndice A do artigo SBC.
- [x] **Declaração de uso de IA específica (AG-C3).** A declaração única registra ferramenta, tarefa, conferência, ajuste e integrante em [Uso de IA](../sobre/uso-de-ia.md), coerente com o Apêndice B.
- [x] **Sem emojis, ícones ou figurinhas no conteúdo.** A busca por caracteres Unicode de emojis nos arquivos Markdown retornou zero ocorrência em 11/11/2026.
- [x] **Coerência com as Fases 1 e 2 já entregues (F2-C11).** A narrativa da [gestão PSM/CID](../gestao/index.md) liga as medidas às fases, e as páginas de [Fase 1](../fase-1/index.md) e [Fase 2](../fase-2/index.md) possuem links cruzados para a gestão.

## Comandos de verificação

```text
python scripts/validar_dados.py
python -m mkdocs build --strict
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Resultado em 11/11/2026: dados sem erros, GitPage construída em modo estrito e artigo compilado com 15 páginas totais, sendo o corpo anterior aos apêndices limitado a 14 páginas.

<p class="legenda">Checklist 1. Verificação final da gestão PSM/CID. Fonte: elaboração própria a partir dos artefatos versionados no repositório.</p>
