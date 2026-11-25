"""Cliente REST de M2.3 (serviços web), issue #69.

Chama as 6 funções da Fase 2 (docs/fase-2/metricas.md, M2.3) com parâmetros conhecidos da massa
(dados/avaliacao/massa/massa.json e notas.csv), salva cada resposta JSON em dados/avaliacao/M2.3/ e
registra o resultado em M2.3/resultados.csv.

Critério de sucesso, fixado no plano da Fase 3 antes da coleta (regra R1): HTTP 200, resposta sem o
campo "exception" e valores iguais aos da massa aplicada na instância, que são os que a interface
web exibe. Cada conferência feita está na coluna "conferencia" do CSV.

O token vem da variável de ambiente MOODLE_TOKEN e nunca é gravado: o script falha se encontrar o
token em algum arquivo que vai salvar.

Uso:
  MOODLE_URL=http://localhost:8080 MOODLE_TOKEN=... python3 scripts/cliente_rest.py [--avaliador MS]
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MASSA = RAIZ / "dados" / "avaliacao" / "massa"
SAIDA = RAIZ / "dados" / "avaliacao" / "M2.3"
FUNCOES = ["core_webservice_get_site_info", "core_user_get_users_by_field",
           "core_course_get_courses_by_field", "core_enrol_get_enrolled_users",
           "mod_assign_get_assignments", "gradereport_user_get_grade_items"]


def achata(parametros, prefixo=""):
    """Converte listas e dicionários na notação do Moodle: courseids[0]=2, values[0]=est01."""
    saida = {}
    for chave, valor in parametros.items():
        nome = f"{prefixo}[{chave}]" if prefixo else str(chave)
        if isinstance(valor, dict):
            saida.update(achata(valor, nome))
        elif isinstance(valor, list):
            saida.update(achata(dict(enumerate(valor)), nome))
        else:
            saida[nome] = valor
    return saida


def chama(url, token, funcao, parametros):
    corpo = {"wstoken": token, "wsfunction": funcao, "moodlewsrestformat": "json"}
    corpo.update(achata(parametros))
    pedido = urllib.request.Request(f"{url}/webservice/rest/server.php",
                                    data=urllib.parse.urlencode(corpo).encode())
    try:
        with urllib.request.urlopen(pedido, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"erro_http": e.reason}


def confere(funcao, resposta, massa, notas, contexto):
    """Devolve (coerente, lista de conferências) comparando a resposta com a massa."""
    cat = massa["catalogo"]
    if funcao == "core_webservice_get_site_info":
        nomes = {f["name"] for f in resposta.get("functions", [])}
        itens = [("username = integracao", resposta.get("username") == "integracao"),
                 ("as 6 funções aparecem no serviço", set(FUNCOES) <= nomes),
                 ("release 5.3", str(resposta.get("release", "")).startswith("5.3"))]
    elif funcao == "core_user_get_users_by_field":
        esperado = massa["contas"]["estudantes"][0]
        u = resposta[0] if resposta else {}
        itens = [(f"{c} = {esperado[c]}", u.get(c) == esperado[c])
                 for c in ("username", "firstname", "lastname", "email", "idnumber")]
        contexto["userid"] = u.get("id")
    elif funcao == "core_course_get_courses_by_field":
        c = (resposta.get("courses") or [{}])[0]
        itens = [(f"shortname = {cat['curso']['shortname']}", c.get("shortname") == cat["curso"]["shortname"]),
                 ("fullname igual ao da massa", c.get("fullname") == cat["curso"]["fullname"])]
        contexto["courseid"] = c.get("id")
    elif funcao == "core_enrol_get_enrolled_users":
        recebidos = {u.get("username") for u in resposta}
        esperados = {e["username"] for e in massa["contas"]["estudantes"]} | {massa["contas"]["docente"]["username"]}
        itens = [(f"{len(esperados)} matriculados (30 estudantes e o docente)", len(resposta) == len(esperados)),
                 ("mesmos usernames da massa", recebidos == esperados)]
    elif funcao == "mod_assign_get_assignments":
        cursos = resposta.get("courses") or [{}]
        nomes = sorted(a.get("name") for a in cursos[0].get("assignments", []))
        itens = [("as 2 tarefas da massa", nomes == sorted(t["nome"] for t in cat["tarefas"]))]
    elif funcao == "gradereport_user_get_grade_items":
        itens_resp = (resposta.get("usergrades") or [{}])[0].get("gradeitems", [])
        por_nome = {i.get("itemname"): i.get("graderaw") for i in itens_resp}
        itens = []
        for nome, valor in zip(cat["itens_nota"], notas):
            obtido = por_nome.get(nome)
            ok = obtido is not None and abs(float(obtido) - valor) < 0.005
            itens.append((f"{nome} = {valor:.2f} (obtido: {obtido})", ok))
    else:
        itens = []
    return all(ok for _, ok in itens) and bool(itens), itens


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--avaliador", default="MS")
    args = ap.parse_args()
    url = os.environ.get("MOODLE_URL", "http://localhost:8080").rstrip("/")
    token = os.environ.get("MOODLE_TOKEN") or sys.exit("defina MOODLE_TOKEN (nunca versionar)")

    massa = json.loads((MASSA / "massa.json").read_text(encoding="utf-8"))
    est01 = massa["contas"]["estudantes"][0]
    notas_est01 = massa["catalogo"]["notas"][est01["username"]]
    contexto = {}
    SAIDA.mkdir(parents=True, exist_ok=True)

    planos = [
        ("core_webservice_get_site_info", lambda: {}),
        ("core_user_get_users_by_field", lambda: {"field": "username", "values": [est01["username"]]}),
        ("core_course_get_courses_by_field", lambda: {"field": "shortname",
                                                      "value": massa["catalogo"]["curso"]["shortname"]}),
        ("core_enrol_get_enrolled_users", lambda: {"courseid": contexto["courseid"]}),
        # includenotenrolledcourses: o usuário de integração não é matriculado no curso. Sem o parâmetro,
        # documentado na função, a resposta vem vazia com um aviso (tentativa 1).
        ("mod_assign_get_assignments", lambda: {"courseids": [contexto["courseid"]],
                                                "includenotenrolledcourses": 1}),
        ("gradereport_user_get_grade_items", lambda: {"courseid": contexto["courseid"],
                                                      "userid": contexto["userid"]}),
    ]
    linhas = []
    for n, (funcao, parametros) in enumerate(planos, 1):
        params = parametros()
        quando = datetime.now().astimezone().isoformat(timespec="seconds")
        status, resposta = chama(url, token, funcao, params)
        excecao = isinstance(resposta, dict) and ("exception" in resposta or "erro_http" in resposta)
        coerente, itens = (False, []) if excecao or status != 200 else confere(
            funcao, resposta, massa, notas_est01, contexto)
        arquivo = f"{n}_{funcao}.json"
        texto = json.dumps({"funcao": funcao, "parametros": params, "http": status, "data_hora": quando,
                            "resposta": resposta}, ensure_ascii=False, indent=2)
        if token in texto:
            sys.exit(f"o token apareceu na resposta de {funcao}; nada foi gravado")
        (SAIDA / arquivo).write_text(texto + "\n", encoding="utf-8")
        sucesso = status == 200 and not excecao and coerente
        linhas.append({"funcao": funcao, "parametros": json.dumps(params, ensure_ascii=False),
                       "data_hora": quando, "avaliador": args.avaliador, "http": status,
                       "exception": "sim" if excecao else "não", "coerente": "sim" if coerente else "não",
                       "sucesso": "sim" if sucesso else "não", "arquivo": arquivo,
                       "conferencia": "; ".join(f"{d}: {'ok' if ok else 'diferente'}" for d, ok in itens)
                       or (resposta.get("message") or resposta.get("erro_http", "") if isinstance(resposta, dict) else "")})
        print(f"{funcao:36s} HTTP {status}  exceção={linhas[-1]['exception']:3s}  "
              f"coerente={linhas[-1]['coerente']:3s}  sucesso={linhas[-1]['sucesso']}")

    with open(SAIDA / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    ws = sum(l["sucesso"] == "sim" for l in linhas)
    print(f"\nM2.3 = Ws / Wt = {ws} / {len(linhas)} = {ws / len(linhas):.2f}")


if __name__ == "__main__":
    main()
