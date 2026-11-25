# Ata 03 – 2026-11-23 (RASCUNHO, a aprovar pela equipe)

> **Rascunho preparado para a reunião.** Os dados das seções 1 e 2 vêm do repositório. Participantes, discussão e decisões só valem depois de preenchidos e aprovados pela equipe. Depois da aprovação, renomear para `2026-11-23-ata-03.md` e retirar esta nota.

| Campo | Valor |
|---|---|
| Data e horário | 2026-11-23, __h__–__h__ |
| Local | |
| Participantes | |
| Ausentes | |
| Responsável pela ata | |

## Pauta

1. Prorrogação da Entrega 2 para 24/11 e cronograma realizado da Fase 4 (issue #123).
2. Sessão de interpretação dos resultados da Fase 4 (issue #122, Aula 08).
3. Decisão sobre o caso A-04 de M1.2.
4. Comparação de M2.2: resolvida pela correção do instrumento (PR #134); fica só o registro.
5. Conferência das coletas por cada responsável (regra R6) e revisão dos pull requests.
6. Release final, artigo e apresentação.

## 1. Cronograma realizado

A docente prorrogou a Entrega 2 de 22/11 para 24/11/2026, às 23h59. A coleta, prevista para 18 a 20/11, foi de 15 a 22/11: M1.1 e M1.3 em 15/11, pela interface; as demais métricas em 22/11, num servidor compartilhado, com execução por scripts versionados. O julgamento foi em 22/11. O cronograma previsto e o realizado estão na Tabela 3 do [plano de execução da Fase 4](../docs/fase-4/plano-de-execucao.md).

## 2. Sessão de interpretação: dados por questão

Cada responsável apresenta os dados da sua questão (detalhes em `dados/avaliacao/<métrica>/README.md`):

| Questão | Responsável | Dados | Nota | Hipótese |
|---|---|---|---|---|
| Q1.1 | Bernardo | M1.1 = 12/12; M1.3 = 12/12 | 4 | H1.1 confirmada |
| Q1.2 | Bernardo | M1.2 = 19/20 (A-04 não conforme) | 1 | H1.2 refutada |
| Q1.3 | Bernardo | M1.3 = 12/12 (nenhum contorno) | 4 | H1.3 refutada (esperava 1 contorno) |
| Q2.1 | Carlos | M2.1 = 7/7 | 4 | H2.1 confirmada |
| Q2.2 | Carlos | M2.1 = 7/7; M2.2 = 132/132 (comparação refeita em 24/11 com o instrumento corrigido) | 4 | H2.2 confirmada |
| Q2.3 | Maykon | M2.3 = 6/6 | 4 | H2.3 confirmada |
| Q2.4 | Maykon | M2.4 = 2/3 (vizinha web sem resposta por cerca de 2 s na instalação) | 2 | H2.4 refutada |
| Q3.1 | João Pedro | M3.1 = 8/8 nos 4 ambientes (A4 emulado) | 4 | H3.1 confirmada |
| Q3.2 | João Pedro | M3.2 = 12/12 em PHP 8.3 e 8.4 | 4 | H3.2 confirmada |
| Q3.3 | Pedro | M3.3 = 6/6; M3.4 = 1,18 min, R = 0 | 4 | H3.3 refutada (nenhuma falha por `public/`) |
| Q3.4 | Pedro | M3.5 = 40/40 nas 3 atualizações | 4 | H3.4 confirmada |

Julgamento pelo critério congelado: G1 não atende; G2 atende com ressalvas; G3 atende. Explicação das hipóteses refutadas pelas medidas de contexto: ______

## 3. Decisões a tomar

| Nº | Assunto | Opção A (manter o critério) | Opção B (registrar a leitura por valor) | Decisão da equipe |
|---|---|---|---|---|
| D1 | A-04 de M1.2: o Moodle exibe 53,00 de 70 (75,71%) e o oráculo esperava 7,57 "na escala de 0 a 10", que a soma natural não oferece | Não conforme: M1.2 = 0,95, nota 1, G1 não atende | O oráculo previa uma conversão que a configuração do caso não tinha; 75,71% = 7,57: M1.2 = 1,00, G1 atende | |
| D2 | M2.2: F3 (o número `10.0` contra o texto `10.00`) e F4 (`# =%100%7:0#` contra `#7`) divergem só na representação | — | — | **Resolvida em 23/11** pela correção do instrumento (PR #134, Registro de decisões): o critério não mudou, e a comparação refeita em 24/11 deu M2.2 = 132/132 = 1,00; G2 atende com ressalvas (M2.4 = 2) |

Observação: a regra R1 proíbe ajustar o critério depois de ver o resultado. Se a equipe escolher a opção B, o artigo e a GitPage devem manter o resultado pelo critério congelado e apresentar a opção B como análise de sensibilidade (é o que já fazem hoje).

## 4. Conferência de M3.1 e M3.2 e desvios a aprovar (proposta de João Pedro)

João Pedro conferiu M3.1 e M3.2 em 23/11, sobre a versão do PR #133 (detalhes nos READMEs de `M3.1/` e `M3.2/`). Os resultados se mantêm: M3.1 = 8/8 e M3.2 = 12/12. Desvios a aprovar:

| Nº | Métrica | Desvio do plano da Fase 3 | Efeito no resultado | Decisão da equipe |
|---|---|---|---|---|
| V1 | M3.1 e M3.2 | Coleta executada por Maykon, e não pelo responsável; o responsável conferiu (R6) | Nenhum | |
| V2 | M3.1 | A4 é um Android emulado (Chromium com perfil Pixel 7); o plano só aceita emulador registrado em ata | Q3.1 vale para o navegador móvel emulado; falta confirmar num aparelho | |
| V3 | M3.2 | T01, T07, T10 e T12 executadas pela API, com a página resultante aberta pela interface | Mede o código do servidor nas duas versões de PHP, mas não o formulário dessas 4 tarefas | |
| V4 | M3.2 | Instâncias `m32php83` e `m32php84` com a massa `contas,catalogo` | Nenhum: as duas instâncias são iguais, exceto pelo PHP | |
| V5 | M3.2 | Sem a captura de T09 no PHP 8.4 | O resultado de T09 no PHP 8.4 se apoia só no registro do script; repetir, se a instância existir | |

## Encaminhamentos

| Tarefa | Responsável | Prazo | Issue/PR |
|---|---|---|---|
| Conferir M1.2 no PR #133 | Bernardo | 24/11 | #133 |
| Conferir M2.1 e M2.2 no PR #133 | Carlos | 24/11 | #133 |
| Conferir M3.1 e M3.2 no PR #133 | João Pedro | 24/11 | #133 |
| Conferir M3.3 a M3.5 e a ação de melhoria no PR #133 | Pedro | 24/11 | #133 |
| Revisar e mergear o PR #133 (inclui #98, #124 a #132) | | 24/11 | #133 |
| Publicar a release final com o PDF do artigo | | 24/11, 23h59 | #78 |
| Enviar o artigo e a apresentação no Moodle | | 24/11 / antes da aula | |
