"""Testes do compara_registros.py com pares de arquivos conhecidos (issue #65).

Rodar da raiz do repositório:  python3 -m unittest discover -s scripts/tests -v
"""

import io
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))

import compara_registros as cr  # noqa: E402

TESTE = RAIZ / "dados" / "avaliacao" / "M2.2" / "teste"


def grava(pasta, nome, conteudo):
    caminho = Path(pasta) / nome
    caminho.write_bytes(conteudo if isinstance(conteudo, bytes) else conteudo.encode("utf-8"))
    return caminho


class ParConhecido(unittest.TestCase):
    """O par de dados/avaliacao/M2.2/teste/ tem resultado esperado documentado no README da pasta."""

    def test_par_csv(self):
        ref = cr.le_registros(TESTE / "referencia.csv")
        dest = cr.le_registros(TESTE / "destino.csv")
        resultados, resumo = cr.compara(ref, dest, "username")
        situacao = {r["chave"]: r["situacao"] for r in resultados}
        self.assertEqual(situacao, {"est01": "identico", "est02": "identico", "est03": "divergente",
                                    "est04": "ausente", "est99": "extra"})
        self.assertEqual((resumo["rt"], resumo["rc"], resumo["m22"]), (4, 2, 0.5))
        est03 = next(r for r in resultados if r["chave"] == "est03")
        self.assertEqual(est03["campos_divergentes"], "firstname;lastname")

    def test_cli_grava_relatorio_e_resumo(self):
        with tempfile.TemporaryDirectory() as tmp:
            rel, res = Path(tmp) / "rel.csv", Path(tmp) / "resumo.csv"
            codigo = cr.main([str(TESTE / "referencia.csv"), str(TESTE / "destino.csv"), "--chave", "username",
                              "--formato", "teste", "--relatorio", str(rel), "--resumo", str(res),
                              "--avaliador", "XX"])
            self.assertEqual(codigo, 0)
            self.assertIn("est03", rel.read_text(encoding="utf-8"))
            linha = res.read_text(encoding="utf-8").splitlines()[1].split(",")
            self.assertEqual(linha[7:10], ["4", "2", "0.5"])


class Normalizacao(unittest.TestCase):
    def test_so_espacos(self):
        self.assertEqual(cr.normaliza("  a \t b\n c "), "a b c")
        self.assertNotEqual(cr.normaliza("7,80"), cr.normaliza("7.8"))
        self.assertNotEqual(cr.normaliza("Ação"), cr.normaliza("Acao"))
        self.assertNotEqual(cr.normaliza("Ana"), cr.normaliza("ana"))

    def test_mapa_e_ignorar(self):
        ref = [{"username": "est01", "firstname": "Ana", "id": "1"}]
        dest = [{"Usuário": "est01", "Nome": "Ana", "id": "77"}]
        _, resumo = cr.compara(ref, dest, "username", ignorar=["id"], mapa={"username": "Usuário", "firstname": "Nome"})
        self.assertEqual(resumo["rc"], 1)

    def test_chave_inexistente(self):
        with self.assertRaises(cr.ErroLeitura):
            cr.compara([{"a": "1"}], [{"a": "1"}], "username")


