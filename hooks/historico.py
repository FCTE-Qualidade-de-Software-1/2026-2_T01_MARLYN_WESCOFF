"""Hook do MkDocs: acrescenta o "Histórico de versões" ao fim de cada página da GitPage.

O histórico vem do git log do arquivo da página (sem commits de merge), e não é escrito à mão: cada
linha é um commit, com data, descrição (a mensagem do commit), autor e link. Os autores são
convertidos para o nome oficial pela Tabela 1 de docs/sobre/equipe.md; os commits do workflow de
coleta aparecem como "Coleta automática". O deploy (deploy.yml) faz checkout com fetch-depth: 0, que
o histórico completo exige; sem o git ou sem histórico, a página sai sem a seção.
"""

import re
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MAX_LINHAS = 25


def _chave(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().casefold().split()
    return (t[0], t[-1]) if t else ("", "")


@lru_cache(maxsize=1)
def _equipe():
    """{login, nome ou (primeiro, último nome)} -> nome oficial."""
    mapa = {}
    texto = (RAIZ / "docs" / "sobre" / "equipe.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*\d+\s*\|\s*\[([^\]]+)\]", texto, re.M):
        nome, login = m.group(1), m.group(2)
        mapa[login.casefold()] = nome
        mapa[_chave(nome)] = nome
    return mapa


def _autor(nome_git):
    if "[bot]" in nome_git:
        return "Coleta automática (GitHub Actions)"
    eq = _equipe()
    return eq.get(nome_git.casefold()) or eq.get(_chave(nome_git)) or nome_git


def _commits(caminho):
    try:
        saida = subprocess.run(
            ["git", "log", "--follow", "--no-merges", "--date=format:%d/%m/%Y",
             "--format=%H%x1f%ad%x1f%an%x1f%s", "--", caminho],
            cwd=RAIZ, capture_output=True, text=True, timeout=30, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [l.split("\x1f") for l in saida.splitlines() if l.count("\x1f") == 3]


def on_page_markdown(markdown, page, config, files, **kwargs):
    commits = _commits(str(Path(config["docs_dir"]).relative_to(RAIZ) / page.file.src_uri))
    if not commits:
        return markdown
    repo = (config.get("repo_url") or "").rstrip("/")
    total = len(commits)
    linhas = ['??? note "Histórico de versões"',
              f"    Gerado do `git log` deste arquivo: {total} versões.", "",
              "    | Versão | Data | Descrição | Autor |", "    |---|---|---|---|"]
    for i, (h, data, autor, assunto) in enumerate(commits[:MAX_LINHAS]):
        versao = total - i
        assunto = assunto.replace("|", "\\|").replace("<", "&lt;")
        link = f"[{h[:7]}]({repo}/commit/{h})" if repo else h[:7]
        linhas.append(f"    | {versao} | {data} | {assunto} ({link}) | {_autor(autor)} |")
    if total > MAX_LINHAS:
        linhas += ["", f"    As {total - MAX_LINHAS} versões mais antigas estão no "
                       f"[histórico do arquivo]({repo}/commits/main/{config['docs_dir'].rsplit('/', 1)[-1]}/{page.file.src_uri})."]
    return markdown.rstrip() + "\n\n---\n\n" + "\n".join(linhas) + "\n"
