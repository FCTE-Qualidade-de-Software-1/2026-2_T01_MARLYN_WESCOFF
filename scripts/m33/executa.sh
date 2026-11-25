#!/usr/bin/env bash
# Uma execução de M3.3/M3.4 (e M3.5, nas atualizações) em um contêiner novo, criado da imagem-base
# do servidor de referência (issue #71). Roda no hospedeiro, com Docker.
#
# Uso: scripts/m33/executa.sh <limpa|atualizacao> <n> <pacotes>
#   <pacotes>: pasta com moodle-latest-503.tgz e moodle-latest-405.tgz (código já baixado, fora do relógio)
# Saída: dados/avaliacao/M3.3/logs/<tipo>-<n>.log e .timing; nas atualizações, também
#        dados/avaliacao/M3.5/<n>-antes.csv e <n>-depois.csv.
set -euo pipefail
tipo=${1:?limpa ou atualizacao} n=${2:?número} pacotes=${3:?pasta dos pacotes}
RAIZ=$(cd "$(dirname "$0")/../.." && pwd)
LOGS=$RAIZ/dados/avaliacao/M3.3/logs; M35=$RAIZ/dados/avaliacao/M3.5
c=m33-$tipo-$n
mkdir -p "$LOGS" "$M35"

docker rm -f "$c" >/dev/null 2>&1 || true
docker run -d --init --name "$c" -v "$RAIZ:/opt/repo:ro" moodle-aval:imagem-base sleep infinity >/dev/null
docker exec "$c" bash -c 'pg_ctlcluster 17 main start; for s in php8.3-fpm php8.4-fpm apache2 cron; do service $s start >/dev/null 2>&1; done'
docker cp "$pacotes/moodle-latest-503.tgz" "$c:/opt/moodle-src/"
docker cp "$pacotes/moodle-latest-405.tgz" "$c:/opt/moodle-src/"
P=/opt/repo/scripts/preparar_servidor.sh

if [[ $tipo == limpa ]]; then
  docker exec "$c" $P codigo 503 /var/www/moodle >/dev/null
  proc=procedimento_instalacao.sh
else
  echo "-- preparação da 4.5 (fora da medição)"
  docker exec "$c" $P instancia m45 405 8.3 8080 > "$LOGS/$tipo-$n-preparo.log" 2>&1
  docker exec "$c" bash -c "cd /opt/repo && python3 scripts/gera_massa.py aplicar --moodle /var/www/m45 --php php8.3 --partes contas,catalogo,oraculo --registro /root/massa.json" >> "$LOGS/$tipo-$n-preparo.log" 2>&1
  docker exec "$c" sudo -u www-data php8.3 /opt/repo/scripts/m35_itens.php --moodle=/var/www/m45 --recalcular > "$M35/$n-antes.csv"
  docker exec "$c" $P codigo 503 /var/www/moodle-503 >/dev/null
  proc=procedimento_atualizacao.sh
fi

echo "-- execução medida: $tipo $n"
docker exec "$c" script -q -T /root/exec.timing -c "/opt/repo/scripts/m33/$proc" /root/exec.log >/dev/null || true
docker cp "$c:/root/exec.log" "$LOGS/$tipo-$n.log"
docker cp "$c:/root/exec.timing" "$LOGS/$tipo-$n.timing"
if [[ $tipo == atualizacao ]]; then
  docker exec "$c" sudo -u www-data php8.3 /opt/repo/scripts/m35_itens.php --moodle=/var/www/m45 > "$M35/$n-depois.csv" || true
fi
docker exec "$c" /opt/repo/scripts/preparar_servidor.sh versoes /tmp/v.txt > "$LOGS/$tipo-$n-versoes.txt"
grep "^### " "$LOGS/$tipo-$n.log" | tail -3
[[ ${MANTER:-0} == 1 ]] || docker rm -f "$c" >/dev/null
