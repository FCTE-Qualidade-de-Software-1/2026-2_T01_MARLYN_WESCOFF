#!/usr/bin/env bash
# Executa os 20 casos do oráculo de M1.2 (issue #67) no servidor de avaliação (contêiner moodle-aval) e
# grava dados/avaliacao/M1.2/execucoes.csv. Roda no hospedeiro, com Docker.
#
# A instância m12 (porta 8083, só dentro do servidor) recebe a massa "contas,oraculo" com D = DIA.
# Os casos P-01 a P-04 rodam com o relógio do PHP deslocado por faketime para o horário do oráculo.
set -euo pipefail
DIA=${DIA:-2026-11-22}
C=${C:-moodle-aval}
RAIZ=$(cd "$(dirname "$0")/.." && pwd)
SAIDA=$RAIZ/dados/avaliacao/M1.2
docker exec "$C" bash -c "command -v faketime >/dev/null || DEBIAN_FRONTEND=noninteractive apt-get install -yq faketime >/dev/null"
if ! docker exec "$C" test -d /var/www/m12; then
  docker exec "$C" /opt/repo/scripts/preparar_servidor.sh instancia m12 503 8.3 8083 > "$SAIDA/preparo-m12.log" 2>&1
  docker exec "$C" bash -c "cd /opt/repo && python3 scripts/gera_massa.py aplicar --moodle /var/www/m12 --php php8.3 --partes contas,oraculo --dia-prazo $DIA --registro /root/massa-m12.json" >> "$SAIDA/preparo-m12.log" 2>&1
fi
declare -A RELOGIO=([P-01]="$DIA 23:58:00" [P-02]="$(date -d "$DIA +1 day" +%F) 00:01:00"
                    [P-03]="$(date -d "$DIA +1 day" +%F) 12:00:00" [P-04]="$DIA 18:01:00")
declare -A ESTUDANTE=([P-01]=est02 [P-02]=est03 [P-03]=est04 [P-04]=est05)
: > "$SAIDA/resultados.jsonl"
for caso in Q-01 Q-02 Q-03 Q-04 Q-05 Q-06 Q-07 Q-08 Q-09 Q-10 A-01 A-02 A-03 A-04 A-05 A-06 P-01 P-02 P-03 P-04; do
  pre=""; est=est01
  if [[ $caso == P-* ]]; then pre="faketime -f '@${RELOGIO[$caso]}'"; est=${ESTUDANTE[$caso]}; fi
  # o sudo limpa LD_PRELOAD: o faketime vem depois dele, para valer no processo do PHP
  docker exec "$C" bash -c "cd /tmp && sudo -u www-data $pre php8.3 /opt/repo/scripts/m12_oraculo.php --moodle=/var/www/m12 --caso=$caso --estudante=$est" \
    | tail -1 | tee -a "$SAIDA/resultados.jsonl"
done
