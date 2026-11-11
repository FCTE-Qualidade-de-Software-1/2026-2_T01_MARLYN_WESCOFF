"""Gera os indicadores gráficos da gestão PSM/CID (issue #26).

Entradas: CSVs gerados por scripts/consolidar_metricas.py.
Saída: oito SVGs em docs/metricas/graficos/ (A1, A2, A3, B1, B2, C1, C2 e C3).

O script não preenche lacunas com zero. Quando uma medida não possui observações,
gera uma figura identificando a ausência do dado e a fonte consultada.

Uso:
  python3 scripts/gerar_graficos.py
  python3 scripts/gerar_graficos.py --data-ref 2026-11-10
"""

import argparse
import csv
import math
from datetime import date, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

matplotlib.rcParams["svg.hashsalt"] = "marlyn-wescoff-psm-cid"


RAIZ = Path(__file__).resolve().parent.parent
ENTRADA_PADRAO = RAIZ / "docs" / "metricas" / "dados" / "consolidados"
SAIDA_PADRAO = RAIZ / "docs" / "metricas" / "graficos"

AZUL = "#1f4e79"
CIANO = "#38b2ac"
AMBAR = "#d99000"
VERMELHO = "#b6403a"
CINZA = "#6b7280"
VERDE = "#2f855a"
ROXO = "#6b46c1"
PALETA = [AZUL, CIANO, AMBAR, VERMELHO, VERDE, ROXO, CINZA]
MARCADORES = ["o", "s", "^", "D", "v", "P", "X"]
HACHURAS = ["//", "xx", "..", "\\\\", "++", "oo", "--"]


def ler_csv(pasta, nome, colunas):
    caminho = pasta / nome
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo obrigatório ausente: {caminho}")
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        ausentes = set(colunas) - set(leitor.fieldnames or [])
        if ausentes:
            raise ValueError(f"{nome}: colunas ausentes: {', '.join(sorted(ausentes))}")
        linhas = list(leitor)
    return caminho, linhas


def numero(valor):
    texto = str(valor or "").strip().replace(",", ".")
    try:
        return float(texto) if texto else None
    except ValueError:
        return None


def data_iso(valor):
    texto = str(valor or "").strip()
    return date.fromisoformat(texto[:10]) if texto else None


def extracao(linhas, data_ref):
    datas = sorted({l.get("data_extracao", "") for l in linhas if l.get("data_extracao")})
    return datas[-1] if datas else data_ref.isoformat()


def preparar(titulo, ylabel, xlabel="Data", figsize=(10.5, 5.8)):
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=False)
    fig.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.20)
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color="#d1d5db", linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def nota_fonte(fig, arquivo, linhas, data_ref, complemento=""):
    texto = (f"Fonte: elaborado pelos autores a partir de {arquivo.name}, "
             f"extraído em {extracao(linhas, data_ref)}.")
    if complemento:
        texto += f" {complemento}"
    fig.text(0.10, 0.035, texto, ha="left", va="bottom", fontsize=8, color="#374151")


def sem_dados(ax, mensagem):
    ax.text(0.5, 0.52, "Sem dados registrados", transform=ax.transAxes,
            ha="center", va="center", fontsize=15, fontweight="bold", color=CINZA)
    ax.text(0.5, 0.40, mensagem, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color="#4b5563", wrap=True)
    ax.set_xticks([])
    ax.set_yticks([])
    for borda in ax.spines.values():
        borda.set_color("#d1d5db")


def marcos(pasta, data_ref):
    caminho, linhas = ler_csv(pasta, "entregas.csv", ["entrega", "prazo", "data_extracao"])
    resultado = {}
    for linha in linhas:
        if linha["entrega"] in {"E1", "PC1", "E2"} and linha.get("prazo"):
            resultado[linha["entrega"]] = data_iso(linha["prazo"])
    return caminho, linhas, resultado


def desenhar_marcos(ax, valores):
    cores = {"E1": CINZA, "PC1": AMBAR, "E2": VERMELHO}
    for nome, dia in valores.items():
        ax.axvline(dia, color=cores[nome], linestyle=":", linewidth=1.5, label=f"Marco {nome}")


