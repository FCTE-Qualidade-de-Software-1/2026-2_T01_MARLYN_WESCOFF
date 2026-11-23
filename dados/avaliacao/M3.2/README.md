# Coleta de M3.2 (adaptabilidade à versão de PHP)

Coleta da issue #70, feita em 22/11/2026. Responsável: João Pedro. A execução foi automatizada pelo Claude Code numa máquina compartilhada pela equipe, e o João Pedro confere na revisão do pull request.

**Resultado: 12/12 tarefas nas duas versões. M3.2 = 1,00 no pior caso (nota 4). H3.2 confirmada.**

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

- A página "Verificação de ambiente" (capturas `M3.2_pagina_ambiente_*`) mostra todas as verificações do servidor com status OK nas duas versões, inclusive "version 8.3.0 is required and you are running 8.4.28". Em "Other checks", aparecem os mesmos avisos nas duas (Composer e HTTPS).
- Os logs de erro do PHP (`log-erros-*.log`) têm as mesmas 11 linhas nas duas versões, todas "Undefined property: stdClass::$noreplyaddress", e nenhuma depreciação no PHP 8.4. O aviso não depende da versão de PHP.
