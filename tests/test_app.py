import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Encurtador", response.data)

    def test_api_encurtar_sucesso(self):
        response = self.client.post(
            "/api/encurtar",
            data=json.dumps({"url": "https://openai.com"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["sucesso"])
        self.assertIn("codigo", data)
        self.assertIn("url_encurtada", data)

    def test_api_encurtar_vazio(self):
        response = self.client.post(
            "/api/encurtar",
            data=json.dumps({"url": ""}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["sucesso"])

    def test_api_buscar_sucesso(self):
        # Primeiro cria
        res_post = self.client.post(
            "/api/encurtar",
            data=json.dumps({"url": "https://flask.palletsprojects.com"}),
            content_type="application/json"
        )
        data_post = res_post.get_json()
        codigo = data_post["codigo"]

        # Busca
        response = self.client.post(
            "/api/buscar",
            data=json.dumps({"termo": codigo}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["sucesso"])
        self.assertEqual(data["destino"], "https://flask.palletsprojects.com")

    def test_api_buscar_inexistente(self):
        response = self.client.post(
            "/api/buscar",
            data=json.dumps({"termo": "99999"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data["sucesso"])

    def test_redirecionamento_302(self):
        res_post = self.client.post(
            "/api/encurtar",
            data=json.dumps({"url": "https://docs.python.org"}),
            content_type="application/json"
        )
        data_post = res_post.get_json()
        codigo = data_post["codigo"]

        # Acessa /<codigo>
        response = self.client.get(f"/{codigo}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "https://docs.python.org")

    def test_redirecionamento_404(self):
        response = self.client.get("/cod_inexistente")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Link", response.data)

    def test_api_links(self):
        response = self.client.get("/api/links")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["sucesso"])
        self.assertIsInstance(data["links"], list)

if __name__ == "__main__":
    unittest.main()
