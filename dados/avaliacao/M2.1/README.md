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

1. Preencher `data`, `avaliador`, `conclui`, `aceito_receptor`, `sucesso` e os nomes dos arquivos na linha do formato em `execucoes.csv`. Uma falha também é registrada, com a mensagem de erro em `observacao` (R4 e R5). Em `codificacao`, anotar a saída de `file -bi` do arquivo trocado (medida de contexto da Fase 2).
2. Guardar os arquivos de entrada e de saída em `dados/avaliacao/M2.1/` e a captura em `dados/avaliacao/evidencias/`, com o nome `M2.1_<formato>_<AAAA-MM-DD>_<iniciais>.png`.
3. Rodar a comparação:

    ```bash
    python3 scripts/compara_registros.py dados/avaliacao/M2.1/referencia/<referência> dados/avaliacao/M2.1/<saída> \
        --chave <chave> --campos <campos> --formato <Fn> --avaliador <iniciais> \
        --relatorio dados/avaliacao/M2.2/<Fn>_relatorio.csv --resumo dados/avaliacao/M2.2/resumo.csv
    ```

4. Se o formato falhar, repetir uma vez para separar falha do produto de erro do avaliador (seção 1 do plano). As duas tentativas são registradas.

## Resultado

- `M2.1 = Fs / 7`, a partir de `execucoes.csv`.
- `M2.2 = soma de Rc / soma de Rt` nos 7 formatos, a partir de `dados/avaliacao/M2.2/resumo.csv`. Nos formatos que falharam em M2.1 e não geraram arquivo, todos os registros esperados contam como não íntegros.
- Os dois valores entram em `dados/avaliacao/calculos.csv` (#72), e um parágrafo de resultado vai para o artigo (#76).
