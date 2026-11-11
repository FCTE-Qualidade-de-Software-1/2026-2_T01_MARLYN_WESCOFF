# Plano de avaliação (Fase 3)

!!! warning "Rascunho para revisão da equipe"
    Este plano parte do que a [Fase 2](../fase-2/index.md) já fixou (métricas, níveis de pontuação e critérios de julgamento) e **não altera nenhum deles**. Os itens marcados com *[confirmar]* dependem de decisão da equipe ou do cronograma da disciplina. Remova este aviso depois da reunião de revisão e do registro em ata.

O plano responde a uma pergunta: **o que cada avaliador faz, em que ordem e com quais recursos, para que duas pessoas diferentes obtenham as mesmas medidas?** Ele cobre as 12 métricas (M1.1 a M3.5) dos objetivos G1 (adequação funcional), G2 (compatibilidade) e G3 (flexibilidade), e alimenta as decisões D1 a D4 do [Propósito](../fase-1/proposito.md).

O progresso deste plano, o tempo de execução das tarefas e o esforço da equipe são monitorados na seção [Gestão do Projeto - Métricas PSM/CID](../gestao/index.md).

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

| Item | Especificação |
|---|---|
| Virtualizador | VirtualBox ou equivalente gratuito *[confirmar o que a equipe tem]* |
| Máquina virtual | Ubuntu 24.04 LTS, 2 vCPU, 4 GB de RAM, 40 GB de disco *[confirmar contra os requisitos oficiais da 5.3 em [Produto avaliado](../fase-1/produto.md)]* |
| Servidor web | Apache 2.4, raiz web apontando para a pasta `public/` do Moodle |
| PHP | 8.3 e 8.4, em duas instâncias idênticas, mudando apenas a versão (M3.2) |
| Banco de dados | PostgreSQL 17, com um segundo banco de outra aplicação para M2.4 |
| Moodle | 5.3.x (a versão corretiva exata e o *build* são registrados na primeira execução) e 4.5.x (origem da atualização) |
| Imagem-base | Um *snapshot* da VM sem o Moodle, usado para criar a máquina limpa de cada execução de M3.3 e M3.4 |

<p class="legenda">Tabela 3. Servidor de referência. Fonte: elaboração própria, a partir de [Produto avaliado](../fase-1/produto.md).</p>

### Ambientes de acesso

