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

## Medidas de contexto

A Aula 08 (slide 38) pede que os fatores que influenciam os resultados também sejam definidos como métricas. Os fatores de variação das três *abstraction sheets* viram, por isso, **medidas de contexto**: não recebem nota nem entram no julgamento, mas são registradas em toda coleta. Como cada integrante coleta no próprio servidor (ata 02, D3), elas também mostram se os servidores eram de fato equivalentes. Na Fase 4, são o primeiro lugar onde procurar a explicação de uma hipótese refutada.

| Fator de variação | Medida de contexto | Escala / unidade | Como se registra | Onde | Objetivos |
|---|---|---|---|---|---|
| Versão corretiva do Moodle | Versão exata instalada (por exemplo, 5.3.2) | Nominal | `$release` de `version.php`, ou *Administração do site > Notificações* | `dados/avaliacao/contexto.csv` | G1, G2, G3 |
| Versão do PHP | Versão exata do PHP da instância (por exemplo, 8.3.6) | Nominal | `php -v` no servidor | `dados/avaliacao/contexto.csv` | G1, G2, G3 |
| Recursos da máquina virtual | RAM e vCPU da VM | Razão / GB e núcleos | `free -g` e `nproc` | `dados/avaliacao/contexto.csv` | G2 (M2.4), G3 |
| Experiência do avaliador | Anos de uso de Linux pelo avaliador | Razão / anos | Declarada pelo avaliador antes da coleta | `dados/avaliacao/contexto.csv` | G3 (M3.3, M3.4) |
| Codificação dos arquivos trocados | Codificação de cada arquivo exportado ou importado (UTF-8, ISO-8859-1) | Nominal | `file -bi <arquivo>` | Coluna `codificacao` de `dados/avaliacao/M2.1/execucoes.csv` | G2 (M2.1, M2.2) |
| Fuso horário | Fuso do servidor e do navegador do avaliador | Nominal | `timedatectl` no servidor e configuração do perfil no Moodle | `dados/avaliacao/contexto.csv` | G1 (M1.2, prazos) |

<p class="legenda">Tabela 4. Medidas de contexto dos fatores de variação. Fonte: elaboração própria, a partir das abstraction sheets e da Aula 08.</p>

Ficam só como texto os fatores que o procedimento já controla: a configuração padrão do site e os dados de teste (fixados pelo `gera_massa.py` e pelo oráculo), o programa que abre os arquivos (fixado na coluna `receptor` de M2.1), a velocidade da rede (o código é baixado antes de iniciar o cronômetro de M3.4) e a ordem de leitura da documentação (regra R3 do plano da Fase 3).
