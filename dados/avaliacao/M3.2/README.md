# Coleta de M3.2 (adaptabilidade à versão de PHP)

Coleta da issue #70, feita em 22/11/2026. Responsável pela métrica e conferência: João Pedro. Execução: Maykon, com os scripts versionados citados abaixo.

**Resultado: 12/12 tarefas nas duas versões. M3.2 = 1,00 no pior caso (nota 4). H3.2 confirmada.**

## Conferência (regra R6)

Conferida por João Pedro, responsável pela métrica, em 23/11/2026, sobre a versão do pull request #133:

| Verificação | Resultado |
|---|---|
| Tarefas por versão de PHP | 12 em cada: 8 em `execucoes.csv` e 4 em `api-*.jsonl`, todas concluídas |
| Evidências citadas que existem | 25 de 26: falta `M3.2_T09_php84_2026-11-22_JPSM.png` |
| Versões de PHP nos registros da API | 8.3.37 e 8.4.28, iguais às da verificação de ambiente |
| Logs de erro | As mesmas linhas nas duas versões, todas sobre `$noreplyaddress` |
| Verificação de ambiente (captura do PHP 8.4) | Verificações do servidor todas OK; em "Other checks", 3 avisos: Composer, roteador e HTTPS |
| Resultado | M3.2 = 12/12 nas duas versões, com a ressalva da evidência de T09 no PHP 8.4 |

<p class="legenda">Tabela 2. Conferência de M3.2. Fonte: elaboração própria.</p>

A captura de T09 no PHP 8.4 não foi gravada, e a linha de `execucoes.csv` passou a dizer isso. O resultado dessa tarefa se apoia só no registro do script. Se a instância `m32php84` ainda existir, a tarefa deve ser repetida para gerar a captura.

Desvios que precisam ser aprovados na ata 03: T01, T07, T10 e T12 executadas pela API, e não pela interface; instâncias `m32php83` e `m32php84`, em vez de `m53php83` e `m53php84`, com a massa `contas,catalogo`, e não só `contas`; e a execução feita pelo Maykon, e não pelo responsável. As iniciais `JPSM` nos nomes das evidências seguem o responsável pela métrica, e não quem executou.

## Ambiente

Duas instâncias novas e iguais no servidor de avaliação, montadas por `scripts/preparar_servidor.sh` com a mesma massa (`contas,catalogo`): `m32php83` (PHP 8.3.37) e `m32php84` (PHP 8.4.28), com o modo de depuração de desenvolvedor ligado, para que avisos e depreciações fossem para o log.

## Tarefas

| Tarefas | Como | PHP 8.3 | PHP 8.4 |
|---|---|---|---|
| T02, T03, T04, T05, T06, T08, T09, T11 | Interface, com `scripts/m31_tarefas.js` (Chromium de computador) | 8/8 | 8/8 |
| T01, T07, T10, T12 | API do Moodle, com `scripts/m32_tarefas_api.php`, e a página resultante aberta pela interface (`scripts/m32_paginas.js`, HTTP 200 sem erro) | 4/4 | 4/4 |

<p class="legenda">Tabela 1. Tarefas por versão de PHP. Fonte: execucoes.csv, api-*.jsonl e paginas.csv.</p>

Desvio: T01, T07, T10 e T12 foram executadas pela API, e não pela interface; a página de cada objeto criado foi aberta pela interface nas duas versões. Na primeira execução, T07 falhou nas duas versões por um defeito do script (o atalho de criar questões depende do PHPUnit); o script passou a criar as questões como a massa, e a tarefa foi repetida.

## Verificação de ambiente e logs

- A página "Verificação de ambiente" (capturas `M3.2_pagina_ambiente_*`) mostra todas as verificações do servidor com status OK nas duas versões, inclusive "version 8.3.0 is required and you are running 8.4.28". Em "Other checks", aparecem os mesmos três avisos nas duas (Composer, roteador não configurado e HTTPS).
- Os logs de erro do PHP (`log-erros-*.log`) têm as mesmas 11 linhas nas duas versões, todas "Undefined property: stdClass::$noreplyaddress", e nenhuma depreciação no PHP 8.4. O aviso não depende da versão de PHP.
