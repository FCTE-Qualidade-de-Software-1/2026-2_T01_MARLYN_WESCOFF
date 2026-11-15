"""Gera a massa de dados fictícia da avaliação e a aplica em uma instância do Moodle (issue #63).

Toda a massa está definida neste arquivo, para que todos os servidores, as três atualizações de M3.3 e
o "antes e depois" de M3.5 partam do mesmo conjunto (plano da Fase 3, seção 2, Tabela 6). Nada é
digitado à mão e nenhum dado é real (regra R7): os e-mails usam o domínio reservado example.invalid.

Etapas:
  arquivos   Gera os arquivos de referência em dados/avaliacao/massa/:
               usuarios.csv  30 estudantes, no formato da carga de usuários do Moodle (F1 de M2.1)
               questoes.gift 15 questões (10 de múltipla escolha e 5 numéricas) (F4 de M2.1)
               notas.csv     notas da massa, 30 estudantes x 3 itens (F2 e F3 de M2.1)
               eventos.csv   os 6 eventos do calendário do curso completo (F6 de M2.1)
               massa.json    manifesto com tudo o que a etapa "aplicar" cria
  verificar  Confere os arquivos versionados: quantidades, domínio dos e-mails, coerência com o oráculo
             de M1.2 e se gerar de novo produz arquivos idênticos.
  aplicar    Cria a massa em uma instância já instalada, pela API do próprio Moodle
             (scripts/gera_massa_moodle.php). Partes, na ordem:
               contas    est01 a est30 e docente01 (o admin-aval já vem do script de preparação)
               catalogo  curso completo (AVAL-CAT) e curso vazio (AVAL-REST), com atividades,
                         notas, eventos, fórum e envios
               oraculo   curso do oráculo de M1.2 (AVAL-ORACULO): questionários Q-01 a Q-10,
                         categorias de nota A-01 a A-06 e atividades com prazo P-01 a P-04

Uso:
  python3 scripts/gera_massa.py arquivos
  python3 scripts/gera_massa.py verificar
  sudo python3 scripts/gera_massa.py aplicar --moodle /var/www/m53php83 --php php8.3 \\
      [--partes contas,catalogo,oraculo] [--dia-prazo AAAA-MM-DD] [--registro ARQUIVO.json]

Qual parte usar em cada métrica está em dados/avaliacao/massa/README.md.
"""

import argparse
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent.parent
SAIDA_PADRAO = RAIZ / "dados" / "avaliacao" / "massa"
ORACULO_CSV = RAIZ / "dados" / "avaliacao" / "M1.2" / "oraculo.csv"
EXECUTOR_PHP = Path(__file__).resolve().parent / "gera_massa_moodle.php"

FUSO = "America/Sao_Paulo"
DOMINIO = "example.invalid"
# Senha fictícia e pública de todas as contas da massa. Só vale dentro das VMs de avaliação.
# Pode ser trocada com a variável MASSA_SENHA na etapa "aplicar".
SENHA_PADRAO = "Aval#2026"
PARTES = ("contas", "catalogo", "oraculo")

# ---------------------------------------------------------------------------------------------
# Contas
# ---------------------------------------------------------------------------------------------
NUM_ESTUDANTES = 30


def estudantes():
    return [{
        "username": f"est{n:02d}",
        "firstname": "Estudante",
        "lastname": f"{n:02d}",
        "email": f"est{n:02d}@{DOMINIO}",
        "idnumber": f"AVAL-EST{n:02d}",
    } for n in range(1, NUM_ESTUDANTES + 1)]


DOCENTE = {"username": "docente01", "firstname": "Docente", "lastname": "01",
           "email": f"docente01@{DOMINIO}", "idnumber": "AVAL-DOC01"}

