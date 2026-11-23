# Ação de melhoria (D4)

Issue #74. A ação foi executada em 22/11/2026 na entrega técnica da avaliação, o script [`scripts/preparar_servidor.sh`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/preparar_servidor.sh), que a Coordenação de TI usaria para montar o servidor. Problema escolhido, prioridade, ação e verificação estão abaixo; o antes e o depois foram medidos com os mesmos instrumentos da coleta.

## Problema e prioridade

Dois resultados da coleta apontaram para a mesma causa, o procedimento de publicação do Moodle num Apache compartilhado:

1. **M2.4 (coexistência), nota 2:** durante a instalação, a aplicação vizinha (E1) ficou sem resposta em 1 de 52 amostras, porque o script reiniciava o Apache (`restart`) para publicar o novo virtual host.
2. **Roteador mal configurado:** com o bloco da página "Apache" da documentação, a raiz do site, `/my/` e `/course/` davam 404, e `admin/cli/checks.php` acusava "Router configuration (core_router)". A configuração correta está só na página "Configuring the Router".

A prioridade vem de três fatores: a nota 2 foi a menor nota de G2 atribuída ao produto em operação; o problema atinge todo servidor montado pelo script (os de todos os integrantes); e a correção é objetiva, pequena e verificável com os instrumentos que já existiam. Pelo tipo de problema (falha técnica objetiva num procedimento), a ação é uma alteração de código no procedimento.

## Ação

Três mudanças em `scripts/preparar_servidor.sh`:

- o virtual host novo é publicado com `reload` (gracioso) do Apache e do PHP-FPM, e não com `restart`;
- `DirectoryIndex index.php` no virtual host e `$CFG->routerconfigured = true` no `config.php`, como na página "Configuring the Router";
- só arquivos `.php` que existem vão para o PHP-FPM (`<If "-f %{REQUEST_FILENAME}">`); os outros caem no `FallbackResource`.

## Verificação: antes e depois

| Medida | Antes (script original) | Depois (script com a ação) |
|---|---|---|
| E1 durante a instalação (M2.4) | 1 de 52 amostras sem resposta: afetada | 44 de 44 amostras ok: não afetada |
| M2.4 na operação de instalação | 2/3 entidades sem impacto | 3/3 entidades sem impacto |
| `/`, `/my/`, `/course/` | HTTP 404 | HTTP 303 para o login |
| Rota de teste `/lib/exampleshimroute2.php` | HTTP 404 | HTTP 302, o esperado pela verificação |
| `admin/cli/checks.php`, core_router | ERROR | sem erro |

<p class="legenda">Tabela 1. Medidas antes e depois da ação de melhoria. Fonte: <a href="https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/M2.4/verificacoes.csv">M2.4/verificacoes.csv</a> e <a href="https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/dados/avaliacao/D4/">dados/avaliacao/D4/</a>.</p>

O "depois" foi medido num servidor novo, criado da mesma imagem-base, com as três vizinhas criadas antes da instalação e verificadas antes, durante (a cada 2 s) e depois, como na coleta de M2.4. A execução foi automatizada pelo Claude Code numa máquina compartilhada pela equipe.

Limites: a medida depois cobre a operação de instalação, onde o problema apareceu; as outras três operações de M2.4 (cron, backup e atualização) já não afetavam as vizinhas. A M2.4 da avaliação continua 0,67, porque é o resultado do procedimento avaliado; a ação mostra que o problema tem correção simples, que vira recomendação para a decisão D2.


A mudança está incorporada ao repositório (entrega técnica) e é usada por quem monta um servidor novo pelo [procedimento de preparação](../fase-3/preparacao-do-servidor.md).
