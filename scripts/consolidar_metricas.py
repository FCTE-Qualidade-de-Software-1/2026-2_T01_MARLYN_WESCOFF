"""Consolida os dados brutos nas medidas da gestão PSM/CID (issue #25).

Lê docs/metricas/dados/brutos/ e grava em docs/metricas/dados/consolidados/, aplicando as fórmulas de
docs/metricas/02-construtos-de-medicao.md (o número da tabela de cada construto está entre parênteses):

  progresso_diario.csv        A1 burndown da entrega (Tabela 3)
  comprometido_concluido.csv  A2 comprometido x concluído por semana ISO (Tabela 4)
  fluxo_estados.csv           A3 fluxo cumulativo, WIP, throughput e Lei de Little (Tabela 5)
  entregas.csv                A4 conclusão de marcos (Tabela 6) e B3 frequência e concentração de véspera (Tabela 9)
  cycle_time.csv              B1 cycle time, lead time, mediana, P80, P90 e issues paradas (Tabela 7)
  velocidade.csv              B2 velocidade, média móvel de 3 semanas e projeção (Tabela 8); merges por semana (B3)
  retrabalho.csv              B4 contidas, escapadas e taxa de escape (Tabela 10)
  esforco_consolidado.csv     C1 esforço da equipe (Tabela 11) e C3 estimado x real (Tabela 13)
  contribuicao.csv            C2 distribuição de contribuição (Tabela 12)

Uso:
  python3 scripts/consolidar_metricas.py --data-ref AAAA-MM-DD

Regras:
  - nenhum consolidado é editado à mão; rodar duas vezes com os mesmos brutos gera arquivos idênticos;
  - pontos de tamanho pelas labels tamanho/P, M e G (1, 3 e 8 pontos);
  - linhas da E1 têm historico=sim e não entram em médias, medianas nem na velocidade de referência
    (Diagnóstico, lacuna L3);
  - linhas de esforco.csv sem horas são ignoradas; a coluna tipo_registro é mantida em C1 a C3;
  - datas no horário de Brasília; semanas ISO de segunda a domingo.
"""

import argparse
import csv
import json
import math
import re
import statistics
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "docs" / "metricas" / "dados" / "brutos"
CONSOLIDADOS = RAIZ / "docs" / "metricas" / "dados" / "consolidados"
EQUIPE = RAIZ / "docs" / "sobre" / "equipe.md"
BRASILIA = timezone(timedelta(hours=-3))

PONTOS = {"tamanho/P": 1, "tamanho/M": 3, "tamanho/G": 8}
CUSTO_HORA = 15.00            # docs/gestao/plano-psm.md, seção "Custo da hora"
LIMITE_PARADA_DIAS = 3        # B1, critério mantido do plano da E1
ENTREGA_CORRENTE = "E2"       # entrega de quem não tem prazo definido depois da E1
STATUS = {"backlog": "backlog", "a fazer": "a_fazer", "em progresso": "em_progresso",
          "em revisao": "em_revisao", "concluido": "concluido"}


# ================================================================ leitura

def ler_json(nome):
    caminho = BRUTOS / nome
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else []


def ler_jsonl(nome):
    caminho = BRUTOS / nome
    if not caminho.exists():
        return []
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]


def ler_csv(caminho):
    if not caminho.exists():
        return []
    with caminho.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ler_membros():
    """Integrantes oficiais: nome e usuário do GitHub da Tabela 1 de docs/sobre/equipe.md."""
    membros = []
    for linha in EQUIPE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*\d+\s*\|\s*\[([^\]]+)\]", linha)
        if m:
            membros.append({"nome": m.group(1), "login": m.group(2)})
    return membros


class Equipe:
    """Resolve nome canônico a partir do nome no Git, do nome em esforco.csv ou do login do GitHub."""

    def __init__(self, membros):
        self.nomes = [m["nome"] for m in membros]
        self.indice = {}
        for m in membros:
            self.indice[m["nome"].casefold()] = m["nome"]
            self.indice[m["login"].casefold()] = m["nome"]

    def canonico(self, quem):
        return self.indice.get((quem or "").strip().casefold())


def ler_esforco():
    """C1, C2 e C3: linhas de esforco.csv com horas; horas em branco são ignoradas."""
    linhas = []
    for l in ler_csv(BRUTOS / "esforco.csv"):
        valor = (l.get("horas") or "").strip()
        if not valor:
            continue
        try:
            horas = float(valor)
        except ValueError:
            continue                       # validar_dados.py aponta o erro de formato
        num = (l.get("issue") or "").strip().lstrip("#")
        linhas.append({**l, "horas": horas, "issue_num": int(num) if num.isdigit() else None,
                       "dia": date.fromisoformat(l["data"]) if (l.get("data") or "").strip() else None})
    return linhas


