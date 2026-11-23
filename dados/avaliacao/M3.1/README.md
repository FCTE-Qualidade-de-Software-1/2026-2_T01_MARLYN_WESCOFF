# Coleta de M3.1 (adaptabilidade a ambientes de acesso)

Coleta da issue #70, feita em 22/11/2026 na instância `m53php83` do servidor de avaliação (Moodle 5.3.1+, PHP 8.3, massa `contas,catalogo`). Responsável: João Pedro. A execução foi automatizada pelo Claude Code numa máquina compartilhada pela equipe, e o João Pedro confere na revisão do pull request.

**Resultado parcial: A1, A3 e A4 concluíram as 8 tarefas (8/8), com o mesmo resultado de A1. M3.1 = 1,00 no pior ambiente coletado (nota 4). A2 (Firefox no Windows) não foi coletado.**

## Como foi executado

`scripts/m31_tarefas.js` executa, pela interface web e com Playwright, as tarefas T02, T03, T04, T05, T06, T08, T09 e T11 do plano da Fase 3. Cada papel usa uma sessão limpa (regra R2), e cada ambiente usa um estudante diferente (A1 `est01`, A3 `est03`, A4 `est04`; `est02` fica para A2), para que envios e tentativas não se misturem. T04 e T06 usam a tarefa criada em T03, porque a tarefa da massa não tem o plugin de comentários. Há uma captura por tarefa em `../evidencias/M3.1_<tarefa>_<ambiente>_2026-11-22_JPSM.png`. Os ambientes estão em [`ambientes.csv`](ambientes.csv), e os resultados, em [`execucoes.csv`](execucoes.csv).

## Desvios

- **A4 não é um celular real:** é o Chromium com o perfil Pixel 7 (tela de 412 × 839, toque e user agent Android). Para a conclusão sobre celular, vale complementar com um aparelho.
- **A2 não foi coletado:** não há Firefox no Windows desta máquina. Para completar, basta repetir as 8 tarefas num Windows com Firefox, acessando o servidor de avaliação (cerca de 20 minutos).

## Depuração do instrumento (antes da coleta, numa instância descartável)

Os ajustes foram feitos na instância `m45php83`, que não entra na coleta, até que o script concluísse as 8 tarefas em todos os ambientes:

- No celular, o Moodle põe os botões do formulário num rodapé fixo que se esconde ao rolar para baixo e reaparece ao rolar para cima; o script rola como uma pessoa antes de tocar em "Salvar". Não é uma falha: o botão é alcançável.
- O painel "Upload a file" é montado de forma assíncrona; o script espera o campo e confere que ele recebeu o arquivo antes de enviar.
- O link "Reply" do fórum tem `role="menuitem"`, e a confirmação do questionário não abre uma caixa de diálogo na 5.3.