# ---------------------------------------------------------------------------------------------
# Questões do arquivo GIFT (F4) e do questionário do catálogo (3 de múltipla escolha e 2 numéricas)
# ---------------------------------------------------------------------------------------------
# Múltipla escolha: (nome, enunciado, [(resposta, fração), ...]). A primeira resposta é a correta.
MULTIPLA_ESCOLHA = [
    ("ME01", "Qual norma define o modelo de qualidade de produto da série SQuaRE?",
     [("ISO/IEC 25010", 100), ("ISO/IEC 25040", 0), ("ISO 9001", 0), ("ISO/IEC 12207", 0)]),
    ("ME02", "Qual destas é uma característica de qualidade de produto da ISO/IEC 25010?",
     [("Compatibilidade", 100), ("Rentabilidade", 0), ("Popularidade", 0), ("Velocidade de escrita", 0)]),
    ("ME03", "No método GQM, o que vem depois do objetivo?",
     [("Questões", 100), ("Métricas", 0), ("Hipóteses de negócio", 0), ("Requisitos", 0)]),
    ("ME04", "Qual é a capital do Brasil?",
     [("Brasília", 100), ("Rio de Janeiro", 0), ("São Paulo", 0), ("Salvador", 0)]),
    ("ME05", "Quantos minutos tem uma hora?",
     [("60", 100), ("100", 0), ("30", 0), ("90", 0)]),
    ("ME06", "Qual destes é um sistema de gestão da aprendizagem?",
     [("Moodle", 100), ("PostgreSQL", 0), ("Apache", 0), ("Git", 0)]),
    ("ME07", "Qual linguagem é usada no núcleo do Moodle?",
     [("PHP", 100), ("COBOL", 0), ("Fortran", 0), ("Pascal", 0)]),
    ("ME08", "Qual alternativa é um número primo?",
     [("7", 100), ("9", 0), ("15", 0), ("21", 0)]),
    # Duas questões com crédito parcial, para que a importação GIFT carregue frações diferentes de 0 e 100.
    ("ME09", "Qual opção descreve melhor um teste de caixa-preta?",
     [("Teste baseado só em entradas e saídas", 100), ("Teste baseado em entradas, saídas e no código", 50),
      ("Inspeção do código-fonte", 0), ("Revisão da arquitetura", 0)]),
    ("ME10", "Qual banco de dados é usado no servidor de referência da avaliação?",
     [("PostgreSQL 17", 100), ("PostgreSQL de versão não informada", 50), ("SQLite", 0), ("Planilha", 0)]),
]

# Numéricas: (nome, enunciado, resposta, tolerância).
NUMERICAS = [
    ("NU01", "Quanto é 12 x 12?", 144, 0),
    ("NU02", "Quanto é 7,5 x 4?", 30, 0),
    ("NU03", "Qual é a média de 6, 8 e 10?", 8, 0),
    ("NU04", "Quantos dias tem uma semana?", 7, 0),
    ("NU05", "Qual é o valor de pi com duas casas decimais?", 3.14, 0.005),
]

QUESTIONARIO_CATALOGO = ["ME01", "ME02", "ME03", "NU01", "NU02"]

# ---------------------------------------------------------------------------------------------
# Curso completo (catálogo T01 a T12) e curso vazio
# ---------------------------------------------------------------------------------------------
ITENS_NOTA = ["Avaliação 1", "Avaliação 2", "Participação"]


def nota(n_estudante, n_item):
    """Nota determinística de 5,00 a 10,00, em passos de 0,50 (sem sorteio, para ser reprodutível)."""
    return 5 + ((n_estudante * 7 + n_item * 3) % 11) * 0.5


# Eventos de curso com data fixa: a referência de F6 não pode depender do dia em que a massa é aplicada.
# (título, data, hora de início, duração em minutos), no fuso de Brasília.
EVENTOS = [
    ("Aula inaugural", "2026-12-01", "19:00", 120),
    ("Plantão de dúvidas 1", "2026-12-03", "14:00", 60),
    ("Prova 1", "2026-12-08", "19:00", 100),
    ("Plantão de dúvidas 2", "2026-12-10", "14:00", 60),
    ("Prova 2", "2026-12-15", "19:00", 100),
    ("Encerramento da disciplina", "2026-12-17", "19:00", 90),
]

