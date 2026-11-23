# Plano de avaliação (Fase 3)

Este plano parte do que a [Fase 2](../fase-2/index.md) já fixou (métricas, níveis de pontuação e critérios de julgamento) e **não altera nenhum deles**. Ele foi aprovado na reunião de 14/11/2026 ([ata 02](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-11-14-ata-02.md), decisão D1), que também fixou o cronograma de 16 a 22/11 (D2), o uso de um servidor por integrante montado pelo mesmo script (D3) e a manutenção das 6 execuções de M3.3 a M3.5 (D4).

O plano responde a uma pergunta: **o que cada avaliador faz, em que ordem e com quais recursos, para que duas pessoas diferentes obtenham as mesmas medidas?** Ele cobre as 12 métricas (M1.1 a M3.5) dos objetivos G1 (adequação funcional), G2 (compatibilidade) e G3 (flexibilidade), e alimenta as decisões D1 a D4 do [Propósito](../fase-1/proposito.md).

O progresso deste plano, o tempo de execução das tarefas e o esforço da equipe são monitorados na seção [Gestão do projeto (PSM/CID)](../gestao/index.md).

## 1. Método de avaliação

| Aspecto | Definição |
|---|---|
| Tipo | Avaliação externa, caixa-preta, orientada a tarefas (ver [Profundidade](../fase-1/escopo.md#profundidade)) |
| Objeto | Núcleo do Moodle 5.3 LTS, tema Boost, sem plugins de terceiros |
| Origem da verdade | Documentação oficial (docs.moodle.org e moodledev.io) e **oráculo calculado à mão** antes da coleta |
| Julgamento | Níveis e regras de [Níveis de pontuação e julgamento](../fase-2/niveis-e-julgamento.md), congelados antes da coleta |
| Repetição | Instalações e atualizações: 3 execuções cada. Demais métricas: uma execução completa, mais a repetição de qualquer caso que falhar (para separar falha do produto de erro do avaliador) |

<p class="legenda">Tabela 1. Resumo do método. Fonte: elaboração própria.</p>

### Regras gerais para todos os avaliadores

| Regra | O que fazer |
|---|---|
| R1. Critério antes da coleta | O critério de sucesso de cada caso está escrito antes da execução. Não se ajusta o critério depois de ver o resultado |
| R2. Sessão limpa | Navegador sem extensões, sem cache e sem sessão anterior. Uma conta fictícia por papel (administrador, docente, estudante) |
| R3. Só a documentação | Em M3.3, a única fonte de instruções é a página oficial da 5.3. Qualquer passo descoberto fora dela é registrado, e a execução conta como sem sucesso |
| R4. Registrar sempre | Cada caso gera uma linha no CSV da métrica, com data, avaliador, resultado e nome do arquivo de evidência. Falha também é registrada |
| R5. Não resolver no improviso | Se o caso falhar, anotar a mensagem de erro e a evidência, e seguir para o próximo. Corrigir a configuração só é permitido se o correto estiver na documentação, e o ajuste é registrado |
| R6. Conferência por segundo integrante | Oráculo (M1.2), uma das três repetições de M3.3 e a lista de itens de M3.5 são conferidos por alguém que não os produziu |
| R7. Sem dados reais | Nenhum dado de estudante, docente ou instituição. Endereços de e-mail fictícios usam o domínio reservado `example.invalid` |
| R8. Sem e-mail de saída | A instância não envia mensagens reais (configuração `noemailever` no `config.php`) |

<p class="legenda">Tabela 2. Regras gerais de execução. Fonte: elaboração própria.</p>

## 2. Recursos e ambiente

### Servidor de referência

Não há um servidor compartilhado: **cada integrante monta o próprio servidor** com o script versionado `scripts/preparar_servidor.sh` (issue #62), para que a coleta ocorra em paralelo (ata 02, D3). O script fixa a mesma configuração em todas as máquinas, e a etapa `versoes` grava as versões exatas de cada uma. A tabela abaixo é a especificação que o script reproduz.

| Item | Especificação |
|---|---|
| Virtualizador | VirtualBox 7 (os comandos de *snapshot* e clone do roteiro usam `VBoxManage`). Outro virtualizador gratuito é aceito se produzir a mesma VM; o script foi testado em QEMU/KVM em 15/11/2026. O virtualizador e a versão usados por cada integrante são registrados no arquivo de versões |
| Máquina virtual | Ubuntu Server 24.04 LTS, 2 vCPU, 4 GB de RAM, 40 GB de disco. Atende aos requisitos oficiais da 5.3 listados em [Produto avaliado](../fase-1/produto.md) e foi validada no teste do script em VM limpa, em 15/11/2026 |
| Rede | NAT com redirecionamento das portas 8080 a 8082 do hospedeiro, ou modo *bridge* quando o ambiente A4 (celular) precisar acessar a VM pela rede local |
| Servidor web | Apache 2.4 com PHP-FPM por *virtual host*, raiz web apontando para a pasta `public/` do Moodle |
| PHP | 8.3 e 8.4 lado a lado, em duas instâncias idênticas que mudam apenas a versão (M3.2). O 8.4 vem de `ppa:ondrej/php`, porque o Ubuntu 24.04 só traz o 8.3. O Moodle 4.5 roda só com o 8.3 |
| Banco de dados | PostgreSQL 17 do repositório oficial PGDG (o Ubuntu 24.04 só traz o 16), com um segundo banco de outra aplicação para M2.4 |
| Moodle | 5.3.x e 4.5.x (origem da atualização), pacotes oficiais de download.moodle.org. A versão corretiva e o *build* de cada servidor são registrados pela etapa `versoes` |
| Imagem-base | *Snapshot* da VM depois da etapa `base` do script, **sem o Moodle**. Inclui Apache, PHP com as extensões exigidas e PostgreSQL, que são pré-requisitos do servidor e não fazem parte do procedimento medido em M3.3. Cada execução de M3.3 e M3.4 começa de um clone desse *snapshot* |

<p class="legenda">Tabela 3. Servidor de referência. Fonte: elaboração própria, a partir de [Produto avaliado](../fase-1/produto.md) e do teste do script de preparação (15/11/2026).</p>

| Instância | Comando do script | Usada em |
|---|---|---|
| `m53php83` (porta 8080) | `instancia m53php83 503 8.3 8080` | G1, G2, M3.1 e M3.2 (PHP 8.3) |
| `m53php84` (porta 8081) | `instancia m53php84 503 8.4 8081` | M3.2 (PHP 8.4) |
| `m45` (porta 8082, em clone da imagem-base) | `instancia m45 405 8.3 8082` | Origem das atualizações de M3.3 a M3.5 |
| Clones da imagem-base | `codigo 503` | Execuções de M3.3 e M3.4: só baixa e extrai o código; o procedimento oficial é executado à mão |

<p class="legenda">Tabela 4. Instâncias montadas pelo script e métricas que usam cada uma. Fonte: elaboração própria.</p>

O servidor é montado pelo script `scripts/preparar_servidor.sh`, conforme [Preparação do servidor](preparacao-do-servidor.md).

### Ambientes de acesso

Os quatro ambientes A1 a A4 são os de [Escopo](../fase-1/escopo.md#ambientes-de-acesso). Antes da primeira tarefa, o avaliador registra em `dados/avaliacao/M3.1/ambientes.csv` o sistema operacional, a versão exata do navegador, a resolução da tela e o dono do dispositivo. Quem não tem o dispositivo A4 (Android) usa o de outro integrante, e o dono do dispositivo é registrado.

### Ferramentas (todas gratuitas)

| Ferramenta | Uso |
|---|---|
| `scripts/preparar_servidor.sh` | Montagem do servidor, das instâncias e registro das versões (issue #62) |
| `scripts/gera_massa.py` | Massa de dados fictícia e arquivos de referência (issue #63) |
| `curl` ou Python 3 | Chamadas REST (M2.3) e script de comparação (M2.2) |
| `scripts/compara_registros.py` | Comparação campo a campo de M2.2 (issue #65) |
| LibreOffice Calc, Thunderbird | Receptores de CSV/XLSX e de iCal (M2.1) |
| `script` (util-linux) | Log do terminal com carimbos de tempo (M3.3 e M3.4) |
| `sha256sum`, consultas SQL de checksum | Verificação das entidades vizinhas (M2.4) e dos itens de M3.5 |
| Captura de tela do sistema | Evidência de cada caso |

<p class="legenda">Tabela 5. Ferramentas. Fonte: elaboração própria.</p>

### Massa de dados fictícia

| Elemento | Quantidade e regra |
|---|---|
| Estudantes | 30 (`est01` a `est30`), e-mail `estNN@example.invalid` |
| Docente | 1 (`docente01`) |
| Administrador | 1 (`admin-aval`, criado pelo script de preparação) |
| Cursos | 3: um completo (`AVAL-CAT`), com as atividades do catálogo T01 a T12; um vazio (`AVAL-REST`), destino da restauração (T12); e o do oráculo (`AVAL-ORACULO`), com as configurações de M1.2 |
| Atividades do catálogo | 2 tarefas (uma dentro do prazo, para T04, e uma com a data limite vencida, para T05), 1 questionário (3 questões de múltipla escolha e 2 numéricas), 1 fórum com 1 tópico e 3 respostas, 1 arquivo de material |
| Dados já lançados | 3 itens de nota com as notas dos 30 estudantes, 10 envios na tarefa aberta e 6 eventos de calendário, para F2, F3 e F6 de M2.1 e para a comparação de M3.5 |
| Configurações do oráculo (M1.2) | Os questionários, os itens e categorias do livro de notas e as atividades com prazo de cada caso de `dados/avaliacao/M1.2/oraculo.csv` (Q-01 a Q-10, A-01 a A-06, P-01 a P-04), com as quantidades de questões, os pesos e o crédito parcial definidos em cada linha |
| Arquivos de referência | `usuarios.csv` (30 linhas) e `questoes.gift` (15 questões), usados em F1 e F4 de M2.1; `notas.csv` e `eventos.csv`, referências de F2, F3 e F6 |
| Dados de comparação | Arquivos congelados em `dados/avaliacao/M2.1/referencia/` antes da primeira troca |

<p class="legenda">Tabela 6. Massa de dados fictícia. Fonte: elaboração própria.</p>

A massa é gerada pelo script versionado `scripts/gera_massa.py` e não digitada à mão, para que todos os servidores e as três atualizações de M3.3 comecem do mesmo conjunto e M3.5 compare "antes" e "depois" sem ruído. As questões dos questionários do oráculo são criadas pelo script no banco de questões de cada questionário; os arquivos de referência continuam separados porque são as entradas congeladas de M2.1. Os arquivos, as partes da massa (`contas`, `catalogo` e `oraculo`) e qual parte usar em cada métrica estão em `dados/avaliacao/massa/README.md`.

### Oráculo (M1.2)

O oráculo é a planilha `dados/avaliacao/M1.2/oraculo.csv`, com **20 casos**: 10 de pontuação de questionário, 6 de agregação ponderada e 4 de controle de prazo. Cada linha traz a regra configurada, as entradas, o cálculo manual, o valor esperado, a tolerância (0,01 ponto) e o critério de comparação. A planilha é produzida por Bernardo e conferida por Carlos antes da coleta de G1 (regra R6; ata 02, D6).

| caso | tipo | regra configurada | entradas | esperado |
|---|---|---|---|---|
| Q-01 | questionário | 3 questões de 1,0 ponto, nota máxima 3,0 | estudante acerta 2 de 3 | 2,00 |
| A-01 | agregação | P1 com peso 40 e P2 com peso 60 | P1 = 7,5; P2 = 8,0 | 7,80 |
| P-01 | prazo | data limite às 23:59 do dia D | envio às 23:58 de D | aceito |
| P-02 | prazo | data limite às 23:59 do dia D | envio às 00:01 de D+1 | bloqueado |

<p class="legenda">Tabela 7. Exemplos de linhas do oráculo (a lista completa de 20 casos está em <code>oraculo.csv</code>). Fonte: elaboração própria.</p>

### Perfil do avaliador

Os avaliadores são os integrantes da equipe. Pré-requisitos: usar o terminal Linux básico (para G2 e G3), ler a documentação oficial do Moodle e seguir o roteiro sem interpretá-lo. Quem executa M3.3 faz antes **uma instalação de treino** descartada: para Pedro, é o piloto (seção 4); para Bernardo, que faz uma das execuções (ata 02, D4), é uma instalação no próprio servidor antes de 19/11. Como a equipe não recruta participantes externos, a coleta **não envolve entrevistas nem pessoas fora do grupo**, e o [Termo de consentimento](../gestao/termo-consentimento.md) só será usado se isso mudar.

## 3. Instruções do avaliador

Cada bloco abaixo é um roteiro. O formato de cada métrica (fórmula, definição, fonte) continua em [Métricas](../fase-2/metricas.md); aqui está **como executar**.

### Antes de qualquer coleta (todos os avaliadores)

1. Montar o próprio servidor com `scripts/preparar_servidor.sh` (etapas `base` e `instancia`), seguindo a página de preparação do servidor da issue #62.
2. Aplicar a massa na instância que será usada, com as partes indicadas para a métrica: `sudo python3 scripts/gera_massa.py aplicar --moodle /var/www/<instância> --php php<versão> --partes <partes>` (ver `dados/avaliacao/massa/README.md`).
3. Rodar a etapa `versoes` e versionar o resultado em `dados/avaliacao/ambiente/versoes-<iniciais>.txt`, acrescentando o virtualizador e a versão dele.

### G1 – Adequação funcional (M1.1, M1.2, M1.3)

1. Usar a instância `m53php83`, recém-criada pelo script, com as partes `contas` e `oraculo` da massa aplicadas (T01 a T12 criam o próprio curso).
2. Abrir `dados/avaliacao/M1.1/execucoes.csv` e executar T01 a T12 **na ordem do catálogo**, com o papel indicado em cada tarefa.
3. Para cada tarefa, registrar: concluída (sim/não), função usada, **contorno necessário** (sim/não, e o passo extra), captura de tela do resultado.
4. Comparar cada passo com a página oficial da função. Qualquer passo fora dela é contorno (M1.3).
5. Configurar os questionários e o livro de notas com os valores do oráculo, registrar as respostas fictícias e anotar o valor exibido. Aceitar a diferença até 0,01 ponto.
6. Nos quatro casos de prazo, tentar o envio no horário do oráculo e anotar se foi aceito, aceito com atraso ou bloqueado.
7. Calcular `M1.1 = 1 − Tf/12`, `M1.2 = Cc/20` e `M1.3 = 1 − Tc/12` com a planilha `dados/avaliacao/calculos.csv`.

### G2 – Compatibilidade (M2.1 a M2.4)

**M2.1 e M2.2 (formatos e integridade)**

1. Para cada um dos 7 formatos (F1 a F7), seguir a direção da [Fase 2](../fase-2/metricas.md#m21-intercambialidade-de-formatos-de-dados): importar o arquivo de referência ou exportar e abrir no receptor indicado.
2. Registrar `conclui` (sim/não) e `aceito pelo receptor` (sim/não). Só conta como sucesso se as duas forem "sim".
3. Rodar `scripts/compara_registros.py` entre a referência e o destino. Só espaços em branco são normalizados.
4. Guardar entrada, saída e relatório em `dados/avaliacao/M2.1/` e `M2.2/`.

**M2.3 (serviços web)**

1. Habilitar serviços web e o protocolo REST. Criar o serviço externo com as **6 funções** da Fase 2, o usuário de integração e o token.
2. Chamar cada função com parâmetros conhecidos e salvar a resposta JSON em `dados/avaliacao/M2.3/`.
3. Conta como sucesso: HTTP 200, sem campo `exception` e valores iguais aos da interface. **O token nunca é versionado**; usar variável de ambiente e remover o valor dos arquivos salvos.

**M2.4 (coexistência)**

1. Criar as 3 entidades vizinhas: aplicação estática em outro *virtual host*, banco de outra aplicação no mesmo PostgreSQL e tarefa agendada de outro usuário.
2. Registrar o estado de referência: *hash* do conteúdo da aplicação (E1), *checksum* das tabelas (E2) e horário esperado da execução (E3).
3. Executar as 4 operações (instalação, cron, backup de curso, atualização). Antes, durante e depois de cada uma, repetir as verificações e registrar em `verificacoes.csv`.
4. Uma verificação falha marca a entidade como afetada.

### G3 – Flexibilidade (M3.1 a M3.5)

**M3.1 (ambientes de acesso)**

1. Acessar a instância `m53php83`. Para A4, criar a instância com `MOODLE_HOST` igual ao IP da VM e usar a rede em modo *bridge*, para que o celular alcance o servidor.
2. Em cada ambiente A1 a A4, registrar a linha de `ambientes.csv`, abrir sessão limpa (R2) e executar T02, T03, T04, T05, T06, T08, T09 e T11, com as mesmas contas.
3. A1 é o ambiente de referência. Em A2 a A4, registrar em `dados/avaliacao/M3.1/execucoes.csv` se cada tarefa foi concluída com o mesmo resultado de A1, com captura de tela. Reportar o **menor** valor entre os quatro.

**M3.2 (versões de PHP)**

1. Usar as instâncias `m53php83` e `m53php84`, criadas pelo script com a mesma massa de dados. Abrir a página "Verificação de ambiente" do Moodle nas duas e guardar a captura.
2. Executar T01 a T12 nas duas, usando o mesmo formulário de M1.1, e registrar em `dados/avaliacao/M3.2/execucoes.csv`. Reportar o **menor** valor.

**M3.3, M3.4 e M3.5 (instalação, tempo e preservação)**

1. Para cada uma das **6 execuções** (3 instalações limpas, 3 atualizações 4.5 → 5.3), criar um clone novo da imagem-base e rodar a etapa `codigo 503` do script, que só baixa e extrai o código.
2. Iniciar o registro com `script` (log e tempos). O relógio de M3.4 começa no primeiro comando do procedimento, **com o código já baixado**.
3. Seguir somente a página oficial de instalação ou atualização da 5.3. Cada passo extra e cada passo repetido por falha é anotado.
4. A execução termina no **primeiro login do administrador**. Conta como sucesso se a verificação de ambiente passou sem erro, o login funcionou e não houve passo fora da documentação.
5. Nas 3 atualizações, antes de atualizar: montar a instância `m45` no clone, popular a 4.5 com a massa de dados e rodar as consultas de M3.5. Depois da atualização, repetir as consultas e a exportação de notas e comparar os **40 itens** da lista congelada.
6. Bernardo executa uma das três instalações limpas de M3.3 (R6; ata 02, D4).

### Preparação do julgamento (Fase 4)

1. Calcular cada métrica na planilha de cálculos e aplicar os níveis de pontuação da Fase 2.
2. Aplicar as regras métrica → questão → objetivo, e comparar com as hipóteses H1.1 a H3.4 (confirmada ou refutada).
3. Fazer a **sessão de interpretação** do GQM (Aula 08): em reunião da equipe, registrada em ata, o responsável por cada questão apresenta os dados dela, a equipe responde às questões, compara com as hipóteses, explica as refutadas pelas medidas de contexto e confirma o julgamento. A pauta e o plano de análise (uma tabela por objetivo, um gráfico das notas por questão e a árvore GQM de resultados) estão no [Plano de execução da Fase 4](../fase-4/plano-de-execucao.md#do-dado-ao-julgamento).
4. Escolher, na mesma sessão, a **ação de melhoria (D4)** entre os resultados com nota 1 ou 2, de acordo com o tipo de problema encontrado: protótipo (fluxo), alteração de código (falha técnica objetiva), modelo técnico (documentação frágil) ou processo (problema recorrente). A justificativa cita a métrica e a evidência.

## 4. Piloto e congelamento

Antes da coleta oficial, uma **execução piloto** de instalação limpa calibra o que a Fase 2 deixou em aberto. O piloto é feito por Pedro até 17/11/2026 (issue #66).

| O que o piloto resolve | Resultado esperado |
|---|---|
| Limites de tempo de M3.4 (valores candidatos) | Limites confirmados ou ajustados, **congelados em ata** antes da primeira execução oficial |
| Lista dos 40 itens de M3.5 | Lista final em `dados/avaliacao/M3.5/itens.csv`, conferida por outro integrante (R6) |
| Clareza dos roteiros | Passos ambíguos reescritos neste plano |
| Tempo real por métrica | Cronograma corrigido |

<p class="legenda">Tabela 8. Finalidade do piloto. Fonte: elaboração própria.</p>

O piloto **não** entra no cálculo das métricas. Depois do congelamento, qualquer mudança em critério ou limite é registrada em ata com o motivo.

## 5. Registro e rastreabilidade

```text
dados/avaliacao/
├── ambiente/versoes-<iniciais>.txt  # versões de cada servidor (etapa versoes)
├── M1.1/execucoes.csv               # também usado por M1.3; modelo do formulário de M3.2
├── M1.2/oraculo.csv
├── M2.1/referencia/                 # arquivos de entrada congelados
├── M2.1/ M2.2/ M2.3/ M2.4/
├── M3.1/ambientes.csv  M3.1/execucoes.csv
├── M3.2/ M3.3/ M3.4/ M3.5/
├── calculos.csv                     # valores, notas e julgamento
└── evidencias/                      # capturas, logs, vídeos (nome = ID do caso)
```

- Nome de evidência: `<métrica>_<caso>_<AAAA-MM-DD>_<iniciais>.png`.
- Toda linha de CSV aponta para o arquivo de evidência correspondente (critério F4-C2: ligação direta entre dado bruto e métrica).
- Gravações de tela, quando feitas, mostram só dados fictícios.
- Senhas e tokens gerados pelo script ficam em `/root/moodle-avaliacao/` na VM e **nunca são versionados**.

## 6. Cronograma

A Entrega 2 é em **22/11/2026**, e o cronograma foi comprimido para o período de 16 a 22/11 (ata 02, D2). A coleta ocorre em paralelo, cada integrante no próprio servidor.

| Data | Atividade | Responsável | Issue | Saída |
|---|---|---|---|---|
| 16–17/11 | Script de preparação do servidor e imagem-base | Maykon | #62 | Script na `main`; servidores montados por todos |
| 16–17/11 | Massa de dados e arquivos de referência | João Pedro | #63 | `gera_massa.py`, `usuarios.csv`, `questoes.gift` |
| 16–17/11 | Oráculo de M1.2 e conferência | Bernardo (conferência: Carlos) | #64 | `M1.2/oraculo.csv` conferido |
| 16–17/11 | Script de comparação e referências de M2.1 | Carlos | #65 | `compara_registros.py`, `M2.1/referencia/` |
| 16–17/11 | Piloto de instalação; congelamento de M3.4 e M3.5 | Pedro | #66 | Ata de congelamento; `M3.5/itens.csv` |
| 18/11 | Apresentação do PC2 pela GitPage | Carlos | #61 | Apresentação |
| 18–20/11 | Coleta das 12 métricas (detalhe na Tabela 10) | Responsáveis da Tabela 10 | #67 a #71 | CSVs e evidências em `dados/avaliacao/` |
| 21/11 | Cálculo, níveis de pontuação e julgamento de G1 a G3 | Carlos | #72 | `calculos.csv` |
| 21/11 | Relações entre as características | Bernardo | #73 | Texto das relações |
| 22/11 | Ação de melhoria (D4) | João Pedro e Pedro | #74 | Ação executada e versionada |
| 22/11 | Página de resultados da Fase 4 | João Pedro | #75 | Página na GitPage |
| 22/11 | Artigo: Fase 4, resultados e conclusão; tabela de contribuição | Maykon; Pedro | #76, #77 | 2ª versão do artigo |
| 22/11, até 23h59 | Declaração de IA final, revisão pela rubrica e release E2 | Bernardo | #78 | Release E2 com o PDF |

<p class="legenda">Tabela 9. Cronograma de 16 a 22/11/2026. Fonte: ata 02 e milestone E2.</p>

| Métrica | Responsável | Issue | Coleta | Dependência |
|---|---|---|---|---|
| M1.1 e M1.3 | Bernardo | #67 | 18/11 | #62, #63 |
| M1.2 | Bernardo | #67 | 19–20/11 | #64 conferido |
| M2.1 e M2.2 | Carlos | #68 | 18–20/11 | #63, #65 |
| M2.3 e M2.4 | Maykon | #69 | 18–20/11 | #62 |
| M3.2 | João Pedro | #70 | 18–19/11 | #62, #63; modelo de `M1.1/execucoes.csv` |
| M3.1 | João Pedro | #70 | 19–20/11 | M1.1 concluída (momento definido na Fase 2) |
| M3.3, M3.4 e M3.5 | Pedro (uma execução de M3.3: Bernardo) | #71 | 18–20/11 | #62, #63, #66 |

<p class="legenda">Tabela 10. Coleta por métrica. Fonte: elaboração própria, a partir da ata 02.</p>

As 6 execuções de G3 são o trecho mais demorado e começam em 18/11, logo depois do congelamento. Se a coleta atrasar, a ordem de corte é: reduzir de 3 para 2 repetições de M3.3 **apenas com registro em ata** da perda de poder estatístico, e nunca pular o piloto. Cada coletor lança as horas no `esforco.csv` ao fechar a issue.

## 7. Papéis

| Integrante | Papel na Fase 3 e na Fase 4 |
|---|---|
| Bernardo Broetto Brun | Oráculo de M1.2; coleta de G1; uma execução de M3.3; relações entre as características; declaração de IA e release E2 |
| Carlos Eduardo Deusdara Motta | Conferência do oráculo; script de comparação e coleta de M2.1 e M2.2; cálculo e julgamento; atas |
| João Pedro Sampaio Maciel | Massa de dados; coleta de M3.1 e M3.2; ação de melhoria (com Pedro); página de resultados da Fase 4; rastreabilidade plano ↔ Fase 2 |
| Maykon Junio dos Santos Soares | Script de preparação do servidor e imagem-base; coleta de M2.3 e M2.4; PSM/CID; artigo da Fase 4 |
| Pedro Goncalves Rocha | Piloto e congelamento dos limites de M3.4 e da lista de M3.5; coleta de M3.3 a M3.5; ação de melhoria (com João Pedro); tabela de contribuição |

<p class="legenda">Tabela 11. Papéis, com um responsável por issue. Fonte: ata 02.</p>

## 8. Riscos

| Risco | Efeito | Resposta |
|---|---|---|
| Máquina de algum integrante não roda a VM | Atraso na coleta em paralelo | O integrante coleta no servidor de outro, montado pelo mesmo script, e o desvio é registrado em ata |
| Versões corretivas diferentes entre os servidores | Resultados de servidores diferentes não comparáveis | Cada servidor registra as versões (etapa `versoes`); as métricas de um mesmo objetivo usam a mesma versão corretiva, e diferenças são declaradas nos resultados |
| Instalação falha por erro do avaliador e não do produto | Nota injusta em M3.3 | R5 e R6: repetir com o segundo integrante antes de julgar |
| Instalação 4.5 → 5.3 exige passo não documentado | Sucesso zero em M3.3 para atualização | É resultado válido, não erro: registrar o passo e julgar pelo critério da Fase 2 |
| Dispositivo Android indisponível ou sem acesso à VM | M3.1 incompleto | Usar o celular de outro integrante, com a VM em modo *bridge*; emulador somente se registrado em ata como desvio |
| Preparação atrasa além de 17/11 | Coleta comprimida em menos de três dias | A coleta de cada métrica começa assim que as suas dependências da Tabela 10 estiverem na `main`, sem esperar as demais |
| Horas não lançadas | R/E e custo continuam zerados no PSM/CID | Lançar horas ao fechar cada issue (decisão de gestão da E1) |

<p class="legenda">Tabela 12. Riscos do plano. Fonte: elaboração própria.</p>

## 9. Consistência com a Fase 2

Cada uma das 12 métricas da Fase 2 aparece abaixo com método, recursos principais, evidência, responsável e data de coleta. Nenhuma fórmula, nível de pontuação ou critério de julgamento foi alterado (ata 02, D1).

| Métrica | Método (seção 3) | Recursos principais | Evidência | Responsável | Coleta |
|---|---|---|---|---|---|
| M1.1 | Execução T01–T12 | Instância `m53php83`, contas fictícias | `M1.1/execucoes.csv` | Bernardo | 18/11 |
| M1.2 | Casos do oráculo | Oráculo, questionários e livro de notas | `M1.2/oraculo.csv` | Bernardo | 19–20/11 |
| M1.3 | Mesma execução de M1.1 | Documentação oficial | `M1.1/execucoes.csv` | Bernardo | 18/11 |
| M2.1 | 7 formatos | LibreOffice, Thunderbird, 2ª instância | `M2.1/` | Carlos | 18–20/11 |
| M2.2 | Comparação campo a campo | `compara_registros.py` | `M2.2/` | Carlos | 18–20/11 |
| M2.3 | 6 funções REST | `curl`/Python, token | `M2.3/` | Maykon | 18–20/11 |
| M2.4 | 3 entidades × 4 operações | Apache, PostgreSQL, `cron` | `M2.4/verificacoes.csv` | Maykon | 18–20/11 |
| M3.1 | 8 tarefas × A1–A4 | 4 ambientes de acesso | `M3.1/` | João Pedro | 19–20/11 |
| M3.2 | T01–T12 × PHP 8.3/8.4 | Instâncias `m53php83` e `m53php84` | `M3.2/` | João Pedro | 18–19/11 |
| M3.3 | 6 execuções | Clones da imagem-base, `script` | `M3.3/execucoes.csv` | Pedro (uma: Bernardo) | 18–20/11 |
| M3.4 | Tempos das mesmas 6 | Log com tempos | `M3.4/` | Pedro | 18–20/11 |
| M3.5 | 40 itens antes/depois | Consultas SQL, massa de dados | `M3.5/` | Pedro | 18–20/11 |

<p class="legenda">Tabela 13. Rastreabilidade entre as métricas da Fase 2 e o plano da Fase 3. Fonte: elaboração própria.</p>

