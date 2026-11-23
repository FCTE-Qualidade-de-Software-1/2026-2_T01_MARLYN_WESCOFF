# Plano de execução da Fase 4

A Fase 4 previa coletar as 12 métricas de **18 a 20/11/2026**, julgar em 21/11 e entregar em 22/11. Na prática, a coleta foi de **15 a 22/11** (M1.1 e M1.3 antecipadas para 15/11 e as demais em 22/11), o julgamento foi em 22/11, e a Entrega 2 foi prorrogada pela docente para **24/11/2026** (Tabela 3). Esta página diz quem coleta cada métrica, até quando, com qual evidência e em qual pasta. O **como** executar cada métrica está no [Plano de avaliação da Fase 3](../fase-3/plano-de-avaliacao.md#3-instrucoes-do-avaliador), e o cronograma e os responsáveis foram aprovados na reunião de 14/11/2026 ([ata 02](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-11-14-ata-02.md)).

Cada integrante coleta no próprio servidor, montado pelo mesmo script de preparação (decisão D3 da ata 02). O andamento de cada tarefa pode ser acompanhado no [quadro de tarefas](https://github.com/users/cadumotta/projects/1) e nas [métricas de gestão PSM/CID](../gestao/index.md).

## Métricas, responsáveis e evidências

| Questão | Métrica | Responsável | Issue | Até | Evidência | Pasta em `dados/avaliacao/` |
|---|---|---|---|---|---|---|
| Q1.1 | M1.1 Cobertura funcional | Bernardo | #67 | 20/11 | Uma linha por tarefa T01 a T12 em `execucoes.csv`, com captura de tela do resultado | `M1.1/` |
| Q1.2 | M1.2 Correção funcional | Bernardo | #67 | 20/11 | Valor exibido pelo Moodle em cada um dos 20 casos do `oraculo.csv`, com captura | `M1.2/` |
| Q1.3 e Q1.1 | M1.3 Pertinência funcional | Bernardo | #67 | 20/11 | Coluna de contorno da mesma `execucoes.csv` de M1.1, com o passo extra descrito | `M1.1/` |
| Q2.1 e Q2.2 | M2.1 Intercâmbio de formatos | Carlos | #68 | 20/11 | Registro dos 7 formatos (F1 a F7) com `conclui` e `aceito pelo receptor`, arquivos de entrada e de saída | `M2.1/` |
| Q2.2 | M2.2 Integridade dos dados | Carlos | #68 | 20/11 | Relatório de `compara_registros.py` de cada formato, contra as referências congeladas | `M2.2/` |
| Q2.3 | M2.3 Serviços web | Maykon | #69 | 20/11 | Resposta JSON de cada uma das 6 funções REST, **sem o token** | `M2.3/` |
| Q2.4 | M2.4 Coexistência | Maykon | #69 | 20/11 | `verificacoes.csv` com as 3 entidades vizinhas antes, durante e depois das 4 operações | `M2.4/` |
| Q3.1 | M3.1 Ambiente de acesso | João Pedro | #70 | 20/11 | As 8 tarefas em A1 a A4, com sistema, navegador, resolução e captura | `M3.1/` |
| Q3.2 | M3.2 Versão de PHP | João Pedro | #70 | 20/11 | Página "Verificação de ambiente" e T01 a T12 nas instâncias com PHP 8.3 e 8.4 | `M3.2/` |
| Q3.3 | M3.3 Sucesso de instalação | Pedro (uma execução: Bernardo) | #71 | 20/11 | `execucoes.csv` das 6 execuções (3 instalações e 3 atualizações) e o log do `script` de cada uma | `M3.3/` |
| Q3.3 | M3.4 Tempo de instalação | Pedro | #71 | 20/11 | Tempos e retentativas extraídos dos mesmos logs | `M3.4/` |
| Q3.4 | M3.5 Preservação na atualização | Pedro | #71 | 20/11 | Consultas dos 40 itens antes e depois de cada atualização | `M3.5/` |

<p class="legenda">Tabela 1. Responsável, prazo, evidência e pasta de cada métrica. Fonte: elaboração própria, a partir do plano da Fase 3 e da ata 02.</p>

Antes da primeira coleta, cada avaliador preenche uma linha de `dados/avaliacao/contexto.csv` com as [medidas de contexto](../fase-2/abstraction-sheets.md#medidas-de-contexto) do próprio servidor (versão exata do Moodle e do PHP, RAM, vCPU, fuso e anos de experiência com Linux). Elas não entram no julgamento, mas explicam diferenças entre servidores e hipóteses refutadas.

As evidências seguem o nome da seção 5 do plano da Fase 3, `<métrica>_<caso>_<AAAA-MM-DD>_<iniciais>.png`, e ficam em `dados/avaliacao/evidencias/`. Toda linha de CSV aponta para o arquivo de evidência correspondente.

## Preparação (até 17/11)

A coleta só começa quando a preparação de que ela depende estiver mergeada na `main`.

| Item | Responsável | Issue | Até | Necessário para |
|---|---|---|---|---|
| Script de preparação do servidor e imagem-base | Maykon | #62 | 17/11 | Todas as métricas |
| `gera_massa.py`, `usuarios.csv` e `questoes.gift` | João Pedro | #63 | 17/11 | M1.1 a M1.3, M2.1, M2.2, M3.5 |
| Oráculo de M1.2 com os 20 casos (conferido por Carlos) | Bernardo | #64 | 17/11 | M1.2 |
| `compara_registros.py` e referências de M2.1 congeladas | Carlos | #65 | 17/11 | M2.2 |
| Piloto de instalação e congelamento de M3.4 e M3.5 | Pedro | #66 | 17/11 | M3.3, M3.4, M3.5 |

<p class="legenda">Tabela 2. Itens de preparação e as métricas que dependem de cada um. Fonte: elaboração própria.</p>

## Sequência até a Entrega 2

| Previsto | Atividade | Issues | Realizado |
|---|---|---|---|
| 16 e 17/11 | Preparação: servidores, massa de dados, oráculo, script de comparação, piloto e congelamento dos limites de M3.4 e da lista de M3.5 | #62 a #66 | Script do servidor em 15/11; massa, oráculo e comparação até 17/11; o piloto (#66) não foi feito, e a lista de M3.5 foi congelada em 22/11, antes da primeira atualização |
| 18/11 | Apresentação do PC2 pela GitPage | #61 | 18/11 |
| 18 a 20/11 | Coleta das 12 métricas, em paralelo, cada integrante no próprio servidor | #67 a #71 | M1.1 e M1.3 em 15/11; M1.2, M2.1 a M2.4 e M3.1 a M3.5 em 22/11, num servidor compartilhado e com execução automatizada |
| 21/11 | Cálculo, notas, julgamento de G1 a G3 e relações entre as características | #72, #73 | 22/11 |
| 22/11 | Ação de melhoria, página de resultados, artigo e release da Entrega 2 | #74 a #78 | Ação de melhoria e página de resultados em 22/11; artigo e release até 24/11 (prazo prorrogado) |

<p class="legenda">Tabela 3. Sequência prevista e realizada da Fase 4. Fonte: ata 02, milestone E2 e histórico do repositório.</p>

## Do dado ao julgamento

1. Cada coletor registra os casos no CSV da métrica, inclusive as falhas (regra R4 do plano), e envia um parágrafo de resultado para o artigo.
2. Em 21/11, os valores entram em `dados/avaliacao/calculos.csv`. Cada métrica recebe a nota pelos [níveis de pontuação](../fase-2/niveis-e-julgamento.md#niveis-de-pontuacao-por-metrica) congelados na Fase 2.
3. As notas viram o julgamento das questões e dos objetivos pelas [regras de julgamento](../fase-2/niveis-e-julgamento.md#regras-de-julgamento), e cada hipótese H1.1 a H3.4 é confirmada ou refutada. A [Árvore GQM de resultados](arvore-gqm-resultados.md) mostra esse caminho das métricas aos objetivos e é gerada de novo com `python3 scripts/gera_arvore_resultados.py` sempre que `calculos.csv` mudar (o teste do PR avisa se ela ficar desatualizada).
4. **Sessão de interpretação** (Aula 08): cada coletor apresenta os dados da sua questão, a equipe responde às questões, compara com as hipóteses, explica as refutadas pelas [medidas de contexto](../fase-2/abstraction-sheets.md) e decide a ação. A sessão é registrada em ata.
5. **Plano de análise (formato dos resultados):** uma tabela por objetivo com as notas das questões, a [árvore GQM de resultados](arvore-gqm-resultados.md) como gráfico das notas por questão e a página [Resultados e julgamento](resultados.md).
6. O julgamento de G1, G2 e G3 responde às decisões D1 a D3 do [Propósito](../fase-1/proposito.md). Um resultado com nota 1 ou 2 é candidato à [ação de melhoria](acao-de-melhoria.md) (D4).

Os critérios não mudam depois de conhecer os resultados (regra R1). Qualquer desvio do plano durante a coleta é registrado em ata, com o motivo.