# Estudantes que já enviaram a tarefa aberta, para M3.5 ter envios a preservar. Ficam de fora
# est01 a est20, que são os usados nas tarefas T04 e T05 de M1.1 e M3.1.
ENVIOS_TAREFA = [f"est{n:02d}" for n in range(21, 31)]
RESPOSTAS_FORUM = ["est02", "est03", "est04"]

# ---------------------------------------------------------------------------------------------
# Oráculo de M1.2 (dados/avaliacao/M1.2/oraculo.csv)
# ---------------------------------------------------------------------------------------------
# Questionários: caso -> (notas máximas de cada questão, nota máxima do questionário).
# Todas as questões têm as alternativas "Correta" (100%), "Parcial (50%)" e duas incorretas, sem
# embaralhar, para que o avaliador marque exatamente o que a coluna "entradas" do oráculo pede.
ORACULO_QUESTIONARIOS = {
    "Q-01": ([1] * 3, 3),
    "Q-02": ([2] * 5, 10),
    "Q-03": ([1, 2, 3, 4], 10),
    "Q-04": ([1] * 10, 10),
    "Q-05": ([2] * 5, 10),
    "Q-06": ([2.5] * 4, 10),
    "Q-07": ([1] * 6, 10),
    "Q-08": ([1] * 8, 10),
    "Q-09": ([2, 3, 5], 10),
    "Q-10": ([0.5] * 20, 10),
}
ALTERNATIVAS_ORACULO = [("Correta", 100), ("Parcial (50%)", 50), ("Incorreta A", 0), ("Incorreta B", 0)]

# Agregação no livro de notas. Cada caso é uma categoria com nota máxima 10, exceto a soma natural
# (A-04), cuja nota máxima é a soma dos itens (70). Itens: (nome, nota máxima, peso).
ORACULO_AGREGACAO = {
    "A-01": {"agregacao": "media_ponderada", "itens": [("P1", 10, 40), ("P2", 10, 60)]},
    "A-02": {"agregacao": "media_simples", "itens": [("N1", 10, None), ("N2", 10, None), ("N3", 10, None)]},
    "A-03": {"agregacao": "media_ponderada", "itens": [("N1", 10, 20), ("N2", 10, 30), ("N3", 10, 50)]},
    "A-04": {"agregacao": "soma_natural", "itens": [("categoria 1", 20, None), ("categoria 2", 50, None)]},
    "A-05": {"agregacao": "media_simples", "descartar_menores": 1,
             "itens": [("N1", 10, None), ("N2", 10, None), ("N3", 10, None), ("N4", 10, None)]},
    "A-06": {"agregacao": "media_ponderada", "subcategorias": [
        ("questionarios", 30, [("Questionário 1", 10, None)]),
        ("tarefas", 70, [("Tarefa 1", 10, None)]),
    ]},
}

# Prazos, relativos ao dia D (--dia-prazo). (dias a partir de D, "HH:MM").
ORACULO_PRAZOS = {
    "P-01 e P-02": {"tipo": "tarefa", "abre": (-1, "00:00"), "vencimento": (0, "23:59"),
                    "data_limite": (0, "23:59")},
    "P-03": {"tipo": "tarefa", "abre": (-1, "00:00"), "vencimento": (0, "23:59"), "data_limite": (2, "23:59")},
    "P-04": {"tipo": "questionario", "abre": (-1, "00:00"), "fecha": (0, "18:00")},
}
ESTUDANTES_ORACULO = [f"est{n:02d}" for n in range(1, 6)]


# ---------------------------------------------------------------------------------------------
# Arquivos de referência
# ---------------------------------------------------------------------------------------------
def gift_escapa(texto):
    for c in "\\~=#{}:":
        texto = texto.replace(c, "\\" + c)
    return texto


def gift_numero(valor):
    return f"{valor:g}"


