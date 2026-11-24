# Processo de trabalho

Esta página descreve como a equipe organiza o trabalho no repositório: do registro da tarefa em uma issue até a entrada da mudança na `main` por pull request revisado. As issues, as labels, os milestones e as horas registradas aqui são a fonte das medidas da [gestão PSM/CID](index.md).

## Fluxo de uma tarefa

1. **Abrir uma issue** com o modelo *Tarefa*: descrição, fase, estimativa em horas e critério de pronto. A issue é associada ao milestone da entrega, recebe as labels da Tabela 1 e é atribuída ao responsável.
2. **Mover a issue para "Em Progresso"** no [quadro de tarefas](https://github.com/orgs/FCTE-Qualidade-de-Software-1/projects/54) quando o trabalho começa, e não só quando termina. Essa data é o início do cycle time (B1).
3. **Criar um branch** a partir da `main`, com prefixo e assunto: `docs/fase-3-ambiente`, `artigo/resultados`, `fix/link-quebrado`.
4. **Fazer commits pequenos**, com mensagem no imperativo e em português, por exemplo "Adiciona as fichas das métricas de G2".
5. **Abrir um pull request** com o modelo do repositório, pedir a revisão de outro integrante e citar a issue com `Closes #N`. O GitHub só fecha a issue automaticamente com palavras-chave em inglês (`Closes`, `Fixes`).
6. **Registrar as horas** ao fim de cada sessão de trabalho, em `docs/metricas/dados/brutos/esforco.csv`, com `tipo_registro = registrado`. Se houve uso de IA, registrar também na [Declaração de uso de IA](../sobre/uso-de-ia.md).

A definição de pronto, que vale para todas as issues, está nos [Construtos de medição](../metricas/02-construtos-de-medicao.md#definicao-de-pronto).

## Labels e milestones

As labels e os milestones alimentam as medidas da gestão PSM/CID. Toda issue recebe as labels da Tabela 1.

| Label | Valores | Uso |
|---|---|---|
| `fase/N` | `fase/1` a `fase/4` | Fase do processo de avaliação (ISO/IEC 25040), quando houver |
| `tipo/...` | `documentacao`, `coleta`, `analise`, `artigo`, `gestao` | Tipo de produto de trabalho |
| `tamanho/...` | `P` (1 ponto, até 2 h), `M` (3 pontos, mais de 2 h e até 5 h), `G` (8 pontos, mais de 5 h) | Derivado da estimativa da issue; base da velocidade e do burndown |
| `prioridade/N` | `prioridade/1` (alta) a `prioridade/3` (baixa) | Opcional, para ordenar o backlog |
| `retrabalho` | — | Produto revisado depois de crítica (revisão interna ou ponto de controle) ou issue reaberta |
| `apontamento-docente` | — | Não conformidade apontada pela docente num ponto de controle ou entrega; usada junto com `retrabalho` (medida B4) |

<p class="legenda">Tabela 1. Labels das issues e seu uso nas medidas. Fonte: elaboração própria.</p>

Cada milestone corresponde a uma entrega da disciplina: `E1 - 26/10/2026` e `PC1` (fechados), `PC2` (15/11/2026) e `E2` (22/11/2026). As apresentações não têm milestone, porque não geram entrega no repositório. Issues abertas sem milestone formam o backlog.

## Antes de abrir o pull request

```bash
pip install -r requirements.txt
mkdocs build --strict                 # o site precisa gerar sem avisos
cd artigo && latexmk -pdf main.tex    # se o artigo foi alterado
```

## Padrões de escrita

- Português formal e direto; termos da ISO/IEC 25010:2023 em português (adequação funcional, compatibilidade, flexibilidade).
- Toda figura e tabela tem número, legenda e fonte, e é citada no texto.
- Toda afirmação sobre o Moodle cita a fonte oficial em [Referências](../sobre/referencias.md).
- Sem emojis, figurinhas ou ícones no relatório e na GitPage.
- Dados brutos ficam em `dados/`, com o identificador da métrica no nome da pasta (por exemplo, `dados/avaliacao/M2.1/`).

## Atas e decisões

Cada reunião gera uma ata em `atas/AAAA-MM-DD-ata-NN.md`, a partir do modelo `atas/modelo-ata.md`. O índice está em [Atas](atas.md). As decisões tomadas a partir das medidas ficam no [Registro de decisões de gestão](../metricas/03-registro-de-decisoes.md).
