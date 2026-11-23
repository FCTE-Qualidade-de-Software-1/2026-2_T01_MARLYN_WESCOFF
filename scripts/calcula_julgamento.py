"""Calcula as 12 métricas, aplica os níveis de pontuação e julga G1 a G3 (Fase 4, issue #72).

Entrada: dados/avaliacao/calculos.csv, uma linha por métrica, com as medidas básicas preenchidas pelos
coletores a partir dos CSVs de cada métrica:
  numerador, denominador   M = numerador / denominador (todas, menos M3.4)
  valor_direto             M3.4: mediana do tempo de instalação, em minutos
  retentativas             M3.4: R, número de retentativas
  condicao                 condições das métricas com regra especial, separadas por ";":
                             M1.2  so_prazo (divergência só em prazo, sem alterar nota) | nota_final_errada
                             M2.4  recuperacao_sem_intervencao
                             M3.5  perda_nao_academica (1 item não acadêmico) | perda_academica

Regras aplicadas, sem nenhuma alteração (docs/fase-2/niveis-e-julgamento.md):
  - níveis de pontuação da Tabela 2: a nota 4 exige o valor exato de 1,00; os demais degraus comparam o
    valor com 2 casas decimais, como na tabela (por exemplo, 11/12 = 0,9167 vira 0,92 e recebe nota 3);
  - questão: mínimo das notas das suas métricas (Q1.1 = M1.1 e M1.3; Q2.2 = M2.1 e M2.2; Q3.3 = M3.3 e
    M3.4; as demais têm uma métrica só, issue #108);
  - objetivo: pior caso (Tabela 4): todas >= 3 Atende; nenhuma 1 e alguma 2 Atende com ressalvas;
    alguma 1 Não atende;
  - hipóteses H1.1 a H3.4 (docs/fase-2/objetivos-questoes-hipoteses.md), na parte numérica.

Saídas:
  dados/avaliacao/julgamento_metricas.csv    valor, nota e hipótese de cada métrica
  dados/avaliacao/julgamento_objetivos.csv   notas das questões e julgamento de G1, G2 e G3
  resumo em Markdown na saída padrão, para a página de resultados (#75) e o artigo (#76)

Uma métrica sem medidas preenchidas fica "pendente", e o objetivo dela fica "incompleto".

Uso:
  python3 scripts/calcula_julgamento.py
"""

import argparse
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AVALIACAO = RAIZ / "dados" / "avaliacao"

# Tabela 2 de Níveis de pontuação e julgamento: (limite mínimo da nota 3, limite mínimo da nota 2).
# A nota 4 exige 1,00 em todas estas métricas. None = o nível não existe para a métrica.
NIVEIS = {
    "M1.1": (0.92, 0.83), "M1.3": (0.92, 0.75),
    "M2.1": (0.85, 0.70), "M2.2": (0.99, 0.95), "M2.3": (0.83, 0.66),
    "M3.1": (0.875, 0.75), "M3.2": (0.92, 0.83), "M3.3": (0.83, 0.66),
}
# M3.4: (mediana máxima em minutos, R máximo) para as notas 4, 3 e 2. Valores candidatos da Fase 2; se o
# piloto (#66) congelar outros limites em ata, atualizar aqui com a referência da ata.
NIVEIS_M34 = [(4, 15, 0), (3, 30, 1), (2, 60, 3)]

QUESTAO_DO_OBJETIVO = {"G1": ["Q1.1", "Q1.2", "Q1.3"], "G2": ["Q2.1", "Q2.2", "Q2.3", "Q2.4"],
                       "G3": ["Q3.1", "Q3.2", "Q3.3", "Q3.4"]}
METRICAS_DA_QUESTAO = {"Q1.1": ["M1.1", "M1.3"], "Q1.2": ["M1.2"], "Q1.3": ["M1.3"], "Q2.1": ["M2.1"],
                       "Q2.2": ["M2.1", "M2.2"], "Q2.3": ["M2.3"], "Q2.4": ["M2.4"], "Q3.1": ["M3.1"],
                       "Q3.2": ["M3.2"], "Q3.3": ["M3.3", "M3.4"], "Q3.4": ["M3.5"]}
DECISAO = {"G1": "D1", "G2": "D2", "G3": "D3"}
ACAO = {"Atende": "Prosseguir",
        "Atende com ressalvas": "Prosseguir com as ações de mitigação listadas no relatório",
        "Não atende": "Não prosseguir sem correção ou contorno documentado; candidata à ação de melhoria (D4)",
        "incompleto": "Aguardar as métricas pendentes"}

# Parte numérica das hipóteses: o valor esperado (baseline), que não é o critério de julgamento (#109).
# Texto completo em objetivos-questoes-hipoteses.md.
HIPOTESES = {
    "M1.1": ("H1.1", "12 de 12 tarefas com função", lambda v, r: v >= 1.0),
    "M1.2": ("H1.2", "todos os casos iguais ao oráculo", lambda v, r: v >= 1.0),
    "M1.3": ("H1.3", "11 de 12 tarefas sem contorno (só a restauração de backup)",
             lambda v, r: abs(v - 11 / 12) < 1e-9),
    "M2.1": ("H2.1", "6 ou 7 de 7 formatos", lambda v, r: v >= 6 / 7 - 1e-9),
    "M2.2": ("H2.2", "todos os registros iguais à referência", lambda v, r: v >= 1.0),
    "M2.3": ("H2.3", "6 de 6 funções", lambda v, r: v >= 1.0),
    "M2.4": ("H2.4", "3 de 3 entidades vizinhas sem efeito", lambda v, r: v >= 1.0),
    "M3.1": ("H3.1", "7 ou 8 de 8 no pior ambiente (conferir também se os 3 desktops concluem tudo)",
             lambda v, r: v >= 7 / 8 - 1e-9),
    "M3.2": ("H3.2", "mesmo resultado nas 12 tarefas com PHP 8.3 e 8.4", lambda v, r: v >= 1.0),
    "M3.3": ("H3.3", "5 de 6 (conferir também se as 3 limpas concluem e a falha é por public/)",
             lambda v, r: abs(v - 5 / 6) < 1e-9),
    "M3.4": ("H3.3", "instalação limpa em menos de 15 min", lambda v, r: v < 15),
    "M3.5": ("H3.4", "40 de 40 itens iguais", lambda v, r: v >= 1.0),
}


