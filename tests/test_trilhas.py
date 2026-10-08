"""Testes do comando /trilha (trilhas.py)."""

import unittest

from geo_explorer.src.trilhas import (
    buscar_trilhas, formatar_lives, formatar_promocao, formatar_trilha,
    listar_tecnologias,
)

MOCK = [
    {"id": 1, "nome": "Alfa: Início", "tecnologia": "Alfa", "nivel": "Básico",
     "carga_horaria": 10, "xp_total": 2500, "vagas_disponiveis": 5,
     "modulos": ["Um", "Dois", "Três"],
     "lives": [{"titulo": "Live A", "data": "2026-11-01", "horario": "19:00"}],
     "promocao": {"ativa": True, "desconto_percentual": 20, "validade": "2026-12-31"}},
    {"id": 2, "nome": "Alfa: Avançado", "tecnologia": "Alfa", "nivel": "Avançado",
     "carga_horaria": 30, "xp_total": 7500, "vagas_disponiveis": 0,
     "modulos": ["X", "Y", "Z"], "lives": [],
     "promocao": {"ativa": False, "desconto_percentual": 0, "validade": None}},
    {"id": 3, "nome": "Beta: Início", "tecnologia": "Beta Café", "nivel": "Básico",
     "carga_horaria": 8, "xp_total": 2000, "vagas_disponiveis": 9,
     "modulos": ["M1", "M2", "M3"], "lives": [],
     "promocao": {"ativa": False, "desconto_percentual": 0, "validade": None}},
]


class TestBuscarTrilhas(unittest.TestCase):
    def test_busca_ignora_caixa(self):
        self.assertEqual(len(buscar_trilhas("ALFA", trilhas=MOCK)), 2)

    def test_busca_ignora_acento(self):
        self.assertEqual(buscar_trilhas("cafe", trilhas=MOCK)[0]["id"], 3)

    def test_busca_parcial_pelo_nome(self):
        self.assertEqual(buscar_trilhas("início", trilhas=MOCK)[0]["id"], 1)

    def test_filtro_por_nivel(self):
        r = buscar_trilhas("alfa", nivel="avancado", trilhas=MOCK)
        self.assertEqual([t["id"] for t in r], [2])

    def test_sem_resultado(self):
        self.assertEqual(buscar_trilhas("cobol", trilhas=MOCK), [])

    def test_termo_vazio_nao_retorna_tudo(self):
        self.assertEqual(buscar_trilhas("   ", trilhas=MOCK), [])

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            buscar_trilhas("alfa", nivel="mestre", trilhas=MOCK)

    def test_exata_tem_prioridade_sobre_parcial(self):
        # "java" existe como tecnologia; não deve trazer "JavaScript"
        techs = {t["tecnologia"] for t in buscar_trilhas("java")}
        self.assertEqual(techs, {"Java"})

    def test_parcial_quando_nao_ha_exata(self):
        techs = {t["tecnologia"] for t in buscar_trilhas("script")}
        self.assertEqual(techs, {"JavaScript", "TypeScript"})

    def test_tecnologia_com_acento_e_espaco(self):
        r = buscar_trilhas("analise de dados", nivel="avancado")
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["nome"], "Análise de Dados: Machine Learning")

    def test_git_exato_nao_traz_outras(self):
        self.assertEqual({t["tecnologia"] for t in buscar_trilhas("git e github")}, {"Git e GitHub"})

    def test_cada_tecnologia_retorna_tres_trilhas(self):
        for tec in listar_tecnologias():
            self.assertEqual(len(buscar_trilhas(tec)), 3, tec)

    def test_base_real_python(self):
        self.assertEqual(len(buscar_trilhas("python")), 3)


class TestListarTecnologias(unittest.TestCase):
    def test_sem_repeticao_e_ordenado(self):
        self.assertEqual(listar_tecnologias(MOCK), ["Alfa", "Beta Café"])

    def test_base_real(self):
        techs = listar_tecnologias()
        self.assertIn("Java", techs)
        self.assertEqual(len(techs), 12)


class TestFormatacao(unittest.TestCase):
    def test_promocao_ativa(self):
        self.assertEqual(formatar_promocao(MOCK[0]),
                         "Desconto de 20% válido até 2026-12-31.")

    def test_promocao_inativa(self):
        self.assertEqual(formatar_promocao(MOCK[1]),
                         "Nenhuma promoção ativa no momento.")

    def test_lives(self):
        self.assertEqual(formatar_lives(MOCK[0]),
                         ["Live A — 2026-11-01 às 19:00"])

    def test_trilha_completa(self):
        texto = formatar_trilha(MOCK[0])
        for esperado in ["## Alfa: Início", "10h", "2500 XP", "1. Um", "3. Três", "Live A"]:
            self.assertIn(esperado, texto)


if __name__ == "__main__":
    unittest.main()
