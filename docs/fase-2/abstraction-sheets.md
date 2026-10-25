# Abstraction sheets

As *abstraction sheets* (Aula 08) registram, antes de definir as métricas, o que a equipe espera medir, o que acredita que vai encontrar (*baseline*) e o que pode alterar os resultados. Elas foram usadas como rascunho das questões e hipóteses e serão usadas de novo na Fase 4, como guia de interpretação.

## G1 – Adequação funcional

| | |
|---|---|
| **Objeto** | Núcleo do Moodle 5.3 LTS |
| **Propósito** | Entender |
| **Foco de qualidade** | Adequação funcional (completude, correção, pertinência) |
| **Ponto de vista** | Coordenação de TI |

| Foco de qualidade (o que medir) | Hipóteses de *baseline* (o que esperamos) |
|---|---|
| Tarefas do catálogo cobertas por funções do núcleo · Casos de teste com resultado igual ao oráculo · Tarefas concluídas sem contorno | O núcleo cobre as 12 tarefas · Nenhuma divergência em notas e prazos · No máximo 1 tarefa exige contorno (a restauração de backup como novo curso tende a exigir passos de configuração não óbvios) |
| **Fatores de variação** | **Impacto nas hipóteses** |
| Versão corretiva 5.3.x · Configurações padrão do site (por exemplo, política de envio após prazo) · Dados de teste mal especificados · Fuso horário do servidor diferente do cliente | Correções entre 5.3.0 e 5.3.x podem mudar o comportamento · Configuração diferente da padrão invalida o oráculo · Fuso horário errado pode causar falso "fora do prazo" em T04/T05 |

<p class="legenda">Tabela 1. Abstraction sheet de G1. Fonte: elaboração própria a partir do modelo da Aula 08.</p>

## G2 – Compatibilidade

| | |
|---|---|
| **Objeto** | Núcleo do Moodle 5.3 LTS e suas interfaces de troca de dados |
| **Propósito** | Entender |
| **Foco de qualidade** | Compatibilidade (interoperabilidade, coexistência) |
| **Ponto de vista** | Coordenação de TI |

| Foco de qualidade (o que medir) | Hipóteses de *baseline* (o que esperamos) |
|---|---|
| Formatos trocados com sucesso · Registros íntegros após a troca · Funções REST respondidas corretamente · Entidades vizinhas não afetadas | Pelo menos 6 de 7 formatos sem problema · 100% dos registros íntegros, exceto possíveis problemas de acentuação em CSV · 6 de 6 funções REST · Nenhuma entidade vizinha afetada |
| **Fatores de variação** | **Impacto nas hipóteses** |
| Codificação de caracteres (UTF-8 × Latin-1) e separador do CSV · Programa usado para abrir o arquivo exportado · Permissões do token de serviço web · Limites de memória do PHP compartilhado | Codificação errada gera falsos negativos de integridade · Planilhas diferentes interpretam números decimais de forma diferente · Token sem capacidade gera erro de permissão, não de interoperabilidade · Limite baixo pode afetar a aplicação vizinha |

<p class="legenda">Tabela 2. Abstraction sheet de G2. Fonte: elaboração própria a partir do modelo da Aula 08.</p>

## G3 – Flexibilidade

| | |
|---|---|
| **Objeto** | Moodle 5.3 LTS e seus procedimentos de instalação e atualização |
| **Propósito** | Entender |
| **Foco de qualidade** | Flexibilidade (adaptabilidade, instalabilidade) |
| **Ponto de vista** | Coordenação de TI |

| Foco de qualidade (o que medir) | Hipóteses de *baseline* (o que esperamos) |
|---|---|
| Tarefas concluídas por ambiente de acesso · Tarefas concluídas por versão de PHP · Instalações/atualizações bem-sucedidas · Tempo e retentativas · Itens preservados após a atualização | Todas as tarefas nos ambientes de desktop; no máximo 1 falha no Android · Nenhuma diferença entre PHP 8.3 e 8.4 · Instalação limpa sem falha; a primeira atualização 4.5 → 5.3 deve falhar por causa da mudança da raiz web para `public/` · Instalação limpa em até 15 min · 100% dos itens preservados |
| **Fatores de variação** | **Impacto nas hipóteses** |
| Experiência do avaliador com Linux e Apache · Velocidade da rede (download do código) · Recursos da máquina virtual · Ordem de leitura da documentação | Avaliador experiente reduz tempo e retentativas, por isso o avaliador e sua experiência serão registrados · Download lento aumenta o tempo, por isso o código é baixado antes de iniciar o cronômetro · Pouca memória pode fazer o instalador falhar |

<p class="legenda">Tabela 3. Abstraction sheet de G3. Fonte: elaboração própria a partir do modelo da Aula 08.</p>
