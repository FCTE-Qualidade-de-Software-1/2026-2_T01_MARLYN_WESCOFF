# Resultados e julgamento

Coleta de 15 a 22/11/2026, no servidor de avaliação montado pelo script de preparação: Moodle 5.3.1+ e 4.5.16+, PHP 8.3.37 e 8.4.28, PostgreSQL 17.12. M1.1 e M1.3 foram coletadas pela interface; as demais foram executadas por scripts versionados (Playwright na interface, API do próprio Moodle, `faketime` nos prazos e um contêiner novo da imagem-base por execução de M3.3), executados pelo Maykon numa máquina compartilhada pela equipe. Desvios e tentativas descartadas estão no README de cada métrica.

## Métricas

| Métrica | Valor | Nota | Hipótese | Observação | Evidência |
|---|---|---|---|---|---|
| M1.1 Cobertura funcional | 12/12 = 1,00 | 4 | H1.1 confirmada | As 12 tarefas com função do núcleo | [M1.1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M1.1/execucoes.csv) |
| M1.2 Correção funcional | 19/20 = 0,95 | 1 | H1.2 refutada | A-04: o Moodle exibe 53,00 de 70 (75,71%); o oráculo espera 7,57 | [M1.2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M1.2/README.md) |
| M1.3 Pertinência funcional | 12/12 = 1,00 | 4 | H1.3 refutada | Nenhum contorno; esperava-se um, na restauração | [M1.1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M1.1/execucoes.csv) |
| M2.1 Intercâmbio de formatos | 7/7 = 1,00 | 4 | H2.1 confirmada | F2 e F3 na segunda tentativa válida | [M2.1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.1/README.md) |
| M2.2 Integridade dos dados | 132/132 = 1,00 | 4 | H2.2 confirmada | Acentuação íntegra; comparação refeita em 24/11 com o instrumento corrigido (a de 22/11 dava 97/132 por diferença de representação) | [M2.2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.2/README.md) |
| M2.3 Serviços web | 6/6 = 1,00 | 4 | H2.3 confirmada | HTTP 200, sem exceção, valores da massa | [M2.3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.3/README.md) |
| M2.4 Coexistência | 2/3 = 0,67 | 2 | H2.4 refutada | Vizinha web sem resposta por cerca de 2 s na instalação | [M2.4](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.4/README.md) |
| M3.1 Ambientes de acesso | 8/8 = 1,00 | 4 | H3.1 confirmada | Chrome e Firefox no Windows, Firefox no Ubuntu e Android emulado | [M3.1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.1/README.md) |
| M3.2 Versões de PHP | 12/12 = 1,00 | 4 | H3.2 confirmada | PHP 8.3 e 8.4 iguais, mesmos avisos no log | [M3.2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.2/README.md) |
| M3.3 Sucesso de instalação | 6/6 = 1,00 | 4 | H3.3 refutada | Nenhuma falha por `public/` | [M3.3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.3/README.md) |
| M3.4 Tempo de instalação | 1,18 min; R = 0 | 4 | H3.3 confirmada | Tempo de procedimento automatizado | [M3.3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.3/execucoes.csv) |
| M3.5 Preservação de dados | 40/40 = 1,00 | 4 | H3.4 confirmada | Nas 3 atualizações | [M3.5](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.5/README.md) |

<p class="legenda">Tabela 1. Valor, nota e hipótese de cada métrica. Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>

## Respostas às questões e julgamento

| Objetivo | Notas das questões | Julgamento (critério congelado) | Análise de sensibilidade | Decisão recomendada |
|---|---|---|---|---|
| **G1** Adequação funcional | Q1.1 = 4 · Q1.2 = 1 · Q1.3 = 4 | **Não atende** | Atende, se o A-04 for tratado como diferença de escala | D1: prosseguir com a adoção, conferindo a exibição de totais em soma natural |
| **G2** Compatibilidade | Q2.1 = 4 · Q2.2 = 4 · Q2.3 = 4 · Q2.4 = 2 | **Atende com ressalvas** | Atende com ressalvas | D2: manter as integrações, publicando virtual hosts com `reload` |
| **G3** Flexibilidade | Q3.1 = 4 · Q3.2 = 4 · Q3.3 = 4 · Q3.4 = 4 | **Atende** | Atende | D3: migrar com o procedimento documentado, lendo "Configuring the Router" |

