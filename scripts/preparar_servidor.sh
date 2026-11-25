#!/usr/bin/env bash
# Prepara o servidor de referência da avaliação do Moodle 5.3 LTS (plano da Fase 3, seção 2).
#
# Etapas, na ordem de uso:
#   base                         Pacotes do sistema: Apache 2.4, PHP 8.3 e 8.4 (FPM), PostgreSQL 17.
#                                NÃO instala o Moodle. Depois desta etapa, tire o snapshot "imagem-base".
#   codigo  <ramo> [destino]     Só baixa e extrai o pacote oficial do Moodle (ex.: 503, 405).
#                                É o ponto de partida de M3.3 e M3.4 ("código já baixado").
#   instancia <nome> <ramo> <php> <porta>
#                                Instância pronta para G1, G2 e M3.2: código, banco, moodledata,
#                                virtual host, instalação pela CLI, noemailever e cron.
#                                NÃO usar nas execuções medidas de M3.3/M3.4.
#   versoes [arquivo]            Registra as versões instaladas (padrão: versoes-servidor.txt).
#
# Uso: sudo ./preparar_servidor.sh <etapa> [argumentos]
# Variáveis opcionais: MOODLE_HOST (padrão: localhost), MOODLE_LANG (padrão: en).
set -euo pipefail

PHP_VERSOES=(8.3 8.4)
PG_VERSAO=17
SEGREDOS=/root/moodle-avaliacao
FONTES=/opt/moodle-src
MOODLE_HOST=${MOODLE_HOST:-localhost}
MOODLE_LANG=${MOODLE_LANG:-en}
export DEBIAN_FRONTEND=noninteractive

log() { printf '\n==> %s\n' "$*"; }
erro() { printf 'erro: %s\n' "$*" >&2; exit 1; }

exige_root() { [[ $EUID -eq 0 ]] || erro "execute com sudo"; }

exige_ubuntu_2404() {
  . /etc/os-release
  [[ ${ID:-} == ubuntu && ${VERSION_ID:-} == 24.04 ]] \
    || erro "o servidor de referência é Ubuntu 24.04 (encontrado: ${PRETTY_NAME:-desconhecido})"
}

# 'service' funciona com systemd (VM) e sem ele (contêiner de teste).
reinicia() { service "$1" restart >/dev/null; }
# Ação de melhoria D4 (#74): numa instância nova, o Apache é recarregado (reload, gracioso), e não
# reiniciado. O restart derrubava por um instante os outros virtual hosts do servidor (M2.4, E1).
recarrega() { service "$1" reload >/dev/null; }

# Lê uma quantidade fixa de bytes: 'tr </dev/urandom | head' morre com SIGPIPE sob pipefail.
senha_aleatoria() { local s; s=$(head -c 18 /dev/urandom | base64); echo "${s//[^A-Za-z0-9]/x}"; }

# A partir da 5.1 o version.php fica em public/.
arquivo_versao() { local d=$1; [[ -f $d/public/version.php ]] && echo "$d/public/version.php" || echo "$d/version.php"; }

etapa_base() {
  exige_root
  exige_ubuntu_2404

  log "Pacotes básicos"
  apt-get update -q
  apt-get install -yq ca-certificates curl gnupg lsb-release software-properties-common \
    apache2 postgresql-common unzip util-linux cron locales

  log "Repositório do PHP 8.4 (ppa:ondrej/php); o Ubuntu 24.04 só traz o 8.3"
  add-apt-repository -y ppa:ondrej/php

  log "Repositório oficial do PostgreSQL (PGDG); o Ubuntu 24.04 só traz o 16"
  /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y

  apt-get update -q
  local pacotes=("postgresql-${PG_VERSAO}")
  for v in "${PHP_VERSOES[@]}"; do
    # Extensões exigidas ou recomendadas pela verificação de ambiente do Moodle.
    pacotes+=("php${v}-fpm" "php${v}-cli" "php${v}-pgsql" "php${v}-curl" "php${v}-zip"
              "php${v}-gd" "php${v}-intl" "php${v}-mbstring" "php${v}-xml" "php${v}-soap"
              "php${v}-opcache")
  done
  log "PostgreSQL ${PG_VERSAO} e PHP ${PHP_VERSOES[*]}"
  apt-get install -yq "${pacotes[@]}"

  log "Apache com PHP-FPM por virtual host (cada instância escolhe a versão do PHP)"
  a2enmod -q proxy_fcgi setenvif rewrite headers >/dev/null
  a2dissite -q 000-default >/dev/null || true

  locale-gen pt_BR.UTF-8 en_US.UTF-8 >/dev/null
  install -d -m 0700 "$SEGREDOS"
  install -d -m 0755 "$FONTES"

  pg_ctlcluster "$PG_VERSAO" main start 2>/dev/null || reinicia postgresql
  for v in "${PHP_VERSOES[@]}"; do reinicia "php${v}-fpm"; done
  reinicia apache2
  reinicia cron

  log "Base pronta. Desligue a VM e tire o snapshot 'imagem-base' (ver instruções na GitPage)."
}

