"""Extrai os dados brutos do GitHub para a gestão PSM/CID (issue #24).

Gera, em docs/metricas/dados/brutos/:
  issues.json          -> A1, A2, A4, B1, B2, B4, C2 (issues fechadas por integrante), C3 (estimativa)
  issue_events.jsonl   -> A1 (fechamentos e reaberturas), A3 (criada/fechada antes do quadro), B4 (reaberturas)
  prs.json             -> B1 (tempo de revisão), B3 (merges por semana), B4 (revisões CHANGES_REQUESTED), C2
  milestones.json      -> A1, A2, A4 (prazo de cada marco)
  releases.json        -> A4 e B3 (data real de cada entrega)
  quadro_eventos.csv   -> A3 e B1 (transições de Status no quadro, com data)
  quadro_retratos.csv  -> A2 e A3 (retrato diário de Status e Iteração de cada issue no quadro)

Uso:
  GITHUB_TOKEN=... python3 scripts/extrair_issues.py --data-ref AAAA-MM-DD

Tokens:
  GITHUB_TOKEN        obrigatório (a API GraphQL não aceita acesso anônimo).
  PSM_PROJECT_TOKEN   opcional, com o escopo read:project. O quadro fica na conta do Carlos, e o
                      GITHUB_TOKEN do Actions não lê projetos de usuário. Sem ele, os dois arquivos do
                      quadro não são alterados e o script avisa.

--data-ref é a data de corte (horário de Brasília, fim do dia). Itens criados depois dela são descartados;
issue ou PR fechado depois dela aparece como aberto; comentários, revisões e eventos posteriores são
descartados. Os demais campos (título, labels, milestone) refletem o estado no momento da extração. O retrato
do quadro só é gravado quando a data de corte é hoje, porque a API não devolve o estado passado do quadro.

Formato: issues.json, prs.json e releases.json seguem a saída do `gh ... --json` (GraphQL); milestones.json é a
resposta crua da API REST; issue_events.jsonl guarda só os campos usados pelas medidas (a resposta completa
passa de 1,7 MB). O campo viewerDidAuthor do gh foi omitido, porque depende de quem executa o script.
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "docs" / "metricas" / "dados" / "brutos"
BRASILIA = timezone(timedelta(hours=-3))
API = "https://api.github.com"


# ---------------------------------------------------------------- acesso à API

def requisitar(url, token, corpo=None):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo else None,
                                 headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def rest_paginado(caminho, token):
    """Mesma paginação de baixar_issues em psm_coleta.py: páginas de 100 até vir uma incompleta."""
    itens, pagina = [], 1
    sep = "&" if "?" in caminho else "?"
    while True:
        lote = requisitar(f"{API}/{caminho}{sep}per_page=100&page={pagina}", token)
        itens += lote
        if len(lote) < 100:
            return itens
        pagina += 1


def graphql(query, variaveis, token):
    resposta = requisitar(f"{API}/graphql", token, {"query": query, "variables": variaveis})
    if resposta.get("errors"):
        raise RuntimeError("; ".join(e.get("message", "") for e in resposta["errors"]))
    return resposta["data"]


def graphql_paginado(query, variaveis, token, caminho):
    """Percorre uma conexão GraphQL (pageInfo/nodes) indicada por caminho, ex.: ["repository", "issues"]."""
    nos, cursor = [], None
    while True:
        dados = graphql(query, {**variaveis, "cursor": cursor}, token)
        conexao = dados
        for chave in caminho:
            conexao = conexao[chave]
        nos += conexao["nodes"]
        if not conexao["pageInfo"]["hasNextPage"]:
            return nos
        cursor = conexao["pageInfo"]["endCursor"]


# ---------------------------------------------------------------- data de corte

def instante(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def depois(iso, corte):
    return iso is not None and instante(iso) > corte


# ---------------------------------------------------------------- formato do gh

AUTOR = "author { __typename login ... on User { id name } ... on Bot { id } ... on Mannequin { id } }"
REACOES = "reactionGroups { content reactors { totalCount } }"


def autor_gh(a):
    if not a:
        return None
    return {"id": a.get("id", ""), "is_bot": a["__typename"] == "Bot", "login": a["login"],
            "name": a.get("name") or ""}


def reacoes_gh(grupos):
    return [{"content": g["content"], "users": {"totalCount": g["reactors"]["totalCount"]}}
            for g in grupos or [] if g["reactors"]["totalCount"]]


# ---------------------------------------------------------------- extrações

Q_ISSUES = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    issues(first: 50, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title state createdAt closedAt
        %s
        assignees(first: 20) { nodes { id login name databaseId } }
        labels(first: 50) { nodes { id name description color } }
        milestone { number title description dueOn }
        comments(first: 100) { nodes { id author { login } authorAssociation body createdAt
          includesCreatedEdit isMinimized minimizedReason %s url } }
      }
    }
  }
}""" % (AUTOR, REACOES)


