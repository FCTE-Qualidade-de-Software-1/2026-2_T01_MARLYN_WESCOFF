# Métricas

Cada métrica responde a uma questão de [Objetivos, questões e hipóteses](objetivos-questoes-hipoteses.md) e foi derivada de uma medida da ISO/IEC 25023 (versão disponibilizada na disciplina), adaptada ao Moodle. As métricas seguem a forma de proporção `X = A / B` ou `X = 1 − A / B`, com escala de 0 a 1, em que **valores mais próximos de 1 são melhores**; a exceção é M3.4 (tempo), em que valores menores são melhores.

Todas as métricas usam **método de medição objetivo** (contagem ou cronometragem com regra explícita) e são coletadas na Fase 4, na instalação de referência descrita em [Produto avaliado](../fase-1/produto.md). Os registros brutos ficarão em `dados/avaliacao/<ID da métrica>/`.

Princípios aplicados (Aula 08): **simplicidade** (uma contagem por métrica), **objetividade** (critério de sucesso definido antes da coleta), **facilidade de coleta** (sem ferramentas pagas) e **validade** (cada métrica mede a subcaracterística da questão).

## G1 – Adequação funcional

### M1.1 – Cobertura funcional das tarefas essenciais

| Campo | Descrição |
|---|---|
| Questão | Q1.1 |
| Subcaracterística | Completude funcional |
| Medida de referência (ISO/IEC 25023) | *Functional implementation coverage* |
| Definição | Proporção das tarefas do [catálogo](../fase-1/escopo.md#recorte-operacional-catalogo-de-tarefas-essenciais) para as quais o núcleo oferece função que permite concluí-la |
| Fórmula | `M1.1 = 1 − (Tf / Tt)` |
| Medidas básicas | `Tt` = número de tarefas do catálogo (12); `Tf` = tarefas sem função no núcleo ou cuja função falha ao executar |
| Fonte dos dados | Formulário de execução de tarefas (`dados/avaliacao/M1.1/execucoes.csv`) e captura de tela do resultado de cada tarefa |
| Procedimento de coleta | Executar T01 a T12 na ordem, com as contas fictícias do papel indicado; registrar para cada tarefa: concluída (sim/não), função usada, evidência |
| Escala / unidade | Razão, 0 a 1 / proporção de tarefas |
| Responsável e momento | Responsável por G1; uma vez, na instalação limpa 5.3 |

### M1.2 – Correção funcional dos resultados calculados

| Campo | Descrição |
|---|---|
| Questão | Q1.2 |
| Subcaracterística | Correção funcional |
| Medida de referência (ISO/IEC 25023) | *Correctness* / *Computational accuracy* |
| Definição | Proporção dos casos de teste em que o resultado mostrado pelo Moodle é igual ao resultado esperado (oráculo) |
| Fórmula | `M1.2 = Cc / Ct` |
| Medidas básicas | `Ct` = casos de teste executados (20: 10 de pontuação de questionário, 6 de agregação ponderada no livro de notas, 4 de controle de prazo); `Cc` = casos com resultado igual ao oráculo |
| Fonte dos dados | Planilha de oráculo (`dados/avaliacao/M1.2/oraculo.csv`), com o resultado esperado calculado à mão a partir das regras configuradas; relatório de notas exportado pelo Moodle |
| Procedimento de coleta | Configurar questionário e livro de notas com os valores da planilha; registrar as respostas fictícias; comparar o valor exibido com o oráculo com tolerância de 0,01 ponto; para prazo, verificar se o envio é aceito ou bloqueado conforme o esperado |
| Escala / unidade | Razão, 0 a 1 / proporção de casos |
| Responsável e momento | Responsável por G1, com conferência do oráculo por um segundo integrante antes da coleta |

### M1.3 – Pertinência funcional (tarefas sem contorno)

| Campo | Descrição |
|---|---|
| Questão | Q1.3 |
| Subcaracterística | Pertinência funcional |
| Medida de referência (ISO/IEC 25023) | *Functional appropriateness* |
| Definição | Proporção das tarefas concluídas que **não** exigiram contorno. Contorno = passo não descrito na documentação oficial da função, ou uso de uma função alheia ao objetivo da tarefa (por exemplo, editar o banco de dados ou mudar uma configuração global para concluir uma tarefa de curso) |
| Fórmula | `M1.3 = 1 − (Tc / Tt)` |
| Medidas básicas | `Tt` = tarefas do catálogo (12); `Tc` = tarefas que só foram concluídas com contorno |
| Fonte dos dados | Mesmo formulário de M1.1, campo "contorno necessário" com descrição do passo extra |
| Procedimento de coleta | Durante a execução de M1.1, comparar os passos executados com a página da documentação oficial da função; anotar qualquer passo fora dela |
| Escala / unidade | Razão, 0 a 1 / proporção de tarefas |
| Responsável e momento | Responsável por G1, junto com M1.1 |

!!! note "Por que M1.3 não é uma métrica de usabilidade"
    M1.3 não mede facilidade, tempo ou satisfação do usuário (capacidade de interação, fora do escopo). Ela mede se o **conjunto de funções** leva ao objetivo da tarefa, que é a definição de pertinência funcional na ISO/IEC 25010:2023.

## G2 – Compatibilidade

### M2.1 – Intercambialidade de formatos de dados

| Campo | Descrição |
|---|---|
| Questão | Q2.1 |
| Subcaracterística | Interoperabilidade |
| Medida de referência (ISO/IEC 25023) | *Data exchangeability (data format based)* |
| Definição | Proporção dos formatos de troca de dados em que a operação conclui e o arquivo é aceito pelo outro lado |
| Fórmula | `M2.1 = Fs / Ft` |
| Medidas básicas | `Ft` = formatos testados (7): F1 CSV de usuários (importação), F2 CSV de notas (exportação), F3 XLSX de notas (exportação), F4 GIFT de questões (importação), F5 Moodle XML de questões (exportação e reimportação), F6 iCal do calendário (exportação para cliente de calendário), F7 backup `.mbz` (backup e restauração); `Fs` = formatos em que a operação conclui sem erro e o arquivo é aberto/aceito pelo sistema receptor |
| Fonte dos dados | Arquivos de entrada e saída versionados em `dados/avaliacao/M2.1/`; registro de execução |
| Procedimento de coleta | Para importações, preparar arquivo de referência e importar; para exportações, exportar e abrir no receptor (LibreOffice Calc para CSV/XLSX, Thunderbird para iCal, segunda instância do curso para `.mbz` e XML) |
| Escala / unidade | Razão, 0 a 1 / proporção de formatos |
| Responsável e momento | Responsável por G2 |

### M2.2 – Integridade dos dados trocados

| Campo | Descrição |
|---|---|
| Questão | Q2.2 |
| Subcaracterística | Interoperabilidade |
| Medida de referência (ISO/IEC 25023) | *Data exchangeability* (adaptada para o nível do registro) |
| Definição | Proporção dos registros trocados que chegam ao destino com todos os campos iguais à referência |
| Fórmula | `M2.2 = Rc / Rt` |
| Medidas básicas | `Rt` = registros esperados nos 7 formatos (por exemplo, 30 usuários, 30 × 3 notas, 15 questões, 6 eventos, itens do curso); `Rc` = registros idênticos à referência em todos os campos comparados |
| Fonte dos dados | Arquivo de referência e arquivo/estado de destino; script de comparação (`scripts/compara_registros.py`, a ser criado na Fase 3) |
| Procedimento de coleta | Comparar campo a campo, normalizando apenas espaços em branco; acentuação, casas decimais e datas **não** são normalizadas, porque erros nelas são perda de integridade |
| Escala / unidade | Razão, 0 a 1 / proporção de registros |
| Responsável e momento | Responsável por G2, logo após M2.1 |

### M2.3 – Conectividade com sistema externo (serviços web)

| Campo | Descrição |
|---|---|
| Questão | Q2.3 |
| Subcaracterística | Interoperabilidade |
| Medida de referência (ISO/IEC 25023) | *Connectivity with external system* |
| Definição | Proporção das funções de serviço web REST selecionadas que respondem sem exceção e com dados coerentes com o estado do Moodle |
| Fórmula | `M2.3 = Ws / Wt` |
| Medidas básicas | `Wt` = funções testadas (6): `core_webservice_get_site_info`, `core_user_get_users_by_field`, `core_course_get_courses_by_field`, `core_enrol_get_enrolled_users`, `mod_assign_get_assignments`, `gradereport_user_get_grade_items`; `Ws` = funções com resposta HTTP 200, sem campo `exception` e com valores iguais aos exibidos na interface web |
| Fonte dos dados | Respostas JSON salvas em `dados/avaliacao/M2.3/`; script cliente (`curl` ou Python) |
| Procedimento de coleta | Habilitar serviços web e protocolo REST; criar serviço externo com as 6 funções, usuário de integração e token; chamar cada função com parâmetros conhecidos; comparar com a interface |
| Escala / unidade | Razão, 0 a 1 / proporção de funções |
| Responsável e momento | Responsável por G2 |

### M2.4 – Coexistência disponível

| Campo | Descrição |
|---|---|
| Questão | Q2.4 |
| Subcaracterística | Coexistência |
| Medida de referência (ISO/IEC 25023) | *Available co-existence* |
| Definição | Proporção das entidades vizinhas no mesmo servidor que continuam funcionando sem alteração durante e após as operações do Moodle |
| Fórmula | `M2.4 = Ec / Et` |
| Medidas básicas | `Et` = entidades vizinhas (3): E1 aplicação web estática em outro *virtual host* do mesmo Apache; E2 banco de dados de outra aplicação no mesmo PostgreSQL; E3 tarefa agendada de outro usuário no mesmo `cron`; `Ec` = entidades sem impacto em todas as verificações |
| Fonte dos dados | Log de verificação (`dados/avaliacao/M2.4/verificacoes.csv`) |
| Procedimento de coleta | Antes, durante e depois de 4 operações do Moodle (instalação, execução do cron, backup de curso, atualização), verificar: E1 responde HTTP 200 com o mesmo *hash* de conteúdo; E2 mantém o mesmo *checksum* das tabelas; E3 executou no horário. Uma falha em qualquer verificação marca a entidade como afetada |
| Escala / unidade | Razão, 0 a 1 / proporção de entidades |
| Responsável e momento | Responsável por G2, junto com a instalação e a atualização de G3 |

## G3 – Flexibilidade

### M3.1 – Adaptabilidade ao ambiente de acesso

| Campo | Descrição |
|---|---|
| Questão | Q3.1 |
| Subcaracterística | Adaptabilidade |
| Medida de referência (ISO/IEC 25023) | *Hardware / system software environmental adaptability* |
| Definição | Para cada ambiente de acesso A1–A4, proporção das tarefas testadas concluídas com o mesmo resultado obtido em A1 |
| Fórmula | `M3.1(Ai) = 1 − (Tfa / Tta)`; valor reportado = mínimo entre A1–A4 |
| Medidas básicas | `Tta` = tarefas testadas por ambiente (8: T02, T03, T04, T05, T06, T08, T09, T11); `Tfa` = tarefas não concluídas ou com resultado diferente no ambiente |
| Fonte dos dados | Formulário por ambiente (`dados/avaliacao/M3.1/`), com versão do sistema e do navegador e captura de tela |
| Procedimento de coleta | Executar as 8 tarefas em cada ambiente com as mesmas contas, em sessão limpa do navegador (sem extensões) |
| Escala / unidade | Razão, 0 a 1 / proporção de tarefas |
| Responsável e momento | Responsável por G3, após M1.1 |

### M3.2 – Adaptabilidade ao ambiente de software de servidor

| Campo | Descrição |
|---|---|
| Questão | Q3.2 |
| Subcaracterística | Adaptabilidade |
| Medida de referência (ISO/IEC 25023) | *System software environmental adaptability* |
| Definição | Para cada versão de PHP suportada (8.3 e 8.4), proporção das tarefas do catálogo concluídas com o resultado esperado |
| Fórmula | `M3.2(PHPi) = 1 − (Tfp / Ttp)`; valor reportado = mínimo entre as duas versões |
| Medidas básicas | `Ttp` = tarefas do catálogo (12); `Tfp` = tarefas que falham ou diferem do resultado esperado naquela versão de PHP |
| Fonte dos dados | Formulário de M1.1 repetido para a segunda versão de PHP; página "Verificação de ambiente" do Moodle |
| Procedimento de coleta | Montar duas instâncias idênticas, mudando apenas a versão do PHP; executar T01 a T12 nas duas |
| Escala / unidade | Razão, 0 a 1 / proporção de tarefas |
| Responsável e momento | Responsável por G3 |

### M3.3 – Taxa de sucesso de instalação e atualização

| Campo | Descrição |
|---|---|
| Questão | Q3.3 |
| Subcaracterística | Instalabilidade |
| Medida de referência (ISO/IEC 25023) | *Ease of installation* (adaptada para sucesso por execução) |
| Definição | Proporção das execuções de instalação/atualização que concluem seguindo **apenas** a documentação oficial |
| Fórmula | `M3.3 = Ps / Pt` |
| Medidas básicas | `Pt` = execuções (6: 3 instalações limpas da 5.3 e 3 atualizações 4.5 → 5.3, cada uma em máquina virtual recém-criada a partir da mesma imagem); `Ps` = execuções que terminam com a verificação de ambiente sem erro, login do administrador funcionando e sem passo fora da documentação |
| Fonte dos dados | Log do terminal (`script`), registro de execução (`dados/avaliacao/M3.3/execucoes.csv`) |
| Procedimento de coleta | Seguir a página oficial de instalação/atualização da 5.3 passo a passo; qualquer passo extra (por exemplo, descobrir sozinho que a raiz web deve apontar para `public/`) é registrado e a execução conta como sem sucesso |
| Escala / unidade | Razão, 0 a 1 / proporção de execuções |
| Responsável e momento | Responsável por G3, com um segundo integrante executando ao menos uma das três repetições |

### M3.4 – Eficiência de tempo de instalação

| Campo | Descrição |
|---|---|
| Questão | Q3.3 |
| Subcaracterística | Instalabilidade |
| Medida de referência (ISO/IEC 25023) | *Installation time efficiency* |
| Definição | Mediana do tempo decorrido entre o início do procedimento e o primeiro login do administrador, e número de retentativas |
| Fórmula | `M3.4 = mediana(tfim − tinício)` em minutos, por tipo (instalação limpa / atualização); `R` = total de retentativas |
| Medidas básicas | `tinício`: primeiro comando do procedimento, com o código já baixado; `tfim`: login do administrador; retentativa = repetir um passo que falhou |
| Fonte dos dados | Carimbos de tempo do log do terminal |
| Procedimento de coleta | Mesmas 6 execuções de M3.3 |
| Escala / unidade | Razão / minutos e contagem |
| Responsável e momento | Responsável por G3, junto com M3.3 |

### M3.5 – Preservação de dados na atualização

| Campo | Descrição |
|---|---|
| Questão | Q3.4 |
| Subcaracterística | Instalabilidade |
| Medida de referência (ISO/IEC 25023) | Medida definida pela equipe (a ISO/IEC 25023 não tem medida específica de preservação de dados) |
| Definição | Proporção dos itens de verificação presentes e idênticos antes e depois da atualização 4.5 → 5.3 |
| Fórmula | `M3.5 = Ip / It` |
| Medidas básicas | `It` = itens de verificação (40: contagens de usuários, cursos, matrículas, envios de tarefa, tentativas de questionário, posts de fórum, arquivos, e as notas finais de 10 estudantes); `Ip` = itens iguais após a atualização |
| Fonte dos dados | Consultas SQL de contagem e relatório de notas exportado antes e depois (`dados/avaliacao/M3.5/`) |
| Procedimento de coleta | Popular a instância 4.5 com o conjunto de dados fictícios; executar as consultas; atualizar; repetir as consultas e comparar |
| Escala / unidade | Razão, 0 a 1 / proporção de itens |
| Responsável e momento | Responsável por G3, em cada atualização de M3.3 |

## Resumo

| Métrica | Fórmula | Questão | Subcaracterística |
|---|---|---|---|
| M1.1 | 1 − Tf/Tt | Q1.1 | Completude funcional |
| M1.2 | Cc/Ct | Q1.2 | Correção funcional |
| M1.3 | 1 − Tc/Tt | Q1.3 | Pertinência funcional |
| M2.1 | Fs/Ft | Q2.1 | Interoperabilidade |
| M2.2 | Rc/Rt | Q2.2 | Interoperabilidade |
| M2.3 | Ws/Wt | Q2.3 | Interoperabilidade |
| M2.4 | Ec/Et | Q2.4 | Coexistência |
| M3.1 | min(1 − Tfa/Tta) | Q3.1 | Adaptabilidade |
| M3.2 | min(1 − Tfp/Ttp) | Q3.2 | Adaptabilidade |
| M3.3 | Ps/Pt | Q3.3 | Instalabilidade |
| M3.4 | mediana(tfim − tinício); R | Q3.3 | Instalabilidade |
| M3.5 | Ip/It | Q3.4 | Instalabilidade |

<p class="legenda">Tabela 1. Resumo das métricas. Fonte: elaboração própria a partir da ISO/IEC 25023.</p>