valida_ramo() { [[ $1 =~ ^[0-9]{3}$ ]] || erro "ramo inválido '$1' (use 503 para 5.3, 405 para 4.5)"; }

etapa_codigo() {
  exige_root
  local ramo=${1:?informe o ramo, ex.: 503}
  valida_ramo "$ramo"
  local destino=${2:-/var/www/moodle-${ramo}}
  local pacote="$FONTES/moodle-latest-${ramo}.tgz"
  local url="https://download.moodle.org/download.php/direct/stable${ramo}/moodle-latest-${ramo}.tgz"

  [[ -e $destino ]] && erro "$destino já existe; remova antes ou escolha outro destino"

  if [[ ! -s $pacote ]]; then
    log "Baixando $url"
    curl -fL --retry 3 -o "$pacote.parcial" "$url"
    mv "$pacote.parcial" "$pacote"
  fi
  sha256sum "$pacote" | tee "$pacote.sha256"

  log "Extraindo em $destino"
  local tmp; tmp=$(mktemp -d)
  tar -xzf "$pacote" -C "$tmp"
  mv "$tmp/moodle" "$destino"
  rmdir "$tmp"
  chown -R root:www-data "$destino"
  chmod -R u=rwX,g=rX,o= "$destino"

  grep -E "^\\\$release" "$(arquivo_versao "$destino")" || true
}