def gera_gift():
    linhas = ["// Questões da massa de dados da avaliação do Moodle 5.3 (gerado por scripts/gera_massa.py).",
              "// Referência de F4 (importação GIFT) de M2.1. Não editar à mão.", "",
              "$CATEGORY: $course$/top/AVAL-F4", ""]
    for nome, enunciado, respostas in MULTIPLA_ESCOLHA:
        alts = []
        for texto, fracao in respostas:
            if fracao == 100:
                alts.append(f"={gift_escapa(texto)}")
            elif fracao == 0:
                alts.append(f"~{gift_escapa(texto)}")
            else:
                alts.append(f"~%{fracao}%{gift_escapa(texto)}")
        linhas.append(f"::{nome}::{gift_escapa(enunciado)} {{ {' '.join(alts)} }}")
        linhas.append("")
    for nome, enunciado, resposta, tolerancia in NUMERICAS:
        alvo = gift_numero(resposta) + (f":{gift_numero(tolerancia)}" if tolerancia else "")
        linhas.append(f"::{nome}::{gift_escapa(enunciado)} {{#{alvo}}}")
        linhas.append("")
    return "\n".join(linhas)


def csv_texto(cabecalho, linhas):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cabecalho)
    w.writerows(linhas)
    return buf.getvalue()


def gera_usuarios_csv():
    cab = ["username", "password", "firstname", "lastname", "email", "idnumber", "timezone"]
    return csv_texto(cab, [[e["username"], SENHA_PADRAO, e["firstname"], e["lastname"], e["email"],
                            e["idnumber"], FUSO] for e in estudantes()])


def gera_notas_csv():
    cab = ["email"] + ITENS_NOTA
    linhas = []
    for n, e in enumerate(estudantes(), start=1):
        linhas.append([e["email"]] + [f"{nota(n, i):.2f}" for i in range(1, len(ITENS_NOTA) + 1)])
    return csv_texto(cab, linhas)


def momento(dia, hora, fuso=FUSO):
    return datetime.combine(date.fromisoformat(dia) if isinstance(dia, str) else dia,
                            time.fromisoformat(hora), tzinfo=ZoneInfo(fuso))


def ical_utc(dt):
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")


def gera_eventos_csv():
    linhas = []
    for titulo, dia, hora, minutos in EVENTOS:
        inicio = momento(dia, hora)
        linhas.append([titulo, ical_utc(inicio), ical_utc(inicio + timedelta(minutes=minutos))])
    return csv_texto(["SUMMARY", "DTSTART", "DTEND"], linhas)


