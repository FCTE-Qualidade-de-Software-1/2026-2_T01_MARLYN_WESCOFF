#!/usr/bin/env bash
# Ponte para o Playwright (no WSL) abrir o Firefox do Windows pelo WebDriver BiDi (canal moz-firefox),
# no ambiente A2 de M3.1. Converte os caminhos do WSL (/mnt/...) para caminhos do Windows antes de
# chamar o firefox.exe. O perfil temporário precisa estar numa pasta do Windows: rode o Playwright com
# TMPDIR=/mnt/c/Users/<usuário>/AppData/Local/Temp/<pasta>.
FIREFOX=${FIREFOX_EXE:-/mnt/c/Users/mayko/AppData/Local/FirefoxAval/firefox.exe}
args=()
for a in "$@"; do
  if [[ $a == /mnt/* ]]; then args+=("$(wslpath -w "$a")"); else args+=("$a"); fi
done
exec "$FIREFOX" "${args[@]}"