Os quatro ambientes A1 a A4 são os de [Escopo](../fase-1/escopo.md#ambientes-de-acesso). Na Fase 3, a equipe preenche a coluna de versões: sistema operacional, versão exata do navegador e resolução. Quem não tem o dispositivo A4 (Android) usa o de outro integrante, e o dono do dispositivo é registrado.

### Ferramentas (todas gratuitas)

| Ferramenta | Uso |
|---|---|
| `curl` ou Python 3 | Chamadas REST (M2.3) e script de comparação (M2.2) |
| `scripts/compara_registros.py` | Comparação campo a campo de M2.2. **A criar nesta fase** |
| LibreOffice Calc, Thunderbird | Receptores de CSV/XLSX e de iCal (M2.1) |
| `script` (util-linux) | Log do terminal com carimbos de tempo (M3.3 e M3.4) |
| `sha256sum`, consultas SQL de checksum | Verificação das entidades vizinhas (M2.4) e dos itens de M3.5 |
| Captura de tela do sistema | Evidência de cada caso |

<p class="legenda">Tabela 4. Ferramentas. Fonte: elaboração própria.</p>

### Massa de dados fictícia

| Elemento | Quantidade e regra |
|---|---|
| Estudantes | 30 (`est01` a `est30`), e-mail `estNN@example.invalid` |
| Docente | 1 (`docente01`) |
| Administrador | 1 (`admin-aval`) |
| Cursos | 2: um completo, com as atividades do catálogo T01 a T12, e um vazio, destino da restauração (T12) |
| Atividades | 1 tarefa com prazo, 1 questionário (3 questões de múltipla escolha e 2 numéricas), 1 fórum, 1 arquivo de material |
| Arquivos de referência de importação | `usuarios.csv` (30 linhas), `questoes.gift` (15 questões) |
| Dados de comparação | Arquivos congelados em `dados/avaliacao/M2.1/referencia/` antes da primeira troca |

<p class="legenda">Tabela 5. Massa de dados fictícia. Fonte: elaboração própria.</p>

A massa é gerada por um script versionado (`scripts/gera_massa.py`, **a criar**) e não digitada à mão, para que as três instalações de M3.3 comecem do mesmo conjunto e M3.5 compare "antes" e "depois" sem ruído.

### Oráculo (M1.2)

O oráculo é a planilha `dados/avaliacao/M1.2/oraculo.csv`, com **20 casos**: 10 de pontuação de questionário, 6 de agregação ponderada e 4 de controle de prazo. Cada linha traz as regras configuradas, as entradas, o valor esperado calculado à mão e a tolerância (0,01 ponto).

| caso | tipo | regra configurada | entradas | esperado |
|---|---|---|---|---|
| Q-01 | questionário | 3 questões de 1,0 ponto, nota máxima 3,0 | estudante acerta 2 de 3 | 2,00 |
| A-01 | agregação | P1 com peso 40 e P2 com peso 60 | P1 = 7,5; P2 = 8,0 | 7,80 |
| P-01 | prazo | data limite às 23:59 do dia D | envio às 23:58 de D | aceito |
| P-02 | prazo | data limite às 23:59 do dia D | envio às 00:01 de D+1 | bloqueado |

<p class="legenda">Tabela 6. Exemplos de linhas do oráculo (a lista completa de 20 casos é produzida e conferida por um segundo integrante antes da coleta). Fonte: elaboração própria.</p>

### Perfil do avaliador

Os avaliadores são os integrantes da equipe. Pré-requisitos: usar o terminal Linux básico (para G2 e G3), ler a documentação oficial do Moodle e seguir o roteiro sem interpretá-lo. Quem executa G3 faz antes **uma instalação de treino** descartada. Como a equipe não recruta participantes externos, a coleta **não envolve entrevistas nem pessoas fora do grupo**, e o [Termo de consentimento](../gestao/termo-consentimento.md) só será usado se isso mudar.

## 3. Instruções do avaliador

Cada bloco abaixo é um roteiro. O formato de cada métrica (fórmula, definição, fonte) continua em [Métricas](../fase-2/metricas.md); aqui está **como executar**.

### G1 – Adequação funcional (M1.1, M1.2, M1.3)

1. Subir uma instância 5.3 **limpa**, pelo procedimento oficial, e criar as contas fictícias da massa de dados.
2. Abrir `dados/avaliacao/M1.1/execucoes.csv` e executar T01 a T12 **na ordem do catálogo**, com o papel indicado em cada tarefa.
3. Para cada tarefa, registrar: concluída (sim/não), função usada, **contorno necessário** (sim/não, e o passo extra), captura de tela do resultado.
4. Comparar cada passo com a página oficial da função. Qualquer passo fora dela é contorno (M1.3).
5. Configurar o questionário e o livro de notas com os valores do oráculo, registrar as respostas fictícias e anotar o valor exibido. Aceitar a diferença até 0,01 ponto.
6. Nos quatro casos de prazo, tentar o envio no horário do oráculo e anotar se foi aceito ou bloqueado.
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

1. Em cada ambiente A1 a A4, abrir sessão limpa e executar T02, T03, T04, T05, T06, T08, T09 e T11, com as mesmas contas.
2. Registrar versão do sistema e do navegador, resultado (igual ao de A1 ou diferente) e captura de tela. Reportar o **menor** valor entre os quatro.

**M3.2 (versões de PHP)**

1. Montar duas instâncias idênticas, uma com PHP 8.3 e outra com 8.4. Abrir a página "Verificação de ambiente" do Moodle e guardar a captura.
2. Executar T01 a T12 nas duas, usando o mesmo formulário de M1.1. Reportar o **menor** valor.

**M3.3, M3.4 e M3.5 (instalação, tempo e preservação)**

1. Para cada uma das **6 execuções** (3 instalações limpas, 3 atualizações 4.5 → 5.3), criar uma VM nova a partir da imagem-base.
2. Iniciar o registro com `script` (log e tempos). O relógio de M3.4 começa no primeiro comando do procedimento, **com o código já baixado**.
3. Seguir somente a página oficial de instalação ou atualização da 5.3. Cada passo extra e cada passo repetido por falha é anotado.
4. A execução termina no **primeiro login do administrador**. Conta como sucesso se a verificação de ambiente passou sem erro, o login funcionou e não houve passo fora da documentação.
5. Nas 3 atualizações, antes de atualizar: popular a 4.5 com a massa de dados e rodar as consultas de M3.5. Depois da atualização, repetir as consultas e a exportação de notas e comparar os **40 itens** da lista congelada.
6. Um segundo integrante executa ao menos uma das três repetições de M3.3.

### Preparação do julgamento (Fase 4)

1. Calcular cada métrica na planilha de cálculos e aplicar os níveis de pontuação da Fase 2.
2. Aplicar as regras métrica → questão → objetivo, e comparar com as hipóteses H1.1 a H3.4 (confirmada ou refutada).
3. Escolher a **ação de melhoria (D4)** entre os resultados com nota 1 ou 2, de acordo com o tipo de problema encontrado: protótipo (fluxo), alteração de código (falha técnica objetiva), modelo técnico (documentação frágil) ou processo (problema recorrente). A justificativa cita a métrica e a evidência.

## 4. Piloto e congelamento

Antes da coleta oficial, uma **execução piloto** de instalação limpa calibra o que a Fase 2 deixou em aberto.

| O que o piloto resolve | Resultado esperado |
|---|---|
| Limites de tempo de M3.4 (valores candidatos) | Limites confirmados ou ajustados, **congelados em ata** antes da primeira execução oficial |
| Lista dos 40 itens de M3.5 | Lista final em `dados/avaliacao/M3.5/itens.csv` |
| Clareza dos roteiros | Passos ambíguos reescritos neste plano |
| Tempo real por métrica | Cronograma corrigido |

<p class="legenda">Tabela 7. Finalidade do piloto. Fonte: elaboração própria.</p>

O piloto **não** entra no cálculo das métricas. Depois do congelamento, qualquer mudança em critério ou limite é registrada em ata com o motivo.

## 5. Registro e rastreabilidade

```text
dados/avaliacao/
├── M1.1/execucoes.csv         # também usado por M1.3 e M3.2
├── M1.2/oraculo.csv
├── M2.1/referencia/           # arquivos de entrada congelados
├── M2.1/ M2.2/ M2.3/ M2.4/
├── M3.1/ M3.2/ M3.3/ M3.4/ M3.5/
├── calculos.csv               # valores, notas e julgamento
└── evidencias/                # capturas, logs, vídeos (nome = ID do caso)
```

- Nome de evidência: `<métrica>_<caso>_<AAAA-MM-DD>_<iniciais>.png`.
- Toda linha de CSV aponta para o arquivo de evidência correspondente (critério F4-C2: ligação direta entre dado bruto e métrica).
- Gravações de tela, quando feitas, mostram só dados fictícios.

## 6. Cronograma

A data da Entrega 2 vem do cronograma publicado no Aprender 3 e **não está nos documentos do repositório** *[confirmar]*. Abaixo, uma proposta em semanas a partir de 11/11/2026, que deve ser ajustada à data real.

| Semana | Atividade | Saída |
|---|---|---|
| S1 (11–16/11) | Revisão e aprovação deste plano em ata; criar a imagem-base da VM; escrever `gera_massa.py` e `compara_registros.py` | Plano aprovado; VM e scripts prontos |
| S2 (17–23/11) | Piloto de instalação; congelar limites de M3.4 e lista de M3.5; conferir o oráculo | Atas de congelamento |
| S3 (24–30/11) | Coleta de G1 e G2 (instância limpa 5.3; formatos; REST; vizinhança) | CSVs de M1.x e M2.x |
| S4 (1–7/12) | Coleta de G3 (6 execuções, PHP 8.3/8.4, ambientes A1–A4) | CSVs de M3.x |
| S5 (8–14/12) | Cálculo, julgamento, ação de melhoria e 2ª versão do artigo | Resultados e conclusão |

<p class="legenda">Tabela 8. Proposta de cronograma. Datas a confirmar com o cronograma da disciplina. Fonte: elaboração própria.</p>

As 6 execuções de G3 são o trecho mais demorado e **não podem ficar para a última semana**. Se a E2 for antes do previsto, a ordem de corte é: reduzir de 3 para 2 repetições de M3.3 **apenas com registro em ata** da perda de poder estatístico, e nunca pular o piloto.

## 7. Papéis (proposta)

| Integrante | Papel na Fase 3 e na Fase 4 |
|---|---|
| Bernardo Broetto Brun | Roteiro e coleta de G1; conferência cruzada de G2 |
| Carlos Eduardo Deusdara Motta | Roteiro e coleta de G2; scripts de comparação e vizinhança; atas |
| João Pedro Sampaio Maciel | Massa de dados e oráculo; ambientes A1–A4 e M3.1; rastreabilidade plano ↔ Fase 2 |
| Maykon Junio dos Santos Soares | Imagem-base da VM; PSM/CID; consolidação do artigo e da GitPage |
| Pedro Goncalves Rocha | Roteiro e coleta de G3 (M3.2 a M3.5); congelamento dos limites de M3.4 |

<p class="legenda">Tabela 9. Proposta de papéis. A confirmar na reunião, com um responsável por issue. Fonte: elaboração própria.</p>

## 8. Riscos

| Risco | Efeito | Resposta |
|---|---|---|
| Máquina de algum integrante não roda a VM | Atraso em G3 | Escolher dois integrantes executores da VM; os demais revisam |
| Instalação falha por erro do avaliador e não do produto | Nota injusta em M3.3 | R5 e R6: repetir com o segundo integrante antes de julgar |
| Instalação 4.5 → 5.3 exige passo não documentado | Sucesso zero em M3.3 para atualização | É resultado válido, não erro: registrar o passo e julgar pelo critério da Fase 2 |
| Dispositivo Android indisponível | M3.1 incompleto | Usar emulador somente se registrado em ata como desvio |
| Horas não lançadas | R/E e custo continuam zerados no PSM/CID | Lançar horas ao fechar cada issue (decisão de gestão da E1) |

<p class="legenda">Tabela 10. Riscos do plano. Fonte: elaboração própria.</p>

## 9. Consistência com a Fase 2

Cada uma das 12 métricas da Fase 2 aparece abaixo com método, recursos principais, evidência e semana de coleta. Os responsáveis estão na [seção 7](#7-papeis-proposta).

| Métrica | Método (seção 3) | Recursos principais | Evidência | Semana |
|---|---|---|---|---|
| M1.1 | Execução T01–T12 | Instância 5.3, contas fictícias | `M1.1/execucoes.csv` | S3 |
| M1.2 | Casos do oráculo | Oráculo, questionário e livro de notas | `M1.2/oraculo.csv` | S3 |
| M1.3 | Mesma execução de M1.1 | Documentação oficial | `M1.1/execucoes.csv` | S3 |
| M2.1 | 7 formatos | LibreOffice, Thunderbird, 2ª instância | `M2.1/` | S3 |
| M2.2 | Comparação campo a campo | `compara_registros.py` | `M2.2/` | S3 |
| M2.3 | 6 funções REST | `curl`/Python, token | `M2.3/` | S3 |
| M2.4 | 3 entidades × 4 operações | Apache, PostgreSQL, `cron` | `M2.4/verificacoes.csv` | S3–S4 |
| M3.1 | 8 tarefas × A1–A4 | 4 ambientes de acesso | `M3.1/` | S4 |
| M3.2 | T01–T12 × PHP 8.3/8.4 | 2 instâncias | `M3.2/` | S4 |
| M3.3 | 6 execuções | VM da imagem-base, `script` | `M3.3/execucoes.csv` | S4 |
| M3.4 | Tempos das mesmas 6 | Log com tempos | `M3.4/` | S4 |
| M3.5 | 40 itens antes/depois | Consultas SQL, massa de dados | `M3.5/` | S4 |

<p class="legenda">Tabela 11. Rastreabilidade entre as métricas da Fase 2 e o plano da Fase 3. Fonte: elaboração própria.</p>
