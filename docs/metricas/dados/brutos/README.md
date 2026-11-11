# Dados brutos da gestão PSM/CID

Saída crua das ferramentas, **sem edição manual**. Todos os indicadores da gestão PSM/CID são derivados destes arquivos. A primeira extração foi manual, em 10/11/2026 por volta das 22h (issue #16). Desde a issue #24, os arquivos são gerados pelos scripts `scripts/extrair_git.py` e `scripts/extrair_issues.py`, todo dia, pelo workflow `psm-coleta.yml`.

**Data de corte:** a data passada em `--data-ref`, até as 23h59 de Brasília, registrada na coluna `data_extracao` dos CSVs. Itens criados depois dela ficam de fora, e issue ou PR fechado depois dela aparece como aberto.

## Como gerar

```bash
python3 scripts/extrair_git.py --data-ref AAAA-MM-DD
GITHUB_TOKEN=$(gh auth token) python3 scripts/extrair_issues.py --data-ref AAAA-MM-DD
```

Para ler o quadro, defina também `PSM_PROJECT_TOKEN` com um token que tenha o escopo `read:project`. Sem ele, os arquivos do quadro não são alterados. Rodar duas vezes com a mesma data de corte e o mesmo estado do repositório gera arquivos idênticos.

| Arquivo | Fonte | Conteúdo | Script e comando ou consulta |
|---|---|---|---|
| `issues.json` | GitHub Issues | Issues abertas e fechadas, com labels, responsáveis, milestone e comentários | `extrair_issues.py`: consulta GraphQL equivalente a `gh issue list --state all --json number,title,state,createdAt,closedAt,labels,assignees,milestone,comments,author` |
| `issue_events.jsonl` | GitHub Issues (eventos) | Um evento por linha (fechamento, reabertura, label, milestone, atribuição, merge), de issues e de PRs | `extrair_issues.py`: `GET /repos/{repo}/issues/events`, só com os campos `id`, `event`, `created_at`, `actor`, `issue`, `label`, `milestone`, `assignee` e `commit_id` |
| `prs.json` | GitHub Pull Requests | Pull requests, com as revisões e o estado de cada uma (`APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`) | `extrair_issues.py`: consulta GraphQL equivalente a `gh pr list --state all --json number,title,state,createdAt,mergedAt,closedAt,reviews,additions,deletions,author` |
| `milestones.json` | GitHub Milestones | Milestones, com prazo e contagem de issues | `extrair_issues.py`: `GET /repos/{repo}/milestones?state=all` |
| `releases.json` | GitHub Releases | Releases das entregas | `extrair_issues.py`: consulta GraphQL equivalente a `gh release list --json tagName,name,createdAt,publishedAt,isLatest` |
| `quadro_eventos.csv` | Project board (GraphQL) | Entrada de cada issue no quadro e cada mudança de Status, com data e hora | `extrair_issues.py`: `timelineItems(itemTypes: [ADDED_TO_PROJECT_V2_EVENT, PROJECT_V2_ITEM_STATUS_CHANGED_EVENT])` |
| `quadro_retratos.csv` | Project board (GraphQL) | Retrato diário do Status e da Iteração de cada issue; uma linha por issue e por dia | `extrair_issues.py`: `user { projectV2 { items { fieldValues } } }` |
| `commits.csv` | git | Commits da `main`: autor canônico, data, arquivos, linhas adicionadas e removidas, diretórios tocados | `extrair_git.py`: `git log main --reverse --no-merges --numstat --date=iso-strict --until=<corte> --pretty=format:@%h\|%aN\|%ad\|%s`, agregado por commit |
| `tags.csv` | git | Tags e o commit para o qual apontam | `extrair_git.py`: `git for-each-ref refs/tags` |
| `esforco.csv` | Apontamento manual | Horas por sessão de trabalho (único arquivo preenchido à mão; ver `dados/README.md`) | Preenchido pelos integrantes |

<p class="legenda">Tabela 1. Arquivos brutos, origem e comando de extração. Fonte: elaboração própria.</p>

## Observações

- Os JSON são gravados com indentação de um espaço, sem alteração de conteúdo, para facilitar a leitura dos diffs. O campo `viewerDidAuthor` do `gh` foi omitido, porque depende de quem executa a extração.
- `issue_events.jsonl` guarda só os campos usados pelas medidas. A resposta completa da API repete a issue inteira em cada evento e passava de 1,7 MB. Os eventos de PRs aparecem com o número do PR no campo `issue`.
- `commits.csv` considera só a `main`. Ficam de fora:
    - os commits do branch `gh-pages`, gerados pelo deploy da GitPage;
    - os commits de merge, que não têm diff próprio (os merges são medidos pelos PRs em `prs.json`);
    - os commits do robô de coleta (`github-actions[bot]`), que não representam trabalho da equipe. A extração manual de 10/11/2026 tinha 4 desses commits.
- O autor sai pelo `%aN`, que aplica o `.mailmap` e entrega o nome canônico de `docs/sobre/equipe.md`. Quem ainda não está no `.mailmap` aparece com o nome configurado no Git; a consolidação (#25) também reconhece o usuário do GitHub da tabela da equipe.
- A API não devolve o estado passado do quadro. O histórico de Status vem dos eventos da linha do tempo de cada issue (`quadro_eventos.csv`). O de Iteração vem dos retratos diários (`quadro_retratos.csv`), que só são gravados quando a data de corte é o dia da execução.
- Os CSVs trazem as colunas `fonte`, `data_extracao` e `comando_ou_query` em todas as linhas, como pedem as regras de integridade dos dados.
