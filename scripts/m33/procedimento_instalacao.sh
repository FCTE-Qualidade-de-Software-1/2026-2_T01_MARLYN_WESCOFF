#!/usr/bin/env bash
# Instalação limpa medida de M3.3/M3.4, pelos passos da página oficial "Installing Moodle" da 5.3
# (docs.moodle.org/503/en/Installing_Moodle) e da página que ela manda ler para o servidor web,
# "Configuring the Router" (docs.moodle.org/503/en/Configuring_the_Router), com o código já baixado.
# A tentativa 1 (dados/avaliacao/M3.3/tentativa-1/) usou só o bloco da página "Apache", sem
# DirectoryIndex nem $CFG->routerconfigured, e não conta como execução da documentação.
# O relógio começa no passo 1 e termina no primeiro login do administrador (passo 7).
set -uo pipefail
. "$(dirname "$0")/comum.sh"
DIR=/var/www/moodle DADOS=/var/moodledata/moodle PHP=php8.3
SENHA_DB=$(head -c 18 /dev/urandom | base64 | tr -dc A-Za-z0-9)
SENHA_ADMIN="Adm$(head -c 18 /dev/urandom | base64 | tr -dc A-Za-z0-9)#1"
( umask 077; echo "ADMIN_SENHA=$SENHA_ADMIN" > /root/m33-admin.env )   # só no contêiner, nunca versionado

echo "### INICIO $(date +%s.%N) instalacao"
executa 1 "Banco vazio e usuário no PostgreSQL (Create an empty database)" \
  sudo -u postgres psql -q -v ON_ERROR_STOP=1 -c "CREATE ROLE moodleuser LOGIN PASSWORD '$SENHA_DB';" \
    -c "CREATE DATABASE moodle OWNER moodleuser ENCODING 'UTF8' TEMPLATE template0;"
executa 2 "Diretório de dados fora da raiz web (Create the moodledata directory)" \
  install -d -o www-data -g www-data -m 0770 "$DADOS"
config_web() {
  echo "max_input_vars = 5000" > /etc/php/8.3/fpm/conf.d/99-moodle.ini
  echo "max_input_vars = 5000" > /etc/php/8.3/cli/conf.d/99-moodle.ini
  service php8.3-fpm reload >/dev/null
  grep -qx "Listen $PORTA" /etc/apache2/ports.conf || echo "Listen $PORTA" >> /etc/apache2/ports.conf
  cat > /etc/apache2/sites-available/moodle.conf <<VH
<VirtualHost *:$PORTA>
    DocumentRoot $DIR/public
    <Directory $DIR/public>
        AllowOverride None
        Require all granted
        DirectoryIndex index.php
        FallbackResource /r.php
    </Directory>
    <FilesMatch \.php$>
        SetHandler "proxy:unix:/run/php/php8.3-fpm.sock|fcgi://localhost"
    </FilesMatch>
</VirtualHost>
VH
  a2ensite -q moodle >/dev/null && service apache2 reload >/dev/null
}
executa 3 "Servidor web pela página Configuring the Router (Method A): raiz public/, DirectoryIndex e FallbackResource" config_web
instala() {
  chown www-data "$DIR"
  sudo -u www-data $PHP "$DIR/admin/cli/install.php" --non-interactive --agree-license --lang=en \
    --wwwroot="http://localhost:$PORTA" --dataroot="$DADOS" --dbtype=pgsql --dbhost=localhost \
    --dbname=moodle --dbuser=moodleuser --dbpass="$SENHA_DB" --fullname="Moodle M3.3" --shortname=m33 \
    --adminuser=admin --adminpass="$SENHA_ADMIN" --adminemail=admin@example.invalid
  local r=$?; chown root "$DIR"; return $r
}
executa 4 "Instalação pela linha de comando (admin/cli/install.php), com a verificação de ambiente" instala
executa 5 "Cron a cada minuto (Set up cron)" \
  bash -c "echo '* * * * * www-data /usr/bin/$PHP $DIR/admin/cli/cron.php >/dev/null 2>&1' > /etc/cron.d/moodle"
roteador() { # Configuring the Router: depois de configurar o servidor, declarar o roteador configurado
  sed -i "/lib\/setup.php/i \$CFG->routerconfigured = true;" "$DIR/config.php"
}
executa 6 "Roteador declarado no config.php (\$CFG->routerconfigured = true, Configuring the Router)" roteador
passo 6b "Verificações do site (admin/cli/checks.php, Test D de Configuring the Router), registradas sem bloquear"
sudo -u www-data $PHP "$DIR/admin/cli/checks.php"; true
executa 7 "Primeiro login do administrador" login_admin admin "$SENHA_ADMIN"
echo "### FIM $(date +%s.%N) sucesso"