<p class="legenda">Tabela 2. Julgamento dos objetivos e decisão para o requisitante. Fonte: elaborado pelos autores, pelas regras de <a href="../../fase-2/niveis-e-julgamento/">Níveis e julgamento</a>.</p>

A única nota 1 (Q1.2, pelo caso A-04) vem da escala de exibição, e não de cálculo errado. Como a regra R1 proíbe mudar o critério depois da coleta, a equipe registra o julgamento pelo critério e a análise de sensibilidade; a decisão sobre o A-04 fica para a ata, com o motivo. M2.2 não entra nessa análise: a divergência de 22/11 era do instrumento de comparação, corrigido antes do julgamento sem mudar o critério (PR #134).

- **Q1.1, O núcleo dá conta das tarefas?** Sim: 12 de 12 tarefas, sem contorno.
- **Q1.2, Notas e prazos saem certos?** Os cálculos, sim (19 de 20 iguais ao oráculo); a exibição do total em soma natural, não na escala esperada.
- **Q2.1 e Q2.2, Os dados entram, saem e chegam como saíram?** Os sete formatos foram trocados e nenhum dado se perdeu; números e questões numéricas mudam de representação.
- **Q2.3, Um sistema externo consegue usar o Moodle?** Sim, com as capacidades e os parâmetros documentados.
- **Q2.4, Divide o servidor sem atrapalhar?** O Moodle, sim; o procedimento de instalação, não (resolvido na [ação de melhoria](acao-de-melhoria.md)).
- **Q3.1 a Q3.4:** funciona nos quatro ambientes e nas duas versões de PHP; instala e atualiza pela documentação, preservando os dados.

## Problemas encontrados no produto

| Problema | Evidência | Consequência para o usuário |
|---|---|---|
| A documentação do servidor web está dividida: o bloco das páginas "Apache" e "Upgrading" não tem o `DirectoryIndex` exigido em "Configuring the Router" | [M3.3, tentativa 1](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.3/README.md) | Quem segue a página "Apache" fica com a raiz do site e o painel `/my/` em 404 |
| O total em soma natural é exibido só em pontos e porcentagem | [M1.2, caso A-04](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M1.2/README.md) | Quem lança notas em pontos não vê o total na escala de 0 a 10 |
| A exportação de notas pendente de recálculo mostra o identificador "grades/gradesneedregrading", sem texto | [M2.1, F2 e F3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.1/README.md) | Mensagem incompreensível para o docente |
| Com PHP-FPM por `FilesMatch`, rotas `.php` do roteador dão 404 (`checks.php`: core_router) | [M3.3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.3/README.md) | Páginas novas do roteador podem não abrir |
| Aviso "Undefined property: $noreplyaddress" em toda página, nas duas versões de PHP | [M3.2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.2/README.md) | Ruído no log do servidor |

<p class="legenda">Tabela 3. Problemas encontrados, evidências e consequências. Fonte: elaborado pelos autores.</p>

## Relações entre as características

- **Compatibilidade × instalabilidade:** a falha de coexistência (M2.4) veio do procedimento de instalação, e a configuração incompleta do roteador afetou ao mesmo tempo a instalação (M3.3) e o acesso às páginas.
- **Correção × interoperabilidade:** o mesmo valor aparece como 53,00, 75,71% ou `10.0`, conforme a tela ou o formato.
- **Sem dados para relacionar** adaptabilidade e adequação funcional: todas as tarefas funcionaram em todos os ambientes e versões.

## Dificuldades e limitações

- Três tentativas de M3.3 foram descartadas por erro do procedimento ou do instrumento, todas guardadas no repositório.
- O Android foi emulado, e não testado num aparelho; o tempo de M3.4 é de um procedimento automatizado, não de uma pessoa.
- No A2, três tarefas passaram só na repetição, por falha do controle do Firefox.
- As conferências por segundo integrante (regra R6) ficaram para a revisão dos pull requests. M3.1 e M3.2 foram conferidas pelo responsável em 23/11/2026; a captura de T09 no PHP 8.4 não foi gravada, e esse resultado se apoia só no registro do script ([M3.2](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M3.2/README.md)).
