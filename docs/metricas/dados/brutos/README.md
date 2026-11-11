# Dados brutos da gestão PSM/CID

Saída crua das ferramentas, **sem edição manual**. Todos os indicadores da gestão PSM/CID são derivados destes arquivos. A extração foi manual nesta primeira vez (issue #16); a partir da Etapa 4, os scripts `scripts/extrair_git.py` e `scripts/extrair_issues.py` (issue #24) passam a gerá-los.

**Data da extração:** 10/11/2026, por volta das 22h (horário de Brasília). Os dados refletem o repositório nesse instante, já com as issues #15 a #32 da gestão PSM/CID criadas.

| Arquivo | Fonte | Conteúdo | Comando ou consulta |
|---|---|---|---|
| `issues.json` | GitHub Issues | 32 issues (abertas e fechadas), com labels, responsáveis, milestone e comentários | `gh issue list --state all --limit 500 --json number,title,state,createdAt,closedAt,labels,assignees,milestone,comments,author` |
| `issue_events.jsonl` | GitHub Issues (eventos) | 158 eventos, um por linha (fechamento, reabertura, label, milestone, atribuição) | `gh api "repos/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/issues/events?per_page=100" --paginate --jq '.[] \| {id, event, created_at, actor: .actor.login, issue: .issue.number, label: .label.name, milestone: .milestone.title, assignee: .assignee.login, commit_id}'` |
| `prs.json` | GitHub Pull Requests | Pull requests (nenhum até a data da extração) | `gh pr list --state all --limit 500 --json number,title,state,createdAt,mergedAt,closedAt,reviews,additions,deletions,author` |
| `milestones.json` | GitHub Milestones | 2 milestones, com datas e contagem de issues | `gh api "repos/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/milestones?state=all"` |
| `releases.json` | GitHub Releases | 1 release (E1) | `gh release list --json tagName,name,createdAt,publishedAt,isLatest` |
| `tags.csv` | git | Tags e o commit para o qual apontam | `git for-each-ref refs/tags` |
| `commits.csv` | git | 18 commits da `main`: autor, data, arquivos, linhas adicionadas e removidas, diretórios tocados | `git log main --numstat --date=iso-strict --pretty=format:@%H\|%an\|%ad\|%s`, agregado por commit |

<p class="legenda">Tabela 1. Arquivos brutos, origem e comando de extração. Fonte: elaboração própria.</p>

## Observações

- Os arquivos JSON foram apenas reformatados com indentação, sem alteração de conteúdo, para facilitar a leitura dos diffs.
- `issue_events.jsonl` guarda só os campos usados pelas medidas. A resposta completa da API repete a issue inteira em cada evento e passava de 1,7 MB.
- `commits.csv` considera só a `main`. Os commits do branch `gh-pages` são gerados pelo deploy da GitPage e não representam trabalho da equipe.
- Os CSVs trazem as colunas `fonte`, `data_extracao` e `comando_ou_query` em todas as linhas, como pedem as regras de integridade dos dados.
- O registro de esforço (`esforco.csv`), único arquivo de preenchimento manual, é tratado na issue #20.
