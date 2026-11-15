# Preparação do servidor de avaliação

Esta página explica como montar o [servidor de referência](plano-de-avaliacao.md#servidor-de-referencia) da Fase 3 com o script versionado [`scripts/preparar_servidor.sh`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/preparar_servidor.sh). Cada integrante que executa a coleta monta o próprio ambiente com o mesmo script, para que todos avaliem a mesma configuração.

## O que o script instala

| Item | Versão | Origem |
|---|---|---|
| Sistema | Ubuntu 24.04 LTS | Imagem oficial do Ubuntu Server |
| Servidor web | Apache 2.4, com PHP-FPM por *virtual host* | Repositório do Ubuntu |
| PHP | 8.3 e 8.4, lado a lado (extensões `pgsql`, `curl`, `zip`, `gd`, `intl`, `mbstring`, `xml`, `soap`, `opcache`) | `ppa:ondrej/php` (o Ubuntu 24.04 só traz o 8.3) |
| Banco de dados | PostgreSQL 17 | Repositório oficial PGDG (o Ubuntu 24.04 só traz o 16) |
| Moodle | 5.3.x e 4.5.x | Pacote oficial `moodle-latest-<ramo>.tgz` de download.moodle.org |

<p class="legenda">Tabela 1. Componentes do servidor de referência. Fonte: elaboração própria, a partir do plano da Fase 3.</p>

## Etapas

O script tem quatro etapas. A separação entre elas existe para não contaminar as medidas de instalabilidade: **M3.3 e M3.4 medem o procedimento oficial de instalação**, então o script nunca instala o Moodle nas máquinas usadas nessas métricas.

| Etapa | Comando | Quando usar |
|---|---|---|
| `base` | `sudo ./preparar_servidor.sh base` | Uma vez, na VM recém-instalada. Gera a imagem-base, sem Moodle |
| `codigo` | `sudo ./preparar_servidor.sh codigo 503` | Em cada clone da imagem-base para M3.3 e M3.4: só baixa e extrai o código em `/var/www/moodle-503`. O relógio começa depois disso |
| `instancia` | `sudo ./preparar_servidor.sh instancia m53php83 503 8.3 8080` | Instâncias prontas para G1, G2 e M3.2: banco, `moodledata`, *virtual host*, instalação pela CLI, `noemailever` (R8) e cron |
| `versoes` | `sudo ./preparar_servidor.sh versoes` | Ao fim da preparação: grava `versoes-servidor.txt` com as versões exatas instaladas |

<p class="legenda">Tabela 2. Etapas do script. Fonte: elaboração própria.</p>

## Passo a passo

1. **Criar a VM.** No VirtualBox (ou equivalente gratuito), criar uma máquina com 2 vCPU, 4 GB de RAM e 40 GB de disco e instalar o Ubuntu Server 24.04 LTS com as opções padrão e o OpenSSH. Em *Rede*, usar NAT com redirecionamento das portas 8080 a 8082 do hospedeiro para as mesmas portas da VM, ou modo *bridge* para acesso pelo celular (A4).
2. **Copiar o script** para a VM (por `git clone` do repositório ou `scp scripts/preparar_servidor.sh`).
3. **Montar a base:** `sudo ./preparar_servidor.sh base`. Leva de 5 a 10 minutos, dependendo da rede.
4. **Tirar o snapshot da imagem-base.** Desligar a VM (`sudo poweroff`) e, no hospedeiro, executar `VBoxManage snapshot "<nome da VM>" take imagem-base`. Cada execução de M3.3 e M3.4 começa de um clone desse snapshot (`VBoxManage clonevm "<nome da VM>" --snapshot imagem-base --name m33-exec1 --register`).
5. **Criar as instâncias de trabalho** na VM principal (não nos clones de M3.3):

    ```bash
    sudo ./preparar_servidor.sh instancia m53php83 503 8.3 8080   # G1, G2 e M3.2 (PHP 8.3)
    sudo ./preparar_servidor.sh instancia m53php84 503 8.4 8081   # M3.2 (PHP 8.4)
    ```

    O Moodle 4.5 só aceita PHP 8.3; para popular a origem da atualização de M3.5, use `instancia m45 405 8.3 8082` em um clone da imagem-base.

6. **Registrar as versões:** `sudo ./preparar_servidor.sh versoes` e copiar o arquivo para `dados/avaliacao/ambiente/versoes-<iniciais>.txt` no repositório.

## Acesso e credenciais

- Cada instância fica em `http://localhost:<porta>`. Para acessar por outro endereço (por exemplo, o IP da VM na rede local), defina `MOODLE_HOST` antes de criar a instância: `sudo MOODLE_HOST=192.168.0.20 ./preparar_servidor.sh instancia ...`.
- O administrador é `admin-aval`, com e-mail `admin-aval@example.invalid` (R7). A senha do administrador e a do banco são geradas aleatoriamente e gravadas em `/root/moodle-avaliacao/<nome>.env`, com permissão só para o root. **Esse arquivo nunca é versionado.**
- O idioma padrão da instalação é inglês, para não depender do download do pacote de idioma. Para português, use `MOODLE_LANG=pt_br`.

## Limites e decisões

- O script assume que as extensões do PHP fazem parte da imagem-base, e não do procedimento medido em M3.3. Se o roteiro de G3 decidir o contrário, rode a etapa `base` sem as extensões e registre a decisão em ata.
- O `max_input_vars = 5000` exigido pelo Moodle é aplicado só pela etapa `instancia`. Nas execuções de M3.3, ele entra apenas se a página oficial de instalação mandar.
- O script foi testado do zero em um contêiner `ubuntu:24.04` em 15/11/2026: etapa `base`, três instâncias (5.3 com PHP 8.3, 5.3 com PHP 8.4 e 4.5 com PHP 8.3) respondendo à página de login, cron executado sem erro e `codigo` extraindo uma cópia limpa. Versões obtidas: Apache 2.4.58, PHP 8.3.36 e 8.4.27, PostgreSQL 17.12, Moodle 5.3+ (Build 20261111) e 4.5.15+ (Build 20261111). A validação final em uma VM limpa, com systemd, ainda deve ser feita e registrada antes do piloto.
