#!/usr/bin/env bash
# Atualização medida 4.5 -> 5.3 de M3.3/M3.4, pelos passos da página oficial "Upgrading" da 5.3
# (docs.moodle.org/503/en/Upgrading) e da página de roteamento ligada no menu "Routing" dela,
# "Configuring the Router", com o código 5.3 já baixado em /var/www/moodle-503. A tentativa 1 usou só o
# bloco FallbackResource da seção Routing de Upgrading, sem DirectoryIndex nem $CFG->routerconfigured.
# A instância 4.5 (m45, porta 8080) foi montada antes, fora da medição, com a massa e os itens de M3.5.
set -uo pipefail
. "$(dirname "$0")/comum.sh"
DIR=/var/www/m45 NOVO=/var/www/moodle-503 PHP=php8.3
. /root/moodle-avaliacao/m45.env   # ADMIN_USUARIO e ADMIN_SENHA, fora do repositório

echo "### INICIO $(date +%s.%N) atualizacao"
executa 1 "Modo de manutenção (Put your site into maintenance mode)" \
  sudo -u www-data $PHP "$DIR/admin/cli/maintenance.php" --enable
troca() {
  mv "$DIR" "$DIR.antigo" && mv "$NOVO" "$DIR" && cp "$DIR.antigo/config.php" "$DIR/config.php" \
    && chown root:www-data "$DIR/config.php" && chmod 0640 "$DIR/config.php"
}
executa 2 "Código novo no lugar do antigo e config.php copiado (Install the new Moodle software)" troca
raiz() {
  sed -i "s#DocumentRoot $DIR\$#DocumentRoot $DIR/public#; s#<Directory $DIR>#<Directory $DIR/public>#" \
    /etc/apache2/sites-available/m45.conf \
  && { grep -q "DirectoryIndex index.php" /etc/apache2/sites-available/m45.conf \
       || sed -i "s#        FallbackResource /r.php#        DirectoryIndex index.php\n        FallbackResource /r.php#" /etc/apache2/sites-available/m45.conf; } \
  && service apache2 reload >/dev/null
}
executa 3 "Raiz web em public/ com DirectoryIndex e FallbackResource (Configuring the Router) e reload" raiz
roteador() { sed -i "/lib\/setup.php/i \$CFG->routerconfigured = true;" "$DIR/config.php"; }
executa 3b "Roteador declarado no config.php (\$CFG->routerconfigured = true)" roteador
executa 4 "Atualização pela linha de comando (admin/cli/upgrade.php)" \
  sudo -u www-data $PHP "$DIR/admin/cli/upgrade.php" --non-interactive
executa 5 "Fim do modo de manutenção" sudo -u www-data $PHP "$DIR/admin/cli/maintenance.php" --disable
executa 6 "Cron apontando para o código novo" sed -i "s#$DIR.antigo#$DIR#; s#/var/www/m45/public/admin#/var/www/m45/admin#" /etc/cron.d/moodle-m45
passo 7 "Verificações do site (admin/cli/checks.php), registradas sem bloquear"
sudo -u www-data $PHP "$DIR/admin/cli/checks.php" 2>/dev/null; true
executa 8 "Primeiro login do administrador" login_admin "$ADMIN_USUARIO" "$ADMIN_SENHA"
echo "### FIM $(date +%s.%N) sucesso"
