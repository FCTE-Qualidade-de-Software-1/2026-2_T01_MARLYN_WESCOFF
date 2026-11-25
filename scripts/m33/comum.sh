# Funções comuns aos procedimentos medidos de M3.3/M3.4 (issue #71). Carregado pelos procedimentos.
# Cada passo grava "### PASSO <n> <epoch> <descrição>" no log; um passo que falha é tentado de novo
# uma vez ("### RETENTATIVA"), e uma segunda falha encerra a execução ("### FALHA").
PORTA=8080
passo() { echo "### PASSO $1 $(date +%s.%N) $2"; }
executa() { # executa <n> <descrição> <comando...>
  local n=$1 d=$2; shift 2
  passo "$n" "$d"
  if "$@"; then return 0; fi
  echo "### RETENTATIVA $n $(date +%s.%N) $d"
  if "$@"; then return 0; fi
  echo "### FALHA $n $(date +%s.%N) $d"; echo "### FIM $(date +%s.%N) falha"; exit 1
}
login_admin() { # login_admin <usuário> <senha>: primeiro login do administrador pela página de login
  local j; j=$(mktemp)
  local tok; tok=$(curl -s -c "$j" -b "$j" "http://localhost:$PORTA/login/index.php" | grep -oP 'name="logintoken" value="\K[^"]+' | head -1)
  curl -s -c "$j" -b "$j" -o /dev/null --data-urlencode "username=$1" --data-urlencode "password=$2" \
    --data-urlencode "logintoken=$tok" "http://localhost:$PORTA/login/index.php"
  # No primeiro acesso o Moodle redireciona o administrador (tentativa 2 falhou por não seguir o
  # redirecionamento): segue os redirecionamentos e confirma a sessão pelo link de sair.
  # Sem "| grep -q": com pipefail, o grep -q sai cedo, o curl recebe SIGPIPE e o sucesso vira falha
  # (causa das falhas da tentativa 3).
  local pagina; pagina=$(curl -s -L -b "$j" -c "$j" "http://localhost:$PORTA/my/")
  [[ $pagina == *login/logout.php* ]]
}