def extrair_issues(owner, nome, token, corte):
    """A1, A2, A4, B1, B2, B4, C2, C3: issues no formato de `gh issue list --json ...`."""
    saida = []
    for i in graphql_paginado(Q_ISSUES, {"owner": owner, "name": nome}, token, ["repository", "issues"]):
        if depois(i["createdAt"], corte):
            continue
        fechada = i["state"] == "CLOSED" and not depois(i["closedAt"], corte)
        saida.append({
            "assignees": i["assignees"]["nodes"],
            "author": autor_gh(i["author"]),
            "closedAt": i["closedAt"] if fechada else None,
            "comments": [{"id": c["id"], "author": {"login": (c["author"] or {}).get("login", "ghost")},
                          "authorAssociation": c["authorAssociation"], "body": c["body"],
                          "createdAt": c["createdAt"], "includesCreatedEdit": c["includesCreatedEdit"],
                          "isMinimized": c["isMinimized"], "minimizedReason": c["minimizedReason"] or "",
                          "reactionGroups": reacoes_gh(c["reactionGroups"]), "url": c["url"]}
                         for c in i["comments"]["nodes"] if not depois(c["createdAt"], corte)],
            "createdAt": i["createdAt"],
            "labels": i["labels"]["nodes"],
            "milestone": i["milestone"],
            "number": i["number"],
            "state": "CLOSED" if fechada else "OPEN",
            "title": i["title"],
        })
    return saida


Q_PRS = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: 50, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title state createdAt mergedAt closedAt additions deletions
        %s
        reviews(first: 100) { nodes { id author { login } authorAssociation body submittedAt
          includesCreatedEdit %s state commit { oid } } }
      }
    }
  }
}""" % (AUTOR, REACOES)


def extrair_prs(owner, nome, token, corte):
    """B1, B3, B4, C2: PRs no formato de `gh pr list --json ...`, com o estado de cada revisão."""
    saida = []
    for p in graphql_paginado(Q_PRS, {"owner": owner, "name": nome}, token, ["repository", "pullRequests"]):
        if depois(p["createdAt"], corte):
            continue
        mergeado = p["mergedAt"] is not None and not depois(p["mergedAt"], corte)
        fechado = p["closedAt"] is not None and not depois(p["closedAt"], corte)
        estado = "MERGED" if mergeado else "CLOSED" if fechado and p["state"] == "CLOSED" else "OPEN"
        saida.append({
            "additions": p["additions"],
            "author": autor_gh(p["author"]),
            "closedAt": p["closedAt"] if fechado else None,
            "createdAt": p["createdAt"],
            "deletions": p["deletions"],
            "mergedAt": p["mergedAt"] if mergeado else None,
            "number": p["number"],
            "reviews": [{"id": r["id"], "author": {"login": (r["author"] or {}).get("login", "ghost")},
                         "authorAssociation": r["authorAssociation"], "body": r["body"],
                         "submittedAt": r["submittedAt"], "includesCreatedEdit": r["includesCreatedEdit"],
                         "reactionGroups": reacoes_gh(r["reactionGroups"]), "state": r["state"],
                         "commit": r["commit"]}
                        for r in p["reviews"]["nodes"] if r["submittedAt"] and not depois(r["submittedAt"], corte)],
            "state": estado,
            "title": p["title"],
        })
    return saida


Q_RELEASES = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    releases(first: 50, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes { createdAt isLatest name publishedAt tagName }
    }
  }
}"""


