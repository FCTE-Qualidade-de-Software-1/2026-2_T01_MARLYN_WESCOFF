"""Gera a árvore GQM de resultados da Fase 4: docs/fase-4/arvore-gqm-resultados.md.

Na Fase 4 o GQM é lido de baixo para cima (Aula 08): cada métrica medida vira uma nota, a nota da
questão é o mínimo das notas das suas métricas, e o objetivo é julgado pelo pior caso. Esta página
mostra esse caminho em uma árvore Métrica → Questão → Objetivo, colorida pela nota, e em uma tabela
por objetivo, com o resultado de cada hipótese.

Tudo vem de dados/avaliacao/calculos.csv, pelas mesmas regras de scripts/calcula_julgamento.py; os
nomes curtos das questões e métricas vêm do Mermaid de docs/fase-2/diagrama-gqm.md. Uma métrica sem
medidas preenchidas aparece como "pendente". Rode de novo sempre que calculos.csv mudar; o teste
test_arvore_resultados.py falha se a página estiver desatualizada.

Uso:
  python3 scripts/gera_arvore_resultados.py           # grava a página
  python3 scripts/gera_arvore_resultados.py --stdout  # só mostra
"""

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calcula_julgamento as cj  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CALCULOS = RAIZ / "dados" / "avaliacao" / "calculos.csv"
DIAGRAMA = RAIZ / "docs" / "fase-2" / "diagrama-gqm.md"
SAIDA = RAIZ / "docs" / "fase-4" / "arvore-gqm-resultados.md"
NIVEL = {4: "Excelente", 3: "Bom", 2: "Insuficiente", 1: "Crítico"}


def rotulos():
    """Nomes curtos do Mermaid da Fase 2: 'Q1.1' -> 'O núcleo dá conta das tarefas?'."""
    nomes = {}
    for m in re.finditer(r'^\s*([GQM])(\d)(\d?)\["([GQM]\d(?:\.\d)?)\s*·?\s*([^"]*)"\]', DIAGRAMA.read_text(
            encoding="utf-8"), re.M):
        nomes[m.group(4)] = m.group(5).strip()
    return nomes


def valor_txt(m):
    if m["valor"] is None:
        return "pendente"
    if m["metrica"] == "M3.4":
        return f"{m['valor']:g} min".replace(".", ",")
    return f"{m['valor']:.2f}".replace(".", ",")


def classe(nota):
    return f"n{nota}" if nota else "pend"


