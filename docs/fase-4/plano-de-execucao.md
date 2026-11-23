# Plano de execução da Fase 4

A Fase 4 previa coletar as 12 métricas de 18 a 20/11/2026, julgar os objetivos G1 a G3 em 21/11 e consolidar os resultados e a ação de melhoria até 22/11. A coleta ocorreu entre 15 e 23/11, e o prazo da Entrega 2 passou para **24/11/2026, até 23h59**; o cronograma real está na [Tabela 3](#sequencia-ate-a-entrega-2). Esta página diz quem coleta cada métrica, até quando, com qual evidência e em qual pasta. O **como** executar cada métrica está no [Plano de avaliação da Fase 3](../fase-3/plano-de-avaliacao.md#3-instrucoes-do-avaliador), e o cronograma e os responsáveis foram aprovados na reunião de 14/11/2026 ([ata 02](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-11-14-ata-02.md)).

Cada integrante coleta no próprio servidor, montado pelo mesmo script de preparação (decisão D3 da ata 02). O andamento de cada tarefa pode ser acompanhado no [quadro de tarefas](https://github.com/users/cadumotta/projects/1) e nos [indicadores de gestão do projeto (PSM/CID)](../gestao/index.md).

## Métricas, responsáveis e evidências

| Métrica | Responsável | Issue | Prazo (ata 02) | Evidência | Pasta em `dados/avaliacao/` |
|---|---|---|---|---|---|
| M1.1 Cobertura funcional | Bernardo | #67 | 20/11 | Uma linha por tarefa T01 a T12 em `execucoes.csv`, com captura de tela do resultado | `M1.1/` |
| M1.2 Correção funcional | Bernardo | #67 | 20/11 | Valor exibido pelo Moodle em cada um dos 20 casos do `oraculo.csv`, com captura | `M1.2/` |
| M1.3 Pertinência funcional | Bernardo | #67 | 20/11 | Coluna de contorno da mesma `execucoes.csv` de M1.1, com o passo extra descrito | `M1.1/` |
| M2.1 Intercâmbio de formatos | Carlos | #68 | 20/11 | Registro dos 7 formatos (F1 a F7) com `conclui` e `aceito pelo receptor`, arquivos de entrada e de saída | `M2.1/` |
| M2.2 Integridade dos dados | Carlos | #68 | 20/11 | Relatório de `compara_registros.py` de cada formato, contra as referências congeladas | `M2.2/` |
| M2.3 Serviços web | Maykon | #69 | 20/11 | Resposta JSON de cada uma das 6 funções REST, **sem o token** | `M2.3/` |
| M2.4 Coexistência | Maykon | #69 | 20/11 | `verificacoes.csv` com as 3 entidades vizinhas antes, durante e depois das 4 operações | `M2.4/` |
| M3.1 Ambiente de acesso | João Pedro | #70 | 20/11 | As 8 tarefas em A1 a A4, com sistema, navegador, resolução e captura | `M3.1/` |
| M3.2 Versão de PHP | João Pedro | #70 | 20/11 | Página "Verificação de ambiente" e T01 a T12 nas instâncias com PHP 8.3 e 8.4 | `M3.2/` |
| M3.3 Sucesso de instalação | Pedro (uma execução: Bernardo) | #71 | 20/11 | `execucoes.csv` das 6 execuções (3 instalações e 3 atualizações) e o log do `script` de cada uma | `M3.3/` |
| M3.4 Tempo de instalação | Pedro | #71 | 20/11 | Tempos e retentativas extraídos dos mesmos logs | `M3.4/` |
| M3.5 Preservação na atualização | Pedro | #71 | 20/11 | Consultas dos 40 itens antes e depois de cada atualização | `M3.5/` |

<p class="legenda">Tabela 1. Responsável, prazo, evidência e pasta de cada métrica. Fonte: elaboração própria, a partir do plano da Fase 3 e da ata 02.</p>

As evidências seguem o nome da seção 5 do plano da Fase 3, `<métrica>_<caso>_<AAAA-MM-DD>_<iniciais>.png`, e ficam em `dados/avaliacao/evidencias/`. Toda linha de CSV aponta para o arquivo de evidência correspondente.

## Preparação (até 17/11)

A coleta só começa quando a preparação de que ela depende estiver mergeada na `main`.

| Item | Responsável | Issue | Previsto | Realizado | Necessário para |
|---|---|---|---|---|---|
| Script de preparação do servidor e imagem-base | Maykon | #62 | 17/11 | 15/11 (PR #88) | Todas as métricas |
| `gera_massa.py`, `usuarios.csv` e `questoes.gift` | João Pedro | #63 | 17/11 | 15/11 (PR #90) | M1.1 a M1.3, M2.1, M2.2, M3.5 |
| Oráculo de M1.2 com os 20 casos (conferido por Carlos) | Bernardo | #64 | 17/11 | 15/11 (PR #87) | M1.2 |
| `compara_registros.py` e referências de M2.1 congeladas | Carlos | #65 | 17/11 | Script em 16/11 (PR #84); correção do instrumento em 23/11 (PR #134); referências congeladas na coleta | M2.2 |
| Piloto de instalação e congelamento de M3.4 e M3.5 | Pedro | #66 | 17/11 | Sem registro de conclusão até 23/11 | M3.3, M3.4, M3.5 |

<p class="legenda">Tabela 2. Itens de preparação, previsto e realizado, e as métricas que dependem de cada um. Fonte: issues e pull requests do GitHub, em 23/11/2026.</p>

## Sequência até a Entrega 2

O prazo da Entrega 2 passou de 22/11 para **24/11/2026, até 23h59**. A tabela compara o previsto na ata 02 com o que ocorreu até 23/11 e mostra o que falta até o prazo novo.

| Previsto (ata 02) | Data real ou nova | Atividade | Issues | Situação em 23/11 |
|---|---|---|---|---|
| 16 e 17/11 | 15 e 16/11 | Preparação: servidor, massa de dados, oráculo e script de comparação | #62 a #65 | Concluída (Tabela 2); o piloto (#66) não tem registro de conclusão |
| 18/11 | 18/11 | Apresentação do PC2 | #61 | Realizada, com slides; os apontamentos da docente viraram as issues #102 a #123 |
| 18 a 20/11 | 15/11 | Coleta de M1.1 e M1.3, antecipada | #67 | Registrada no PR #98, em revisão |
| 18 a 20/11 | 22 e 23/11 | Coleta de M1.2, M2.1 a M2.4 e M3.1 a M3.5 | #67 a #71 | Registrada nos PRs #129 e #133, em revisão |
| — | 23/11 | Correção do instrumento de M2.2 e nova comparação | #65, #68 | Correção no PR #134; nova comparação depois do merge |
| — | 23/11 | Revisão dos PRs das coletas e das correções da vistoria | #102 a #123 | Em andamento |
| 21/11 | até 24/11 | Sessão de interpretação; cálculo, notas e julgamento de G1 a G3; relações entre as características | #72, #73 | A fazer |
| 22/11 | até 24/11 | Ação de melhoria, página de resultados e artigo (Fase 4, conclusão e contribuição) | #74 a #77 | Ação registrada no PR #133; demais a fazer |
| 22/11 | 24/11, até 23h59 | Declaração de IA final, revisão pela rubrica e release da Entrega 2 | #78 | A fazer |

<p class="legenda">Tabela 3. Sequência da Fase 4: previsto na ata 02, realizado até 23/11/2026 e restante até a Entrega 2. Fonte: ata 02, issues e pull requests do GitHub, em 23/11/2026.</p>

## Do dado ao julgamento

1. Cada coletor registra os casos no CSV da métrica, inclusive as falhas (regra R4 do plano), e envia um parágrafo de resultado para o artigo.
2. Em 21/11, os valores entram em `dados/avaliacao/calculos.csv`. Cada métrica recebe a nota pelos [níveis de pontuação](../fase-2/niveis-e-julgamento.md#niveis-de-pontuacao-por-metrica) congelados na Fase 2.
3. As notas viram o julgamento das questões e dos objetivos pelas [regras de julgamento](../fase-2/niveis-e-julgamento.md#regras-de-julgamento), e cada hipótese H1.1 a H3.4 é confirmada ou refutada.
4. O julgamento de G1, G2 e G3 responde às decisões D1 a D3 do [Propósito](../fase-1/proposito.md). Um resultado com nota 1 ou 2 é candidato à ação de melhoria (D4).

Os critérios não mudam depois de conhecer os resultados (regra R1). Qualquer desvio do plano durante a coleta é registrado em ata, com o motivo.
