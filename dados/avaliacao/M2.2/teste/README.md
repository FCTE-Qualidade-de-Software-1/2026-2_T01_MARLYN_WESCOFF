# Par de teste do compara_registros.py

Par de arquivos conhecido, com dados fictícios (regra R7), usado para conferir o `scripts/compara_registros.py` antes da coleta. **Não entra no cálculo de M2.2.**

| Registro | Diferença no destino | Resultado esperado |
|---|---|---|
| est01 | Nenhuma | idêntico |
| est02 | Espaços em volta do nome | idêntico (espaço é a única normalização) |
| est03 | Acentos removidos (José → Jose, Araújo → Araujo) | divergente em `firstname` e `lastname` |
| est04 | Ausente no destino | ausente |
| est99 | Só existe no destino | extra (não entra em Rt) |

Resultado esperado: Rt = 4, Rc = 2, M2.2 = 0,5000.

```bash
python3 scripts/compara_registros.py dados/avaliacao/M2.2/teste/referencia.csv dados/avaliacao/M2.2/teste/destino.csv --chave username --formato teste
python3 -m unittest discover -s scripts/tests -v
```
