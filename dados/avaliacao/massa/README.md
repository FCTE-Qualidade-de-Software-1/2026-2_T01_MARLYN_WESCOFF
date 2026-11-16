# Massa de dados fictícia

Massa de dados da avaliação, gerada por [`scripts/gera_massa.py`](../../../scripts/gera_massa.py) (issue #63), conforme a Tabela 6 do [plano da Fase 3](../../../docs/fase-3/plano-de-avaliacao.md#massa-de-dados-ficticia). Nenhum arquivo desta pasta é editado à mão e nenhum dado é real (regra R7). Para gerar de novo e conferir:

```bash
python3 scripts/gera_massa.py arquivos    # grava os arquivos abaixo
python3 scripts/gera_massa.py verificar   # quantidades, e-mails, oráculo e reprodutibilidade
```

## Arquivos de referência

| Arquivo | Conteúdo | Usado em |
|---|---|---|
| `usuarios.csv` | 30 estudantes (`est01` a `est30`), no formato da carga de usuários do Moodle | F1 de M2.1 |
| `questoes.gift` | 15 questões: 10 de múltipla escolha (2 com crédito parcial de 50%) e 5 numéricas | F4 de M2.1 |
| `notas.csv` | Notas de 30 estudantes em 3 itens (Avaliação 1, Avaliação 2, Participação), com 2 casas decimais | F2 e F3 de M2.1 |
| `eventos.csv` | Os 6 eventos do calendário do curso completo, com início e fim em UTC, no formato do iCal | F6 de M2.1 |
| `massa.json` | Manifesto de tudo o que a etapa `aplicar` cria, com os prazos relativos ao dia D | Rastreabilidade de M1.2, M3.1, M3.2 e M3.5 |

<p class="legenda">Tabela 1. Arquivos de referência da massa. Fonte: elaboração própria.</p>

Os quatro primeiros são os que o Carlos congela com `scripts/congela_referencia.py` (#65).

## Aplicar a massa em uma instância

A instância precisa ter sido criada pelo [script de preparação](../../../docs/fase-3/preparacao-do-servidor.md) (#62), que já cria o `admin-aval`. Na VM, a partir da cópia do repositório:

```bash
sudo python3 scripts/gera_massa.py aplicar --moodle /var/www/m53php83 --php php8.3 \
    --partes contas,oraculo --dia-prazo 2026-11-19 \
    --registro dados/avaliacao/ambiente/massa-m53php83-<iniciais>.json
```

O script roda o PHP como `www-data`, cria tudo dentro de uma única transação e grava o registro do que foi criado. Se algo falhar, **nada fica gravado**. A massa é aplicada uma vez por instância: se um curso da massa já existir, o script para sem alterar nada. Contas que já existem com os mesmos dados (por exemplo, importadas pelo `usuarios.csv` em F1) são mantidas e listadas como ignoradas.

| Parte | O que cria |
|---|---|
| `contas` | `est01` a `est30` e `docente01`, com e-mail em `example.invalid` e fuso `America/Sao_Paulo` |
| `catalogo` | Curso completo `AVAL-CAT`: 30 estudantes e o docente matriculados, material, tarefa dentro do prazo (com 10 envios, de `est21` a `est30`), tarefa com data limite vencida, questionário de 3 questões de múltipla escolha e 2 numéricas, fórum com 1 tópico e 3 respostas, 3 itens de nota com as notas de `notas.csv` e os 6 eventos de `eventos.csv`. Curso vazio `AVAL-REST`, destino da restauração |
| `oraculo` | Curso `AVAL-ORACULO` com `est01` a `est05` e o docente: questionários Q-01 a Q-10, categorias de nota A-01 a A-06 e atividades P-01 a P-04, com as quantidades, os pesos, o crédito parcial e os horários de `M1.2/oraculo.csv` |

<p class="legenda">Tabela 2. Partes da massa. Fonte: elaboração própria.</p>

### Qual parte usar em cada métrica

| Métrica | Partes | Observação |
|---|---|---|
| M1.1, M1.3 e M3.2 | `contas` | As tarefas T01 a T12 criam o próprio curso e as atividades; a massa só fornece as contas |
| M1.2 | `contas,oraculo` | `--dia-prazo` é o dia em que os casos P-01 a P-04 serão executados |
| M2.1 e M2.2 | `contas,catalogo` | Para F1, importar `usuarios.csv` **antes** de aplicar a massa; a parte `contas` reconhece as contas importadas e cria só o docente |
| M2.3 e M2.4 | `contas,catalogo` | |
| M3.1 | `contas,catalogo` | As 8 tarefas usam o curso `AVAL-CAT` |
| M3.5 | `contas,catalogo,oraculo` | Na instância 4.5, antes da atualização |

<p class="legenda">Tabela 3. Partes da massa por métrica. Fonte: elaboração própria, a partir do plano da Fase 3.</p>

### Contas e prazos

- A senha de todas as contas da massa é a senha fictícia `Aval#2026`. Ela é pública de propósito e só vale nas VMs de avaliação. Para usar outra, defina `MASSA_SENHA` antes de `aplicar`.
- Os prazos do oráculo são relativos ao dia D (`--dia-prazo`, padrão: o dia da aplicação), no fuso de Brasília. P-01 e P-02 usam a mesma tarefa, com vencimento e data limite às 23:59 de D: o envio de P-01 é feito por um estudante e a tentativa de P-02 por outro. P-03 tem data limite às 23:59 de D+2; P-04 fecha às 18:00 de D.
- As tarefas do curso completo também são relativas ao dia da aplicação: uma vence em D+7 e a outra já está vencida. Os 6 eventos do calendário têm data fixa (1 a 17/12/2026), para que a referência de F6 não mude.

## Teste da massa

Em 15/11/2026, a massa foi aplicada em uma instância limpa do **Moodle 4.5.16 (Build 20261112)**, com PHP 8.3 e PostgreSQL 16, e conferida por consultas ao banco e pela API do Moodle. Esse teste valida a massa, e **não substitui a coleta**.

| Verificação | Resultado |
|---|---|
| Aplicação completa (`contas,catalogo,oraculo`) | 67 itens criados, sem erro |
| Contas, matrículas, envios, fórum e eventos | 31 contas da massa, 31 matrículas no `AVAL-CAT`, 10 envios, 4 mensagens no fórum e 6 eventos |
| Notas do `AVAL-CAT` contra `notas.csv` | 90 notas iguais |
| Respostas simuladas nos casos Q-01 a Q-10, lançamentos nos casos A-01 a A-06 e datas de P-01 a P-04 | Os 20 resultados iguais ao valor esperado de `oraculo.csv` |
| Importação de `questoes.gift` pelo importador GIFT do Moodle | 15 questões, com as frações de crédito parcial preservadas |
| `usuarios.csv` pela carga de usuários (CLI) e depois `aplicar` | 30 contas criadas e login com a senha da massa; a massa ignorou as 30 e criou o restante |
| Segunda aplicação na mesma instância | Recusada, sem nenhuma alteração no banco |

<p class="legenda">Tabela 4. Resultado do teste da massa. Fonte: elaboração própria.</p>

O Moodle 5.3 não pôde ser instalado no ambiente de teste. Todas as funções do Moodle usadas pelo executor (`scripts/gera_massa_moodle.php`) foram conferidas no código-fonte da 5.3.1 e têm a mesma assinatura. A primeira aplicação em um servidor 5.3 deve conferir o registro gerado antes de iniciar a coleta.
