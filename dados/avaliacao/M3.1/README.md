# Coleta de M3.1 (adaptabilidade a ambientes de acesso)

Coleta da issue #70, feita em 22/11/2026 na instância `m53php83` do servidor de avaliação (Moodle 5.3.1+, PHP 8.3, massa `contas,catalogo`). Responsável pela métrica e conferência: João Pedro. Execução: Maykon, com os scripts versionados citados abaixo.

**Resultado: os quatro ambientes concluíram as 8 tarefas (8/8), com o mesmo resultado de A1. M3.1 = 1,00 no pior ambiente (nota 4). H3.1 confirmada (o Android emulado não falhou em nenhuma).**

## Conferência (regra R6)

Conferida por João Pedro, responsável pela métrica, em 23/11/2026, sobre a versão do pull request #133:

| Verificação | Resultado |
|---|---|
| Linhas de `execucoes.csv` | 35: 8 tarefas em A1, A3 e A4, 8 em A2 na primeira tentativa e 3 repetições em A2 |
| Evidências citadas que existem em `../evidencias/` | 35 de 35 |
| Captura x linha do CSV (amostra: A4/T05 e A2/T09 na repetição) | Iguais: tarefa vencida sem botão de envio; resposta do `est02` publicada |
| User agent de cada linha x ambiente de `ambientes.csv` | Coerentes nos 4 ambientes |
| Ordem da Fase 2 (M3.1 depois de M1.1) | Cumprida: M1.1 em 15/11, M3.1 em 22/11 |
| Resultado | M3.1 = 8/8 no pior ambiente, confirmado |

<p class="legenda">Tabela 1. Conferência de M3.1. Fonte: elaboração própria.</p>

Desvios que precisam ser aprovados na ata 03: o A4 é um Android **emulado**, e o plano da Fase 3 só aceita emulador registrado em ata; e a coleta foi executada pelo Maykon, e não pelo responsável. As iniciais `JPSM` nos nomes das evidências seguem o responsável pela métrica, e não quem executou.

## Como foi executado

`scripts/m31_tarefas.js` executa, pela interface web e com Playwright, as tarefas T02, T03, T04, T05, T06, T08, T09 e T11 do plano da Fase 3. Cada papel usa uma sessão limpa (regra R2), e cada ambiente usa um estudante diferente (A1 `est01`, A2 `est02`, A3 `est03`, A4 `est04`), para que envios e tentativas não se misturem. T04 e T06 usam a tarefa criada em T03, porque a tarefa da massa não tem o plugin de comentários. Há uma captura por tarefa em `../evidencias/M3.1_<tarefa>_<ambiente>_2026-11-22_JPSM.png`. Os ambientes estão em [`ambientes.csv`](ambientes.csv), e os resultados, em [`execucoes.csv`](execucoes.csv).

## Desvios

- **A4 não é um celular real:** é o Chromium com o perfil Pixel 7 (tela de 412 × 839, toque e user agent Android). Para a conclusão sobre celular, vale complementar com um aparelho.
- **A2 (Firefox no Windows):** o Firefox 160.0.1 oficial foi extraído do instalador da Mozilla (SHA-256 conferido com a lista publicada) para `AppData\Local\FirefoxAval`, porque a instalação completa pede administrador. O Playwright controla esse Firefox pelo WebDriver BiDi (canal `moz-firefox`), com a ponte `scripts/firefox_windows.sh`, que converte os caminhos do WSL para o Windows. Na primeira tentativa, T02, T08 e T09 falharam por falha do controle (a tela de login ficou sem preenchimento e um clique não foi registrado; as capturas mostram as páginas normais) e, repetidas uma vez como manda a seção 1 do plano, passaram. As duas tentativas estão em `execucoes.csv` (a repetição tem o prefixo "repetição" e capturas com o sufixo `_rep`).

## Depuração do instrumento (antes da coleta, numa instância descartável)

Os ajustes foram feitos na instância `m45php83`, que não entra na coleta, até que o script concluísse as 8 tarefas em todos os ambientes:

- No celular, o Moodle põe os botões do formulário num rodapé fixo que se esconde ao rolar para baixo e reaparece ao rolar para cima; o script rola como uma pessoa antes de tocar em "Salvar". Não é uma falha: o botão é alcançável.
- O painel "Upload a file" é montado de forma assíncrona; o script espera o campo e confere que ele recebeu o arquivo antes de enviar.
- O link "Reply" do fórum tem `role="menuitem"`, e a confirmação do questionário não abre uma caixa de diálogo na 5.3.