etapa_instancia() {
  exige_root
  local nome=${1:?informe o nome, ex.: m53php83} ramo=${2:?informe o ramo} php=${3:?informe o PHP} porta=${4:?informe a porta}
  [[ $nome =~ ^[a-z][a-z0-9_]{1,30}$ ]] || erro "nome inválido '$nome' (minúsculas, dígitos e _)"
  valida_ramo "$ramo"
  [[ " ${PHP_VERSOES[*]} " == *" $php "* ]] || erro "PHP $php não faz parte do servidor de referência"
  [[ $porta =~ ^[0-9]+$ && $porta -ge 1024 ]] || erro "porta inválida '$porta'"
  if [[ $ramo == 405 && $php != 8.3 ]]; then erro "o Moodle 4.5 não suporta PHP $php; use 8.3"; fi
  command -v "php$php" >/dev/null || erro "rode a etapa 'base' antes"

  local dir=/var/www/$nome dados=/var/moodledata/$nome
  etapa_codigo "$ramo" "$dir"

  # A partir da 5.1 a raiz web é a pasta public/ e os scripts da CLI ficam dentro dela.
  local raiz_web=$dir
  [[ -d $dir/public ]] && raiz_web=$dir/public
  local cli=$raiz_web/admin/cli
  [[ -f $cli/install.php ]] || cli=$dir/admin/cli
  [[ -f $cli/install.php ]] || erro "admin/cli/install.php não encontrado em $dir"

  log "moodledata em $dados"
  install -d -o www-data -g www-data -m 0770 "$dados"

  log "Banco PostgreSQL '$nome'"
  local senha_db senha_admin
  senha_db=$(senha_aleatoria)
  senha_admin=$(senha_aleatoria)
  sudo -u postgres psql -q -v ON_ERROR_STOP=1 \
    -c "CREATE ROLE \"$nome\" LOGIN PASSWORD '$senha_db';" \
    -c "CREATE DATABASE \"$nome\" OWNER \"$nome\" ENCODING 'UTF8' TEMPLATE template0;"

  log "PHP $php: max_input_vars = 5000 (requisito do Moodle)"
  for sapi in fpm cli; do
    echo "max_input_vars = 5000" > "/etc/php/$php/$sapi/conf.d/99-moodle.ini"
  done
  recarrega "php${php}-fpm"

  log "Virtual host na porta $porta, raiz $raiz_web"
  grep -qx "Listen $porta" /etc/apache2/ports.conf || echo "Listen $porta" >> /etc/apache2/ports.conf
  cat > "/etc/apache2/sites-available/$nome.conf" <<EOF
<VirtualHost *:$porta>
    DocumentRoot $raiz_web
    <Directory $raiz_web>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
        DirectoryIndex index.php
        FallbackResource /r.php
    </Directory>
    # Ação de melhoria D4 (#74): só arquivos .php que existem vão para o PHP-FPM; os outros caem no
    # FallbackResource (roteador). Sem o <If>, um caminho .php inexistente dava 404 do FPM e
    # admin/cli/checks.php acusava "A routed page with path ending in .php did not respond correctly".
    <FilesMatch \.php$>
        <If "-f %{REQUEST_FILENAME}">
            SetHandler "proxy:unix:/run/php/php${php}-fpm.sock|fcgi://localhost"
        </If>
    </FilesMatch>
    ErrorLog \${APACHE_LOG_DIR}/$nome-error.log
    CustomLog \${APACHE_LOG_DIR}/$nome-access.log combined
</VirtualHost>
EOF
  a2ensite -q "$nome" >/dev/null
  recarrega apache2

  log "Instalação pela CLI (contas fictícias, domínio example.invalid)"
  chown www-data "$dir"   # install.php grava o config.php na raiz do código
  sudo -u www-data "php$php" "$cli/install.php" --non-interactive --agree-license \
    --lang="$MOODLE_LANG" --wwwroot="http://$MOODLE_HOST:$porta" --dataroot="$dados" \
    --dbtype=pgsql --dbhost=localhost --dbname="$nome" --dbuser="$nome" --dbpass="$senha_db" \
    --fullname="Moodle avaliação $nome" --shortname="$nome" \
    --adminuser=admin-aval --adminpass="$senha_admin" --adminemail=admin-aval@example.invalid \
    --supportemail=suporte@example.invalid
  chown root "$dir"

  local config=$dir/config.php
  [[ -f $config ]] || erro "config.php não foi criado"
  log "R8: noemailever no config.php"
  sed -i "/lib\/setup.php/i \$CFG->noemailever = true;" "$config"
  # Ação de melhoria D4 (#74): roteador configurado como na página oficial "Configuring the Router"
  # (DirectoryIndex no virtual host, acima, e esta declaração). Sem isso, "/" e "/my/" davam 404 e
  # admin/cli/checks.php acusava "Router configuration (core_router)".
  [[ -d $dir/public ]] && sed -i "/lib\/setup.php/i \$CFG->routerconfigured = true;" "$config"
  chown root:www-data "$config"
  chmod 0640 "$config"

  log "Cron do Moodle a cada minuto"
  echo "* * * * * www-data /usr/bin/php$php $cli/cron.php >/dev/null 2>&1" > "/etc/cron.d/moodle-$nome"

  umask 077
  cat > "$SEGREDOS/$nome.env" <<EOF
# Credenciais locais da instância $nome. Nunca versionar.
URL=http://$MOODLE_HOST:$porta
ADMIN_USUARIO=admin-aval
ADMIN_SENHA=$senha_admin
DB_NOME=$nome
DB_SENHA=$senha_db
EOF
  log "Instância pronta em http://$MOODLE_HOST:$porta (credenciais em $SEGREDOS/$nome.env)"
}

etapa_versoes() {
  local saida=${1:-versoes-servidor.txt}
  {
    echo "# Versões do servidor de referência - $(date -Iseconds) - $(hostname)"
    . /etc/os-release; echo "Sistema: $PRETTY_NAME ($(uname -r))"
    echo "Apache: $(apache2 -v 2>/dev/null | head -1 || echo 'não instalado')"
    for v in "${PHP_VERSOES[@]}"; do
      echo "PHP $v: $("php$v" -r 'echo PHP_VERSION;' 2>/dev/null || echo 'não instalado')"
    done
    echo "PostgreSQL: $(/usr/lib/postgresql/$PG_VERSAO/bin/postgres --version 2>/dev/null || echo 'não instalado')"
    for d in /var/www/*/; do
      local vp; vp=$(arquivo_versao "${d%/}")
      [[ -f $vp ]] || continue
      echo "Moodle $(basename "$d"): $(grep -E '^\$release' "$vp" | cut -d"'" -f2)"
    done
  } | tee "$saida"
}

case ${1:-} in
  base)      etapa_base ;;
  codigo)    shift; etapa_codigo "$@" ;;
  instancia) shift; etapa_instancia "$@" ;;
  versoes)   shift; etapa_versoes "$@" ;;
  *) sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
