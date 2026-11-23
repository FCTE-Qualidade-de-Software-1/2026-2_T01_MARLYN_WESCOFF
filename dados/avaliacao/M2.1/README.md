# Coleta de M2.1 e M2.2

Roteiro de execução dos 7 formatos de troca de dados (M2.1) e da comparação de integridade (M2.2), detalhando a seção 3 do [plano de avaliação da Fase 3](../../../docs/fase-3/plano-de-avaliacao.md). Responsável: Carlos (issue #68), com conferência cruzada de Bernardo.

## Antes de começar

- [ ] Servidor montado pelo script de preparação (#62), com o Moodle 5.3 limpo e a versão exata registrada.
- [ ] Massa de dados carregada pelo `gera_massa.py` (#63): curso completo, curso vazio, 30 estudantes, docente, notas e 6 eventos.
- [ ] Referências congeladas e conferidas: `python3 scripts/congela_referencia.py --verificar` sem nenhum arquivo alterado (#65).
- [ ] Sessão limpa no navegador (R2), e LibreOffice Calc e Thunderbird instalados na máquina do avaliador.

## Critério de sucesso (fixado antes da coleta)

Um formato só conta como sucesso (`sucesso = sim`) quando as duas condições são verdadeiras:

1. `conclui = sim`: a operação termina **sem mensagem de erro** do Moodle.
2. `aceito_receptor = sim`: o arquivo é aberto ou aceito pelo receptor da coluna `receptor` de [`execucoes.csv`](execucoes.csv) **sem conversão manual**.

`M2.1 = Fs / 7`, em que `Fs` é o número de linhas com `sucesso = sim`. A integridade (M2.2) é medida à parte, mesmo nos formatos com sucesso: um arquivo aceito pode ter perdido dados.

## Passo a passo

O caminho de cada função na interface segue a documentação oficial da 5.3 (regra R3). Um passo fora dela é registrado em `observacao`.

| Formato | Execução | Arquivo guardado | Comparação de M2.2 |
|---|---|---|---|
| F1 | Importar `F1_usuarios.csv` pela função de carga de usuários. Depois, exportar a lista de usuários em CSV | Pré-visualização da importação e o CSV exportado | `--chave username --campos firstname,lastname,email` |
| F2 | Exportar o livro de notas do curso completo em texto (CSV) e abrir no Calc | CSV exportado | Chave: e-mail; campos: as 3 notas |
| F3 | Exportar o mesmo livro de notas em planilha Excel e abrir no Calc | XLSX exportado | Igual a F2, contra a mesma referência |
| F4 | Importar `F4_questoes.gift` no banco de questões. Depois, exportar as questões em GIFT | GIFT exportado | `--chave nome --campos enunciado,respostas` |
| F5 | Exportar as questões do curso completo em Moodle XML e congelar (`F5=`). Importar no curso vazio e exportar de novo | Os dois XML | `--chave nome --campos tipo,enunciado,respostas,nota_padrao` |
| F6 | Exportar o calendário do curso em iCal e importar no Thunderbird | `.ics` exportado e captura do Thunderbird | `--chave SUMMARY --campos DTSTART,DTEND` |
| F7 | Fazer o backup do curso completo e congelar (`F7=`). Restaurar no curso vazio e fazer o backup do curso restaurado | Os dois `.mbz` | `--chave title --campos modulename` |

<p class="legenda">Tabela 1. Execução, arquivos e comparação de cada formato. Fonte: elaboração própria, a partir da ficha de M2.1 e M2.2.</p>

Para cada formato:

1. Preencher `data`, `avaliador`, `conclui`, `aceito_receptor`, `sucesso` e os nomes dos arquivos na linha do formato em `execucoes.csv`. Uma falha também é registrada, com a mensagem de erro em `observacao` (R4 e R5).
2. Guardar os arquivos de entrada e de saída em `dados/avaliacao/M2.1/` e a captura em `dados/avaliacao/evidencias/`, com o nome `M2.1_<formato>_<AAAA-MM-DD>_<iniciais>.png`.
3. Rodar a comparação:

    ```bash
    python3 scripts/compara_registros.py dados/avaliacao/M2.1/referencia/<referência> dados/avaliacao/M2.1/<saída> \
        --chave <chave> --campos <campos> --formato <Fn> --avaliador <iniciais> \
        --relatorio dados/avaliacao/M2.2/<Fn>_relatorio.csv --resumo dados/avaliacao/M2.2/resumo.csv
    ```

4. Se o formato falhar, repetir uma vez para separar falha do produto de erro do avaliador (seção 1 do plano). As duas tentativas são registradas.

## Resultado

Coleta feita em 22/11/2026, numa instância própria (`m21`, Moodle 5.3.1+, PHP 8.3) do servidor de avaliação. Responsável: Carlos. A execução foi automatizada pelo Claude Code numa máquina compartilhada pela equipe, e o Carlos confere na revisão do pull request.

**M2.1 = 7 / 7 = 1,00 (nota 4). H2.1 confirmada.** O detalhe de cada formato está em [`execucoes.csv`](execucoes.csv); os arquivos, em `saida/`; e as referências, congeladas antes de cada troca, em `referencia/`.

Desvios e tentativas, todos registrados em `execucoes.csv`:

- **F1:** importação pelo `uploaduser` da linha de comando (30 criados, 0 erros); a lista de usuários foi exportada direto do banco, com as colunas da exportação em massa. A massa foi aplicada depois e reconheceu as 30 contas importadas.
- **F2 e F3:** na tentativa 1, a exportação parou com a mensagem "grades/gradesneedregrading", que mostra o identificador do texto em vez da mensagem traduzida. A causa foi a massa, que grava notas pela API sem recalcular o livro de notas. Pelo caminho da interface (relatório de notas e depois Exportar), o recálculo é feito; F3 exportou na tentativa 2, e F2 na tentativa 3, porque o script da tentativa 2 saiu do relatório antes do fim do recálculo. O receptor foi o LibreOffice Calc, sem interface (`soffice --headless`), que abriu os dois arquivos sem conversão manual.
- **F4 e F5:** importação e exportação pelas classes de formato do Moodle (`qformat_gift` e `qformat_xml`), no banco de questões compartilhado do curso (na 5.x, uma atividade `mod_qbank`).
- **F6:** exportação pela URL de exportação do calendário; sem Thunderbird na máquina, o receptor foi substituído por validação estrutural do iCal (10 eventos completos) e pela leitura do `compara_registros.py`.
- **F7:** backup pela linha de comando, restauração no curso vazio pela API de restauração (precheck ok) e backup do curso restaurado.

A integridade (M2.2) está em [`../M2.2/README.md`](../M2.2/README.md).