def manifesto(dia_prazo=None):
    """Tudo o que a etapa "aplicar" cria. Sem --dia-prazo, os prazos ficam relativos ao dia D."""
    def quando(rel):
        dias, hora = rel
        if dia_prazo is None:
            return {"dia": f"D{dias:+d}" if dias else "D", "hora": hora}
        return int(momento(dia_prazo + timedelta(days=dias), hora).timestamp())

    def questao_me(nome, enunciado, respostas, nota_padrao=1):
        return {"tipo": "multichoice", "nome": nome, "enunciado": enunciado, "nota_padrao": nota_padrao,
                "respostas": [{"texto": t, "fracao": f / 100} for t, f in respostas]}

    def questao_nu(nome, enunciado, resposta, tolerancia):
        return {"tipo": "numerical", "nome": nome, "enunciado": enunciado, "nota_padrao": 1,
                "resposta": resposta, "tolerancia": tolerancia}

    todas = {q[0]: questao_me(*q) for q in MULTIPLA_ESCOLHA}
    todas.update({q[0]: questao_nu(*q) for q in NUMERICAS})

    questionarios = []
    for caso, (notas, nota_max) in ORACULO_QUESTIONARIOS.items():
        questoes = [dict(questao_me(f"{caso} questão {i}", f"{caso}, questão {i} de {len(notas)}. "
                                    "Marque a alternativa pedida no oráculo.", ALTERNATIVAS_ORACULO),
                         nota_max_slot=n) for i, n in enumerate(notas, start=1)]
        questionarios.append({"caso": caso, "nome": f"{caso} Questionário do oráculo",
                              "nota_maxima": nota_max, "questoes": questoes})

    agregacoes = []
    for caso, cfg in ORACULO_AGREGACAO.items():
        cat = {"caso": caso, "nome": f"{caso} Agregação", "agregacao": cfg["agregacao"],
               "descartar_menores": cfg.get("descartar_menores", 0),
               "nota_maxima": None if cfg["agregacao"] == "soma_natural" else 10,
               "itens": [{"nome": f"{caso} {n}", "nota_maxima": m, "peso": p} for n, m, p in cfg.get("itens", [])],
               "subcategorias": [{"nome": f"{caso} {n}", "peso": p, "agregacao": "media_simples", "nota_maxima": 10,
                                  "itens": [{"nome": f"{caso} {i}", "nota_maxima": m, "peso": w} for i, m, w in itens]}
                                 for n, p, itens in cfg.get("subcategorias", [])]}
        agregacoes.append(cat)

    prazos = []
    for caso, cfg in ORACULO_PRAZOS.items():
        p = {"caso": caso, "tipo": cfg["tipo"], "nome": f"{caso} {'Tarefa' if cfg['tipo'] == 'tarefa' else 'Questionário'} com prazo"}
        for chave in ("abre", "vencimento", "data_limite", "fecha"):
            if chave in cfg:
                p[chave] = quando(cfg[chave])
        if cfg["tipo"] == "questionario":
            p["questoes"] = [dict(questao_me(f"{caso} questão 1", f"{caso}: questão única.", ALTERNATIVAS_ORACULO),
                                  nota_max_slot=10)]
        prazos.append(p)

    hoje_rel = (lambda d, h: quando((d, h)))
    return {
        "gerado_por": "scripts/gera_massa.py",
        "fuso": FUSO,
        "dia_prazo": dia_prazo.isoformat() if dia_prazo else "D (informado em --dia-prazo)",
        "contas": {"estudantes": estudantes(), "docente": DOCENTE},
        "catalogo": {
            "curso": {"shortname": "AVAL-CAT", "fullname": "Curso completo da avaliação (catálogo T01 a T12)"},
            "curso_vazio": {"shortname": "AVAL-REST", "fullname": "Curso vazio (destino da restauração, T12)"},
            "material": {"nome": "Material da disciplina", "arquivo": "plano-de-ensino.txt",
                         "conteudo": "Plano de ensino fictício da avaliação do Moodle 5.3.\n"},
            "tarefas": [
                {"nome": "Tarefa dentro do prazo (T04)", "abre": hoje_rel(-1, "00:00"),
                 "vencimento": hoje_rel(7, "23:59"), "data_limite": hoje_rel(9, "23:59")},
                {"nome": "Tarefa com data limite vencida (T05)", "abre": hoje_rel(-10, "00:00"),
                 "vencimento": hoje_rel(-3, "23:59"), "data_limite": hoje_rel(-1, "23:59")},
            ],
            "envios": {"tarefa": "Tarefa dentro do prazo (T04)", "estudantes": ENVIOS_TAREFA},
            "questionario": {"nome": "Questionário da massa (T08)", "nota_maxima": 10,
                             "abre": hoje_rel(-1, "00:00"), "fecha": hoje_rel(7, "23:59"),
                             "questoes": [dict(todas[n], nota_max_slot=2) for n in QUESTIONARIO_CATALOGO]},
            "forum": {"nome": "Fórum de dúvidas (T09)", "topico": "Dúvidas sobre a disciplina",
                      "mensagem": "Use este tópico para dúvidas gerais.", "respostas": RESPOSTAS_FORUM},
            "itens_nota": ITENS_NOTA,
            "notas": {e["username"]: [round(nota(n, i), 2) for i in range(1, len(ITENS_NOTA) + 1)]
                      for n, e in enumerate(estudantes(), start=1)},
            "eventos": [{"titulo": t, "inicio": int(momento(d, h).timestamp()), "duracao_min": m}
                        for t, d, h, m in EVENTOS],
        },
        "oraculo": {
            "curso": {"shortname": "AVAL-ORACULO", "fullname": "Oráculo de M1.2 (casos Q, A e P)"},
            "estudantes": ESTUDANTES_ORACULO,
            "questionarios": questionarios,
            "agregacoes": agregacoes,
            "prazos": prazos,
        },
    }