def salvar(fig, pasta, nome, png_artigo=False):
    destino = pasta / nome
    fig.savefig(destino, format="svg", metadata={"Date": None})
    if png_artigo:
        fig.savefig(destino.with_suffix(".png"), format="png", dpi=180,
                    metadata={"Software": "Matplotlib"})
    plt.close(fig)
    # O backend SVG do Matplotlib deixa espaços ao fim das linhas dos paths.
    # Normalizar evita ruído em revisões e mantém `git diff --check` limpo.
    conteudo = destino.read_text(encoding="utf-8")
    destino.write_text("\n".join(linha.rstrip() for linha in conteudo.splitlines()) + "\n",
                       encoding="utf-8", newline="\n")
    return destino


def grafico_a1(entrada, saida, data_ref, datas_marcos):
    arquivo, linhas = ler_csv(entrada, "progresso_diario.csv",
                              ["entrega", "data", "aberto_pontos", "ideal_pontos", "data_extracao"])
    fig, ax = preparar("A1 — Burndown das entregas", "Trabalho restante (pontos)")
    validas = [l for l in linhas if data_iso(l["data"]) <= data_ref]
    for indice, entrega in enumerate(sorted({l["entrega"] for l in validas})):
        grupo = [l for l in validas if l["entrega"] == entrega]
        x = [data_iso(l["data"]) for l in grupo]
        y = [numero(l["aberto_pontos"]) for l in grupo]
        ax.plot(x, y, color=PALETA[indice], marker=MARCADORES[indice], linewidth=2,
                label=f"Aberto — {entrega}")
        ideal = [(data_iso(l["data"]), numero(l["ideal_pontos"])) for l in grupo
                 if numero(l["ideal_pontos"]) is not None]
        if ideal:
            ax.plot([p[0] for p in ideal], [p[1] for p in ideal], color=PALETA[indice],
                    linestyle="--", marker="x", label=f"Ideal — {entrega}")
    if validas:
        xs = [data_iso(l["data"]) for l in validas]
        desenhar_marcos(ax, datas_marcos)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(ncol=2, fontsize=8)
    else:
        sem_dados(ax, "Nenhuma observação de progresso foi consolidada.")
    nota_fonte(fig, arquivo, linhas, data_ref,
               "Linhas ideais aparecem somente quando o milestone possui prazo.")
    return salvar(fig, saida, "fig-a1-burndown.svg")


def grafico_a2(entrada, saida, data_ref):
    arquivo, linhas = ler_csv(entrada, "comprometido_concluido.csv",
                              ["semana", "comprometidos", "concluidos", "pc_acumulado_pct", "data_extracao"])
    fig, ax = preparar("A2 — Comprometido versus concluído", "Quantidade de issues", "Semana ISO")
    validas = [l for l in linhas if numero(l["comprometidos"]) is not None]
    if validas:
        x = list(range(len(validas)))
        largura = 0.36
        ax.bar([i - largura / 2 for i in x], [numero(l["comprometidos"]) for l in validas],
               largura, color=AZUL, hatch=HACHURAS[0], label="Comprometidas")
        ax.bar([i + largura / 2 for i in x], [numero(l["concluidos"]) or 0 for l in validas],
               largura, color=CIANO, hatch=HACHURAS[1], label="Concluídas")
        ax.set_xticks(x, [l["semana"] for l in validas])
        ax2 = ax.twinx()
        acumulado = [numero(l["pc_acumulado_pct"]) for l in validas]
        ax2.plot(x, [v if v is not None else math.nan for v in acumulado], color=VERMELHO,
                 marker="D", linestyle="--", label="% acumulado")
        ax2.set_ylabel("Conclusão acumulada (%)")
        ax2.set_ylim(0, 105)
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, fontsize=8)
    else:
        sem_dados(ax, "O quadro ainda não possui retrato do compromisso semanal. "
                      "As semanas não foram convertidas artificialmente em zero.")
    nota_fonte(fig, arquivo, linhas, data_ref)
    return salvar(fig, saida, "fig-a2-comprometido-concluido.svg", png_artigo=True)


