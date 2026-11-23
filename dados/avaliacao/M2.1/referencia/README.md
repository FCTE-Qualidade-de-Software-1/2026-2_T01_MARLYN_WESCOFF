# Referências congeladas de M2.1 e M2.2

Os arquivos desta pasta são a **verdade** contra a qual os dados trocados são comparados em M2.2. Eles são congelados **antes da primeira troca** (regra R1 do [plano da Fase 3](../../../../docs/fase-3/plano-de-avaliacao.md)) e não são editados depois. O `MANIFESTO.csv` guarda a origem, o sha256, o tamanho, a data e o responsável de cada arquivo.

## Referências esperadas

| Formato | Arquivo de referência | Origem | Destino comparado | Chave e campos |
|---|---|---|---|---|
| F1 CSV de usuários (importação) | `usuarios.csv` (30 estudantes) | `gera_massa.py` (#63) | Lista de usuários exportada da instância depois da importação | `username`; `firstname`, `lastname`, `email` |
| F2 CSV de notas (exportação) | Notas lançadas da massa (30 × 3) | `gera_massa.py` (#63) | CSV exportado do livro de notas | e-mail do estudante; uma coluna por item de nota |
| F3 XLSX de notas (exportação) | O mesmo arquivo de notas de F2 | `gera_massa.py` (#63) | XLSX exportado do livro de notas | Iguais a F2 |
| F4 GIFT de questões (importação) | `questoes.gift` (15 questões) | `gera_massa.py` (#63) | Banco de questões exportado depois da importação | `nome`; `enunciado`, `respostas` |
| F5 Moodle XML de questões (exportação e reimportação) | XML exportado do curso de origem | Instância de avaliação, antes da reimportação | XML exportado de novo depois da reimportação no segundo curso | `nome`; `tipo`, `enunciado`, `respostas`, `nota_padrao` |
| F6 iCal do calendário (exportação) | Os 6 eventos da massa (título, início e fim) | `gera_massa.py` (#63) | `.ics` exportado e aberto no Thunderbird | `SUMMARY`; `DTSTART`, `DTEND` |
| F7 backup `.mbz` (backup e restauração) | Backup do curso completo | Instância de avaliação, antes da restauração | Backup do curso restaurado no curso vazio | `title`; `modulename` |

<p class="legenda">Tabela 1. Referências de cada formato de M2.1 e o que é comparado em M2.2. Fonte: elaboração própria, a partir da ficha de M2.1 em <a href="../../../../docs/fase-2/metricas.md">Métricas</a>.</p>

As referências de F5 e F7 são geradas na própria instância, porque o que se mede é a ida e a volta do mesmo conteúdo. Elas são congeladas logo depois de exportadas, antes da reimportação e da restauração.

## Como congelar e verificar

```bash
# depois que gera_massa.py (#63) gerar os arquivos da massa
python3 scripts/congela_referencia.py --responsavel CD F1=<caminho>/usuarios.csv F2=<caminho>/notas.csv \
    F3=<caminho>/notas.csv F4=<caminho>/questoes.gift F6=<caminho>/eventos.csv

# antes de cada troca e antes do cálculo de M2.2
python3 scripts/congela_referencia.py --verificar
```

Um formato já congelado só é trocado com `--substituir`, e a troca é registrada em ata, com o motivo.

## Como comparar (M2.2)

```bash
python3 scripts/compara_registros.py dados/avaliacao/M2.1/referencia/F1_usuarios.csv <destino>.csv \
    --chave username --campos firstname,lastname,email --formato F1 --avaliador CD \
    --relatorio dados/avaliacao/M2.2/F1_relatorio.csv --resumo dados/avaliacao/M2.2/resumo.csv
```

Quando o nome da coluna muda no destino (por exemplo, o Moodle exporta "Endereço de email"), use `--mapa email="Endereço de email"`. A única normalização é de espaços em branco: acentos, maiúsculas, casas decimais e datas diferentes contam como divergência. O par de teste conhecido está em [`../../M2.2/teste/`](../../M2.2/teste/README.md).