def extrair_releases(owner, nome, token, corte):
    """A4 e B3: releases no formato de `gh release list --json tagName,name,createdAt,publishedAt,isLatest`."""
    nos = graphql_paginado(Q_RELEASES, {"owner": owner, "name": nome}, token, ["repository", "releases"])
    return [r for r in nos if not depois(r["createdAt"], corte)]


def extrair_milestones(repo, token, corte):
    """A1, A2, A4: resposta crua de GET /milestones?state=all."""
    return [m for m in rest_paginado(f"repos/{repo}/milestones?state=all", token)
            if not depois(m["created_at"], corte)]


def extrair_eventos(repo, token, corte):
    """A1, A3, B4: eventos de issues e PRs, só com os campos usados pelas medidas."""
    eventos = []
    for e in rest_paginado(f"repos/{repo}/issues/events", token):
        if depois(e["created_at"], corte):
            continue
        eventos.append({
            "id": e["id"], "event": e["event"], "created_at": e["created_at"],
            "actor": (e.get("actor") or {}).get("login"),
            "issue": (e.get("issue") or {}).get("number"),
            "label": (e.get("label") or {}).get("name"),
            "milestone": (e.get("milestone") or {}).get("title"),
            "assignee": (e.get("assignee") or {}).get("login"),
            "commit_id": e.get("commit_id"),
        })
    return eventos