def arquivos_referencia():
    return {
        "usuarios.csv": gera_usuarios_csv(),
        "questoes.gift": gera_gift(),
        "notas.csv": gera_notas_csv(),
        "eventos.csv": gera_eventos_csv(),
        "massa.json": json.dumps(manifesto(), ensure_ascii=False, indent=2) + "\n",
    }


def etapa_arquivos(args):
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    for nome, conteudo in arquivos_referencia().items():
        (saida / nome).write_text(conteudo, encoding="utf-8", newline="\n")
        print(f"gravado {saida / nome}")
    return 0


# ---------------------------------------------------------------------------------------------
# Verificação
# ---------------------------------------------------------------------------------------------
def conta_gift(texto):
    blocos = [b.strip() for b in texto.split("\n\n")]
    return [b for b in blocos if b.startswith("::")]


def casos_oraculo_csv():
    if not ORACULO_CSV.exists():
        return None
    with ORACULO_CSV.open(encoding="utf-8") as f:
        return [linha["caso"] for linha in csv.DictReader(f)]


def etapa_verificar(args):
    saida = Path(args.saida)
    erros = []

    def confere(cond, msg):
        print(("ok    " if cond else "ERRO  ") + msg)
        if not cond:
            erros.append(msg)

    esperados = arquivos_referencia()
    for nome, conteudo in esperados.items():
        arq = saida / nome
        confere(arq.exists(), f"{nome} existe")
        if arq.exists():
            confere(arq.read_text(encoding="utf-8") == conteudo, f"{nome} igual ao que o script gera (reprodutível)")

    usuarios = list(csv.DictReader(io.StringIO(esperados["usuarios.csv"])))
    confere(len(usuarios) == 30, f"usuarios.csv tem 30 linhas de dados ({len(usuarios)})")
    confere(len({u["username"] for u in usuarios}) == 30, "usuarios.csv sem username repetido")
    emails = [u["email"] for u in usuarios] + [DOCENTE["email"]]
    confere(all(e.endswith("@" + DOMINIO) for e in emails), f"todos os e-mails em {DOMINIO} (R7)")
    confere(len(conta_gift(esperados["questoes.gift"])) == 15,
            f"questoes.gift tem 15 questões ({len(conta_gift(esperados['questoes.gift']))})")
    notas = list(csv.DictReader(io.StringIO(esperados["notas.csv"])))
    confere(len(notas) == 30 and all(len(n) == 1 + len(ITENS_NOTA) for n in notas), "notas.csv tem 30 x 3 notas")
    confere(len(EVENTOS) == 6, "eventos.csv tem 6 eventos")

    m = manifesto()
    casos = [q["caso"] for q in m["oraculo"]["questionarios"]] + [a["caso"] for a in m["oraculo"]["agregacoes"]]
    casos += [c for p in m["oraculo"]["prazos"] for c in p["caso"].split(" e ")]
    confere(len(casos) == 20, f"massa cobre 20 casos do oráculo ({len(casos)})")
    do_csv = casos_oraculo_csv()
    if do_csv is None:
        print(f"aviso {ORACULO_CSV.relative_to(RAIZ)} ainda não está no repositório; coerência não conferida")
    else:
        confere(sorted(do_csv) == sorted(casos), "casos da massa iguais aos de oraculo.csv")
    for caso, (notas_q, nota_max) in ORACULO_QUESTIONARIOS.items():
        # Ou a soma das questões é a nota máxima, ou as questões têm o mesmo peso e o Moodle escala
        # a soma para a nota máxima (Q-07 e Q-08).
        confere(abs(sum(notas_q) - nota_max) < 1e-9 or len(set(notas_q)) == 1,
                f"{caso}: questões coerentes com a nota máxima")

    print(f"\n{len(erros)} erro(s).")
    return 1 if erros else 0


