#!/usr/bin/env bash
# Operação 4 de M2.4: atualização da instância m45php83 (4.5) para a 5.3, pelos passos da página
# oficial "Upgrading" da 5.3 (docs.moodle.org/503/en/Upgrading), com o código já baixado.
# Não é a execução medida de M3.3/M3.4 (Pedro, #71); serve só para observar as vizinhas.
# A mudança da raiz web para public/ usa "reload" (gracioso) do Apache, e não "restart".
set -euo pipefail
NOME=m45php83 DIR=/var/www/m45php83 PHP=php8.3
CLI_ANTIGO=$DIR/admin/cli

echo "==> 1. Modo de manutenção"
sudo -u www-data $PHP $CLI_ANTIGO/maintenance.php --enable

echo "==> 2. Código antigo guardado e código 5.3 extraído no lugar"
mv "$DIR" "$DIR.4.5"
tmp=$(mktemp -d); tar -xzf /opt/moodle-src/moodle-latest-503.tgz -C "$tmp"; mv "$tmp/moodle" "$DIR"; rmdir "$tmp"
cp "$DIR.4.5/config.php" "$DIR/config.php"
chown -R root:www-data "$DIR"; chmod -R u=rwX,g=rX,o= "$DIR"; chmod 0640 "$DIR/config.php"
grep -E '^\$release' "$DIR/public/version.php"

echo "==> 3. Raiz web em public/ (mudança da 5.1) e reload do Apache"
sed -i "s#DocumentRoot $DIR\$#DocumentRoot $DIR/public#; s#<Directory $DIR>#<Directory $DIR/public>#" \
  /etc/apache2/sites-available/$NOME.conf
grep -E "DocumentRoot|<Directory" /etc/apache2/sites-available/$NOME.conf
service apache2 reload

echo "==> 4. Atualização pela CLI"
CLI=$DIR/admin/cli
sudo -u www-data $PHP $CLI/upgrade.php --non-interactive

echo "==> 5. Fim do modo de manutenção"
sudo -u www-data $PHP $CLI/maintenance.php --disable
sed -i "s#$CLI_ANTIGO/cron.php#$CLI/cron.php#" /etc/cron.d/moodle-$NOME
echo "==> Atualização concluída"
