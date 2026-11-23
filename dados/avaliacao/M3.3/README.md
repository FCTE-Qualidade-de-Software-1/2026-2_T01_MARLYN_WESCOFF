# Coleta de M3.3 e M3.4 (instalação e atualização)

Coleta da issue #71, feita em 22/11/2026. Responsável: Pedro (a ata 02 previa que o Bernardo fizesse uma das três instalações, pela regra R6; aqui as seis execuções foram automatizadas, então a conferência independente fica para a revisão do pull request). A execução foi automatizada pelo Claude Code numa máquina compartilhada pela equipe.

**Resultado: M3.3 = 6 / 6 = 1,00 (nota 4). M3.4: mediana de 1,18 min na instalação limpa e 0,90 min na atualização, sem retentativas (nota 4). H3.3 refutada na parte qualitativa: nenhuma atualização falhou por causa de `public/`.**

## Como foi executado

Cada execução roda em um contêiner novo, criado da `imagem-base` do servidor de referência (`scripts/m33/executa.sh`), com o código já baixado e extraído fora do relógio. O procedimento roda dentro do `script` (log e tempos em `logs/<tipo>-<n>.log` e `.timing`) e grava uma marca de tempo por passo. O relógio vai do primeiro passo ao primeiro login do administrador. Um passo que falha é tentado de novo uma vez (retentativa).

- **Instalação limpa** (`scripts/m33/procedimento_instalacao.sh`): passos da página oficial "Installing Moodle" da 5.3 e da página que ela manda ler para o servidor web, "Configuring the Router": banco e usuário, `moodledata`, virtual host com a raiz em `public/`, `DirectoryIndex` e `FallbackResource`, instalação pela CLI, cron, `$CFG->routerconfigured` e login.
- **Atualização 4.5 → 5.3** (`scripts/m33/procedimento_atualizacao.sh`): a 4.5 é montada antes, com a massa completa e os itens de M3.5; depois vêm os passos da página "Upgrading": modo de manutenção, troca do código, raiz em `public/` com o roteador configurado, `upgrade.php`, fim da manutenção e login.

O resultado de cada execução está em [`execucoes.csv`](execucoes.csv), gerado por `scripts/m33/consolida.py`.

## Tentativas descartadas

As tentativas abaixo não contam como execuções do procedimento oficial e ficam guardadas para rastreabilidade:

| Tentativa | O que aconteceu | Causa | Pasta |
|---|---|---|---|
| 1 | Login falhou nas 6 execuções: `/` e `/my/` davam 404 | O procedimento usou só o bloco da página "Apache", sem `DirectoryIndex` nem `$CFG->routerconfigured`, que estão na página "Configuring the Router". **Erro do procedimento**, não do Moodle | `tentativa-1/` |
| 2 | Login falhou nas 5 execuções que chegaram ao fim (a limpa-1 caiu na preparação, ao ler o script enquanto ele era editado) | A verificação do login não seguia o redirecionamento do primeiro acesso (suspeita inicial) | `tentativa-2/` |
| 3 | Login falhou nas 6 execuções | **Erro do instrumento:** com `pipefail`, o `grep -q` encerrava o `curl` e o sucesso virava falha. Comprovado com a senha certa (aceita) e uma errada (recusada) | `tentativa-3/` |

<p class="legenda">Tabela 1. Tentativas descartadas de M3.3. Fonte: logs de cada pasta.</p>

## Ressalvas

- **Validade de M3.4:** o tempo é do procedimento automatizado, não de um administrador seguindo a página. Ele mostra que os passos documentados funcionam em pouco mais de um minuto, mas não mede o tempo de leitura e decisão de uma pessoa.
- **H3.3:** a hipótese esperava uma falha na primeira atualização por causa da nova raiz `public/`. Como o procedimento foi escrito a partir da documentação, que já descreve a mudança, essa falha não tinha como aparecer. O tropeço real foi outro: a documentação do servidor web está dividida, e o bloco da página "Apache" (e da seção Routing de "Upgrading") não traz o `DirectoryIndex` que "Configuring the Router" exige.
- **Roteador com PHP-FPM:** nas seis execuções, `admin/cli/checks.php` acusou "Router configuration (core_router)": um caminho `.php` inexistente não chegava ao `r.php`, porque o PHP-FPM recebe todo `.php`. Não é parte do critério de sucesso de M3.3 (verificação de ambiente, login e passos só da documentação), mas entrou na ação de melhoria (`../D4/`).