# ---------------------------------------------------------------------------------------------
# Aplicação no Moodle
# ---------------------------------------------------------------------------------------------
def acha_config(moodle):
    moodle = Path(moodle)
    for d in (moodle, moodle.parent):
        if (d / "config.php").exists():
            return d / "config.php"
    raise SystemExit(f"erro: config.php não encontrado em {moodle}")


def etapa_aplicar(args):
    partes = [p.strip() for p in args.partes.split(",") if p.strip()]
    invalidas = [p for p in partes if p not in PARTES]
    if invalidas:
        raise SystemExit(f"erro: partes inválidas {invalidas}; use {','.join(PARTES)}")
    partes = [p for p in PARTES if p in partes]  # ordem fixa
    dia = date.fromisoformat(args.dia_prazo) if args.dia_prazo else datetime.now(ZoneInfo(FUSO)).date()
    config = acha_config(args.moodle)

    dados = manifesto(dia)
    dados["partes"] = partes
    dados["senha"] = os.environ.get("MASSA_SENHA", SENHA_PADRAO)

    with tempfile.TemporaryDirectory(prefix="massa-") as tmp:
        tmp = Path(tmp)
        entrada, saida = tmp / "massa.json", tmp / "resultado.json"
        entrada.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        executor = tmp / "gera_massa_moodle.php"
        shutil.copy(EXECUTOR_PHP, executor)
        if os.geteuid() == 0 and args.usuario_web:
            shutil.chown(tmp, args.usuario_web)
            for arq in (entrada, executor):
                shutil.chown(arq, args.usuario_web)
        cmd = [args.php, str(executor), f"--config={config}", f"--entrada={entrada}", f"--saida={saida}"]
        if os.geteuid() == 0 and args.usuario_web:
            cmd = ["sudo", "-u", args.usuario_web] + cmd
        print(f"Aplicando {', '.join(partes)} em {config.parent} (dia D = {dia.isoformat()}, fuso {FUSO})")
        rc = subprocess.run(cmd).returncode
        if not saida.exists():
            print("erro: o executor PHP não gravou o resultado", file=sys.stderr)
            return rc or 1
        resultado = json.loads(saida.read_text(encoding="utf-8"))

    resultado.update({"partes": partes, "dia_prazo": dia.isoformat(), "fuso": FUSO,
                      "moodle": str(config.parent), "aplicado_em": datetime.now(ZoneInfo(FUSO)).isoformat()})
    registro = Path(args.registro) if args.registro else Path(f"massa-{config.parent.name}-{dia.isoformat()}.json")
    registro.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registro da aplicação em {registro}")
    return rc


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = p.add_subparsers(dest="etapa", required=True)
    a = sub.add_parser("arquivos", help="gera os arquivos de referência")
    a.add_argument("--saida", default=SAIDA_PADRAO)
    v = sub.add_parser("verificar", help="confere os arquivos versionados")
    v.add_argument("--saida", default=SAIDA_PADRAO)
    ap = sub.add_parser("aplicar", help="cria a massa em uma instância do Moodle")
    ap.add_argument("--moodle", required=True, help="pasta da instância, onde está o config.php (ex.: /var/www/m53php83)")
    ap.add_argument("--php", default="php", help="binário do PHP da instância (ex.: php8.3)")
    ap.add_argument("--partes", default=",".join(PARTES), help="contas, catalogo e/ou oraculo")
    ap.add_argument("--dia-prazo", help="dia D dos casos de prazo do oráculo (AAAA-MM-DD; padrão: hoje)")
    ap.add_argument("--registro", help="arquivo JSON com o que foi criado (padrão: massa-<instância>-<D>.json)")
    ap.add_argument("--usuario-web", default="www-data", help="usuário que roda o PHP quando chamado com sudo")
    args = p.parse_args()
    return {"arquivos": etapa_arquivos, "verificar": etapa_verificar, "aplicar": etapa_aplicar}[args.etapa](args)


if __name__ == "__main__":
    sys.exit(main())
