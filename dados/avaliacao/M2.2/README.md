# Resultado de M2.2 (integridade dos dados)

Comparação refeita em 24/11/2026 com `scripts/compara_registros.py`, na versão corrigida do PR #134, entre as referências congeladas em `M2.1/referencia/` (sha256 no `MANIFESTO.csv`, conferidos contra o conteúdo versionado no Git) e os arquivos de `M2.1/saida/`, os mesmos da coleta de 22/11. Responsável: Carlos.

| Formato | Rt | Rc | Observação |
|---|---|---|---|
| F1 CSV de usuários | 30 | 30 | — |
| F2 CSV de notas | 30 | 30 | — |
| F3 XLSX de notas | 30 | 30 | A célula numérica é comparada como número (10.0 = 10.00) |
| F4 GIFT | 15 | 15 | A resposta numérica é comparada por peso, valor e tolerância (`#7` = `=%100%7:0`) |
| F5 Moodle XML | 15 | 15 | — |
| F6 iCal | 6 | 6 | 4 eventos extras de atividades, que não entram em Rt |
| F7 backup | 6 | 6 | — |
| **Total** | **132** | **132** | |

<p class="legenda">Tabela 1. Registros íntegros por formato. Fonte: resumo.csv e F1_relatorio.csv a F7_relatorio.csv, de 24/11/2026.</p>

**M2.2 = 132 / 132 = 1,00 (nota 4). H2.2 confirmada:** a acentuação, o risco previsto na hipótese, chegou íntegra em todos os formatos.

## Histórico

A primeira comparação, de 22/11/2026, deu 97 / 132 = 0,73. As divergências de F3 (30 registros) e de F4 (5 questões numéricas) eram de representação, e não de dado: o XLSX guarda o número, e o Moodle exporta o GIFT numérico na forma estendida. O instrumento foi corrigido antes do julgamento, sem mudar o critério de M2.2 (só espaços em branco são normalizados; acentos, maiúsculas, casas decimais em texto e datas continuam contando como divergência), e a decisão está no [Registro de decisões](../../../docs/gestao/atas.md). Os relatórios e o resumo de 22/11 estão em [`historico-2026-11-22/`](historico-2026-11-22/). Rodando o instrumento antigo com os mesmos parâmetros, o resultado de 22/11 se reproduz exatamente.

## Comandos

```bash
D=dados/avaliacao/M2.1; O=dados/avaliacao/M2.2
NOTAS="email=Email address,Avaliação 1=Avaliação 1 (Real),Avaliação 2=Avaliação 2 (Real),Participação=Participação (Real)"
python3 scripts/compara_registros.py $D/referencia/F1_usuarios.csv $D/saida/F1_usuarios_exportados.csv --chave username --campos firstname,lastname,email,idnumber --formato F1 --relatorio $O/F1_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F2_notas.csv $D/saida/F2_notas_exportadas.csv --chave email --mapa "$NOTAS" --formato F2 --relatorio $O/F2_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F3_notas.csv $D/saida/F3_notas_exportadas.xlsx --chave email --mapa "$NOTAS" --formato F3 --relatorio $O/F3_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F4_questoes.gift $D/saida/F4_questoes_exportadas.gift --chave nome --campos enunciado,respostas --formato F4 --relatorio $O/F4_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F5_F5_questoes_origem.xml $D/saida/F5_questoes_reexportadas.xml --chave nome --campos tipo,enunciado,respostas,nota_padrao --formato F5 --relatorio $O/F5_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F6_eventos.csv $D/saida/F6_calendario.ics --chave SUMMARY --campos DTSTART,DTEND --formato F6 --relatorio $O/F6_relatorio.csv --resumo $O/resumo.csv
python3 scripts/compara_registros.py $D/referencia/F7_F7_backup_origem.mbz $D/saida/F7_backup_restaurado.mbz --chave title --campos modulename --formato F7 --relatorio $O/F7_relatorio.csv --resumo $O/resumo.csv
```
