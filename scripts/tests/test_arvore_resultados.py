"""A página da árvore GQM de resultados está em dia com calculos.csv e com o Mermaid da Fase 2."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import gera_arvore_resultados as gar  # noqa: E402


class ArvoreResultados(unittest.TestCase):
    def test_pagina_em_dia(self):
        self.assertEqual(gar.SAIDA.read_text(encoding="utf-8"), gar.gera(),
                         "rode: python3 scripts/gera_arvore_resultados.py")

    def test_todas_as_metricas_e_questoes_tem_nome(self):
        nomes = gar.rotulos()
        for chave in list(gar.cj.HIPOTESES) + list(gar.cj.METRICAS_DA_QUESTAO) + list(gar.cj.QUESTAO_DO_OBJETIVO):
            with self.subTest(chave=chave):
                self.assertTrue(nomes.get(chave), f"{chave} sem nome no Mermaid de diagrama-gqm.md")


if __name__ == "__main__":
    unittest.main()