def grafico_a3(entrada, saida, data_ref, datas_marcos):
    estados = ["aberta_sem_estado", "backlog", "a_fazer", "em_progresso", "em_revisao", "concluido"]
    rotulos = ["Aberta sem estado", "Backlog", "A fazer", "Em progresso", "Em revisão", "Concluído"]
    arquivo, linhas = ler_csv(entrada, "fluxo_estados.csv", ["data", *estados, "data_extracao"])
    fig, ax = preparar("A3 — Fluxo cumulativo", "Quantidade de issues")
    validas = [l for l in linhas if data_iso(l["data"]) <= data_ref]
    if validas:
        x = [data_iso(l["data"]) for l in validas]
        ys = [[numero(l[e]) or 0 for l in validas] for e in estados]
        colecoes = ax.stackplot(x, *ys, colors=PALETA[:len(estados)], labels=rotulos, alpha=0.88)
        for colecao, hachura in zip(colecoes, HACHURAS):
            colecao.set_hatch(hachura)
            colecao.set_edgecolor("#ffffff")
            colecao.set_linewidth(0.3)
        desenhar_marcos(ax, datas_marcos)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(ncol=3, fontsize=7, loc="upper left")
    else:
        sem_dados(ax, "Nenhum estado diário foi consolidado.")
    nota_fonte(fig, arquivo, linhas, data_ref,
               "Sem histórico do quadro, o período mostra apenas issues abertas e concluídas.")
    return salvar(fig, saida, "fig-a3-fluxo-cumulativo.svg")


def grafico_b1(entrada, saida, data_ref):
    arquivo, linhas = ler_csv(entrada, "cycle_time.csv",
                              ["entrega", "cycle_time_dias", "historico", "mediana_entrega",
                               "p80_entrega", "p90_entrega", "data_extracao"])
    fig, ax = preparar("B1 — Distribuição do cycle time", "Quantidade de issues", "Cycle time (dias)")
    validas = [l for l in linhas if l["historico"] != "sim" and numero(l["cycle_time_dias"]) is not None]
    if validas:
        valores = [numero(l["cycle_time_dias"]) for l in validas]
        bins = max(1, min(10, len(set(valores))))
        ax.hist(valores, bins=bins, color=AZUL, edgecolor="#ffffff", hatch=HACHURAS[0], label="Issues")
        primeira = validas[0]
        for coluna, rotulo, cor, estilo in [("mediana_entrega", "Mediana", CIANO, "--"),
                                             ("p80_entrega", "P80", AMBAR, "-."),
                                             ("p90_entrega", "P90", VERMELHO, ":")]:
            valor = numero(primeira[coluna])
            if valor is not None:
                ax.axvline(valor, color=cor, linestyle=estilo, linewidth=2, label=f"{rotulo}: {valor:g} d")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(fontsize=8)
    else:
        sem_dados(ax, "Não há cycle time não histórico com conclusão registrada.")
    nota_fonte(fig, arquivo, linhas, data_ref,
               "Dados históricos da E1 são excluídos dos percentis conforme o diagnóstico.")
    return salvar(fig, saida, "fig-b1-cycle-time.svg", png_artigo=True)


def grafico_b2(entrada, saida, data_ref):
    arquivo, linhas = ler_csv(entrada, "velocidade.csv",
                              ["semana", "pontos_concluidos", "velocidade_media_3s", "data_extracao"])
    fig, ax = preparar("B2 — Velocidade e média móvel", "Pontos concluídos", "Semana ISO")
    if linhas:
        x = list(range(len(linhas)))
        ax.bar(x, [numero(l["pontos_concluidos"]) or 0 for l in linhas], color=AZUL,
               hatch=HACHURAS[0], label="Pontos concluídos")
        media = [numero(l["velocidade_media_3s"]) for l in linhas]
        ax.plot(x, [v if v is not None else math.nan for v in media], color=AMBAR,
                marker="D", linestyle="--", linewidth=2, label="Média móvel (3 semanas)")
        ax.set_xticks(x, [l["semana"] for l in linhas], rotation=20)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(fontsize=8)
    else:
        sem_dados(ax, "Nenhuma semana foi consolidada.")
    nota_fonte(fig, arquivo, linhas, data_ref)
    return salvar(fig, saida, "fig-b2-velocidade.svg")


def grafico_c1(entrada, saida, data_ref):
    arquivo, linhas = ler_csv(entrada, "esforco_consolidado.csv",
                              ["entrega", "nivel", "chave", "horas", "data_extracao"])
    fig, ax = preparar("C1 — Esforço da equipe por integrante", "Esforço (horas)", "Integrante")
    validas = [l for l in linhas if l["nivel"] == "membro" and numero(l["horas"]) is not None]
    if validas:
        nomes = [l["chave"] for l in validas]
        barras = ax.bar(range(len(validas)), [numero(l["horas"]) for l in validas], color=AZUL)
        for barra, hachura in zip(barras, (HACHURAS * 10)[:len(barras)]):
            barra.set_hatch(hachura)
        ax.set_xticks(range(len(nomes)), nomes, rotation=25, ha="right")
        media = sum(numero(l["horas"]) for l in validas) / len(validas)
        ax.axhline(media, color=AMBAR, linestyle="--", label=f"Média: {media:.1f} h")
        ax.axhspan(media * 0.7, media * 1.3, color=AMBAR, alpha=0.12, label="Faixa ±30%")
        ax.legend(fontsize=8)
    else:
        sem_dados(ax, "Nenhuma hora foi preenchida em esforço.csv. "
                      "Atividades sem quantidade não foram tratadas como zero.")
    nota_fonte(fig, arquivo, linhas, data_ref)
    return salvar(fig, saida, "fig-c1-esforco.svg")


