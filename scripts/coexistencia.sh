#!/usr/bin/env bash
# Entidades vizinhas e verificações de M2.4 (coexistência), issue #69.
#
# Roda no servidor de referência, como root, depois da etapa "base" de preparar_servidor.sh.
#
#   criar                               Cria as 3 entidades vizinhas:
#                                         E1 aplicação web estática no virtual host da porta 8090;
#                                         E2 banco "outraapp" no mesmo PostgreSQL, com 2 tabelas;
#                                         E3 tarefa do usuário "outraapp" no cron, a cada minuto.
#   referencia                          Grava o estado de referência: hash do conteúdo de E1 e
#                                         checksum das tabelas de E2.
#   verificar <operacao> <momento> <csv>
#                                       Verifica as 3 entidades uma vez e acrescenta 3 linhas ao CSV.
#   durante <operacao> <csv> -- <comando...>
#                                       Roda o comando e verifica as 3 entidades a cada 2 s enquanto
#                                       ele roda. Acrescenta 3 linhas ao CSV (uma por entidade) com o
#                                       número de amostras e a primeira falha. Sai com o código do comando.
#
# Critérios (fixados antes da coleta, regra R1):
#   E1: HTTP 200 e sha256 do conteúdo igual ao da referência.
#   E2: checksum md5 das linhas das 2 tabelas igual ao da referência.
#   E3: a última execução registrada tem no máximo 90 s (o cron roda a cada 60 s).
set -euo pipefail

ESTADO=/root/moodle-avaliacao/coexistencia.ref
E1_PORTA=8090
E1_DIR=/var/www/vizinha-estatica
E3_LOG=/home/outraapp/execucoes.log
E3_IDADE_MAX=90
AVALIADOR=${AVALIADOR:-MS}

erro() { printf 'erro: %s\n' "$*" >&2; exit 1; }
[[ $EUID -eq 0 ]] || erro "execute como root"

criar() {
  echo "==> E1: aplicação estática na porta $E1_PORTA"
  install -d -m 0755 "$E1_DIR"
  cat > "$E1_DIR/index.html" <<'EOF'
<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Portal de avisos (aplicação vizinha)</title></head>
<body><h1>Portal de avisos</h1><p>Aplicação fictícia que divide o servidor com o Moodle (M2.4, E1).</p></body></html>
EOF
  grep -qx "Listen $E1_PORTA" /etc/apache2/ports.conf || echo "Listen $E1_PORTA" >> /etc/apache2/ports.conf
  cat > /etc/apache2/sites-available/vizinha-estatica.conf <<EOF
<VirtualHost *:$E1_PORTA>
    DocumentRoot $E1_DIR
    <Directory $E1_DIR>
        Require all granted
    </Directory>
</VirtualHost>
EOF
  a2ensite -q vizinha-estatica >/dev/null
  service apache2 reload >/dev/null

  echo "==> E2: banco outraapp no PostgreSQL"
  sudo -u postgres psql -q -v ON_ERROR_STOP=1 <<'EOF'
CREATE ROLE outraapp LOGIN;
CREATE DATABASE outraapp OWNER outraapp ENCODING 'UTF8' TEMPLATE template0;
\c outraapp
CREATE TABLE clientes (id int PRIMARY KEY, nome text NOT NULL, email text NOT NULL);
CREATE TABLE pedidos (id int PRIMARY KEY, cliente_id int REFERENCES clientes(id), valor numeric(10,2));
INSERT INTO clientes SELECT g, 'Cliente ' || g, 'cliente' || g || '@example.invalid' FROM generate_series(1, 100) g;
INSERT INTO pedidos SELECT g, 1 + (g % 100), round((g * 7.31)::numeric, 2) FROM generate_series(1, 500) g;
ALTER TABLE clientes OWNER TO outraapp;
ALTER TABLE pedidos OWNER TO outraapp;
EOF

  echo "==> E3: tarefa do usuário outraapp no cron"
  id outraapp >/dev/null 2>&1 || useradd -m -s /usr/sbin/nologin outraapp
  echo "* * * * * outraapp date -Iseconds >> $E3_LOG" > /etc/cron.d/outraapp
  chmod 0644 /etc/cron.d/outraapp
  echo "Pronto. Espere a primeira execução de E3 (até 1 min) e rode: $0 referencia"
}

# Nenhuma verificação pode derrubar o script: uma entidade fora do ar vira uma linha de falha no CSV.
e1_hash() { { curl -s --max-time 5 "http://localhost:$E1_PORTA/" || true; } | sha256sum | cut -c1-16; }
e1_http() { curl -s --max-time 5 -o /dev/null -w '%{http_code}' "http://localhost:$E1_PORTA/" || true; }
e2_checksum() {
  sudo -u postgres psql -d outraapp -tAq -c \
    "SELECT md5((SELECT string_agg(c::text, '|' ORDER BY id) FROM clientes c) ||
                (SELECT string_agg(p::text, '|' ORDER BY id) FROM pedidos p));" 2>/dev/null | cut -c1-16 || true
}
e3_idade() {
  local ultima; ultima=$(tail -1 "$E3_LOG" 2>/dev/null) || { echo -1; return; }
  [[ -n $ultima ]] || { echo -1; return; }
  local t; t=$(date -d "$ultima" +%s 2>/dev/null) || { echo -1; return; }
  echo $(( $(date +%s) - t ))
}

