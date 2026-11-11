"""Valida os dados brutos e consolidados da gestão PSM/CID (issue #25).

Verificações (erro faz o script terminar com código 1; aviso só é listado):
  1. Datas invertidas: issue ou PR fechado antes de criado, PR mergeado antes de criado,
     milestone fechado antes de criado, revisão antes da abertura do PR.          (A1, A3, B1, B3)
  2. Integrantes fora da lista oficial de docs/sobre/equipe.md: esforco.csv, autores de commit,
     responsáveis pelas issues e revisores de PR.                                 (C1, C2)
  3. Percentuais de C2 que não somam 100 em cada entrega e dimensão.               (C2)
  4. esforco.csv: linha sem tipo_registro ou com valor inválido, horas com vírgula ou não numéricas,
     horas sem data, data em formato errado ou depois da data de corte.            (C1, C3)
  5. Todo CSV bruto e consolidado tem as colunas fonte, data_extracao e comando_ou_query.

Uso:
  python3 scripts/validar_dados.py [--data-ref AAAA-MM-DD]
"""

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date, datetime

from consolidar_metricas import (BRASILIA, BRUTOS, CONSOLIDADOS, RAIZ, Equipe, ler_csv, ler_json,
                                 ler_membros)

TIPOS_REGISTRO = {"registrado", "reconstruido"}
ROBOS = {"github-actions[bot]"}
COLUNAS_ORIGEM = {"fonte", "data_extracao", "comando_ou_query"}
TOLERANCIA_PCT = 0.01


class Relatorio:
    def __init__(self):
        self.erros, self.avisos = [], []

    def erro(self, msg):
        self.erros.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)


