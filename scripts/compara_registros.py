"""Compara, campo a campo, os registros de um arquivo de referência com os de um arquivo de destino (M2.2).

Mede a integridade dos dados trocados (Fase 2, M2.2 = Rc / Rt):
  Rt = registros do arquivo de referência;
  Rc = registros da referência encontrados no destino com todos os campos comparados iguais.

Única normalização: espaços em branco (espaços no início e no fim são removidos e sequências de espaços,
tabulações e quebras de linha viram um espaço). Acentuação, maiúsculas, casas decimais e datas NÃO são
normalizadas, porque diferenças nelas são perda de integridade.

Equivalências de representação (não são normalizações: o dado é o mesmo, só a forma de gravar muda):
  - célula numérica de XLSX: o arquivo guarda o número, e não o texto exibido; o valor é comparado como
    número (10.0 = 10.00). Uma célula de texto continua comparada como texto;
  - resposta numérica de GIFT: "#144" e a forma que o Moodle exporta, "=%100%144:0", são a mesma resposta
    (peso 100%, valor 144, tolerância 0); a resposta é comparada por peso, valor, tolerância e feedback.

Formatos lidos (inferidos pela extensão, ou informados com --formato-ref e --formato-dest):
  csv   F1 usuários, F2 notas           um registro por linha; a primeira linha é o cabeçalho
  xlsx  F3 notas                        primeira planilha; a primeira linha é o cabeçalho
  gift  F4 questões                     um registro por questão: nome, enunciado e respostas
  xml   F5 questões em Moodle XML       um registro por <question> (categorias ignoradas)
  ics   F6 calendário                   um registro por VEVENT, com as propriedades como campos
  mbz   F7 backup de curso              um registro por atividade de moodle_backup.xml
A referência e o destino podem ter formatos diferentes (por exemplo, eventos.csv contra eventos.ics).

Uso:
  python3 scripts/compara_registros.py REFERENCIA DESTINO --chave CAMPO [opções]

Opções principais:
  --chave CAMPO            campo que identifica o registro nos dois arquivos (ex.: username, nome, SUMMARY)
  --campos A,B,C           campos comparados (padrão: todos os campos do registro de referência)
  --ignorar A,B            campos excluídos da comparação (ex.: UID,DTSTAMP)
  --mapa ref=dest,...      nome do campo no destino quando difere da referência (ex.: firstname=Nome)
  --formato NOME           rótulo do formato no resumo (F1 a F7)
  --relatorio ARQ.csv      grava o resultado de cada registro
  --resumo ARQ.csv         acrescenta uma linha de resumo (Rt, Rc, M2.2), com data, avaliador e sha256
  --avaliador INICIAIS     iniciais de quem executou a comparação (vai para o resumo)

Código de saída: 0 quando a comparação roda (mesmo com divergências), 2 em erro de leitura ou de uso.
"""

import argparse
import csv
import hashlib
import io
import re
import sys
import tarfile
import zipfile
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree

ESPACOS = re.compile(r"\s+")
NS_XLSX = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
EXTENSOES = {".csv": "csv", ".xlsx": "xlsx", ".gift": "gift", ".txt": "gift", ".xml": "xml",
             ".ics": "ics", ".mbz": "mbz"}


class ErroLeitura(Exception):
    pass


class NumeroCelula(str):
    """Valor de uma célula numérica de XLSX: o arquivo guarda o número, e não o texto formatado."""


def normaliza(valor):
    """Única normalização permitida em M2.2: espaços em branco."""
    if valor is None:
        return None
    return ESPACOS.sub(" ", str(valor)).strip()


def _decimal(texto):
    try:
        return Decimal(texto)
    except (InvalidOperation, TypeError):
        return None


def iguais(esperado, obtido):
    """Compara dois valores de campo. Só espaços são normalizados; uma célula numérica de XLSX é
    comparada como número com a referência, porque o arquivo não guarda casas decimais."""
    a, b = normaliza(esperado), normaliza(obtido)
    if a == b:
        return True
    if isinstance(esperado, NumeroCelula) or isinstance(obtido, NumeroCelula):
        da, db = _decimal(a), _decimal(b)
        return da is not None and db is not None and da == db
    return False


# ---------------------------------------------------------------- leitores (cada um devolve lista de dicts)

def le_csv(caminho, delimitador=None):
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    if delimitador is None:
        try:
            delimitador = csv.Sniffer().sniff(texto.splitlines()[0], delimiters=",;\t").delimiter
        except (csv.Error, IndexError):
            delimitador = ","
    return [dict(linha) for linha in csv.DictReader(io.StringIO(texto), delimiter=delimitador)]


