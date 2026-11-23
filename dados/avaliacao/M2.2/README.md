# Resultado de M2.2 (integridade dos dados)

Comparação feita em 22/11/2026 com `scripts/compara_registros.py`, entre as referências congeladas em `M2.1/referencia/` (com sha256 no `MANIFESTO.csv`, verificadas antes de cada troca) e os arquivos de `M2.1/saida/`. Responsável: Carlos (execução automatizada pelo Claude Code; ver o README de M2.1).

| Formato | Rt | Rc estrito | Divergências | Por valor |
|---|---|---|---|---|
| F1 CSV de usuários | 30 | 30 | — | 30 |
| F2 CSV de notas | 30 | 30 | — | 30 |
| F3 XLSX de notas | 30 | **0** | a planilha guarda o número `10.0` onde a referência tem o texto `10.00` | 30 |
| F4 GIFT | 15 | **10** | as 5 questões numéricas voltam como `# =%100%7:0#` em vez de `#7` (mesma resposta, tolerância 0) | 15 |
| F5 Moodle XML | 15 | 15 | — | 15 |
| F6 iCal | 6 | 6 | 4 eventos extras de atividades (não contam como falha) | 6 |
| F7 backup | 6 | 6 | — | 6 |
| **Total** | **132** | **97** | | **132** |

<p class="legenda">Tabela 1. Registros íntegros por formato. Fonte: resumo.csv e F1_relatorio.csv a F7_relatorio.csv.</p>

**M2.2 estrito = 97 / 132 = 0,73 (nota 1). H2.2 refutada.** Esse é o valor pelo critério congelado no plano da Fase 3: "só espaços em branco são normalizados".

**Por valor, M2.2 = 132 / 132 = 1,00.** Nenhum registro perdeu ou alterou dados: as divergências de F3 e F4 são de representação (zeros à direita de um número e sintaxe estendida do GIFT numérico). A acentuação, o risco previsto na hipótese, chegou íntegra em todos os formatos.

**Decisão pendente da equipe:** qual dos dois valores entra no julgamento de G2 (com o estrito, G2 não atende; por valor, G2 atende com ressalvas, por causa de M2.4). Se a equipe adotar a comparação por valor, a mudança do critério precisa ir para a ata, com o motivo. O artigo apresenta os dois cenários.
