# Coleta de M2.3 (serviços web REST)

Coleta da issue #69, feita em 22/11/2026, seguindo a seção 3 do [plano de avaliação da Fase 3](../../../docs/fase-3/plano-de-avaliacao.md#g2-compatibilidade-q21-a-q24-m21-a-m24). Responsável: Maykon, que fez a execução com scripts versionados.

**Resultado: M2.3 = Ws / Wt = 6 / 6 = 1,00 (nota 4). H2.3 confirmada.**

## Ambiente

| Item | Valor |
|---|---|
| Instância | `m53php83`, Moodle **5.3.1+ (Build: 20261117)**, PHP 8.3.37, PostgreSQL 17.12, Apache 2.4.58 |
| Servidor | Contêiner Docker Ubuntu 24.04.5 (com `--init`) no WSL2 da máquina do Maykon, montado por `scripts/preparar_servidor.sh` (etapas `base` e `instancia`), sem alteração no script |
| Desvio do plano | O plano prevê VM com 2 vCPU e 4 GB; o contêiner usa os recursos do WSL2 (12 vCPU e 13 GB). M2.3 não depende de desempenho |
| Massa | `contas,catalogo` de `scripts/gera_massa.py` (43 itens criados) |
| Cliente | `scripts/cliente_rest.py`, a partir do hospedeiro, em `http://localhost:8080` |

<p class="legenda">Tabela 1. Ambiente da coleta de M2.3. Fonte: versoes-servidor.txt de M2.4 e registro da massa.</p>

## Procedimento

1. `scripts/habilita_rest.php` habilita os serviços web e o protocolo REST e cria o serviço externo `aval_integracao`, com as 6 funções da Fase 2. Cria também o usuário `integracao`, o papel `aval_integracao` (contexto de sistema, só com capacidades de leitura) e o token. O token só existe em variável de ambiente e nunca é gravado: o cliente para se o encontrar em algum arquivo, e uma busca no repositório depois da coleta não o encontrou.
2. `scripts/cliente_rest.py` chama cada função com parâmetros da massa (`est01`, curso `AVAL-CAT`) e salva a resposta em `<n>_<função>.json`.
3. **Critério de sucesso** (plano da Fase 3, fixado antes da coleta): HTTP 200, sem `exception` e valores iguais aos do Moodle. Os valores esperados vêm de `massa.json` e `notas.csv`, que são o que a massa gravou e o que a interface exibe. Cada conferência está na coluna `conferencia` de `resultados.csv`.

## Tentativa 1 e ajuste (regra R5)

A primeira execução ([`tentativa-1/`](tentativa-1/resultados.csv)) deu 4/6. As duas diferenças eram de configuração do cliente, e não do Moodle:

| Função | O que aconteceu | Causa | Ajuste |
|---|---|---|---|
| `core_user_get_users_by_field` | Resposta sem o campo `email` | O papel de integração não tinha `moodle/site:viewuseridentity`, a capacidade que mostra o e-mail de outros usuários | Capacidade incluída em `habilita_rest.php` |
| `mod_assign_get_assignments` | `courses` vazio, com o aviso "User is not enrolled or does not have requested capability" | O usuário de integração não é matriculado no curso. Para esse caso, a função tem o parâmetro `includenotenrolledcourses`, documentado na própria função | Parâmetro `includenotenrolledcourses=1` incluído no cliente |

<p class="legenda">Tabela 2. Diferenças da tentativa 1 e ajustes. Fonte: tentativa-1/resultados.csv.</p>

Os dois ajustes estão na documentação, o que a regra R5 permite, e ficam registrados aqui. A tentativa 2 (arquivos desta pasta) deu 6/6. O comportamento observado é o esperado de uma API com controle de acesso: uma integração com permissões mínimas precisa das capacidades certas, e o Moodle avisou da falta, em vez de devolver dados errados.

## Pendente

- [ ] Capturas de tela da interface (perfil de `est01`, participantes e relatório de notas de `AVAL-CAT`) para `dados/avaliacao/evidencias/`, no padrão `M2.3_<caso>_2026-11-22_MS.png`. A conferência com a interface foi feita contra a massa, e não visualmente.