def _coluna(ref_celula):
    letras = re.match(r"[A-Z]+", ref_celula).group(0)
    n = 0
    for letra in letras:
        n = n * 26 + ord(letra) - 64
    return n - 1


def le_xlsx(caminho):
    """Lê a primeira planilha sem dependências externas. Células numéricas viram NumeroCelula."""
    with zipfile.ZipFile(caminho) as z:
        compartilhadas = []
        if "xl/sharedStrings.xml" in z.namelist():
            raiz = ElementTree.fromstring(z.read("xl/sharedStrings.xml"))
            for si in raiz.findall("m:si", NS_XLSX):
                compartilhadas.append("".join(t.text or "" for t in si.iter(f"{{{NS_XLSX['m']}}}t")))
        planilhas = sorted(n for n in z.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
        if not planilhas:
            raise ErroLeitura("o XLSX não tem planilha")
        raiz = ElementTree.fromstring(z.read(planilhas[0]))
    linhas = []
    for row in raiz.iter(f"{{{NS_XLSX['m']}}}row"):
        valores = {}
        for c in row.findall("m:c", NS_XLSX):
            tipo, v = c.get("t"), c.find("m:v", NS_XLSX)
            if tipo == "s" and v is not None:
                valor = compartilhadas[int(v.text)]
            elif tipo == "inlineStr":
                valor = "".join(t.text or "" for t in c.iter(f"{{{NS_XLSX['m']}}}t"))
            elif tipo in (None, "n") and v is not None:
                valor = NumeroCelula(v.text)
            else:
                valor = v.text if v is not None else ""
            valores[_coluna(c.get("r"))] = valor
        if valores:
            linhas.append([valores.get(i, "") for i in range(max(valores) + 1)])
    if not linhas:
        return []
    cabecalho = linhas[0]
    return [dict(zip(cabecalho, linha + [""] * (len(cabecalho) - len(linha)))) for linha in linhas[1:]]


def le_gift(caminho):
    """Um registro por questão: nome (::nome::), enunciado e respostas (o conteúdo entre chaves)."""
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    sem_comentarios = "\n".join(l for l in texto.splitlines() if not l.lstrip().startswith("//"))
    registros = []
    for bloco in re.split(r"\n\s*\n", sem_comentarios):
        bloco = bloco.strip()
        if not bloco or bloco.startswith("$CATEGORY"):
            continue
        m = re.match(r"::(.*?)::(.*)", bloco, re.S)
        nome, resto = (m.group(1), m.group(2)) if m else ("", bloco)
        abre = resto.find("{")
        fecha = resto.rfind("}")
        if abre == -1 or fecha < abre:
            raise ErroLeitura(f"questão GIFT sem respostas entre chaves: {bloco[:60]!r}")
        enunciado = re.sub(r"^\[(html|moodle|markdown|plain)\]", "", resto[:abre].strip())
        registros.append({"nome": nome, "enunciado": enunciado,
                          "respostas": respostas_gift(resto[abre + 1:fecha])})
    return registros


def respostas_gift(bloco):
    """Respostas de uma questão GIFT. As numéricas ("#...") viram uma forma única, para que "#144" e a forma
    exportada pelo Moodle, "#=%100%144:0#", sejam a mesma resposta; as demais ficam como estão."""
    texto = normaliza(bloco)
    if not texto.startswith("#"):
        return bloco
    corpo = texto[1:].strip()
    partes = [p for p in re.split(r"\s*=\s*", corpo) if p] if corpo.startswith("=") else [corpo]
    canonicas = []
    for parte in partes:
        m = re.fullmatch(r"(?:%(-?[\d.]+)%)?\s*([^:#]+?)\s*(?::\s*([^#]+?))?\s*(?:#(.*))?", parte, re.S)
        if not m:
            return bloco
        peso, valor, tolerancia, feedback = m.groups()
        canonicas.append(f"{_num(peso or '100')}%{_num(valor)}:{_num(tolerancia or '0')}#{normaliza(feedback or '')}")
    return "numerica " + " | ".join(canonicas)


def _num(texto):
    """Número de uma resposta GIFT na forma decimal mínima (144, 3.14, 0.005); texto não numérico fica igual."""
    d = _decimal(texto.strip())
    return texto.strip() if d is None else format(d.normalize(), "f")


def le_moodle_xml(caminho):
    """Um registro por <question> que não seja categoria: tipo, nome, enunciado, respostas e nota padrão."""
    raiz = ElementTree.parse(caminho).getroot()
    registros = []
    for q in raiz.iter("question"):
        if q.get("type") == "category":
            continue
        texto = lambda caminho_xml: (q.findtext(caminho_xml) or "")  # noqa: E731
        respostas = " | ".join(f"{a.get('fraction', '')}:{a.findtext('text') or ''}" for a in q.findall("answer"))
        registros.append({"tipo": q.get("type", ""), "nome": texto("name/text"),
                          "enunciado": texto("questiontext/text"), "respostas": respostas,
                          "nota_padrao": texto("defaultgrade")})
    return registros


def le_ics(caminho):
    """Um registro por VEVENT. Linhas dobradas (RFC 5545) são desdobradas; parâmetros saem do nome."""
    bruto = Path(caminho).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    linhas = []
    for linha in bruto.split("\n"):
        if linha[:1] in (" ", "\t") and linhas:
            linhas[-1] += linha[1:]
        else:
            linhas.append(linha)
    registros, atual = [], None
    for linha in linhas:
        if linha == "BEGIN:VEVENT":
            atual = {}
        elif linha == "END:VEVENT" and atual is not None:
            registros.append(atual)
            atual = None
        elif atual is not None and ":" in linha:
            nome, valor = linha.split(":", 1)
            atual[nome.split(";", 1)[0].upper()] = valor
    return registros


def le_mbz(caminho):
    """Um registro por atividade listada em moodle_backup.xml (o .mbz pode ser tar.gz ou zip)."""
    conteudo = None
    if zipfile.is_zipfile(caminho):
        with zipfile.ZipFile(caminho) as z:
            if "moodle_backup.xml" in z.namelist():
                conteudo = z.read("moodle_backup.xml")
    else:
        try:
            with tarfile.open(caminho, "r:*") as t:
                membro = next((m for m in t.getmembers() if m.name.lstrip("./") == "moodle_backup.xml"), None)
                if membro is not None:
                    conteudo = t.extractfile(membro).read()
        except tarfile.TarError as erro:
            raise ErroLeitura(f"backup .mbz ilegível: {erro}") from erro
    if conteudo is None:
        raise ErroLeitura("moodle_backup.xml não encontrado no .mbz")
    raiz = ElementTree.fromstring(conteudo)
    return [{"modulename": a.findtext("modulename") or "", "title": a.findtext("title") or "",
             "sectionid": a.findtext("sectionid") or ""}
            for a in raiz.iter("activity") if a.find("modulename") is not None]


LEITORES = {"csv": le_csv, "xlsx": le_xlsx, "gift": le_gift, "xml": le_moodle_xml, "ics": le_ics, "mbz": le_mbz}


def le_registros(caminho, formato=None, delimitador=None):
    formato = formato or EXTENSOES.get(Path(caminho).suffix.lower())
    if formato not in LEITORES:
        raise ErroLeitura(f"formato não reconhecido para {caminho}; use --formato-ref/--formato-dest")
    try:
        if formato == "csv":
            return le_csv(caminho, delimitador)
        return LEITORES[formato](caminho)
    except (OSError, UnicodeDecodeError, ElementTree.ParseError, zipfile.BadZipFile) as erro:
        raise ErroLeitura(f"não foi possível ler {caminho}: {erro}") from erro


# ---------------------------------------------------------------- comparação

def indexa(registros, chave, origem):
    indice, duplicadas = {}, []
    for r in registros:
        if chave not in r:
            raise ErroLeitura(f"o campo-chave {chave!r} não existe em {origem}; campos: {', '.join(r)}")
        k = normaliza(r[chave])
        if k in indice:
            duplicadas.append(k)
        indice[k] = r
    return indice, duplicadas


def compara(referencia, destino, chave, campos=None, ignorar=(), mapa=None):
    """Devolve (resultados por registro, resumo). Cada resultado: chave, situacao, campos_divergentes, detalhe."""
    mapa = mapa or {}
    chave_dest = mapa.get(chave, chave)
    idx_ref, dup_ref = indexa(referencia, chave, "referência")
    idx_dest, dup_dest = indexa(destino, chave_dest, "destino")
    resultados = []
    for k, reg in idx_ref.items():
        if k not in idx_dest:
            resultados.append({"chave": k, "situacao": "ausente", "campos_divergentes": "", "detalhe": ""})
            continue
        alvo = idx_dest[k]
        lista = campos or [c for c in reg if c not in ignorar]
        divergentes, detalhes = [], []
        for campo in lista:
            bruto_esperado, bruto_obtido = reg.get(campo), alvo.get(mapa.get(campo, campo))
            esperado, obtido = normaliza(bruto_esperado), normaliza(bruto_obtido)
            if not iguais(bruto_esperado, bruto_obtido):
                divergentes.append(campo)
                detalhes.append(f"{campo}: esperado={esperado!r} obtido={obtido!r}")
        resultados.append({"chave": k, "situacao": "divergente" if divergentes else "identico",
                           "campos_divergentes": ";".join(divergentes), "detalhe": " | ".join(detalhes)})
    for k in idx_dest:
        if k not in idx_ref:
            resultados.append({"chave": k, "situacao": "extra", "campos_divergentes": "", "detalhe": ""})
    for k in dup_ref:
        resultados.append({"chave": k, "situacao": "chave_duplicada_ref", "campos_divergentes": "", "detalhe": ""})
    for k in dup_dest:
        resultados.append({"chave": k, "situacao": "chave_duplicada_dest", "campos_divergentes": "", "detalhe": ""})
    rt = len(referencia)
    rc = sum(1 for r in resultados if r["situacao"] == "identico")
    resumo = {"rt": rt, "rc": rc, "m22": round(rc / rt, 4) if rt else None,
              "ausentes": sum(r["situacao"] == "ausente" for r in resultados),
              "divergentes": sum(r["situacao"] == "divergente" for r in resultados),
              "extras": sum(r["situacao"] == "extra" for r in resultados)}
    return resultados, resumo


def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def lista(valor):
    return [v.strip() for v in valor.split(",") if v.strip()] if valor else []


def main(argv=None):
    p = argparse.ArgumentParser(description="Comparação campo a campo de M2.2 (só espaços normalizados).")
    p.add_argument("referencia")
    p.add_argument("destino")
    p.add_argument("--chave", required=True)
    p.add_argument("--campos")
    p.add_argument("--ignorar")
    p.add_argument("--mapa", help="ref=dest,ref2=dest2")
    p.add_argument("--formato-ref", choices=sorted(LEITORES))
    p.add_argument("--formato-dest", choices=sorted(LEITORES))
    p.add_argument("--delimitador", help="delimitador dos CSVs (padrão: detectado)")
    p.add_argument("--formato", default="", help="rótulo do formato no resumo (F1 a F7)")
    p.add_argument("--relatorio")
    p.add_argument("--resumo")
    p.add_argument("--avaliador", default="")
    a = p.parse_args(argv)

    try:
        ref = le_registros(a.referencia, a.formato_ref, a.delimitador)
        dest = le_registros(a.destino, a.formato_dest, a.delimitador)
        mapa = dict(par.split("=", 1) for par in lista(a.mapa))
        resultados, resumo = compara(ref, dest, a.chave, lista(a.campos), lista(a.ignorar), mapa)
    except (ErroLeitura, ValueError) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2

    if a.relatorio:
        Path(a.relatorio).parent.mkdir(parents=True, exist_ok=True)
        with open(a.relatorio, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["formato", "chave", "situacao", "campos_divergentes", "detalhe"])
            w.writeheader()
            for r in resultados:
                w.writerow({"formato": a.formato, **r})
    if a.resumo:
        caminho = Path(a.resumo)
        novo = not caminho.exists()
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if novo:
                w.writerow(["data", "avaliador", "formato", "referencia", "sha256_referencia", "destino",
                            "sha256_destino", "rt", "rc", "m22", "ausentes", "divergentes", "extras", "relatorio"])
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), a.avaliador, a.formato,
                        Path(a.referencia).as_posix(), sha256(a.referencia), Path(a.destino).as_posix(),
                        sha256(a.destino), resumo["rt"], resumo["rc"], resumo["m22"], resumo["ausentes"],
                        resumo["divergentes"], resumo["extras"], a.relatorio or ""])

    m22 = "sem registros na referência" if resumo["m22"] is None else f"{resumo['m22']:.4f}"
    print(f"{a.formato or 'comparação'}: Rt = {resumo['rt']}, Rc = {resumo['rc']}, M2.2 = {m22} "
          f"(ausentes {resumo['ausentes']}, divergentes {resumo['divergentes']}, extras {resumo['extras']})")
    for r in resultados:
        if r["situacao"] != "identico":
            print(f"  {r['situacao']}: {r['chave']} {r['detalhe']}".rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