Q_TRANSICOES = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    issues(first: 50, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        timelineItems(first: 100, itemTypes: [ADDED_TO_PROJECT_V2_EVENT, PROJECT_V2_ITEM_STATUS_CHANGED_EVENT]) {
          nodes {
            __typename
            ... on AddedToProjectV2Event { createdAt }
            ... on ProjectV2ItemStatusChangedEvent { createdAt previousStatus status }
          }
        }
      }
    }
  }
}"""


def extrair_transicoes(owner, nome, token, corte):
    """A3 e B1: entrada no quadro e cada mudança de Status, com data (histórico do quadro)."""
    linhas = []
    for i in graphql_paginado(Q_TRANSICOES, {"owner": owner, "name": nome}, token, ["repository", "issues"]):
        for t in i["timelineItems"]["nodes"]:
            if not t or depois(t.get("createdAt"), corte):
                continue
            adicionada = t["__typename"] == "AddedToProjectV2Event"
            linhas.append({"issue": i["number"], "data_hora": t["createdAt"],
                           "evento": "adicionada" if adicionada else "status",
                           "status_anterior": "" if adicionada else t.get("previousStatus") or "",
                           "status": "" if adicionada else t.get("status") or ""})
    return sorted(linhas, key=lambda l: (l["data_hora"], l["issue"]))


Q_QUADRO = """
query($login: String!, $numero: Int!, $cursor: String) {
  user(login: $login) {
    projectV2(number: $numero) {
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          content { ... on Issue { number repository { nameWithOwner } } }
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldIterationValue { title startDate field { ... on ProjectV2FieldCommon { name } } }
            }
          }
        }
      }
    }
  }
}"""


def extrair_retrato(repo, login, numero, token, hoje):
    """A2 e A3: Status e Iteração de cada issue do repositório no quadro, hoje."""
    linhas = []
    for item in graphql_paginado(Q_QUADRO, {"login": login, "numero": numero}, token,
                                 ["user", "projectV2", "items"]):
        conteudo = item.get("content") or {}
        if (conteudo.get("repository") or {}).get("nameWithOwner") != repo:
            continue
        campos = {(v.get("field") or {}).get("name"): v for v in item["fieldValues"]["nodes"] if v}
        iteracao = campos.get("Iteração") or {}
        linhas.append({"data": hoje.isoformat(), "issue": conteudo["number"],
                       "status": (campos.get("Status") or {}).get("name", ""),
                       "iteracao": iteracao.get("title", ""), "iteracao_inicio": iteracao.get("startDate", "")})
    return sorted(linhas, key=lambda l: l["issue"])


# ---------------------------------------------------------------- gravação

def gravar_json(nome, dados):
    caminho = BRUTOS / nome
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"{caminho.relative_to(RAIZ)}: {len(dados)} itens")


def gravar_jsonl(nome, dados):
    caminho = BRUTOS / nome
    with caminho.open("w", encoding="utf-8", newline="\n") as f:
        for d in dados:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"{caminho.relative_to(RAIZ)}: {len(dados)} linhas")


def gravar_csv(nome, linhas, campos, fonte, data_ref, comando, manter=None):
    """Grava o CSV com as colunas de origem. `manter` preserva linhas antigas (retratos de outros dias)."""
    caminho = BRUTOS / nome
    extras = {"fonte": fonte, "data_extracao": data_ref.isoformat(), "comando_ou_query": comando}
    antigas = []
    if manter and caminho.exists():
        with caminho.open(encoding="utf-8", newline="") as f:
            antigas = [l for l in csv.DictReader(f) if manter(l)]
    with caminho.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos + list(extras), lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(antigas)
        escritor.writerows({**{c: l[c] for c in campos}, **extras} for l in linhas)
    print(f"{caminho.relative_to(RAIZ)}: {len(antigas) + len(linhas)} linhas")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default="FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF")
    parser.add_argument("--data-ref", type=date.fromisoformat, default=datetime.now(BRASILIA).date(),
                        help="data de corte AAAA-MM-DD (padrão: hoje, em Brasília)")
    parser.add_argument("--quadro-usuario", default="cadumotta", help="dono do project board")
    parser.add_argument("--quadro-numero", type=int, default=1, help="número do project board")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("Defina GITHUB_TOKEN (por exemplo, GITHUB_TOKEN=$(gh auth token)).")
    token_quadro = os.environ.get("PSM_PROJECT_TOKEN") or token
    owner, nome = args.repo.split("/")
    corte = datetime.combine(args.data_ref, datetime.max.time(), BRASILIA)
    hoje = datetime.now(BRASILIA).date()
    BRUTOS.mkdir(parents=True, exist_ok=True)

    gravar_json("issues.json", extrair_issues(owner, nome, token, corte))
    gravar_jsonl("issue_events.jsonl", extrair_eventos(args.repo, token, corte))
    gravar_json("prs.json", extrair_prs(owner, nome, token, corte))
    gravar_json("milestones.json", extrair_milestones(args.repo, token, corte))
    gravar_json("releases.json", extrair_releases(owner, nome, token, corte))

    try:
        transicoes = extrair_transicoes(owner, nome, token_quadro, corte)
        gravar_csv("quadro_eventos.csv", transicoes, ["issue", "data_hora", "evento", "status_anterior", "status"],
                   "GitHub GraphQL (timelineItems)", args.data_ref,
                   "issues { timelineItems(itemTypes: [ADDED_TO_PROJECT_V2_EVENT, PROJECT_V2_ITEM_STATUS_CHANGED_EVENT]) }")
        if args.data_ref == hoje:
            retrato = extrair_retrato(args.repo, args.quadro_usuario, args.quadro_numero, token_quadro, hoje)
            gravar_csv("quadro_retratos.csv", retrato, ["data", "issue", "status", "iteracao", "iteracao_inicio"],
                       "GitHub GraphQL (projectV2)", args.data_ref,
                       f"user(login: {args.quadro_usuario}) {{ projectV2(number: {args.quadro_numero}) {{ items {{ fieldValues }} }} }}",
                       manter=lambda l: l["data"] != hoje.isoformat())
        else:
            print("quadro_retratos.csv: não alterado (o retrato só é gravado com a data de corte de hoje)")
    except (RuntimeError, urllib.error.HTTPError) as erro:
        print(f"Aviso: quadro não lido ({erro}). Use PSM_PROJECT_TOKEN com o escopo read:project. "
              "quadro_eventos.csv e quadro_retratos.csv não foram alterados.", file=sys.stderr)


if __name__ == "__main__":
    main()
