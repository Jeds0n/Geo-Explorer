"""Testes do comando /certificado (certificado.py)."""

import os
import re
import tempfile
import unittest
from datetime import date

from geo_explorer.src.certificado import (
    formatar_certificado, gerar_certificado, parsear_argumentos, salvar_certificado,
)

HOJE = date(2026, 10, 7)


class TestParsearArgumentos(unittest.TestCase):
    def test_nome_e_trilha(self):
        self.assertEqual(parsear_argumentos("Ana Souza | Python"), ("Ana Souza", "Python", None))

    def test_com_nivel(self):
        self.assertEqual(parsear_argumentos("Ana | Python | Básico"), ("Ana", "Python", "Básico"))

    def test_sem_separador(self):
        with self.assertRaises(ValueError):
            parsear_argumentos("Ana Python")


class TestGerarCertificado(unittest.TestCase):
    def test_dados_vem_da_trilha(self):
        c = gerar_certificado("Ana Souza", "Python", "Básico", seed=1, hoje=HOJE)
        self.assertEqual(c["trilha"], "Python: Primeiros Passos")
        self.assertEqual(c["xp_total"], 5000)
        self.assertEqual(c["data_emissao"], "07/10/2026")
        self.assertEqual(len(c["conteudos"]), 5)

    def test_busca_pelo_nome_completo(self):
        c = gerar_certificado("Ana", "Python: Dados e APIs", hoje=HOJE)
        self.assertEqual(c["nivel"], "Intermediário")

    def test_codigo_no_formato(self):
        c = gerar_certificado("Ana", "sql", "avancado", hoje=HOJE)
        self.assertRegex(c["codigo"], r"^GEO-2026\d{6}$")

    def test_mesma_seed_mesmo_codigo(self):
        a = gerar_certificado("Ana", "sql", "básico", seed=5, hoje=HOJE)
        b = gerar_certificado("Bia", "sql", "básico", seed=5, hoje=HOJE)
        self.assertEqual(a["codigo"], b["codigo"])

    def test_trilha_inexistente(self):
        with self.assertRaises(ValueError):
            gerar_certificado("Ana", "cobol")

    def test_termo_ambiguo_pede_nivel(self):
        with self.assertRaises(ValueError) as ctx:
            gerar_certificado("Ana", "Python")
        self.assertIn("mais de uma trilha", str(ctx.exception))

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            gerar_certificado("  ", "Python", "Básico")


class TestTodasAsTrilhas(unittest.TestCase):
    def test_certificado_para_cada_trilha_da_base(self):
        from geo_explorer.src.dados import carregar_trilhas
        trilhas = carregar_trilhas()
        self.assertEqual(len(trilhas), 36)
        for t in trilhas:
            c = gerar_certificado("Ana", t["nome"], hoje=HOJE, seed=1)
            self.assertEqual(c["trilha"], t["nome"])
            self.assertEqual(c["conteudos"], t["modulos"])


class TestFormatarESalvar(unittest.TestCase):
    def setUp(self):
        self.cert = gerar_certificado("Maria da Silva", "Java", "Avançado", seed=3, hoje=HOJE)

    def test_texto_do_certificado(self):
        texto = formatar_certificado(self.cert)
        for esperado in ["MARIA DA SILVA", "Java: Microsserviços e Concorrência",
                         self.cert["codigo"], "07/10/2026", "Parabéns, Maria", "fictício"]:
            self.assertIn(esperado, texto)

    def test_lista_todos_os_modulos(self):
        texto = formatar_certificado(self.cert)
        for m in self.cert["conteudos"]:
            self.assertIn(m, texto)

    def test_salvar_cria_arquivo(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = salvar_certificado(self.cert, pasta)
            self.assertTrue(os.path.exists(caminho))
            self.assertRegex(os.path.basename(caminho), r"^GEO-\d+-maria-da-silva\.md$")
            with open(caminho, encoding="utf-8") as f:
                self.assertIn("MARIA DA SILVA", f.read())


if __name__ == "__main__":
    unittest.main()
