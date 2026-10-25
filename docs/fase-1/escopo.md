# Escopo e profundidade da avaliação

## Objetos de avaliação

| Objeto | Descrição | Característica |
|---|---|---|
| O1. Núcleo do Moodle 5.3 LTS | Instalação padrão, tema Boost, sem plugins de terceiros | Todas |
| O2. Catálogo de tarefas essenciais | 12 tarefas acadêmicas (Tabela 3) executadas com dados fictícios | Adequação funcional |
| O3. Interfaces de troca de dados | 7 formatos de arquivo e 6 funções de serviço web REST (ver [Métricas](../fase-2/metricas.md)) | Compatibilidade |
| O4. Servidor compartilhado | Moodle + uma segunda aplicação web no mesmo Apache e um segundo banco no mesmo PostgreSQL | Compatibilidade |
| O5. Ambientes de acesso e de servidor | 4 combinações de cliente e 2 versões de PHP | Flexibilidade |
| O6. Procedimentos de instalação e atualização | Instalação limpa da 5.3 e atualização de uma cópia 4.5 → 5.3, seguindo a documentação oficial | Flexibilidade |
| O7. Documentação oficial | Requisitos e procedimentos publicados em docs.moodle.org e moodledev.io | Fonte dos resultados esperados |

<p class="legenda">Tabela 1. Objetos de avaliação. Fonte: elaboração própria.</p>

## Profundidade

- **Tipo de avaliação:** externa, predominantemente **caixa-preta**, orientada a tarefas. Observam-se entradas, saídas, estados e mensagens.
- **Código-fonte:** pode ser consultado para explicar um comportamento observado, sem caracterizar inspeção de código.
- **Repetição:** cada caso de teste é executado ao menos uma vez por ambiente; instalações e atualizações são repetidas 3 vezes para medir tempo e retentativas.
- **Nível de rigor:** suficiente para que outro avaliador, com o plano da Fase 3, reproduza as medições na mesma versão.

## O que fica fora e por quê

| Item | Situação | Justificativa |
|---|---|---|
| Capacidade de interação (usabilidade) | Fora | Regra da disciplina |
| Segurança, eficiência, confiabilidade, manutenibilidade, segurança operacional | Fora | Priorização (ver [Seleção e priorização](caracteristicas.md#trade-offs-discutidos)) |
| Escalabilidade e substituibilidade | Fora | Exigem ambiente de carga ou um LMS de origem, que não existem no cenário |
| Plugins de terceiros | Fora | Milhares de plugins heterogêneos; o resultado deixaria de valer para o núcleo |
| Aplicativo móvel Moodle | Fora | Produto distribuído separadamente; o acesso móvel é avaliado pelo navegador |
| Integração LTI, SCORM, autenticação externa (LDAP, SSO) | Fora | Exigem sistemas externos que a equipe não tem; podem entrar na E2 se houver folga |
| Instalação institucional em produção | Fora | O objeto é uma instalação local controlada |
| Desempenho sob carga | Fora | Sem ambiente de carga |

<p class="legenda">Tabela 2. Itens fora do escopo e justificativa de cada corte. Fonte: elaboração própria.</p>

## Recorte operacional: catálogo de tarefas essenciais

| ID | Tarefa | Papel |
|---|---|---|
| T01 | Criar curso e matricular estudantes e docente | Administrador |
| T02 | Publicar material (arquivo) no curso | Docente |
| T03 | Criar tarefa com data de entrega e data limite | Docente |
| T04 | Enviar arquivo para a tarefa dentro do prazo | Estudante |
| T05 | Tentar enviar após a data limite (deve ser bloqueado) | Estudante |
| T06 | Corrigir a tarefa com nota e comentário | Docente |
| T07 | Criar questionário com questões de múltipla escolha e numéricas | Docente |
| T08 | Responder o questionário e receber a nota automática | Estudante |
| T09 | Abrir fórum e responder a uma discussão | Docente e estudante |
| T10 | Configurar categorias e pesos no livro de notas | Docente |
| T11 | Consultar a própria nota final | Estudante |
| T12 | Fazer backup do curso e restaurá-lo como novo curso | Docente/administrador |

<p class="legenda">Tabela 3. Catálogo de tarefas essenciais. Fonte: elaboração própria a partir das funções acadêmicas mais usadas em um LMS.</p>

## Ambientes de acesso

| ID | Sistema | Navegador | Justificativa |
|---|---|---|---|
| A1 | Windows 11 | Google Chrome (versão estável) | Combinação mais comum entre estudantes e docentes |
| A2 | Windows 11 | Mozilla Firefox (versão estável) | Navegador testado oficialmente pelo Moodle |
| A3 | Ubuntu 24.04 | Mozilla Firefox | Laboratórios da universidade usam Linux |
| A4 | Android (smartphone) | Google Chrome | Acesso móvel pelo navegador |

<p class="legenda">Tabela 4. Ambientes de acesso. As versões exatas serão registradas na Fase 3. Fonte: elaboração própria.</p>

## Limites de validade dos resultados

- Os resultados valem para a **versão 5.3.x registrada**, a **configuração de referência** e os **ambientes testados**.
- Não serão generalizados para instalações com plugins, para outros bancos de dados não testados ou para todos os dispositivos.
- A avaliação **não** demonstrará estabilidade de longo prazo, resistência a ataques nem desempenho com muitos usuários simultâneos.
- O teste de atualização usa dados fictícios em pequena quantidade; o tempo medido não representa a atualização de uma base institucional real.
- Se a versão-alvo mudar, dependências, procedimentos e conclusões afetadas serão revisados e o motivo será registrado em ata.
