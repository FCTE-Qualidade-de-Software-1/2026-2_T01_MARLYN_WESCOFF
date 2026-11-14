# Dados consolidados da gestão PSM/CID

Medidas calculadas a partir de [`dados/brutos/`](../brutos/README.md) pelo `scripts/consolidar_metricas.py`, com as fórmulas dos [Construtos de medição](../../02-construtos-de-medicao.md). **Nenhum arquivo desta pasta é editado à mão.** O workflow `psm-coleta.yml` regenera todos os arquivos todo dia.

## Como gerar

O comando abaixo faz a extração, a consolidação e a validação, na ordem, com a mesma data de corte:

```bash
D=AAAA-MM-DD
python3 scripts/extrair_git.py --data-ref $D
GITHUB_TOKEN=$(gh auth token) python3 scripts/extrair_issues.py --data-ref $D
python3 scripts/consolidar_metricas.py --data-ref $D
python3 scripts/validar_dados.py --data-ref $D
python3 scripts/gerar_graficos.py --data-ref $D
```

O último comando gera os oito indicadores obrigatórios em `docs/metricas/graficos/`. Lacunas de coleta não
são transformadas em zero: quando uma medida não possui observações, a figura registra explicitamente
"sem dados registrados" e preserva a rastreabilidade até este consolidado.

O `validar_dados.py` termina com código 1 quando encontra erro. Ele confere:
- datas invertidas;
- integrantes fora de `docs/sobre/equipe.md`;
- percentuais de C2 que não somam 100;
- linhas do `esforco.csv` sem `tipo_registro` ou com formato inválido;
- CSVs sem as colunas `fonte`, `data_extracao` e `comando_ou_query`.

## Arquivos

| Arquivo | Medida | Granularidade | Colunas principais |
|---|---|---|---|
| `progresso_diario.csv` | A1 (Tabela 3) | Entrega e dia | `planejado_pontos`, `concluido_pontos`, `aberto_pontos`, `ideal_pontos`, `desvio_pct`, `issues_sem_tamanho`, `prazo` |
| `comprometido_concluido.csv` | A2 (Tabela 4) | Semana ISO | `comprometidos`, `concluidos`, `pc_pct`, `diferenca_pct`, `pc_acumulado_pct`, `fonte_compromisso` |
| `fluxo_estados.csv` | A3 (Tabela 5) | Dia | `aberta_sem_estado`, `backlog`, `a_fazer`, `em_progresso`, `em_revisao`, `concluido`, `wip`, `throughput`, `wip_medio_7d`, `throughput_medio_7d`, `ct_little_7d`, `origem_estado` |
| `entregas.csv` | A4 (Tabela 6) e B3 (Tabela 9) | Entrega | `prazo`, `publicada_em`, `desvio_dias`, `duracao_dias`, `linhas_periodo`, `linhas_48h`, `concentracao_pct`, `prs_mergeados_periodo` |
| `cycle_time.csv` | B1 (Tabela 7) | Issue | `inicio`, `fonte_inicio`, `fim`, `cycle_time_dias`, `lead_time_dias`, `idade_sem_atualizacao_dias`, `parada`, `media_entrega`, `mediana_entrega`, `p80_entrega`, `p90_entrega`, `acima_media_10pct` |
| `velocidade.csv` | B2 (Tabela 8) e B3 | Semana ISO | `pontos_concluidos`, `velocidade_media_3s`, `aceleracao_pct`, `backlog_pontos`, `semanas_ate_prazo`, `semanas_restantes`, `prs_mergeados`, `linhas_alteradas_main` |
| `retrabalho.csv` | B4 (Tabela 10) | Entrega | `reabertas`, `contidas_revisao`, `contidas_issues`, `contidas`, `escapadas`, `taxa_escape_pct` |
| `esforco_consolidado.csv` | C1 (Tabela 11) e C3 (Tabela 13) | Entrega, tipo de registro e nível (`membro`, `fase`, `tipo_atividade`, `issue`, `issue_sem_horas`, `total`) | `chave`, `horas`, `percentual`, `desvio_pct`, `previsto_h`, `estimado_h`, `acuracia`, `erro_pct`, `custo_rs`, `custo_estimado_rs`, `observacao` |
| `contribuicao.csv` | C2 (Tabela 12) | Entrega e integrante | `commits`, `linhas`, `issues`, `revisoes`, `horas`, `horas_registrado`, `horas_reconstruido`, `pct_commits`, `pct_linhas`, `pct_issues`, `pct_revisoes`, `pct_horas`, `divergencia_pp` |

