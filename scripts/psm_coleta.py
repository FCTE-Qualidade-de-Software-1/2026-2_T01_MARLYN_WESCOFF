"""Coleta as medidas do PSM/CID do projeto a partir das issues do GitHub e do registro de horas.

Medidas (ver docs/gestao/plano-psm.md):
  1. Planejado vs. concluído por milestone (Calendário e Progresso)
  2. Esforço estimado vs. realizado e custo (Recursos e Custos)
  3. Tempo de ciclo e issues paradas (Desempenho dos Processos)

Uso:
  python3 scripts/psm_coleta.py --repo FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF
Variável opcional GITHUB_TOKEN para evitar o limite de requisições anônimas.
Grava dados/gestao/psm-AAAA-MM-DD.csv e imprime um resumo em Markdown.
"""

import argparse
import csv
import json
import os
import re
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CUSTO_HORA = 15.00
LIMITE_DIAS_PARADA = 3
RAIZ = Path(__file__).resolve().parent.parent


def baixar_issues(repo):
    token = os.environ.get("GITHUB_TOKEN")
    issues, pagina = [], 1
    while True:
        url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={pagina}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            lote = json.load(resp)
        issues += [i for i in lote if "pull_request" not in i]
        if len(lote) < 100:
            return issues
        pagina += 1


def estimativa(corpo):
    """Valor do campo 'Estimativa (horas)' do formulário de issue."""
    m = re.search(r"###\s*Estimativa \(horas\)\s*\n+\s*([\d.,]+)", corpo or "")
    return float(m.group(1).replace(",", ".")) if m else None


def data(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def ler_horas():
    arquivo = RAIZ / "dados" / "gestao" / "horas.csv"
    linhas = []
    if arquivo.exists():
        with arquivo.open(encoding="utf-8") as f:
            for linha in csv.DictReader(f):
                valor = (linha.get("horas") or "").strip().replace(",", ".")
                if (linha.get("membro") or "").strip() and valor:
                    linha["horas"] = float(valor)
                    linhas.append(linha)
    return linhas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    agora = datetime.now(timezone.utc)
    issues = baixar_issues(args.repo)
    horas = ler_horas()
    horas_por_issue = defaultdict(float)
    for h in horas:
        if str(h.get("issue", "")).strip().isdigit():
            horas_por_issue[int(h["issue"])] += h["horas"]

    sprints = defaultdict(list)
    for i in issues:
        sprints[(i.get("milestone") or {}).get("title") or "Sem sprint"].append(i)

    linhas_csv = []
    print(f"Medição de {agora.date().isoformat()} ({len(issues)} issues)\n")
    print("| Sprint | Planejadas | Concluídas | % concluído | Estimado (h) | Realizado (h) | R/E | Custo | TC mediana (dias) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for nome, lista in sorted(sprints.items()):
        planejadas = len(lista)
        concluidas = sum(1 for i in lista if i["state"] == "closed")
        pct = concluidas / planejadas * 100 if planejadas else 0
        est = sum(e for e in (estimativa(i.get("body")) for i in lista) if e is not None)
        real = sum(horas_por_issue[i["number"]] for i in lista)
        razao = real / est if est else 0
        ciclos = [(data(i["closed_at"]) - data(i["created_at"])).total_seconds() / 86400
                  for i in lista if i["state"] == "closed" and i.get("closed_at")]
        tc = statistics.median(ciclos) if ciclos else 0
        print(f"| {nome} | {planejadas} | {concluidas} | {pct:.0f}% | {est:.1f} | {real:.1f} | "
              f"{razao:.2f} | R$ {real * CUSTO_HORA:.2f} | {tc:.1f} |")
        linhas_csv.append({"data": agora.date().isoformat(), "sprint": nome, "planejadas": planejadas,
                           "concluidas": concluidas, "pct_concluido": round(pct, 1), "horas_estimadas": est,
                           "horas_realizadas": real, "razao_esforco": round(razao, 2),
                           "custo": round(real * CUSTO_HORA, 2), "tempo_ciclo_mediana": round(tc, 1)})

    paradas = [i for i in issues if i["state"] == "open"
               and (agora - data(i["updated_at"])).days > LIMITE_DIAS_PARADA]
    print(f"\nIssues paradas há mais de {LIMITE_DIAS_PARADA} dias: "
          + (", ".join(f"#{i['number']}" for i in paradas) or "nenhuma"))

    por_membro = defaultdict(float)
    for h in horas:
        por_membro[h["membro"].strip()] += h["horas"]
    total = sum(por_membro.values())
    if total:
        print("\n| Integrante | Horas | % |\n|---|---|---|")
        for nome, v in sorted(por_membro.items(), key=lambda x: -x[1]):
            print(f"| {nome} | {v:.1f} | {v / total * 100:.0f}% |")

    destino = RAIZ / "dados" / "gestao" / f"psm-{agora.date().isoformat()}.csv"
    if linhas_csv:
        with destino.open("w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=list(linhas_csv[0]))
            escritor.writeheader()
            escritor.writerows(linhas_csv)
        print(f"\nRetrato gravado em {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
