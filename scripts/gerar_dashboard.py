"""Gera o dashboard Markdown das métricas PSM/CID (issue #27)."""

import csv
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
CONSOLIDADOS = RAIZ / "docs" / "metricas" / "dados" / "consolidados"
DESTINO = RAIZ / "docs" / "metricas" / "dashboard.md"


def ler(nome):
    with (CONSOLIDADOS / nome).open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def numero(valor):
    texto = str(valor or "").strip().replace(",", ".")
    return float(texto) if texto else None


def fmt(valor, casas=2):
    if valor is None:
        return "sem dado"
    texto = f"{valor:.{casas}f}".replace(".", ",")
    return texto.rstrip("0").rstrip(",")


def pontos(valor):
    quantidade = numero(valor)
    unidade = "ponto" if quantidade == 1 else "pontos"
    return f"{fmt(quantidade, 0)} {unidade}"


def atuais(linhas):
    correntes = [linha for linha in linhas if linha.get("historico") != "sim"]
    return correntes or linhas


def gerar_linhas():
    progresso = atuais(ler("progresso_diario.csv"))
    a1 = max(progresso, key=lambda linha: linha["data"])
    compromisso = [linha for linha in atuais(ler("comprometido_concluido.csv"))
                   if numero(linha.get("diferenca_pct")) is not None]
    a2 = max(compromisso, key=lambda linha: linha["semana"])
    fluxo = atuais(ler("fluxo_estados.csv"))
    a3 = max(fluxo, key=lambda linha: linha["data"])
    wip = sum(numero(a3.get(campo)) or 0 for campo in ("em_progresso", "em_revisao"))
    ciclos = [linha for linha in atuais(ler("cycle_time.csv"))
              if numero(linha.get("mediana_entrega")) is not None]
    b1 = ciclos[0]
    velocidade = atuais(ler("velocidade.csv"))
    b2 = max(velocidade, key=lambda linha: linha["semana"])
    projecao = numero(b2.get("semanas_restantes"))
    prazo = numero(b2.get("semanas_ate_prazo"))
    esforco = atuais(ler("esforco_consolidado.csv"))
    membros = [linha for linha in esforco if linha["nivel"] == "membro"]
    maior_desvio = max((abs(numero(linha.get("desvio_pct")) or 0) for linha in membros), default=None)
    total = next((linha for linha in esforco
                  if linha["nivel"] == "total" and linha["chave"] == "total"), None)
    acuracia = numero(total.get("acuracia")) if total else None
    contribuicao = atuais(ler("contribuicao.csv"))
    divergencia = max((numero(linha.get("divergencia_pp")) or 0 for linha in contribuicao),
                      default=None)
    conjuntos = (progresso, compromisso, fluxo, ciclos, velocidade, esforco, contribuicao)
    data = max(linha.get("data_extracao", "") for conjunto in conjuntos for linha in conjunto)
    data_br = "/".join(reversed(data.split("-")))

    return [
        ("A1 — Burndown", f"{pontos(a1['aberto_pontos'])} abertos; "
         f"desvio {fmt(numero(a1['desvio_pct']))}%", "desvio acima da linha ideal ≤ 5%",
         numero(a1["desvio_pct"]) <= 5, data_br),
        ("A2 — Comprometido × concluído", f"{a2['concluidos']}/{a2['comprometidos']} issues; "
         f"diferença {fmt(numero(a2['diferenca_pct']))}%", "diferença ≤ 5%",
         numero(a2["diferenca_pct"]) <= 5, data_br),
        ("A3 — Fluxo cumulativo", f"WIP atual: {fmt(wip, 0)} issue",
         "sem crescimento de Em Revisão por 2 semanas", numero(a3["em_revisao"]) == 0, data_br),
        ("B1 — Cycle time", f"mediana: {fmt(numero(b1['mediana_entrega']))} dia",
         "mediana ≤ 5 dias", numero(b1["mediana_entrega"]) <= 5, data_br),
        ("B2 — Velocidade", f"projeção: {fmt(projecao)} semanas; prazo: {fmt(prazo)} semana",
         "projeção ≤ semanas até o prazo", projecao is not None and prazo is not None and projecao <= prazo,
         data_br),
        ("C1 — Esforço", f"maior desvio individual: {fmt(maior_desvio)}%",
         "desvio individual entre −30% e +30%", maior_desvio is not None and maior_desvio <= 30,
         data_br),
        ("C2 — Contribuição", f"maior divergência: {fmt(divergencia)} p.p.",
         "divergência ≤ 30 p.p.", divergencia is not None and divergencia <= 30, data_br),
        ("C3 — Estimado × real", f"acurácia agregada: {fmt(acuracia)}",
         "acurácia entre 0,85 e 1,25", acuracia is not None and 0.85 <= acuracia <= 1.25,
         data_br),
    ], data_br


