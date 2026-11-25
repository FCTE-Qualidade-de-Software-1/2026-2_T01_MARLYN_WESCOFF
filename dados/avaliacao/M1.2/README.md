# Coleta de M1.2 (correção funcional)

Coleta da issue #67, feita em 22/11/2026. Responsável pela issue: Bernardo. A execução foi feita pelo Maykon, com scripts versionados, numa máquina compartilhada pela equipe; a conferência é feita na revisão do pull request. O oráculo (`oraculo.csv`) foi feito e conferido antes da coleta.

**Resultado: M1.2 = 19 / 20 = 0,95. Pela Tabela 2 da Fase 2, a divergência não é só de prazo, então a nota é 1. H1.2 refutada.**

## Como foi executado

- Instância `m12` (Moodle 5.3.1+, PHP 8.3) no servidor de avaliação, com a massa `contas,oraculo` e D = 22/11/2026 (`preparo-m12.log`).
- `scripts/m12_executa.sh` roda `scripts/m12_oraculo.php` uma vez por caso, pela API do próprio Moodle, que é o mesmo código que calcula o que a interface exibe:
  - **Q-01 a Q-10:** tentativa do estudante com as respostas do oráculo (Correta, Parcial 50% ou Incorreta); observado = nota do questionário.
  - **A-01 a A-06:** notas do oráculo lançadas nos itens; observado = total da categoria depois do recálculo do livro de notas, no formato exibido (real, 2 casas).
  - **P-01 a P-04:** envio ou tentativa no horário do oráculo, com o relógio do PHP deslocado por `faketime` (D 23:58, D+1 00:01, D+1 12:00 e D 18:01).
- Desvio do plano: os casos foram executados pela API, e não pela interface; a nota observada é a que o Moodle grava e exibe. Os resultados linha a linha estão em `resultados.jsonl`, e a comparação, em `execucoes.csv`.

## Caso não conforme: A-04

O oráculo pede a soma natural de 18 de 20 e 35 de 50 (70 pontos) "convertida para a escala de 0 a 10", com resultado esperado 7,57. O Moodle soma corretamente 53 de 70 e exibe o total da categoria em pontos (53,00) e em porcentagem (75,71%). A soma natural não tem opção para exibir o total na escala de 0 a 10. Em porcentagem, 75,71% equivale exatamente a 7,57; pelo critério congelado, porém, compara-se a nota exibida (53,00) com 7,57, e o caso é não conforme. O Bernardo já tinha registrado falha no A-04 na coleta parcial do PR #98.

**Decisão pendente da equipe:** manter o caso como não conforme (M1.2 = 0,95, nota 1, G1 não atende) ou registrar em ata que o oráculo do A-04 previa uma conversão que a configuração não tinha (M1.2 = 1,00, nota 4). O artigo apresenta os dois cenários.

## Incidente do instrumento

Na primeira rodada, o P-04 travou com o relógio congelado pelo `faketime` (formato sem `@`), e um laço do Moodle esperou o tempo avançar. O processo foi encerrado, e os quatro casos de prazo foram rodados de novo com o relógio deslocado e andando (`faketime -f '@...'`). Os resultados de P-01 a P-03 foram os mesmos nas duas rodadas.
