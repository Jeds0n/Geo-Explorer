"""Testes do comando /desafio (desafio.py)."""

import unittest

from geo_explorer.src.dados import NIVEIS, carregar_desafios
from geo_explorer.src.desafio import formatar_desafio, obter_desafio


class TestObterDesafio(unittest.TestCase):
    def test_retorna_desafio_do_catalogo(self):
        d = obter_desafio("Python", "Básico", seed=1)
        titulos = [x["titulo"] for x in carregar_desafios()["Python"]["Básico"]]
        self.assertIn(d["titulo"], titulos)
        self.assertEqual(d["nivel"], "Básico")

    def test_mesma_seed_mesmo_desafio(self):
        self.assertEqual(obter_desafio("java", "avançado", seed=7),
                         obter_desafio("java", "avançado", seed=7))

    def test_aceita_nivel_sem_acento_e_tecnologia_em_minusculas(self):
        d = obter_desafio("sql", "avancado", seed=0)
        self.assertEqual((d["tecnologia"], d["nivel"]), ("SQL", "Avançado"))

    def test_nivel_padrao_e_intermediario(self):
        self.assertEqual(obter_desafio("python", seed=0)["nivel"], "Intermediário")

    def test_sorteio_varia_entre_seeds(self):
        titulos = {obter_desafio("python", "básico", seed=s)["titulo"] for s in range(30)}
        self.assertGreater(len(titulos), 1)

    def test_tecnologia_inexistente(self):
        with self.assertRaises(ValueError) as ctx:
            obter_desafio("cobol", "básico")
        self.assertIn("Disponíveis", str(ctx.exception))

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            obter_desafio("python", "mestre")

    def test_todas_as_combinacoes_funcionam(self):
        for tec in carregar_desafios():
            for nivel in NIVEIS:
                self.assertIn("enunciado", obter_desafio(tec, nivel, seed=0))


class TestCatalogoCompleto(unittest.TestCase):
    def test_72_desafios_com_titulos_unicos_por_nivel(self):
        total = 0
        for tec, niveis in carregar_desafios().items():
            for nivel, lista in niveis.items():
                titulos = [d["titulo"] for d in lista]
                self.assertEqual(len(titulos), len(set(titulos)), f"{tec}/{nivel}")
                total += len(lista)
        self.assertEqual(total, 72)

    def test_campos_de_texto_nao_vazios(self):
        for niveis in carregar_desafios().values():
            for lista in niveis.values():
                for d in lista:
                    for campo in ("titulo", "enunciado", "entrada", "saida"):
                        self.assertTrue(d[campo].strip(), campo)
                    self.assertTrue(d["dicas"] and d["restricoes"])

    def test_novas_tecnologias(self):
        for tec in ("TypeScript", "React", "Análise de Dados", "DevOps", "Segurança", "Git e GitHub"):
            self.assertIn("enunciado", obter_desafio(tec, "avançado", seed=0))


class TestFormatarDesafio(unittest.TestCase):
    def test_contem_secoes(self):
        texto = formatar_desafio(obter_desafio("java", "básico", seed=0))
        for secao in ["Enunciado", "Entrada", "Saída esperada", "Dicas", "Restrições", "Java (Básico)"]:
            self.assertIn(secao, texto)


if __name__ == "__main__":
    unittest.main()
