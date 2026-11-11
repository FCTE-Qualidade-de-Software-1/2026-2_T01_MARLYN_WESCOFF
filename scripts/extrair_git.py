"""Extrai os dados brutos do Git para a gestão PSM/CID (issue #24).

Gera, em docs/metricas/dados/brutos/:
  commits.csv  -> B3 (linhas alteradas por dia, concentração de véspera) e C2 (commits e linhas por integrante)
  tags.csv     -> A4 e B3 (tags das entregas)

Uso:
  python3 scripts/extrair_git.py --data-ref AAAA-MM-DD

--data-ref é a data de corte (horário de Brasília, fim do dia). Só entram commits e tags até essa data,
e a coluna data_extracao recebe a própria data de corte. Rodar duas vezes com a mesma data e o mesmo
histórico gera arquivos idênticos.

Regras (docs/metricas/dados/brutos/README.md):
  - só a branch main: o gh-pages tem commits gerados pelo deploy;
  - sem commits de merge (--no-merges): eles não têm diff próprio, e os merges são medidos pelos
    pull requests em prs.json;
  - autor pelo %aN, que aplica o .mailmap e entrega o nome canônico;
  - sem os commits do robô de coleta (github-actions[bot]).
"""

import argparse
import csv
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "docs" / "metricas" / "dados" / "brutos"
BRASILIA = timezone(timedelta(hours=-3))
# Commits do robô de coleta (psm-coleta.yml) não são trabalho da equipe. Mantê-los faria cada coleta diária
# gerar um commit novo só por registrar o commit da coleta anterior.
ROBOS = {"github-actions[bot]"}


def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def fim_do_dia(data_ref):
    """Último instante da data de corte, em Brasília, no formato aceito pelo git."""
    return datetime.combine(data_ref, datetime.max.time().replace(microsecond=0), BRASILIA).isoformat()


def diretorio(caminho):
    """Diretório de primeiro nível de um arquivo; '.' para a raiz. Trata renomeações do numstat."""
    caminho = caminho.split(" => ")[0].replace("{", "")
    return caminho.split("/", 1)[0] if "/" in caminho else "."


def extrair_commits(ref, data_ref):
    """B3 e C2: um registro por commit, com arquivos, linhas e diretórios tocados."""
    formato = "@%h|%aN|%ad|%s"
    args = ["log", ref, "--reverse", "--no-merges", "--numstat", "--date=iso-strict",
            f"--until={fim_do_dia(data_ref)}", f"--pretty=format:{formato}"]
    comando = "git " + " ".join(args)
    commits, atual = [], None
    for linha in git(*args).splitlines():
        if linha.startswith("@"):
            sha, autor, quando, mensagem = linha[1:].split("|", 3)
            atual = {"sha": sha, "autor": autor, "data": quando, "arquivos": 0,
                     "linhas_adicionadas": 0, "linhas_removidas": 0, "dirs": set(), "mensagem": mensagem}
            if autor not in ROBOS:
                commits.append(atual)
        elif linha.strip() and atual is not None:
            adic, remov, caminho = linha.split("\t", 2)
            atual["arquivos"] += 1
            atual["linhas_adicionadas"] += int(adic) if adic.isdigit() else 0   # binário: "-"
            atual["linhas_removidas"] += int(remov) if remov.isdigit() else 0
            atual["dirs"].add(diretorio(caminho))
    for c in commits:
        c["diretorios"] = ";".join(sorted(c.pop("dirs")))
    return commits, comando


def extrair_tags(data_ref):
    """A4 e B3: tag, commit apontado e data (tags anotadas apontam para o commit desreferenciado)."""
    formato = "%(refname:short)|%(objectname:short)|%(*objectname:short)|%(creatordate:short)"
    comando = "git for-each-ref refs/tags --format=" + formato
    tags = []
    for linha in git("for-each-ref", "refs/tags", f"--format={formato}").splitlines():
        nome, objeto, alvo, quando = linha.split("|")
        if quando and date.fromisoformat(quando) <= data_ref:
            tags.append({"tag": nome, "commit": alvo or objeto, "data_tag": quando})
    return tags, comando


def gravar_csv(caminho, linhas, campos, fonte, data_ref, comando):
    extras = {"fonte": fonte, "data_extracao": data_ref.isoformat(), "comando_ou_query": comando}
    with caminho.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos + list(extras), lineterminator="\n")
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({**{c: linha[c] for c in campos}, **extras})
    print(f"{caminho.relative_to(RAIZ)}: {len(linhas)} linhas")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-ref", type=date.fromisoformat, default=datetime.now(BRASILIA).date(),
                        help="data de corte AAAA-MM-DD (padrão: hoje, em Brasília)")
    parser.add_argument("--ref", default="main", help="branch analisada (padrão: main)")
    args = parser.parse_args()

    BRUTOS.mkdir(parents=True, exist_ok=True)
    commits, cmd = extrair_commits(args.ref, args.data_ref)
    gravar_csv(BRUTOS / "commits.csv", commits,
               ["sha", "autor", "data", "arquivos", "linhas_adicionadas", "linhas_removidas", "diretorios",
                "mensagem"], "git log", args.data_ref, cmd)
    tags, cmd = extrair_tags(args.data_ref)
    gravar_csv(BRUTOS / "tags.csv", tags, ["tag", "commit", "data_tag"], "git for-each-ref", args.data_ref, cmd)


if __name__ == "__main__":
    main()