def grafico_c2(entrada, saida, data_ref):
    dimensoes = [("pct_commits", "Commits"), ("pct_linhas", "Linhas"),
                 ("pct_issues", "Issues"), ("pct_revisoes", "Revisões"), ("pct_horas", "Horas")]
    arquivo, linhas = ler_csv(entrada, "contribuicao.csv",
                              ["entrega", "membro", *[d[0] for d in dimensoes], "data_extracao"])
    fig, ax = preparar("C2 — Distribuição multidimensional da contribuição", "Participação (%)", "Integrante",
                       figsize=(11.5, 6.2))
    validas = [l for l in linhas if l["historico"] != "sim"]
    if validas:
        x = list(range(len(validas)))
        largura = 0.15
        for indice, (coluna, rotulo) in enumerate(dimensoes):
            valores = [numero(l[coluna]) for l in validas]
            if not any(v is not None for v in valores):
                continue
            posicoes = [i + (indice - 2) * largura for i in x]
            ax.bar(posicoes, [v or 0 for v in valores], largura, color=PALETA[indice],
                   hatch=HACHURAS[indice], label=rotulo)
        nomes = [l["membro"].split()[0] for l in validas]
        ax.set_xticks(x, nomes)
        ax.set_ylim(0, 105)
        ax.legend(ncol=5, fontsize=7)
    else:
        sem_dados(ax, "Não há contribuição da entrega corrente consolidada.")
    nota_fonte(fig, arquivo, linhas, data_ref,
               "Dimensões sem observação, como horas, permanecem ausentes.")
    return salvar(fig, saida, "fig-c2-contribuicao.svg", png_artigo=True)


def grafico_c3(entrada, saida, data_ref):
    arquivo, linhas = ler_csv(entrada, "esforco_consolidado.csv",
                              ["nivel", "chave", "estimado_h", "horas", "data_extracao"])
    fig, ax = preparar("C3 — Esforço estimado versus realizado", "Esforço realizado (horas)",
                       "Esforço estimado (horas)")
    validas = [l for l in linhas if l["nivel"] == "issue" and numero(l["estimado_h"]) is not None
               and numero(l["horas"]) is not None]
    if validas:
        x = [numero(l["estimado_h"]) for l in validas]
        y = [numero(l["horas"]) for l in validas]
        ax.scatter(x, y, color=AZUL, marker="o", s=55, label="Issues")
        limite = max(x + y) * 1.08 if x + y else 1
        ax.plot([0, limite], [0, limite], color=AMBAR, linestyle="--", label="Estimado = realizado")
        ax.set_xlim(0, limite)
        ax.set_ylim(0, limite)
        ax.legend(fontsize=8)
    else:
        sem_dados(ax, "As issues possuem estimativas, mas não possuem horas realizadas. "
                      "Não foi criada uma relação estimado × zero.")
    nota_fonte(fig, arquivo, linhas, data_ref)
    return salvar(fig, saida, "fig-c3-estimado-real.svg")


def main():
    parser = argparse.ArgumentParser(description="Gera os oito indicadores obrigatórios do PSM/CID.")
    parser.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    parser.add_argument("--data-ref", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    args.saida.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.unicode_minus": False})
    _, _, datas_marcos = marcos(args.entrada, args.data_ref)
    gerados = [
        grafico_a1(args.entrada, args.saida, args.data_ref, datas_marcos),
        grafico_a2(args.entrada, args.saida, args.data_ref),
        grafico_a3(args.entrada, args.saida, args.data_ref, datas_marcos),
        grafico_b1(args.entrada, args.saida, args.data_ref),
        grafico_b2(args.entrada, args.saida, args.data_ref),
        grafico_c1(args.entrada, args.saida, args.data_ref),
        grafico_c2(args.entrada, args.saida, args.data_ref),
        grafico_c3(args.entrada, args.saida, args.data_ref),
    ]
    print("Figuras geradas:")
    for caminho in gerados:
        print(f"- {caminho.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
