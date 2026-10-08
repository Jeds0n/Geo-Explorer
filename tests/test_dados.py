"""Testes da base de dados e dos utilitários (dados.py)."""

import json
import unittest

from geo_explorer.src.dados import (
    DESAFIOS_PATH, NIVEIS, carregar_desafios, carregar_trilhas,
    normalizar, normalizar_nivel,
)

CAMPOS = {"id", "nome", "tecnologia", "nivel", "carga_horaria", "xp_total",
          "vagas_disponiveis", "modulos", "lives", "promocao"}


class TestNormalizar(unittest.TestCase):
    def test_remove_acento_e_caixa(self):
        self.assertEqual(normalizar("  Avançado "), "avancado")

    def test_nivel_sem_acento(self):
        self.assertEqual(normalizar_nivel("basico"), "Básico")
        self.assertEqual(normalizar_nivel("INTERMEDIARIO"), "Intermediário")

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            normalizar_nivel("mestre")


class TestBaseDeTrilhas(unittest.TestCase):
    def setUp(self):
        self.trilhas = carregar_trilhas()

    def test_campos_obrigatorios(self):
        for t in self.trilhas:
            self.assertTrue(CAMPOS <= set(t), f"campos faltando em {t.get('nome')}")

    def test_ids_unicos(self):
        ids = [t["id"] for t in self.trilhas]
        self.assertEqual(len(ids), len(set(ids)))

    def test_niveis_validos_e_modulos_nao_vazios(self):
        for t in self.trilhas:
            self.assertIn(t["nivel"], NIVEIS)
            self.assertGreaterEqual(len(t["modulos"]), 3)

    def test_cada_tecnologia_tem_os_tres_niveis(self):
        por_tec = {}
        for t in self.trilhas:
            por_tec.setdefault(t["tecnologia"], set()).add(t["nivel"])
        for tec, niveis in por_tec.items():
            self.assertEqual(niveis, set(NIVEIS), tec)

    def test_promocao_ativa_tem_validade(self):
        for t in self.trilhas:
            p = t["promocao"]
            if p["ativa"]:
                self.assertTrue(p["validade"])
                self.assertGreater(p["desconto_percentual"], 0)


class TestBaseDeDesafios(unittest.TestCase):
    def test_json_valido(self):
        with open(DESAFIOS_PATH, encoding="utf-8") as f:
            json.load(f)

    def test_todas_tecnologias_das_trilhas_tem_desafio(self):
        techs = {t["tecnologia"] for t in carregar_trilhas()}
        self.assertEqual(techs, set(carregar_desafios()))

    def test_estrutura_dos_desafios(self):
        chaves = {"titulo", "enunciado", "entrada", "saida", "dicas", "restricoes"}
        for tec, niveis in carregar_desafios().items():
            self.assertEqual(set(niveis), set(NIVEIS), tec)
            for nivel, lista in niveis.items():
                self.assertGreaterEqual(len(lista), 2, f"{tec}/{nivel}")
                for d in lista:
                    self.assertEqual(set(d), chaves)


if __name__ == "__main__":
    unittest.main()
