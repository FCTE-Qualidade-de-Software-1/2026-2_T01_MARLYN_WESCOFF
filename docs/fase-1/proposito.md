# Propósito da avaliação e uso pretendido

## Por que avaliar

O Moodle 5.3 foi lançado em 05/10/2026 como versão de suporte estendido (LTS) e exige mudanças de infraestrutura em relação às versões anteriores: PHP 8.3 ou superior de 64 bits, extensão `sodium`, PostgreSQL 17 ou superior (ou MariaDB 11.4 / MySQL 8.4) e atualização a partir do Moodle 4.4 ou posterior [(Moodle, 2026)](../sobre/referencias.md). Uma instituição que mantém um Moodle precisa, portanto, decidir **se e como** migrar para a nova LTS.

Essa decisão envolve três riscos concretos:

1. **Risco acadêmico:** após a mudança, alguma tarefa essencial de ensino (entregar atividade, aplicar questionário, lançar nota) deixar de funcionar ou produzir resultados errados.
2. **Risco de integração:** o Moodle deixar de trocar dados corretamente com os sistemas vizinhos (cadastro de usuários, exportação de notas para a secretaria, serviços web consumidos por outros sistemas) ou interferir em outros serviços hospedados no mesmo servidor.
3. **Risco operacional:** a instalação ou a atualização falhar, exigir retrabalho, perder dados, ou o sistema não funcionar nos navegadores e dispositivos usados por estudantes e docentes.

A avaliação produz evidências objetivas sobre esses três riscos. Há também um propósito acadêmico: aplicar o processo de avaliação de produto da série SQuaRE na disciplina FGA0315.

## Cenário de aplicação

O cenário é o de uma **instituição pública de ensino superior** que já usa o Moodle como ambiente virtual de aprendizagem e analisa a atualização para a versão 5.3 LTS. O cenário é inspirado no uso do Moodle em universidades brasileiras, inclusive na UnB, mas **nenhuma instituição solicitou formalmente esta avaliação**. Os resultados valem para a instalação de referência descrita em [Produto avaliado](produto.md).

## Decisões apoiadas

| ID | Decisão a apoiar | Quem decide | Pergunta que a avaliação responde | Característica |
|---|---|---|---|---|
| D1 | Adotar o Moodle 5.3 LTS usando apenas o núcleo, ou prever plugins/customizações para cobrir tarefas essenciais | Coordenação de TI, com a gestão acadêmica | O núcleo cobre e executa corretamente as tarefas acadêmicas essenciais? | Adequação funcional |
| D2 | Manter as integrações atuais (CSV, serviços web) ou planejar adaptações e testes de regressão antes da migração | Equipe de TI e integradores | O Moodle troca dados com os sistemas vizinhos sem perdas e sem interferir em serviços que compartilham o servidor? | Compatibilidade |
| D3 | Seguir o procedimento oficial de instalação e atualização, ou preparar procedimento próprio e janela de manutenção maior; definir os ambientes de acesso suportados | Administradores de TI | A instalação e a atualização concluem com êxito e os fluxos funcionam nos ambientes de acesso previstos? | Flexibilidade |
| D4 | Escolher a ação de melhoria obrigatória da Entrega 2 | Equipe avaliadora, com a docente | Onde estão as falhas de maior impacto? | Todas |

<p class="legenda">Tabela 1. Decisões apoiadas pela avaliação. Fonte: elaboração própria.</p>

## Como os resultados serão usados

Cada objetivo de medição termina em um julgamento de três níveis (ver [Níveis de pontuação e julgamento](../fase-2/niveis-e-julgamento.md)), que corresponde diretamente a uma ação para o decisor:

| Julgamento do objetivo | Ação recomendada ao decisor |
|---|---|
| **Atende** | Prosseguir com a adoção/atualização para a característica avaliada |
| **Atende com ressalvas** | Prosseguir, mas com ações de mitigação listadas no relatório (teste de regressão, ajuste de procedimento, comunicação aos usuários) |
| **Não atende** | Não prosseguir sem correção ou contorno documentado; priorizar a falha como ação de melhoria (D4) |

<p class="legenda">Tabela 2. Relação entre o julgamento e o uso pretendido. Fonte: elaboração própria.</p>

O relatório final será entregue à docente (requisitante acadêmica) e publicado nesta GitPage. As falhas reproduzíveis serão descritas de forma que possam ser relatadas à comunidade mantenedora do Moodle.
