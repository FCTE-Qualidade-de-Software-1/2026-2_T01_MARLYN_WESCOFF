# Coleta de M3.5 (preservação na atualização)

Coleta da issue #71, feita em 22/11/2026, junto com as três atualizações de M3.3. Responsável pela issue: Pedro (execução feita pelo Maykon, por script; ver o README de M3.3).

**Resultado: M3.5 = 40 / 40 = 1,00 nas três atualizações (nota 4). H3.4 confirmada.**

A lista dos 40 itens deveria ter sido congelada no piloto (#66), que não aconteceu. Ela foi congelada em `scripts/m35_itens.php` antes da primeira atualização medida (regra R1): 30 contagens (usuários, cursos, matrículas, papéis, módulos, tarefas, envios, questionários, tentativas, questões, fóruns, discussões, posts, recursos, arquivos, itens e categorias de nota, soma das notas e eventos) e a nota final de `est01` a `est10` no curso `AVAL-CAT`. A conferência da lista por outro integrante (regra R6) fica para a revisão do pull request.

Em cada atualização, os itens são lidos na 4.5 (com o livro de notas recalculado) e de novo depois da atualização, sem recalcular, para ver o valor gravado: `<n>-antes.csv` e `<n>-depois.csv`. A comparação está em [`comparacao.csv`](comparacao.csv). As pastas `tentativa-1` a `tentativa-3` são das tentativas descartadas de M3.3, também com 40/40.