def figura(numero_figura, titulo, arquivo, csv):
    return (f"### Figura {numero_figura}. {titulo}\n\n"
            f"![{titulo}](graficos/{arquivo})\n\n"
            f'<p class="legenda">Figura {numero_figura}. {titulo}. Fonte: elaborado pelos autores '
            f'a partir de <a href="dados/consolidados/{csv}">{csv}</a>.</p>\n')


def main():
    linhas, data = gerar_linhas()
    tabela = ["| Medida | Valor atual | Limiar de decisão | Situação | Última atualização |",
              "|---|---:|---|:---:|:---:|"]
    for medida, valor, limiar, dentro, atualizacao in linhas:
        tabela.append(f"| {medida} | {valor} | {limiar} | "
                      f"**{'Dentro' if dentro else 'Fora'}** | {atualizacao} |")

    partes = [
        "# Dashboard das métricas PSM/CID\n",
        f"> Retrato gerado automaticamente em **{data}** a partir dos dados consolidados. "
        "Os valores de esforço dependem do apontamento da equipe e devem ser substituídos pelos "
        "registros reais quando disponíveis.\n",
        "## Tabela-resumo\n", "\n".join(tabela) + "\n",
        '<p class="legenda">Tabela 1. Situação das medidas obrigatórias. Fonte: elaborado pelos '
        'autores a partir dos CSVs consolidados e dos limiares dos '
        '<a href="02-construtos-de-medicao/">construtos de medição</a>.</p>\n',
        "A situação indica se o valor atual permanece dentro do limiar de decisão. Um resultado "
        "fora do limiar demanda análise ou ação de gestão; não significa, isoladamente, falha do projeto.\n",
        "## Calendário e Progresso\n",
        figura(1, "A1 — Burndown das entregas", "fig-a1-burndown.svg", "progresso_diario.csv"),
        figura(2, "A2 — Comprometido versus concluído", "fig-a2-comprometido-concluido.svg", "comprometido_concluido.csv"),
        figura(3, "A3 — Fluxo cumulativo", "fig-a3-fluxo-cumulativo.svg", "fluxo_estados.csv"),
        "## Desempenho dos Processos\n",
        figura(4, "B1 — Distribuição do cycle time", "fig-b1-cycle-time.svg", "cycle_time.csv"),
        figura(5, "B2 — Velocidade e média móvel", "fig-b2-velocidade.svg", "velocidade.csv"),
        "## Recursos e Custos\n",
        figura(6, "C1 — Esforço da equipe por integrante", "fig-c1-esforco.svg", "esforco_consolidado.csv"),
        figura(7, "C2 — Distribuição multidimensional da contribuição", "fig-c2-contribuicao.svg", "contribuicao.csv"),
        figura(8, "C3 — Esforço estimado versus realizado", "fig-c3-estimado-real.svg", "esforco_consolidado.csv"),
        "## Dados e scripts\n",
        "- [Diretório dos dados consolidados](dados/consolidados/README.md)\n"
        "- [Diretório dos dados brutos](dados/brutos/README.md)\n"
        "- [`consolidar_metricas.py`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/consolidar_metricas.py) — gera os CSVs consolidados\n"
        "- [`gerar_graficos.py`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/gerar_graficos.py) — gera as oito figuras\n"
        "- [`gerar_dashboard.py`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/gerar_dashboard.py) — gera esta página e a tabela-resumo\n"
        "- [`validar_dados.py`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/validar_dados.py) — verifica a consistência dos dados\n",
        "## Como atualizar\n",
        "```bash\npython scripts/consolidar_metricas.py --data-ref AAAA-MM-DD\n"
        "python scripts/gerar_graficos.py --data-ref AAAA-MM-DD\n"
        "python scripts/gerar_dashboard.py\npython scripts/validar_dados.py\n```\n",
    ]
    DESTINO.write_text("\n".join(partes), encoding="utf-8", newline="\n")
    print(f"Dashboard gerado: {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