# ================================================================ utilidades

def dia(iso):
    """Data no horário de Brasília de um instante ISO do GitHub ou do Git."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(BRASILIA).date() if iso else None


def semana(d):
    ano, num, _ = d.isocalendar()
    return f"{ano}-W{num:02d}"


def segunda(d):
    return d - timedelta(days=d.weekday())


def pontos(issue):
    return sum(PONTOS.get(l["name"], 0) for l in issue["labels"])


def tem_tamanho(issue):
    return any(l["name"] in PONTOS for l in issue["labels"])


def labels(issue):
    return {l["name"] for l in issue["labels"]}


def estimativa(issue):
    """C3: valor do campo 'Estimativa (horas)' do formulário de issue (mesma regra de psm_coleta.py)."""
    m = re.search(r"###\s*Estimativa \(horas\)\s*\n+\s*([\d.,]+)", issue.get("body") or "")
    return float(m.group(1).replace(",", ".")) if m else None


def codigo(titulo):
    """Código da entrega a partir do título do milestone: 'E1 - 26/10/2026' -> 'E1'."""
    return (titulo or "").split(" ")[0] or ""


def num(valor, casas=2):
    if valor is None or valor == "":
        return ""
    if isinstance(valor, float):
        return f"{round(valor, casas):.{casas}f}".rstrip("0").rstrip(".") if not valor.is_integer() else str(int(valor))
    return valor


def percentil(valores, p):
    """Percentil com interpolação linear (método 'inclusive')."""
    v = sorted(valores)
    if not v:
        return None
    if len(v) == 1:
        return float(v[0])
    pos = (len(v) - 1) * p
    baixo = math.floor(pos)
    return v[baixo] + (v[min(baixo + 1, len(v) - 1)] - v[baixo]) * (pos - baixo)


def percentuais_100(valores):
    """Percentuais com duas casas que somam exatamente 100 (maiores restos). Total zero -> vazio."""
    total = sum(valores)
    if not total:
        return [None] * len(valores)
    brutos = [v * 10000 / total for v in valores]
    inteiros = [math.floor(b) for b in brutos]
    for i in sorted(range(len(brutos)), key=lambda i: brutos[i] - inteiros[i], reverse=True)[:10000 - sum(inteiros)]:
        inteiros[i] += 1
    return [i / 100 for i in inteiros]


# ================================================================ contexto comum

class Dados:
    def __init__(self, data_ref):
        self.data_ref = data_ref
        self.issues = [i for i in ler_json("issues.json") if dia(i["createdAt"]) <= data_ref]
        self.prs = [p for p in ler_json("prs.json") if dia(p["createdAt"]) <= data_ref]
        self.numeros_pr = {p["number"] for p in self.prs}
        self.eventos = [e for e in ler_jsonl("issue_events.jsonl") if dia(e["created_at"]) <= data_ref]
        self.milestones = ler_json("milestones.json")
        self.releases = [r for r in ler_json("releases.json") if r.get("publishedAt")]
        self.commits = [c for c in ler_csv(BRUTOS / "commits.csv") if dia(c["data"]) <= data_ref]
        self.quadro_eventos = [q for q in ler_csv(BRUTOS / "quadro_eventos.csv") if dia(q["data_hora"]) <= data_ref]
        self.retratos = [r for r in ler_csv(BRUTOS / "quadro_retratos.csv") if date.fromisoformat(r["data"]) <= data_ref]
        self.equipe = Equipe(ler_membros())
        self.esforco = [l for l in ler_esforco() if l["dia"] is None or l["dia"] <= data_ref]
        self.por_numero = {i["number"]: i for i in self.issues}

        self.prazos = {}                   # código da entrega -> prazo (date) ou None
        for m in self.milestones:
            self.prazos[codigo(m["title"])] = date.fromisoformat(m["due_on"][:10]) if m.get("due_on") else None
        self.fim_e1 = self.prazos.get("E1") or date(2026, 10, 26)

        self.fechamentos = defaultdict(list)   # issue -> [(dia, 'closed'|'reopened')]
        for e in self.eventos:
            if e["event"] in ("closed", "reopened") and e["issue"] not in self.numeros_pr:
                self.fechamentos[e["issue"]].append((dia(e["created_at"]), e["event"]))
        for v in self.fechamentos.values():
            v.sort()

        self.status = defaultdict(list)        # issue -> [(dia, status normalizado)]
        for q in self.quadro_eventos:
            if q["evento"] == "status" and q["status"]:
                self.status[int(q["issue"])].append((dia(q["data_hora"]), normalizar_status(q["status"])))
        for v in self.status.values():
            v.sort()

    # ---- entrega e histórico

    def entrega_por_data(self, d):
        if d is None:
            return ""
        if d <= self.fim_e1:
            return "E1"
        # E2 e Apresentação podem compartilhar o mesmo prazo. Nesse caso, o trabalho de execução
        # pertence à E2; "Apresentação" só recebe itens explicitamente vinculados ao milestone.
        prioridade = {"E2": 0, "PC1": 1, "Apresentação": 2}
        futuros = sorted((p, prioridade.get(c, 9), c)
                         for c, p in self.prazos.items() if p and p >= d and c != "E1")
        return futuros[0][2] if futuros else ENTREGA_CORRENTE

    def entrega_da_issue(self, issue):
        return codigo((issue.get("milestone") or {}).get("title")) or self.entrega_por_data(dia(issue["createdAt"]))

    @staticmethod
    def historico(entrega):
        return "sim" if entrega == "E1" else "nao"

    # ---- estado das issues

    def fechada_em(self, issue, d):
        """A issue estava fechada no fim do dia d? Usa os eventos closed/reopened; na falta, closedAt."""
        eventos = [ev for ev in self.fechamentos.get(issue["number"], []) if ev[0] <= d]
        if eventos:
            return eventos[-1][1] == "closed"
        return issue["state"] == "CLOSED" and dia(issue["closedAt"]) <= d

    def dia_fechamento(self, issue):
        return dia(issue["closedAt"]) if issue["state"] == "CLOSED" else None

    def status_em(self, numero, d):
        estados = [s for s in self.status.get(numero, []) if s[0] <= d]
        return estados[-1][1] if estados else None

    def dias(self):
        inicio = min(dia(i["createdAt"]) for i in self.issues)
        return [inicio + timedelta(days=k) for k in range((self.data_ref - inicio).days + 1)]

    def semanas(self):
        return sorted({segunda(d) for d in self.dias()})


def normalizar_status(nome):
    sem_acento = nome.casefold().translate(str.maketrans("áâãàéêíóôõúç", "aaaaeeiooouc"))
    return STATUS.get(sem_acento.strip(), "outro")


# ================================================================ Calendário e Progresso

def a1_progresso_diario(dd):
    """A1 (Tabela 3): Planejado(d), Concluído(d), Aberto(d), Ideal(d) e desvio %, por entrega e por dia."""
    linhas = []
    por_entrega = defaultdict(list)
    for i in dd.issues:
        if i.get("milestone"):
            por_entrega[codigo(i["milestone"]["title"])].append(i)
    for entrega, issues in sorted(por_entrega.items()):
        d0 = min(dia(i["createdAt"]) for i in issues)
        prazo = dd.prazos.get(entrega)
        fim = min(dd.data_ref, prazo) if prazo and prazo < dd.data_ref else dd.data_ref
        planejado_d0 = sum(pontos(i) for i in issues if dia(i["createdAt"]) <= d0)
        d = d0
        while d <= fim:
            existentes = [i for i in issues if dia(i["createdAt"]) <= d]
            planejado = sum(pontos(i) for i in existentes)
            concluido = sum(pontos(i) for i in existentes if dd.fechada_em(i, d))
            aberto = planejado - concluido
            ideal = desvio = None
            if prazo and prazo > d0:
                ideal = planejado_d0 * (1 - (d - d0).days / (prazo - d0).days)
                desvio = (aberto - ideal) / planejado_d0 * 100 if planejado_d0 else None
            linhas.append({"entrega": entrega, "data": d.isoformat(), "planejado_pontos": planejado,
                           "concluido_pontos": concluido, "aberto_pontos": aberto, "ideal_pontos": num(ideal),
                           "desvio_pct": num(desvio), "issues_planejadas": len(existentes),
                           "issues_concluidas": sum(dd.fechada_em(i, d) for i in existentes),
                           "issues_sem_tamanho": sum(not tem_tamanho(i) for i in existentes),
                           "prazo": prazo.isoformat() if prazo else "", "historico": dd.historico(entrega)})
            d += timedelta(days=1)
    return linhas


def a2_comprometido_concluido(dd):
    """A2 (Tabela 4): issues comprometidas na iteração (retrato de segunda) x concluídas até domingo."""
    linhas, soma_comp, soma_conc = [], 0, 0
    retratos_por_dia = defaultdict(list)
    for r in dd.retratos:
        retratos_por_dia[date.fromisoformat(r["data"])].append(r)
    for seg in dd.semanas():
        dom = seg + timedelta(days=6)
        dias_semana = sorted(d for d in retratos_por_dia if seg <= d <= dom)
        base = {"semana": semana(seg), "inicio": seg.isoformat(), "fim": dom.isoformat(),
                "entrega": dd.entrega_por_data(dom), "historico": "sim" if dom <= dd.fim_e1 else "nao"}
        if not dias_semana:
            linhas.append({**base, "comprometidos": "", "concluidos": "", "pc_pct": "", "diferenca_pct": "",
                           "pc_acumulado_pct": "", "fonte_compromisso": "sem registro de compromisso"})
            continue
        retrato = retratos_por_dia[dias_semana[0]]
        comprometidas = [int(r["issue"]) for r in retrato
                         if r.get("iteracao_inicio") and seg <= date.fromisoformat(r["iteracao_inicio"]) <= dom]
        concluidas = [n for n in comprometidas if n in dd.por_numero and dd.fechada_em(dd.por_numero[n], dom)]
        pc = len(concluidas) / len(comprometidas) * 100 if comprometidas else None
        if base["historico"] == "nao":
            soma_comp += len(comprometidas)
            soma_conc += len(concluidas)
        linhas.append({**base, "comprometidos": len(comprometidas), "concluidos": len(concluidas),
                       "pc_pct": num(pc), "diferenca_pct": num(100 - pc if pc is not None else None),
                       "pc_acumulado_pct": num(soma_conc / soma_comp * 100 if soma_comp else None),
                       "fonte_compromisso": f"retrato do quadro de {dias_semana[0].isoformat()}"})
    return linhas


def a3_fluxo_estados(dd):
    """A3 (Tabela 5): issues por estado no fim de cada dia; WIP, throughput e CT pela Lei de Little (7 dias)."""
    linhas = []
    for d in dd.dias():
        contagem = defaultdict(int)
        usou_quadro = False
        for i in dd.issues:
            if dia(i["createdAt"]) > d:
                continue
            if dd.fechada_em(i, d):
                contagem["concluido"] += 1
                continue
            estado = dd.status_em(i["number"], d)
            usou_quadro |= estado is not None
            contagem[estado if estado and estado != "concluido" else "aberta_sem_estado"] += 1
        entradas = sum(1 for i in dd.issues if dd.dia_fechamento(i) == d)
        linhas.append({"data": d.isoformat(), "aberta_sem_estado": contagem["aberta_sem_estado"],
                       "backlog": contagem["backlog"], "a_fazer": contagem["a_fazer"],
                       "em_progresso": contagem["em_progresso"], "em_revisao": contagem["em_revisao"],
                       "concluido": contagem["concluido"], "outro": contagem["outro"],
                       "wip": contagem["em_progresso"] + contagem["em_revisao"], "throughput": entradas,
                       "origem_estado": "quadro e issues" if usou_quadro else "issues (criada e fechada)",
                       "historico": "sim" if d <= dd.fim_e1 else "nao"})
    for k, l in enumerate(linhas):
        janela = linhas[max(0, k - 6):k + 1]
        wip = statistics.mean(x["wip"] for x in janela)
        th = statistics.mean(x["throughput"] for x in janela)
        l["wip_medio_7d"], l["throughput_medio_7d"] = num(wip), num(th)
        l["ct_little_7d"] = num(wip / th) if th and wip else ""
    return linhas


def a4_b3_entregas(dd):
    """A4 (Tabela 6): prazo x data real de cada marco. B3 (Tabela 9): duração, merges e concentração de véspera."""
    linhas = []
    releases = sorted(dd.releases, key=lambda r: r["publishedAt"])
    inicio = min(datetime.fromisoformat(c["data"]) for c in dd.commits) if dd.commits else None
    anterior = inicio
    marcos = {codigo(m["title"]) for m in dd.milestones}
    for r in releases:
        publicada = datetime.fromisoformat(r["publishedAt"].replace("Z", "+00:00"))
        if publicada.astimezone(BRASILIA).date() > dd.data_ref:
            continue
        entrega = codigo(r["tagName"])
        prazo = dd.prazos.get(entrega)
        no_periodo = [c for c in dd.commits if anterior < datetime.fromisoformat(c["data"]) <= publicada]
        vespera = [c for c in no_periodo if datetime.fromisoformat(c["data"]) > publicada - timedelta(hours=48)]
        linhas_periodo = sum(int(c["linhas_adicionadas"]) + int(c["linhas_removidas"]) for c in no_periodo)
        linhas_vespera = sum(int(c["linhas_adicionadas"]) + int(c["linhas_removidas"]) for c in vespera)
        merges = sum(1 for p in dd.prs if p["mergedAt"] and anterior
                     < datetime.fromisoformat(p["mergedAt"].replace("Z", "+00:00")) <= publicada)
        real = publicada.astimezone(BRASILIA).date()
        linhas.append({"entrega": entrega, "tag": r["tagName"], "prazo": prazo.isoformat() if prazo else "",
                       "publicada_em": publicada.astimezone(BRASILIA).isoformat(), "desvio_dias":
                       (real - prazo).days if prazo else "", "inicio_periodo": anterior.astimezone(BRASILIA).isoformat(),
                       "duracao_dias": num((publicada - anterior).total_seconds() / 86400, 1),
                       "linhas_periodo": linhas_periodo, "linhas_48h": linhas_vespera,
                       "concentracao_pct": num(linhas_vespera / linhas_periodo * 100 if linhas_periodo else None),
                       "prs_mergeados_periodo": merges, "historico": dd.historico(entrega)})
        anterior = publicada
        marcos.discard(entrega)
    for entrega in sorted(marcos):          # marcos ainda sem release: só o prazo (A4)
        prazo = dd.prazos.get(entrega)
        linhas.append({"entrega": entrega, "tag": "", "prazo": prazo.isoformat() if prazo else "",
                       "publicada_em": "", "desvio_dias": "", "inicio_periodo": "", "duracao_dias": "",
                       "linhas_periodo": "", "linhas_48h": "", "concentracao_pct": "",
                       "prs_mergeados_periodo": "", "historico": dd.historico(entrega)})
    return linhas


# ================================================================ Desempenho dos Processos

def b1_cycle_time(dd):
    """B1 (Tabela 7): CT = fim - início + 1; LT = fim - criação + 1; mediana, P80 e P90 por entrega; paradas."""
    ultima_atividade = defaultdict(lambda: date.min)
    for e in dd.eventos:
        ultima_atividade[e["issue"]] = max(ultima_atividade[e["issue"]], dia(e["created_at"]))
    for i in dd.issues:
        for c in i["comments"]:
            ultima_atividade[i["number"]] = max(ultima_atividade[i["number"]], dia(c["createdAt"]))
    linhas = []
    for i in sorted(dd.issues, key=lambda i: i["number"]):
        entrega = dd.entrega_da_issue(i)
        criada = dia(i["createdAt"])
        progresso = [s[0] for s in dd.status.get(i["number"], []) if s[1] == "em_progresso"]
        inicio = min(progresso) if progresso else criada
        fim = dd.dia_fechamento(i)
        ativa = max(ultima_atividade[i["number"]], criada)
        idade = (dd.data_ref - ativa).days if not fim else None
        linhas.append({"issue": i["number"], "titulo": i["title"], "entrega": entrega,
                       "estado": "fechada" if fim else "aberta", "criada": criada.isoformat(),
                       "inicio": inicio.isoformat(), "fonte_inicio": "quadro" if progresso else "criacao",
                       "fim": fim.isoformat() if fim else "",
                       "cycle_time_dias": (fim - inicio).days + 1 if fim else "",
                       "lead_time_dias": (fim - criada).days + 1 if fim else "",
                       "idade_sem_atualizacao_dias": idade if idade is not None else "",
                       "parada": "sim" if idade is not None and idade > LIMITE_PARADA_DIAS else "nao",
                       "historico": dd.historico(entrega)})
    for entrega in {l["entrega"] for l in linhas}:
        grupo = [l for l in linhas if l["entrega"] == entrega and l["cycle_time_dias"] != ""]
        valores = [l["cycle_time_dias"] for l in grupo]
        usar = valores and entrega != "E1"
        media = statistics.mean(valores) if usar else None
        estat = {"media_entrega": num(media), "mediana_entrega": num(statistics.median(valores) if usar else None),
                 "p80_entrega": num(percentil(valores, 0.8) if usar else None),
                 "p90_entrega": num(percentil(valores, 0.9) if usar else None)}
        for l in (x for x in linhas if x["entrega"] == entrega):
            l.update(estat)
            l["acima_media_10pct"] = ("sim" if l["cycle_time_dias"] > media * 1.1 else "nao") \
                if media and l["cycle_time_dias"] != "" else ""
    return linhas


def b2_velocidade(dd):
    """B2 (Tabela 8): pontos concluídos por semana, média móvel de 3 semanas, aceleração e projeção.
    B3 (Tabela 9): PRs mergeados e linhas alteradas na main por semana."""
    linhas, referencia, v_anterior = [], [], None
    prazo = dd.prazos.get(ENTREGA_CORRENTE)
    for seg in dd.semanas():
        dom = seg + timedelta(days=6)
        historico = "sim" if dom <= dd.fim_e1 else "nao"
        concluidas = [i for i in dd.issues if dd.dia_fechamento(i) and seg <= dd.dia_fechamento(i) <= dom]
        p = sum(pontos(i) for i in concluidas)
        if historico == "nao":
            referencia.append(p)
        v = statistics.mean(referencia[-3:]) if historico == "nao" and referencia else None
        aceleracao = (v - v_anterior) / v_anterior * 100 if v is not None and v_anterior else None
        abertas = [i for i in dd.issues if dd.entrega_da_issue(i) == ENTREGA_CORRENTE
                   and dia(i["createdAt"]) <= dom and not dd.fechada_em(i, dom)]
        b = sum(pontos(i) for i in abertas)
        s = math.ceil((prazo - dom).days / 7) if prazo and prazo > dom else ("0" if prazo else "")
        projecao = "" if historico == "sim" else (num(b / v) if v else "sem projeção")
        merges = sum(1 for pr in dd.prs if pr["mergedAt"] and seg <= dia(pr["mergedAt"]) <= dom)
        linhas_main = sum(int(c["linhas_adicionadas"]) + int(c["linhas_removidas"])
                          for c in dd.commits if seg <= dia(c["data"]) <= dom)
        linhas.append({"semana": semana(seg), "inicio": seg.isoformat(), "fim": dom.isoformat(),
                       "issues_concluidas": len(concluidas), "pontos_concluidos": p,
                       "velocidade_media_3s": num(v), "aceleracao_pct": num(aceleracao),
                       "backlog_pontos": b, "semanas_ate_prazo": s, "semanas_restantes": projecao,
                       "prs_mergeados": merges, "linhas_alteradas_main": linhas_main, "historico": historico})
        if historico == "nao":
            v_anterior = v
    return linhas


def b4_retrabalho(dd):
    """B4 (Tabela 10): reabertas, contidas (Changes requested + retrabalho) e escapadas (apontamento-docente)."""
    entregas = sorted({codigo(m["title"]) for m in dd.milestones})
    contagem = {e: defaultdict(int) for e in entregas}
    for i in dd.issues:
        e = dd.entrega_da_issue(i)
        if e not in contagem:
            continue
        rotulos = labels(i)
        contagem[e]["reabertas"] += sum(1 for ev in dd.fechamentos.get(i["number"], []) if ev[1] == "reopened")
        if "retrabalho" in rotulos and "apontamento-docente" in rotulos:
            contagem[e]["escapadas"] += 1
        elif "retrabalho" in rotulos:
            contagem[e]["contidas_issues"] += 1
    for pr in dd.prs:
        for r in pr["reviews"]:
            if r["state"] == "CHANGES_REQUESTED":
                e = dd.entrega_por_data(dia(r["submittedAt"]))
                if e in contagem:
                    contagem[e]["contidas_revisao"] += 1
    linhas = []
    for e in entregas:
        c = contagem[e]
        contidas = c["contidas_revisao"] + c["contidas_issues"]
        total = contidas + c["escapadas"]
        linhas.append({"entrega": e, "reabertas": c["reabertas"], "contidas_revisao": c["contidas_revisao"],
                       "contidas_issues": c["contidas_issues"], "contidas": contidas, "escapadas": c["escapadas"],
                       "taxa_escape_pct": num(c["escapadas"] / total * 100 if total else None),
                       "historico": dd.historico(e)})
    return linhas


# ================================================================ Recursos e Custos

def entrega_do_esforco(dd, linha):
    issue = dd.por_numero.get(linha["issue_num"]) if linha["issue_num"] else None
    if issue and issue.get("milestone"):
        return codigo(issue["milestone"]["title"])
    if linha["dia"]:
        return dd.entrega_por_data(linha["dia"])
    return "E1" if linha.get("tipo_registro") == "reconstruido" else ""


def c1_c3_esforco(dd):
    """C1 (Tabela 11): horas por integrante, fase e tipo, desvio da média e do previsto, custo.
    C3 (Tabela 13): acurácia R/E por issue e agregada, erro percentual médio. Agrupado por tipo_registro."""
    grupos = defaultdict(list)
    for l in dd.esforco:
        grupos[(entrega_do_esforco(dd, l), l.get("tipo_registro") or "")].append(l)
    linhas = []

    def linha(entrega, tipo, nivel, chave, **campos):
        base = {"entrega": entrega, "tipo_registro": tipo, "nivel": nivel, "chave": chave, "horas": "",
                "percentual": "", "desvio_pct": "", "previsto_h": "", "estimado_h": "", "acuracia": "",
                "erro_pct": "", "custo_rs": "", "observacao": "", "historico": dd.historico(entrega)}
        base.update({k: num(v) if isinstance(v, float) else v for k, v in campos.items()})
        linhas.append(base)

    for (entrega, tipo), itens in sorted(grupos.items()):
        total = sum(l["horas"] for l in itens)
        # C1: por integrante (todos os integrantes oficiais, mesmo com zero)
        por_membro = defaultdict(float)
        for l in itens:
            por_membro[dd.equipe.canonico(l["membro"]) or l["membro"].strip()] += l["horas"]
        media = total / len(dd.equipe.nomes) if dd.equipe.nomes else 0
        for nome in sorted(set(dd.equipe.nomes) | set(por_membro)):
            h = por_membro.get(nome, 0.0)
            linha(entrega, tipo, "membro", nome, horas=h, percentual=h / total * 100 if total else None,
                  desvio_pct=(h - media) / media * 100 if media else None)
        # C1: por fase, com o previsto pela soma das estimativas das issues da fase
        por_fase = defaultdict(float)
        for l in itens:
            por_fase[(l.get("fase") or "").strip() or "transversal"] += l["horas"]
        for fase, h in sorted(por_fase.items()):
            previsto = sum(estimativa(i) or 0 for i in dd.issues if dd.entrega_da_issue(i) == entrega and (
                f"fase/{fase}" in labels(i) if fase != "transversal" else not any(x.startswith("fase/") for x in labels(i))))
            linha(entrega, tipo, "fase", fase, horas=h, percentual=h / total * 100 if total else None,
                  previsto_h=previsto or None, desvio_pct=(h - previsto) / previsto * 100 if previsto else None)
        # C1: por tipo de atividade
        por_tipo = defaultdict(float)
        for l in itens:
            por_tipo[(l.get("tipo_atividade") or "").strip()] += l["horas"]
        for t, h in sorted(por_tipo.items()):
            linha(entrega, tipo, "tipo_atividade", t, horas=h, percentual=h / total * 100 if total else None)
        # C3: estimado x real por issue
        por_issue = defaultdict(float)
        for l in itens:
            if l["issue_num"]:
                por_issue[l["issue_num"]] += l["horas"]
        soma_r = soma_e = 0.0
        erros = []
        for n, r in sorted(por_issue.items()):
            e = estimativa(dd.por_numero[n]) if n in dd.por_numero else None
            if e:
                soma_r, soma_e = soma_r + r, soma_e + e
                erros.append(abs(r - e) / e * 100)
            linha(entrega, tipo, "issue", f"#{n}", horas=r, estimado_h=e, acuracia=r / e if e else None,
                  erro_pct=abs(r - e) / e * 100 if e else None,
                  observacao="" if e else "sem estimativa numérica: fora da acurácia")
        linha(entrega, tipo, "total", "total", horas=total, custo_rs=total * CUSTO_HORA,
              estimado_h=soma_e or None, acuracia=soma_r / soma_e if soma_e else None,
              erro_pct=statistics.mean(erros) if erros else None,
              observacao="acurácia e erro percentual médio só com as issues que têm estimativa e horas")
    # C3: issues concluídas com estimativa e sem nenhuma hora lançada, listadas à parte
    com_horas = {l["issue_num"] for l in dd.esforco if l["issue_num"]}
    for i in sorted(dd.issues, key=lambda i: i["number"]):
        if i["state"] == "CLOSED" and i["number"] not in com_horas and i["number"] not in dd.numeros_pr:
            entrega = dd.entrega_da_issue(i)
            linha(entrega, "", "issue_sem_horas", f"#{i['number']}", estimado_h=estimativa(i),
                  observacao="issue concluída sem horas lançadas em esforco.csv: fora da acurácia")
    return linhas


def c2_contribuicao(dd):
    """C2 (Tabela 12): commits, linhas, issues, revisões e horas por integrante e entrega; % por dimensão."""
    dados = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))   # entrega -> membro -> dimensão
    for c in dd.commits:
        nome = dd.equipe.canonico(c["autor"])
        if nome:
            e = dd.entrega_por_data(dia(c["data"]))
            dados[e][nome]["commits"] += 1
            dados[e][nome]["linhas"] += int(c["linhas_adicionadas"]) + int(c["linhas_removidas"])
    for i in dd.issues:
        if i["state"] != "CLOSED":
            continue
        responsaveis = [n for n in (dd.equipe.canonico(a["login"]) for a in i["assignees"]) if n]
        for nome in responsaveis:
            dados[dd.entrega_da_issue(i)][nome]["issues"] += 1 / len(responsaveis)
    for pr in dd.prs:
        autor = (pr.get("author") or {}).get("login")
        for r in pr["reviews"]:
            nome = dd.equipe.canonico(r["author"]["login"])
            if nome and r["author"]["login"] != autor:
                dados[dd.entrega_por_data(dia(r["submittedAt"]))][nome]["revisoes"] += 1
    for l in dd.esforco:
        nome = dd.equipe.canonico(l["membro"])
        if nome:
            e = entrega_do_esforco(dd, l)
            dados[e][nome]["horas"] += l["horas"]
            dados[e][nome][f"horas_{l.get('tipo_registro') or 'sem_tipo'}"] += l["horas"]

    dimensoes = ["commits", "linhas", "issues", "revisoes", "horas"]
    linhas = []
    for entrega in sorted(dados):
        nomes = sorted(set(dd.equipe.nomes))
        pct = {d: dict(zip(nomes, percentuais_100([dados[entrega][n][d] for n in nomes]))) for d in dimensoes}
        for nome in nomes:
            v = dados[entrega][nome]
            com_dado = [pct[d][nome] for d in dimensoes if pct[d][nome] is not None]
            linhas.append({"entrega": entrega, "membro": nome, "commits": int(v["commits"]),
                           "linhas": int(v["linhas"]), "issues": num(round(v["issues"], 2)),
                           "revisoes": int(v["revisoes"]), "horas": num(v["horas"]),
                           "horas_registrado": num(v["horas_registrado"]),
                           "horas_reconstruido": num(v["horas_reconstruido"]),
                           **{f"pct_{d}": num(pct[d][nome]) for d in dimensoes},
                           "divergencia_pp": num(max(com_dado) - min(com_dado)) if len(com_dado) > 1 else "",
                           "historico": dd.historico(entrega)})
    return linhas


# ================================================================ gravação

SAIDAS = [
    ("progresso_diario.csv", a1_progresso_diario, "issues.json; issue_events.jsonl; milestones.json"),
    ("comprometido_concluido.csv", a2_comprometido_concluido, "quadro_retratos.csv; issues.json; issue_events.jsonl"),
    ("fluxo_estados.csv", a3_fluxo_estados, "issues.json; issue_events.jsonl; quadro_eventos.csv"),
    ("entregas.csv", a4_b3_entregas, "releases.json; milestones.json; commits.csv; prs.json"),
    ("cycle_time.csv", b1_cycle_time, "issues.json; issue_events.jsonl; quadro_eventos.csv"),
    ("velocidade.csv", b2_velocidade, "issues.json; issue_events.jsonl; milestones.json; prs.json; commits.csv"),
    ("retrabalho.csv", b4_retrabalho, "issues.json; issue_events.jsonl; prs.json; milestones.json"),
    ("esforco_consolidado.csv", c1_c3_esforco, "esforco.csv; issues.json; milestones.json"),
    ("contribuicao.csv", c2_contribuicao, "commits.csv; issues.json; prs.json; esforco.csv; docs/sobre/equipe.md"),
]


def gravar(nome, linhas, fonte, data_ref, campos_vazios):
    extras = {"fonte": fonte, "data_extracao": data_ref.isoformat(),
              "comando_ou_query": f"python3 scripts/consolidar_metricas.py --data-ref {data_ref.isoformat()}"}
    campos = list(linhas[0]) if linhas else campos_vazios
    assert not set(campos) & set(extras), f"{nome}: coluna reservada {set(campos) & set(extras)}"
    caminho = CONSOLIDADOS / nome
    with caminho.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos + list(extras), lineterminator="\n")
        escritor.writeheader()
        escritor.writerows({**l, **extras} for l in linhas)
    print(f"{caminho.relative_to(RAIZ)}: {len(linhas)} linhas")


CAMPOS_VAZIOS = {
    "esforco_consolidado.csv": ["entrega", "tipo_registro", "nivel", "chave", "horas", "percentual", "desvio_pct",
                                "previsto_h", "estimado_h", "acuracia", "erro_pct", "custo_rs", "observacao",
                                "historico"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-ref", type=date.fromisoformat, default=datetime.now(BRASILIA).date(),
                        help="data de corte AAAA-MM-DD (padrão: hoje, em Brasília)")
    args = parser.parse_args()
    CONSOLIDADOS.mkdir(parents=True, exist_ok=True)
    dd = Dados(args.data_ref)
    for nome, funcao, fonte in SAIDAS:
        gravar(nome, funcao(dd), fonte, args.data_ref, CAMPOS_VAZIOS.get(nome, ["sem_dados"]))


if __name__ == "__main__":
    main()
