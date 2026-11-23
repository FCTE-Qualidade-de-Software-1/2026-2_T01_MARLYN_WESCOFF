"""Consolida as execuções medidas de M3.3, M3.4 e M3.5 (issue #71) a partir dos logs do `script`.

Lê dados/avaliacao/M3.3/logs/<tipo>-<n>.log (marcas "### INICIO/PASSO/RETENTATIVA/FALHA/FIM" gravadas
por scripts/m33/comum.sh) e dados/avaliacao/M3.5/<n>-antes.csv e <n>-depois.csv, e grava:
  dados/avaliacao/M3.3/execucoes.csv   uma linha por execução (M3.3 e M3.4)
  dados/avaliacao/M3.5/comparacao.csv  os 40 itens, antes e depois, de cada atualização
e imprime M3.3, M3.4 (mediana por tipo e retentativas) e M3.5.

Critério de sucesso de M3.3 (plano da Fase 3, fixado antes da coleta): verificação de ambiente sem
erro (o instalador e o upgrade.php param se ela falhar), login do administrador funcionando e nenhum
passo fora da documentação. Os procedimentos só têm passos das páginas oficiais.

Uso: python3 scripts/m33/consolida.py [--avaliador "Nome"]
"""

import argparse
import csv
import re
import statistics
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M33 = RAIZ / "dados" / "avaliacao" / "M3.3"
M35 = RAIZ / "dados" / "avaliacao" / "M3.5"


def le_log(caminho):
    texto = re.sub(r"\x1b\[[0-9;]*m", "", caminho.read_text(encoding="utf-8", errors="replace"))
    marcas = re.findall(r"^### (\w+) (\S+) (\S+)\s*(.*)$", texto, re.M)
    inicio = next((float(b) for a, b, c, d in marcas if a == "INICIO"), None)
    fim = [(float(b), c) for a, b, c, _ in marcas if a == "FIM"]
    falhas = [f"{b} {d}".strip() for a, b, c, d in marcas if a == "FALHA"]
    retent = [f"passo {b}" for a, b, c, d in marcas if a == "RETENTATIVA"]
    roteador = "ERROR" if re.search(r"ERROR \| Router configuration \(core_router\)", texto) else "OK"
    detalhe = ""
    m = re.search(r"Router configuration \(core_router\)\s*\n\s*\|\s*(.+?)\n\s*\|\s*(.+?)\n", texto)
    if roteador == "ERROR" and m:
        detalhe = (m.group(1) + " " + m.group(2)).strip()
    return {"inicio": inicio, "fim": fim[0][0] if fim else None, "resultado": fim[0][1] if fim else "sem fim",
            "falhas": falhas, "retentativas": retent, "roteador": roteador, "detalhe_roteador": detalhe}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--avaliador", default="Pedro Goncalves Rocha (execução automatizada pelo Claude Code)")
    args = ap.parse_args()

    linhas, minutos = [], {"limpa": [], "atualizacao": []}
    for tipo in ("limpa", "atualizacao"):
        for n in (1, 2, 3):
            log = M33 / "logs" / f"{tipo}-{n}.log"
            if not log.exists():
                continue
            r = le_log(log)
            dur = (r["fim"] - r["inicio"]) / 60 if r["inicio"] and r["fim"] else None
            sucesso = r["resultado"] == "sucesso" and not r["falhas"]
            if dur is not None:
                minutos[tipo].append(dur)
            obs = []
            if r["roteador"] == "ERROR":
                obs.append(f"admin/cli/checks.php: Router configuration (core_router) ERROR: {r['detalhe_roteador']}")
            if r["falhas"]:
                obs.append("falha no passo " + "; ".join(r["falhas"]))
            linhas.append({
                "execucao": f"{tipo}-{n}", "tipo": "instalação limpa" if tipo == "limpa" else "atualização 4.5 → 5.3",
                "data": datetime.fromtimestamp(r["inicio"]).strftime("%Y-%m-%d") if r["inicio"] else "",
                "avaliador": args.avaliador,
                "inicio": datetime.fromtimestamp(r["inicio"]).isoformat(timespec="seconds") if r["inicio"] else "",
                "fim": datetime.fromtimestamp(r["fim"]).isoformat(timespec="seconds") if r["fim"] else "",
                "minutos": f"{dur:.2f}" if dur is not None else "",
                "retentativas": len(r["retentativas"]),
                "passos_fora_da_documentacao": 0,
                "verificacao_ambiente": "ok" if not any(f.startswith("4 ") for f in r["falhas"]) else "falha",
                "login_admin": "ok" if r["resultado"] == "sucesso" else "falha",
                "checks_roteador": r["roteador"],
                "sucesso": "sim" if sucesso else "não",
                "log": f"M3.3/logs/{tipo}-{n}.log",
                "observacao": " | ".join(obs),
            })
    with open(M33 / "execucoes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)

    comp, iguais, total = [], 0, 0
    for n in (1, 2, 3):
        a, d = M35 / f"{n}-antes.csv", M35 / f"{n}-depois.csv"
        if not (a.exists() and d.exists()):
            continue
        antes = {l["item"]: l for l in csv.DictReader(open(a, encoding="utf-8"))}
        depois = {l["item"]: l for l in csv.DictReader(open(d, encoding="utf-8"))}
        for item, la in antes.items():
            vd = depois.get(item, {}).get("valor", "ausente")
            ok = la["valor"] == vd
            iguais += ok
            total += 1
            comp.append({"atualizacao": n, "item": item, "descricao": la["descricao"], "antes": la["valor"],
                         "depois": vd, "igual": "sim" if ok else "não"})
    if comp:
        with open(M35 / "comparacao.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(comp[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(comp)

    ps = sum(l["sucesso"] == "sim" for l in linhas)
    r_total = sum(l["retentativas"] for l in linhas)
    print(f"M3.3 = {ps} / {len(linhas)}")
    for tipo, v in minutos.items():
        if v:
            print(f"M3.4 {tipo}: mediana {statistics.median(v):.2f} min (execuções: {', '.join(f'{x:.2f}' for x in v)})")
    print(f"M3.4 retentativas (R) = {r_total}")
    if total:
        por = total // 3 if total % 3 == 0 else total
        print(f"M3.5 = {iguais} / {total} itens comparados (40 por atualização); "
              f"pior atualização: {min(sum(c['igual'] == 'sim' for c in comp if c['atualizacao'] == n) for n in {c['atualizacao'] for c in comp})} / {por}")


if __name__ == "__main__":
    main()