def gera():
    with open(CALCULOS, encoding="utf-8-sig") as f:
        metricas, questoes, objetivos = cj.calcula(list(csv.DictReader(f)))
    nomes = rotulos()
    coletadas = sum(m["valor"] is not None for m in metricas.values())

    l = ["# Árvore GQM de resultados", "",
         "<!-- Página gerada por scripts/gera_arvore_resultados.py a partir de dados/avaliacao/calculos.csv. "
         "Não editar à mão. -->", "",
         "Na Fase 2 o GQM foi definido de cima para baixo: objetivo, questões e métricas "
         "([Diagrama GQM](../fase-2/diagrama-gqm.md)). Na Fase 4 ele é **interpretado de baixo para cima**: "
         "cada métrica medida recebe uma nota pelos [níveis de pontuação](../fase-2/niveis-e-julgamento.md), "
         "a nota da questão é o mínimo das notas das suas métricas e o objetivo é julgado pelo pior caso entre "
         "as questões.", "",
         f"!!! info \"Situação da coleta: {coletadas} de {len(metricas)} métricas\"",
         "    Gerada a partir de `dados/avaliacao/calculos.csv`. Métricas ainda sem medidas aparecem em cinza, "
         "como *pendente*, e o objetivo correspondente fica *incompleto*.", "",
         "## Árvore", "", "```mermaid", "flowchart BT"]
    for g, qs in cj.QUESTAO_DO_OBJETIVO.items():
        o = objetivos[g]
        l.append(f'    {g.replace(".", "")}["<b>{g} · {nomes.get(g, "")}</b><br/>{o["julgamento"]}"]:::'
                 f'{ {"Atende": "n4", "Atende com ressalvas": "n2", "Não atende": "n1"}.get(o["julgamento"], "pend")}')
        for q in qs:
            nq = questoes[q]
            l.append(f'    {q.replace(".", "")}["<b>{q}</b> {nomes.get(q, "")}<br/>'
                     f'{"nota " + str(nq) if nq else "pendente"}"]:::{classe(nq)}')
            l.append(f"    {q.replace('.', '')} --> {g}")
    for m_id, m in metricas.items():
        hip = m["resultado_hipotese"]
        detalhe = f"{valor_txt(m)} · nota {m['nota']}<br/>{m['hipotese']} {hip}" if m["nota"] else "pendente"
        l.append(f'    {m_id.replace(".", "")}["<b>{m_id}</b> {nomes.get(m_id, "")}<br/>{detalhe}"]:::'
                 f'{classe(m["nota"])}')
    for q, ms in cj.METRICAS_DA_QUESTAO.items():
        for m_id in ms:
            l.append(f"    {m_id.replace('.', '')} --> {q.replace('.', '')}")
    l += ["    classDef n4 fill:#c8e6c9,stroke:#2e7d32,color:#1b1b1b",
          "    classDef n3 fill:#e6f4d7,stroke:#558b2f,color:#1b1b1b",
          "    classDef n2 fill:#ffe0b2,stroke:#ef6c00,color:#1b1b1b",
          "    classDef n1 fill:#ffcdd2,stroke:#c62828,color:#1b1b1b",
          "    classDef pend fill:#eeeeee,stroke:#9e9e9e,color:#555555,stroke-dasharray:4 3",
          "```", "",
          "<p class=\"legenda\">Figura 1. Árvore GQM de resultados, das métricas (embaixo) aos objetivos (em cima). "
          "Verde: nota 4 ou 3; laranja: nota 2; vermelho: nota 1; cinza tracejado: pendente. "
          "Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>", "",
          "## Por objetivo", ""]
    n_tab = 0
    for g, qs in cj.QUESTAO_DO_OBJETIVO.items():
        o = objetivos[g]
        n_tab += 1
        l += [f"### {g} – {nomes.get(g, '')}", "",
              f"**Julgamento: {o['julgamento']}.** Decisão {o['decisao']}: {o['acao']}.", "",
              "| Questão | Métricas (valor · nota) | Nota da questão | Hipóteses |", "|---|---|---|---|"]
        for q in qs:
            ms = cj.METRICAS_DA_QUESTAO[q]
            txt = "<br>".join(f"{m} {valor_txt(metricas[m])}" + (f" · {metricas[m]['nota']}" if metricas[m]["nota"]
                                                                   else "") for m in ms)
            hips = "<br>".join(sorted({f"{metricas[m]['hipotese']}: {metricas[m]['resultado_hipotese']}"
                                       for m in ms}))
            nq = questoes[q]
            l.append(f"| **{q}** {nomes.get(q, '')} | {txt} | {f'{nq} ({NIVEL[nq]})' if nq else 'pendente'} | {hips} |")
        l += ["", f"<p class=\"legenda\">Tabela {n_tab}. Notas das questões de {g}: mínimo das notas das métricas. "
                  "Fonte: elaborado pelos autores a partir de <code>dados/avaliacao/calculos.csv</code>.</p>", ""]
    l += ["As evidências de cada métrica estão em `dados/avaliacao/<métrica>/` no repositório, e as hipóteses "
          "refutadas são explicadas pelas [medidas de contexto](../fase-2/abstraction-sheets.md) de cada coleta."]
    return "\n".join(l) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stdout", action="store_true")
    texto = gera()
    if ap.parse_args().stdout:
        print(texto, end="")
    else:
        SAIDA.write_text(texto, encoding="utf-8")
        print(f"gravado {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
