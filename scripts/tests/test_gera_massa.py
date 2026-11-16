"""Testes da etapa "arquivos" de scripts/gera_massa.py (issue #63).

Uso: python3 -m unittest discover -s scripts/tests
"""

import csv
import importlib.util
import io
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "gera_massa.py"
spec = importlib.util.spec_from_file_location("gera_massa", SCRIPT)
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)


class TestArquivos(unittest.TestCase):
    def setUp(self):
        self.arquivos = gm.arquivos_referencia()

    def test_usuarios(self):
        linhas = list(csv.DictReader(io.StringIO(self.arquivos["usuarios.csv"])))
        self.assertEqual(len(linhas), 30)
        self.assertEqual(linhas[0]["username"], "est01")
        self.assertTrue(all(l["email"].endswith("@example.invalid") for l in linhas))

    def test_gift_tem_15_questoes_com_nome_e_respostas(self):
        questoes = gm.conta_gift(self.arquivos["questoes.gift"])
        self.assertEqual(len(questoes), 15)
        self.assertTrue(all("{" in q and q.endswith("}") for q in questoes))
        self.assertIn("~%50%", self.arquivos["questoes.gift"])

    def test_notas_e_eventos(self):
        notas = list(csv.reader(io.StringIO(self.arquivos["notas.csv"])))
        self.assertEqual(notas[0], ["email", "Avaliação 1", "Avaliação 2", "Participação"])
        self.assertEqual(len(notas), 31)
        eventos = list(csv.DictReader(io.StringIO(self.arquivos["eventos.csv"])))
        self.assertEqual(len(eventos), 6)
        # 19:00 em Brasília (UTC-3) é 22:00 UTC
        self.assertEqual(eventos[0]["DTSTART"], "20261201T220000Z")

    def test_reprodutivel(self):
        self.assertEqual(self.arquivos, gm.arquivos_referencia())

    def test_manifesto_cobre_20_casos_e_prazos_no_fuso(self):
        from datetime import date
        m = gm.manifesto(date(2026, 11, 19))
        o = m["oraculo"]
        self.assertEqual(len(o["questionarios"]) + len(o["agregacoes"]) + 4, 20)
        p01 = next(p for p in o["prazos"] if p["caso"] == "P-01 e P-02")
        self.assertEqual(p01["data_limite"], 1795143540)  # 2026-11-19 23:59 em Brasília
        json.dumps(m)  # serializável para o executor PHP

    def test_verificar_aceita_os_arquivos_gerados(self):
        with tempfile.TemporaryDirectory() as tmp:
            gm.etapa_arquivos(Namespace(saida=tmp))
            self.assertEqual(gm.etapa_verificar(Namespace(saida=tmp)), 0)


if __name__ == "__main__":
    unittest.main()