<p class="legenda">Tabela 1. Arquivos consolidados, medida atendida e colunas. Todos têm também as colunas <code>historico</code>, <code>fonte</code>, <code>data_extracao</code> e <code>comando_ou_query</code>. Fonte: elaboração própria.</p>

## Regras de cálculo

- **Datas:** horário de Brasília. A semana é a semana ISO, de segunda a domingo.
- **Pontos de tamanho:** labels `tamanho/P`, `tamanho/M` e `tamanho/G`, com 1, 3 e 8 pontos. Uma issue sem label de tamanho vale 0 e é contada em `issues_sem_tamanho`.
- **Entrega:**
    - de uma issue: o milestone dela;
    - de um commit, de uma revisão ou de uma hora sem issue: a data. Até o prazo da E1, conta como E1. Depois, conta para o próximo marco com prazo. Sem prazo definido, conta para a E2.
- **`historico = sim`:** marca os dados da E1. As datas das issues da E1 não refletem o trabalho (Diagnóstico, lacuna L3), então essas linhas não entram em médias, medianas, percentis nem na velocidade de referência.
- **Horas:** linhas do `esforco.csv` sem horas são ignoradas. C1 e C3 são agrupados por `tipo_registro`, para separar o registrado no dia do reconstruído depois. C2 mostra as duas parcelas.
- **C2:** os percentuais de cada dimensão são arredondados pelo método dos maiores restos e somam exatamente 100.
    - Uma issue com `k` responsáveis vale `1/k` para cada um.
    - Revisões de um autor no próprio PR não contam.
    - Autores e responsáveis são reconhecidos pelo nome de `docs/sobre/equipe.md` ou pelo usuário do GitHub da mesma tabela.
- **Início do cycle time (B1):** o primeiro movimento para "Em Progresso" no quadro. Sem histórico do quadro, vale a data de criação, indicada em `fonte_inicio`.
- **Estado no quadro (A3):** uma issue fechada conta como `concluido`. Uma issue aberta sem histórico de Status no quadro conta como `aberta_sem_estado`.
- **Compromisso da semana (A2):** issues com a Iteração da semana no primeiro retrato do quadro daquela semana. Sem retrato, a semana fica sem medida (`sem registro de compromisso`), como define o construto.

## Limitações conhecidas

- O milestone e as labels de cada issue são os do momento da extração: mudanças anteriores de milestone não são reconstruídas.
- Enquanto o quadro não puder ser lido (falta o token `PSM_PROJECT_TOKEN` com o escopo `read:project`), A2 fica sem medida, A3 tem só os estados "aberta" e "concluído", e o cycle time começa na criação da issue.
- As issues da E2 da gestão PSM/CID foram criadas e várias fechadas no mesmo dia (10/11/2026). Por isso, o cycle time delas é de 1 dia e não representa a duração do trabalho, que começou antes da abertura das issues.

## Decisão sobre o `psm_coleta.py`

O `scripts/psm_coleta.py` foi **mantido sem alteração** e continua gerando o retrato semanal em `dados/gestao/psm-AAAA-MM-DD.csv` às segundas-feiras. Ele não foi absorvido pelos novos scripts por três motivos:

1. Os retratos dele são a evidência das medições da E1 e da decisão das duas semanas sem progresso (Diagnóstico, lacuna L10). Mudar o script quebraria a comparação com esses retratos.
2. Ele usa as definições do plano de medição da E1, que o [Registro de medições](../../../gestao/registro-medicoes.md) cita.
3. A partir da E2, os indicadores oficiais saem destes consolidados.

A remoção do script fica para depois da E2, quando a série antiga não for mais necessária.
