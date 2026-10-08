"""Testes da interface de linha de comando (cli.py)."""

import contextlib
import io
import unittest

from geo_explorer.src.cli import executar


def rodar(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        codigo = executar(list(argv))
    return codigo, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_listar(self):
        codigo, out, _ = rodar("listar")
        self.assertEqual(codigo, 0)
        self.assertIn("- Python", out)

    def test_trilha(self):
        codigo, out, _ = rodar("trilha", "java", "--nivel", "básico")
        self.assertEqual(codigo, 0)
        self.assertIn("Java: Orientação a Objetos do Zero", out)

    def test_trilha_inexistente(self):
        codigo, out, _ = rodar("trilha", "cobol")
        self.assertEqual(codigo, 1)
        self.assertIn("Disponíveis", out)

    def test_desafio(self):
        codigo, out, _ = rodar("desafio", "sql", "básico")
        self.assertEqual(codigo, 0)
        self.assertIn("Desafio de Código", out)

    def test_desafio_nivel_invalido(self):
        codigo, _, err = rodar("desafio", "sql", "mestre")
        self.assertEqual(codigo, 1)
        self.assertIn("Nível inválido", err)

    def test_certificado(self):
        codigo, out, _ = rodar("certificado", "Ana Souza", "python", "básico")
        self.assertEqual(codigo, 0)
        self.assertIn("ANA SOUZA", out)

    def test_certificado_salvar(self):
        import os, tempfile
        antes = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                codigo, out, _ = rodar("certificado", "Ana Souza", "git e github", "básico", "--salvar")
                self.assertEqual(codigo, 0)
                self.assertIn("Salvo em:", out)
                self.assertEqual(len(os.listdir("docs/certificados-emitidos")), 1)
            finally:
                os.chdir(antes)

    def test_listar_mostra_12_tecnologias(self):
        _, out, _ = rodar("listar")
        self.assertEqual(len(out.strip().splitlines()), 12)

    def test_certificado_ambiguo(self):
        codigo, _, err = rodar("certificado", "Ana", "python")
        self.assertEqual(codigo, 1)
        self.assertIn("mais de uma trilha", err)


if __name__ == "__main__":
    unittest.main()
