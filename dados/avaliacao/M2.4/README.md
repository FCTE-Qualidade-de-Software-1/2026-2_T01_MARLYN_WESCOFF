# Coleta de M2.4 (coexistência)

Coleta da issue #69, feita em 22/11/2026, seguindo a seção 3 do [plano de avaliação da Fase 3](../../../docs/fase-3/plano-de-avaliacao.md#g2-compatibilidade-q21-a-q24-m21-a-m24). Responsável: Maykon. A execução foi conduzida com o Claude Code, sob a direção do Maykon (ver [Declaração de uso de IA](../../../docs/sobre/uso-de-ia.md)).

**Resultado: M2.4 = Ec / Et = 2 / 3 = 0,67 (nota 2, "com recuperação sem intervenção"). H2.4 refutada.**

## Ambiente

Contêiner Docker Ubuntu 24.04.5 (com `--init`) no WSL2 da máquina do Maykon, montado por `scripts/preparar_servidor.sh` sem alteração. As versões estão em [`versoes-servidor.txt`](versoes-servidor.txt): Apache 2.4.58, PHP 8.3.37, PostgreSQL 17.12, Moodle 5.3.1+ e 4.5.16+ (Build: 20261117). **Desvio do plano:** em vez de uma VM com 2 vCPU e 4 GB, o contêiner usa os recursos do WSL2 (12 vCPU e 13 GB). Com mais recursos, a disputa por memória entre o Moodle e as vizinhas fica *menos* provável, o que deve ser lembrado ao generalizar o resultado.

## Entidades vizinhas e critérios

Criadas por `scripts/coexistencia.sh criar` **antes** da instalação do Moodle. O estado de referência foi gravado por `coexistencia.sh referencia`.

| Entidade | O que é | Verificação (critério fixado antes da coleta) |
|---|---|---|
| E1 | Aplicação estática no virtual host da porta 8090, no mesmo Apache | HTTP 200 e sha256 do conteúdo igual ao da referência |
| E2 | Banco `outraapp` no mesmo PostgreSQL (100 clientes e 500 pedidos) | Checksum md5 das linhas das 2 tabelas igual ao da referência |
| E3 | Tarefa do usuário `outraapp` no mesmo `cron`, a cada minuto | Última execução há no máximo 90 s |

<p class="legenda">Tabela 1. Entidades vizinhas e verificações. Fonte: scripts/coexistencia.sh.</p>

Cada operação teve uma verificação antes, uma depois e, durante, uma amostra a cada 2 s enquanto a operação rodava (`coexistencia.sh durante`). O log de cada operação está em [`logs/`](logs/).

## Resultado por operação

| Operação | Como foi executada | E1 | E2 | E3 |
|---|---|---|---|---|
| Instalação | `preparar_servidor.sh instancia m53php83 503 8.3 8080` | **Afetada:** 1 de 52 amostras sem resposta (HTTP 000) durante; ok antes e depois | ok (52/52) | ok (52/52) |
| Cron | `admin/cli/cron.php` da `m53php83`, com a massa aplicada | ok (88/88) | ok | ok |
| Backup de curso | `admin/cli/backup.php` do curso `AVAL-CAT` (arquivo `.mbz` de 20 KB) | ok (1/1) | ok | ok |
| Atualização 4.5 → 5.3 | [`atualiza_m45_para_m53.sh`](atualiza_m45_para_m53.sh): manutenção, troca do código, raiz em `public/` com `reload` do Apache e `upgrade.php` | ok (29/29) | ok | ok |

<p class="legenda">Tabela 2. Verificações das entidades vizinhas por operação. Fonte: verificacoes.csv.</p>

`Ec` = 2 (E2 e E3, sem impacto em nenhuma verificação), `Et` = 3. E1 voltou a responder sozinha, com o mesmo conteúdo, sem nenhuma intervenção. Por isso a condição `recuperacao_sem_intervencao` foi marcada em `calculos.csv`.

## Interpretação

A falha de E1 tem causa identificada: a etapa `instancia` do script de preparação reinicia o Apache (`service apache2 restart`) depois de criar o virtual host do Moodle. O restart encerra todos os virtual hosts, inclusive o da vizinha, por um instante. Na atualização, a troca da raiz web usou `reload`, que é gracioso, e E1 não foi afetada. O próprio Moodle (instalação pela CLI, cron, backup e `upgrade.php`) não alterou nenhuma vizinha. A interrupção vem do **procedimento** usado para instalar no servidor compartilhado. Para a decisão D2, a recomendação é usar `reload` em vez de `restart` ao publicar um novo virtual host. É uma candidata à ação de melhoria (D4).

A escolha de `reload` na atualização foi feita depois de observar a falha na instalação, porque é o que um administrador usa para mudar a raiz de um virtual host. As operações não foram repetidas: a falha da instalação fica registrada como ocorreu (regra R4).

## Incidente de ambiente (não conta na métrica)

Uma primeira montagem do contêiner, sem `--init`, travou no restart do Apache: sem um processo init, o processo antigo do Apache ficou como zumbi, e o script de init esperou para sempre. Nenhuma operação foi medida nessa montagem. O contêiner foi recriado com `--init` a partir da imagem-base, as vizinhas foram criadas de novo e a coleta começou do zero. Nessa ocasião também foi corrigido um defeito do `coexistencia.sh`: uma vizinha fora do ar derrubava o script em vez de gerar uma linha de falha.