class Leitores(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pasta = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_csv_ponto_e_virgula(self):
        c = grava(self.pasta, "notas.csv", "email;P1;P2\nest01@example.invalid;7,50;8,00\n")
        self.assertEqual(cr.le_registros(c), [{"email": "est01@example.invalid", "P1": "7,50", "P2": "8,00"}])

    def test_xlsx(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("xl/sharedStrings.xml",
                       '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                       "<si><t>email</t></si><si><t>P1</t></si><si><t>est01@example.invalid</t></si></sst>")
            z.writestr("xl/worksheets/sheet1.xml",
                       '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
                       '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
                       '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2"><v>7.5</v></c></row>'
                       "</sheetData></worksheet>")
        x = grava(self.pasta, "notas.xlsx", buf.getvalue())
        self.assertEqual(cr.le_registros(x), [{"email": "est01@example.invalid", "P1": "7.5"}])

    def test_gift(self):
        g = grava(self.pasta, "q.gift", "// comentário\n$CATEGORY: $course$/Teste\n\n"
                                       "::Q01:: Quanto é 2 + 2? {=4 ~3 ~5}\n\n"
                                       "::Q02::[html]A capital do Brasil é {=Brasília ~Rio}\n")
        regs = cr.le_registros(g)
        self.assertEqual([r["nome"] for r in regs], ["Q01", "Q02"])
        self.assertEqual(regs[0]["enunciado"], "Quanto é 2 + 2?")
        self.assertEqual(cr.normaliza(regs[0]["respostas"]), "=4 ~3 ~5")
        self.assertEqual(regs[1]["enunciado"], "A capital do Brasil é")

    def test_moodle_xml(self):
        x = grava(self.pasta, "q.xml", '<?xml version="1.0"?><quiz>'
                                      '<question type="category"><category><text>$course$/T</text></category></question>'
                                      '<question type="multichoice"><name><text>Q01</text></name>'
                                      "<questiontext><text>2 + 2?</text></questiontext><defaultgrade>1.0000000</defaultgrade>"
                                      '<answer fraction="100"><text>4</text></answer><answer fraction="0"><text>3</text></answer>'
                                      "</question></quiz>")
        self.assertEqual(cr.le_registros(x), [{"tipo": "multichoice", "nome": "Q01", "enunciado": "2 + 2?",
                                               "respostas": "100:4 | 0:3", "nota_padrao": "1.0000000"}])

    def test_ics_com_linha_dobrada(self):
        i = grava(self.pasta, "c.ics", "BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:1@x\r\n"
                                      "SUMMARY:Entrega da tarefa 1 do curso de\r\n  avaliação\r\n"
                                      "DTSTART;VALUE=DATE-TIME:20261120T235900Z\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
        self.assertEqual(cr.le_registros(i), [{"UID": "1@x", "SUMMARY": "Entrega da tarefa 1 do curso de avaliação",
                                               "DTSTART": "20261120T235900Z"}])

    def test_mbz_tar_gz(self):
        xml = (b"<moodle_backup><information><contents><activities>"
               b"<activity><moduleid>5</moduleid><sectionid>2</sectionid><modulename>assign</modulename>"
               b"<title>Tarefa 1</title></activity></activities></contents></information></moodle_backup>")
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t:
            info = tarfile.TarInfo("moodle_backup.xml")
            info.size = len(xml)
            t.addfile(info, io.BytesIO(xml))
        m = grava(self.pasta, "curso.mbz", buf.getvalue())
        self.assertEqual(cr.le_registros(m), [{"modulename": "assign", "title": "Tarefa 1", "sectionid": "2"}])

    def test_formato_desconhecido(self):
        f = grava(self.pasta, "x.pdf", "nada")
        with self.assertRaises(cr.ErroLeitura):
            cr.le_registros(f)


class Congelamento(unittest.TestCase):
    """congela_referencia.py, apontado para uma pasta temporária."""

    def setUp(self):
        import congela_referencia as cg
        self.cg = cg
        self.tmp = tempfile.TemporaryDirectory()
        self.antigos = (cg.PASTA, cg.MANIFESTO)
        cg.PASTA = Path(self.tmp.name) / "referencia"
        cg.MANIFESTO = cg.PASTA / "MANIFESTO.csv"
        self.origem = grava(self.tmp.name, "usuarios.csv", "username\nest01\n")

    def tearDown(self):
        self.cg.PASTA, self.cg.MANIFESTO = self.antigos
        self.tmp.cleanup()

    def test_congela_verifica_e_detecta_alteracao(self):
        self.assertEqual(self.cg.main(["--responsavel", "XX", f"F1={self.origem}"]), 0)
        self.assertTrue((self.cg.PASTA / "F1_usuarios.csv").exists())
        self.assertEqual(self.cg.main(["--verificar"]), 0)
        (self.cg.PASTA / "F1_usuarios.csv").write_bytes(b"username\nest02\n")
        self.assertEqual(self.cg.main(["--verificar"]), 1)

    def test_nao_substitui_sem_opcao(self):
        self.cg.main(["--responsavel", "XX", f"F1={self.origem}"])
        self.assertEqual(self.cg.main(["--responsavel", "XX", f"F1={self.origem}"]), 2)
        self.assertEqual(self.cg.main(["--responsavel", "XX", "--substituir", f"F1={self.origem}"]), 0)


if __name__ == "__main__":
    unittest.main()
