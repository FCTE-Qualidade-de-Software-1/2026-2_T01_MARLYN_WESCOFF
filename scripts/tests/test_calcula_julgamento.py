"""Testes do calcula_julgamento.py contra a Tabela 2 e a Tabela 4 de Níveis de pontuação e julgamento (#72).

Rodar da raiz do repositório:  python3 -m unittest discover -s scripts/tests -v
"""

import csv
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))

import calcula_julgamento as cj  # noqa: E402


def linha(metrica, num=None, den=None, valor=None, r=None, condicao=""):
    return {"metrica": metrica, "numerador": "" if num is None else str(num),
            "denominador": "" if den is None else str(den), "valor_direto": "" if valor is None else str(valor),
            "retentativas": "" if r is None else str(r), "condicao": condicao}


class NiveisPorContagem(unittest.TestCase):
    """Os degraus da Tabela 2 expressos em contagem (12/12, 11/12, ...) caem na nota indicada."""

    def casos(self, metrica, total, esperado):
        for acertos, nota in esperado.items():
            with self.subTest(metrica=metrica, acertos=acertos):
                self.assertEqual(cj.nota(metrica, acertos / total), nota)

    def test_m11_e_m32(self):
        for m in ("M1.1", "M3.2"):
            self.casos(m, 12, {12: 4, 11: 3, 10: 2, 9: 1})

    def test_m13(self):
        self.casos("M1.3", 12, {12: 4, 11: 3, 9: 2, 8: 1})

    def test_m21(self):
        self.casos("M2.1", 7, {7: 4, 6: 3, 5: 2, 4: 1})

    def test_m23_e_m33(self):
        for m in ("M2.3", "M3.3"):
            self.casos(m, 6, {6: 4, 5: 3, 4: 2, 3: 1})

    def test_m31(self):
        self.casos("M3.1", 8, {8: 4, 7: 3, 6: 2, 5: 1})

    def test_m22(self):
        for valor, n in ((1.0, 4), (0.99, 3), (0.97, 2), (0.95, 2), (0.94, 1)):
            with self.subTest(valor=valor):
                self.assertEqual(cj.nota("M2.2", valor), n)


    def test_nota_4_exige_valor_exato(self):
        """Revisão do PR #86: 0,995 não pode virar 1,00 e ganhar nota 4."""
        self.assertEqual(cj.nota("M2.2", 199 / 200), 3)
        self.assertEqual(cj.nota("M3.2", 0.996), 3)
        self.assertEqual(cj.nota("M3.5", 199 / 200, None, {"perda_nao_academica"}), 2)
        self.assertEqual(cj.nota("M1.2", 199 / 200, condicoes={"so_prazo"}), 2)
        self.assertEqual(cj.nota("M2.2", 1.0), 4)
        metricas, _, _ = cj.calcula([linha("M2.2", 199, 200)] + [linha(m) for m in cj.HIPOTESES if m != "M2.2"])
        self.assertEqual((metricas["M2.2"]["nota"], metricas["M2.2"]["resultado_hipotese"]), (3, "refutada"))


class RegrasEspeciais(unittest.TestCase):
    def test_m12_sem_nota_3(self):
        self.assertEqual(cj.nota("M1.2", 1.0), 4)
        self.assertEqual(cj.nota("M1.2", 19 / 20, condicoes={"so_prazo"}), 2)
        self.assertEqual(cj.nota("M1.2", 19 / 20), 1)
        self.assertEqual(cj.nota("M1.2", 19 / 20, condicoes={"so_prazo", "nota_final_errada"}), 1)

    def test_m24_sem_nota_3(self):
        self.assertEqual(cj.nota("M2.4", 3 / 3), 4)
        self.assertEqual(cj.nota("M2.4", 2 / 3, condicoes={"recuperacao_sem_intervencao"}), 2)
        self.assertEqual(cj.nota("M2.4", 2 / 3), 1)
        self.assertEqual(cj.nota("M2.4", 1 / 3, condicoes={"recuperacao_sem_intervencao"}), 1)

    def test_m34_tempo_e_retentativas(self):
        for minutos, r, n in ((12, 0, 4), (12, 1, 3), (25, 0, 3), (45, 2, 2), (61, 0, 1), (10, 4, 1)):
            with self.subTest(minutos=minutos, r=r):
                self.assertEqual(cj.nota("M3.4", minutos, r), n)

    def test_m35_sem_nota_3(self):
        self.assertEqual(cj.nota("M3.5", 40 / 40), 4)
        self.assertEqual(cj.nota("M3.5", 39 / 40, condicoes={"perda_nao_academica"}), 2)
        self.assertEqual(cj.nota("M3.5", 39 / 40, condicoes={"perda_academica"}), 1)
        self.assertEqual(cj.nota("M3.5", 39 / 40), 1)


class Julgamento(unittest.TestCase):
    def test_exemplo_da_fase_2(self):
        """Exemplo de aplicação da página Níveis de pontuação e julgamento: G2 = Atende com ressalvas."""
        linhas = [linha("M2.1", 6, 7), linha("M2.2", 97, 100), linha("M2.3", 6, 6), linha("M2.4", 3, 3)]
        metricas, questoes, objetivos = cj.calcula(linhas + [linha(m) for m in cj.HIPOTESES if m[:2] != "M2"])
        self.assertEqual([questoes[q] for q in ("Q2.1", "Q2.2", "Q2.3", "Q2.4")], [3, 2, 4, 4])
        self.assertEqual(objetivos["G2"]["julgamento"], "Atende com ressalvas")
        self.assertEqual(metricas["M2.2"]["resultado_hipotese"], "refutada")
        self.assertEqual(metricas["M2.1"]["resultado_hipotese"], "confirmada")
        self.assertEqual(objetivos["G1"]["julgamento"], "incompleto")

    def test_pior_caso(self):
        self.assertEqual(cj.julga_objetivo([4, 4, 3]), "Atende")
        self.assertEqual(cj.julga_objetivo([4, 2, 3]), "Atende com ressalvas")
        self.assertEqual(cj.julga_objetivo([4, 2, 1]), "Não atende")
        self.assertEqual(cj.julga_objetivo([4, None]), "incompleto")

    def test_q33_e_o_minimo_de_m33_e_m34(self):
        linhas = [linha("M3.3", 6, 6), linha("M3.4", valor=25, r=0)]
        _, questoes, _ = cj.calcula(linhas + [linha(m) for m in cj.HIPOTESES if m not in ("M3.3", "M3.4")])
        self.assertEqual(questoes["Q3.3"], 3)

    def test_planilha_versionada_ainda_pendente(self):
        with open(RAIZ / "dados" / "avaliacao" / "calculos.csv", encoding="utf-8-sig") as f:
            linhas = list(csv.DictReader(f))
        self.assertEqual(sorted(l["metrica"] for l in linhas), sorted(cj.HIPOTESES))
        metricas, _, objetivos = cj.calcula(linhas)
        self.assertTrue(all(m["resultado_hipotese"] == "pendente" for m in metricas.values()))
        self.assertTrue(all(o["julgamento"] == "incompleto" for o in objetivos.values()))


if __name__ == "__main__":
    unittest.main()