def duas_casas(valor):
    return float(Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def nota(metrica, valor, retentativas=None, condicoes=()):
    """Nota de 1 a 4 de uma métrica, pela Tabela 2 de Níveis de pontuação e julgamento."""
    if metrica == "M3.4":
        r = retentativas or 0
        for n, minutos, r_max in NIVEIS_M34:
            if valor <= minutos and r <= r_max:
                return n
        return 1
    exato = valor >= 1.0  # a nota 4 exige 1,00 exato, sem arredondar
    v = duas_casas(valor)  # os demais degraus usam 2 casas, como a Tabela 2
    if metrica == "M1.2":
        if "nota_final_errada" in condicoes:
            return 1
        if exato:
            return 4
        return 2 if v >= 0.95 and "so_prazo" in condicoes else 1
    if metrica == "M2.4":
        if exato:
            return 4
        return 2 if v >= 0.66 and "recuperacao_sem_intervencao" in condicoes else 1
    if metrica == "M3.5":
        if "perda_academica" in condicoes:
            return 1
        if exato:
            return 4
        return 2 if v >= 0.975 and "perda_nao_academica" in condicoes else 1
    n3, n2 = NIVEIS[metrica]
    if exato:
        return 4
    if v >= n3:
        return 3
    if v >= n2:
        return 2
    return 1


def julga_objetivo(notas):
    if any(n is None for n in notas):
        return "incompleto"
    if any(n == 1 for n in notas):
        return "Não atende"
    if any(n == 2 for n in notas):
        return "Atende com ressalvas"
    return "Atende"


def numero(texto):
    texto = (texto or "").strip().replace(",", ".")
    return float(texto) if texto else None


def calcula(linhas):
    """Recebe as linhas de calculos.csv e devolve (métricas, questões, objetivos)."""
    metricas = {}
    for l in linhas:
        m = l["metrica"].strip()
        condicoes = {c.strip() for c in (l.get("condicao") or "").split(";") if c.strip()}
        if m == "M3.4":
            valor, r = numero(l.get("valor_direto")), numero(l.get("retentativas"))
        else:
            num, den = numero(l.get("numerador")), numero(l.get("denominador"))
            valor = num / den if num is not None and den else None
            r = None
        if valor is None:
            metricas[m] = {"metrica": m, "valor": None, "nota": None, "hipotese": HIPOTESES[m][0],
                           "criterio_hipotese": HIPOTESES[m][1], "resultado_hipotese": "pendente"}
            continue
        h, criterio, teste = HIPOTESES[m]
        metricas[m] = {"metrica": m, "valor": round(valor, 4), "nota": nota(m, valor, r, condicoes),
                       "hipotese": h, "criterio_hipotese": criterio,
                       "resultado_hipotese": "confirmada" if teste(valor, r) else "refutada"}
    questoes = {q: (min(metricas[m]["nota"] for m in ms) if all(metricas.get(m, {}).get("nota") for m in ms)
                    else None) for q, ms in METRICAS_DA_QUESTAO.items()}
    objetivos = {}
    for g, qs in QUESTAO_DO_OBJETIVO.items():
        j = julga_objetivo([questoes[q] for q in qs])
        objetivos[g] = {"objetivo": g, "notas_questoes": "; ".join(f"{q}={questoes[q] or '-'}" for q in qs),
                        "julgamento": j, "decisao": DECISAO[g], "acao": ACAO[j]}
    return metricas, questoes, objetivos


def main(argv=None):
    p = argparse.ArgumentParser(description="Notas e julgamento da Fase 4 a partir de calculos.csv.")
    p.add_argument("--entrada", default=str(AVALIACAO / "calculos.csv"))
    p.add_argument("--saida", default=str(AVALIACAO))
    a = p.parse_args(argv)
    with open(a.entrada, encoding="utf-8-sig") as f:
        metricas, questoes, objetivos = calcula(list(csv.DictReader(f)))

    saida = Path(a.saida)
    with open(saida / "julgamento_metricas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metrica", "valor", "nota", "hipotese", "criterio_hipotese",
                                          "resultado_hipotese"])
        w.writeheader()
        w.writerows(metricas[m] for m in sorted(metricas))
    with open(saida / "julgamento_objetivos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["objetivo", "notas_questoes", "julgamento", "decisao", "acao"])
        w.writeheader()
        w.writerows(objetivos.values())

    print("| Métrica | Valor | Nota | Hipótese | Resultado |\n|---|---|---|---|---|")
    for m in sorted(metricas):
        d = metricas[m]
        valor = "pendente" if d["valor"] is None else f"{d['valor']:.2f}".replace(".", ",")
        print(f"| {m} | {valor} | {d['nota'] or '-'} | {d['hipotese']} | {d['resultado_hipotese']} |")
    print("\n| Objetivo | Notas das questões | Julgamento | Decisão |\n|---|---|---|---|")
    for g, d in objetivos.items():
        print(f"| {g} | {d['notas_questoes']} | {d['julgamento']} | {d['decisao']}: {d['acao']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