referencia() {
  [[ $(e1_http) == 200 ]] || erro "E1 não responde"
  [[ $(e3_idade) -ge 0 ]] || erro "E3 ainda não executou; espere 1 min"
  umask 077
  { echo "E1_HASH=$(e1_hash)"; echo "E2_CHECKSUM=$(e2_checksum)"; } > "$ESTADO"
  cat "$ESTADO"
}

carrega_ref() { [[ -f $ESTADO ]] || erro "rode '$0 referencia' antes"; . "$ESTADO"; }

# Uma amostra das 3 entidades: imprime "E1|ok|observado", "E2|...", "E3|...".
amostra() {
  local http hash soma idade
  http=$(e1_http); hash=$(e1_hash)
  if [[ $http == 200 && $hash == "$E1_HASH" ]]; then echo "E1|ok|HTTP $http, hash $hash"
  else echo "E1|falha|HTTP $http, hash $hash"; fi
  soma=$(e2_checksum)
  if [[ $soma == "$E2_CHECKSUM" ]]; then echo "E2|ok|checksum $soma"; else echo "E2|falha|checksum ${soma:-sem resposta}"; fi
  idade=$(e3_idade)
  if [[ $idade -ge 0 && $idade -le $E3_IDADE_MAX ]]; then echo "E3|ok|última execução há ${idade} s"
  else echo "E3|falha|última execução há ${idade} s"; fi
}

esperado() {
  case $1 in
    E1) echo "HTTP 200, hash $E1_HASH" ;;
    E2) echo "checksum $E2_CHECKSUM" ;;
    E3) echo "última execução há no máximo ${E3_IDADE_MAX} s" ;;
  esac
}

verificacao() {
  case $1 in
    E1) echo "aplicação estática: HTTP e hash do conteúdo" ;;
    E2) echo "banco outraapp: checksum das tabelas clientes e pedidos" ;;
    E3) echo "tarefa do usuário outraapp: execução no horário" ;;
  esac
}

cabecalho() {
  [[ -s $1 ]] || echo "data_hora,operacao,momento,entidade,verificacao,esperado,observado,resultado,amostras,avaliador,evidencia,observacao" > "$1"
}

linha() { # csv operacao momento entidade observado resultado amostras observacao
  local csv=$1 op=$2 mom=$3 ent=$4 obs=$5 res=$6 n=$7 nota=${8:-}
  printf '%s,%s,%s,%s,"%s","%s","%s",%s,%s,%s,%s,"%s"\n' "$(date -Iseconds)" "$op" "$mom" "$ent" \
    "$(verificacao "$ent")" "$(esperado "$ent")" "$obs" "$res" "$n" "$AVALIADOR" \
    "M2.4/logs/${op}.log" "$nota" >> "$csv"
}

verificar() {
  local op=${1:?operação} mom=${2:?momento} csv=${3:?csv}
  carrega_ref; cabecalho "$csv"
  while IFS='|' read -r ent res obs; do linha "$csv" "$op" "$mom" "$ent" "$obs" "$res" 1; done < <(amostra)
}

durante() {
  local op=${1:?operação} csv=${2:?csv}; shift 2
  [[ ${1:-} == -- ]] && shift
  [[ $# -gt 0 ]] || erro "informe o comando depois de --"
  carrega_ref; cabecalho "$csv"
  local amostras; amostras=$(mktemp)
  "$@" & local pid=$!
  while kill -0 "$pid" 2>/dev/null; do amostra >> "$amostras"; sleep 2; done
  local codigo=0; wait "$pid" || codigo=$?
  for ent in E1 E2 E3; do
    local total falhas primeira
    total=$(grep -c "^$ent|" "$amostras" || true)
    falhas=$(grep -c "^$ent|falha|" "$amostras" || true)
    primeira=$(grep -m1 "^$ent|falha|" "$amostras" | cut -d'|' -f3 || true)
    if [[ $total -eq 0 ]]; then
      linha "$csv" "$op" durante "$ent" "comando terminou antes da primeira amostra" "sem_amostra" 0
    elif [[ $falhas -eq 0 ]]; then
      linha "$csv" "$op" durante "$ent" "$total de $total amostras ok" ok "$total"
    else
      linha "$csv" "$op" durante "$ent" "$falhas de $total amostras com falha; primeira: $primeira" falha "$total"
    fi
  done
  rm -f "$amostras"
  echo "comando terminou com código $codigo"
  return "$codigo"
}

case ${1:-} in
  criar) criar ;;
  referencia) referencia ;;
  verificar) shift; verificar "$@" ;;
  durante) shift; durante "$@" ;;
  *) sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