def instante(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def checar_datas(rel):
    """1. Datas invertidas em issues, PRs, revisões e milestones."""
    for i in ler_json("issues.json"):
        if i["closedAt"] and instante(i["closedAt"]) < instante(i["createdAt"]):
            rel.erro(f"issues.json: issue #{i['number']} fechada antes de criada")
    for p in ler_json("prs.json"):
        criado = instante(p["createdAt"])
        for campo in ("mergedAt", "closedAt"):
            if p.get(campo) and instante(p[campo]) < criado:
                rel.erro(f"prs.json: PR #{p['number']} com {campo} antes da criação")
        for r in p["reviews"]:
            if r.get("submittedAt") and instante(r["submittedAt"]) < criado:
                rel.erro(f"prs.json: revisão do PR #{p['number']} antes da abertura do PR")
    for m in ler_json("milestones.json"):
        if m.get("closed_at") and instante(m["closed_at"]) < instante(m["created_at"]):
            rel.erro(f"milestones.json: milestone '{m['title']}' fechado antes de criado")


def checar_integrantes(rel, equipe):
    """2. Todo nome ou login precisa corresponder a um integrante de docs/sobre/equipe.md."""
    for n, l in enumerate(ler_csv(BRUTOS / "esforco.csv"), start=2):
        if not equipe.canonico(l.get("membro")):
            rel.erro(f"esforco.csv, linha {n}: integrante '{l.get('membro')}' fora de docs/sobre/equipe.md")
    for c in ler_csv(BRUTOS / "commits.csv"):
        if c["autor"] not in ROBOS and not equipe.canonico(c["autor"]):
            rel.erro(f"commits.csv: autor '{c['autor']}' do commit {c['sha']} fora da equipe "
                     "(acrescente a identidade ao .mailmap)")
    for i in ler_json("issues.json"):
        for a in i["assignees"]:
            if not equipe.canonico(a["login"]):
                rel.erro(f"issues.json: responsável '{a['login']}' da issue #{i['number']} fora da equipe")
    for p in ler_json("prs.json"):
        for r in p["reviews"]:
            if not equipe.canonico(r["author"]["login"]):
                rel.aviso(f"prs.json: revisor '{r['author']['login']}' do PR #{p['number']} fora da equipe")


def checar_contribuicao(rel):
    """3. Em contribuicao.csv, cada dimensão soma 100% por entrega (ou está toda vazia)."""
    somas = defaultdict(lambda: defaultdict(float))
    vazias = defaultdict(lambda: defaultdict(int))
    linhas = ler_csv(CONSOLIDADOS / "contribuicao.csv")
    if not linhas:
        rel.erro("contribuicao.csv não existe ou está vazio: rode consolidar_metricas.py")
        return
    for l in linhas:
        for coluna, valor in l.items():
            if coluna.startswith("pct_"):
                if valor == "":
                    vazias[l["entrega"]][coluna] += 1
                else:
                    somas[l["entrega"]][coluna] += float(valor)
    for entrega, colunas in somas.items():
        for coluna, soma in colunas.items():
            if vazias[entrega][coluna]:
                rel.erro(f"contribuicao.csv: {entrega}, {coluna} tem valores vazios e preenchidos")
            elif abs(soma - 100) > TOLERANCIA_PCT:
                rel.erro(f"contribuicao.csv: {entrega}, {coluna} soma {soma:.2f}%, e não 100%")


def checar_esforco(rel, data_ref):
    """4. Formato do apontamento manual de esforço."""
    for n, l in enumerate(ler_csv(BRUTOS / "esforco.csv"), start=2):
        tipo = (l.get("tipo_registro") or "").strip()
        if not tipo:
            rel.erro(f"esforco.csv, linha {n}: sem tipo_registro")
        elif tipo not in TIPOS_REGISTRO:
            rel.erro(f"esforco.csv, linha {n}: tipo_registro '{tipo}' inválido (use registrado ou reconstruido)")
        horas = (l.get("horas") or "").strip()
        data = (l.get("data") or "").strip()
        if horas:
            if "," in horas:
                rel.erro(f"esforco.csv, linha {n}: horas '{horas}' com vírgula (use ponto decimal)")
            else:
                try:
                    if float(horas) <= 0:
                        rel.erro(f"esforco.csv, linha {n}: horas deve ser maior que 0")
                except ValueError:
                    rel.erro(f"esforco.csv, linha {n}: horas '{horas}' não é número")
            if not data:
                rel.erro(f"esforco.csv, linha {n}: horas lançadas sem data")
        elif tipo == "registrado":
            rel.erro(f"esforco.csv, linha {n}: registro do dia sem horas")
        if data:
            try:
                if date.fromisoformat(data) > data_ref:
                    rel.erro(f"esforco.csv, linha {n}: data {data} depois da data de corte")
            except ValueError:
                rel.erro(f"esforco.csv, linha {n}: data '{data}' fora do formato AAAA-MM-DD")
    pendentes = sum(1 for l in ler_csv(BRUTOS / "esforco.csv") if not (l.get("horas") or "").strip())
    if pendentes:
        rel.aviso(f"esforco.csv: {pendentes} linhas ainda sem horas (ignoradas nos consolidados)")


def checar_colunas_origem(rel):
    """5. Regra de integridade: todo CSV declara fonte, data_extracao e comando_ou_query."""
    for pasta in (BRUTOS, CONSOLIDADOS):
        for caminho in sorted(pasta.glob("*.csv")):
            if caminho.name == "esforco.csv":
                continue                  # preenchimento manual; a origem é o próprio integrante
            with caminho.open(encoding="utf-8", newline="") as f:
                cabecalho = set(next(csv.reader(f), []))
            faltam = COLUNAS_ORIGEM - cabecalho
            if faltam:
                rel.erro(f"{caminho.relative_to(RAIZ)}: faltam as colunas {', '.join(sorted(faltam))}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-ref", type=date.fromisoformat, default=datetime.now(BRASILIA).date())
    args = parser.parse_args()
    rel = Relatorio()
    equipe = Equipe(ler_membros())
    if not equipe.nomes:
        rel.erro("docs/sobre/equipe.md: tabela de integrantes não encontrada")
    checar_datas(rel)
    checar_integrantes(rel, equipe)
    checar_contribuicao(rel)
    checar_esforco(rel, args.data_ref)
    checar_colunas_origem(rel)
    for a in rel.avisos:
        print(f"AVISO  {a}")
    for e in rel.erros:
        print(f"ERRO   {e}")
    print(f"\n{len(rel.erros)} erro(s), {len(rel.avisos)} aviso(s).")
    sys.exit(1 if rel.erros else 0)


if __name__ == "__main__":
    main()
