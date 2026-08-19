import unittest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from service.encurtador import Encurtador, Encutador

class TestEncurtadorService(unittest.TestCase):
    def setUp(self):
        self.service = Encurtador()

    def test_encurtar_url_nova(self):
        url = "https://google.com"
        res = self.service.encutar_url(url)
        self.assertTrue(res["sucesso"])
        self.assertFalse(res["ja_existia"])
        self.assertEqual(len(res["codigo"]), 5)
        self.assertTrue(res["url_encurtada"].endswith(res["codigo"]))

    def test_encurtar_url_existente(self):
        url = "https://github.com"
        res1 = self.service.encutar_url(url)
        res2 = self.service.encutar_url(url)
        self.assertTrue(res2["sucesso"])
        self.assertTrue(res2["ja_existia"])
        self.assertEqual(res1["codigo"], res2["codigo"])

    def test_obter_destino_por_codigo_e_url(self):
        url = "https://python.org"
        res = self.service.encutar_url(url)
        codigo = res["codigo"]

        # Busca pelo código simples
        busca_cod = self.service.obter_destino(codigo)
        self.assertTrue(busca_cod["sucesso"])
        self.assertEqual(busca_cod["destino"], url)

        # Busca pela URL completa
        busca_url = self.service.obter_destino(f"https://encutador.com.br/{codigo}")
        self.assertTrue(busca_url["sucesso"])
        self.assertEqual(busca_url["destino"], url)

    def test_codigo_inexistente(self):
        busca = self.service.obter_destino("codigo_falso_123")
        self.assertFalse(busca["sucesso"])

    def test_listar_links(self):
        self.service.encutar_url("https://site1.com")
        self.service.encutar_url("https://site2.com")
        lista = self.service.listar_links()
        self.assertEqual(len(lista), 2)

if __name__ == "__main__":
    unittest.main()
