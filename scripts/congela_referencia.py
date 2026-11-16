"""Congela os arquivos de referência de M2.1 e M2.2 antes da primeira troca de dados (regra R1 do plano da Fase 3).

Copia cada arquivo para dados/avaliacao/M2.1/referencia/ com o prefixo do formato (F1 a F7) e registra no
MANIFESTO.csv a origem, o sha256, o tamanho, a data e o responsável. Depois do congelamento, --verificar
confere se nenhum arquivo foi alterado; rode antes de cada troca e antes do cálculo de M2.2.

Uso:
  python3 scripts/congela_referencia.py --responsavel CD F1=caminho/usuarios.csv F4=caminho/questoes.gift ...
  python3 scripts/congela_referencia.py --verificar

Um formato já congelado só é substituído com --substituir, e a substituição precisa ser registrada em ata.
Código de saída: 0 sem problemas; 1 quando --verificar encontra arquivo alterado ou ausente; 2 em erro de uso.
"""

import argparse
import csv
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "dados" / "avaliacao" / "M2.1" / "referencia"
MANIFESTO = PASTA / "MANIFESTO.csv"
FORMATOS = {f"F{i}" for i in range(1, 8)}
COLUNAS = ["formato", "arquivo", "origem", "sha256", "bytes", "congelado_em", "responsavel"]


def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def relativo(caminho):
    """Caminho relativo à raiz do repositório, ou só o nome quando o arquivo está fora dele."""
    try:
        return Path(caminho).resolve().relative_to(RAIZ).as_posix()
    except ValueError:
        return Path(caminho).name


def le_manifesto():
    if not MANIFESTO.exists():
        return []
    with MANIFESTO.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def grava_manifesto(linhas):
    PASTA.mkdir(parents=True, exist_ok=True)
    with MANIFESTO.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(sorted(linhas, key=lambda l: (l["formato"], l["arquivo"])))


def verificar():
    linhas = le_manifesto()
    if not linhas:
        print("nenhuma referência congelada ainda")
        return 1
    problemas = 0
    for l in linhas:
        caminho = PASTA / l["arquivo"]
        if not caminho.exists():
            print(f"AUSENTE   {l['formato']} {l['arquivo']}")
            problemas += 1
        elif sha256(caminho) != l["sha256"]:
            print(f"ALTERADO  {l['formato']} {l['arquivo']}")
            problemas += 1
        else:
            print(f"ok        {l['formato']} {l['arquivo']}")
    return 1 if problemas else 0


def congelar(pares, responsavel, substituir):
    linhas = le_manifesto()
    ja = {l["formato"] for l in linhas}
    for par in pares:
        if "=" not in par:
            print(f"erro: use FORMATO=caminho, recebido {par!r}", file=sys.stderr)
            return 2
        formato, origem = par.split("=", 1)
        formato = formato.upper()
        if formato not in FORMATOS:
            print(f"erro: formato {formato!r} fora de F1 a F7", file=sys.stderr)
            return 2
        origem = Path(origem)
        if not origem.is_file():
            print(f"erro: arquivo não encontrado: {origem}", file=sys.stderr)
            return 2
        if formato in ja and not substituir:
            print(f"erro: {formato} já está congelado; use --substituir e registre o motivo em ata", file=sys.stderr)
            return 2
        linhas = [l for l in linhas if l["formato"] != formato or not substituir]
        PASTA.mkdir(parents=True, exist_ok=True)
        destino = PASTA / f"{formato}_{origem.name}"
        shutil.copyfile(origem, destino)
        linhas.append({"formato": formato, "arquivo": destino.name, "origem": relativo(origem),
                       "sha256": sha256(destino), "bytes": destino.stat().st_size,
                       "congelado_em": datetime.now().strftime("%Y-%m-%d %H:%M"), "responsavel": responsavel})
        print(f"congelado {formato} -> {relativo(destino)}")
    grava_manifesto(linhas)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Congela e verifica as referências de M2.1/M2.2.")
    p.add_argument("pares", nargs="*", help="FORMATO=caminho, por exemplo F1=dados/massa/usuarios.csv")
    p.add_argument("--responsavel", default="")
    p.add_argument("--substituir", action="store_true")
    p.add_argument("--verificar", action="store_true")
    a = p.parse_args(argv)
    if a.verificar:
        return verificar()
    if not a.pares:
        p.error("informe ao menos um FORMATO=caminho, ou use --verificar")
    if not a.responsavel:
        p.error("--responsavel é obrigatório ao congelar")
    return congelar(a.pares, a.responsavel, a.substituir)


if __name__ == "__main__":
    sys.exit(main())
