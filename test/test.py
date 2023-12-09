import unittest
from fastapi.testclient import TestClient
from app.main import app  # Importando o aplicativo FastAPI

client = TestClient(app)


class TestCarRoutes(unittest.TestCase):
    def test_create_car(self):
        # Substitua com os dados de teste relevantes
        response = client.post("/cars/", json={"marca": "Teste", "modelo": "Teste"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("marca", response.json())

    # Adicione métodos de teste para read, update e delete


class TestUserRoutes(unittest.TestCase):
    def test_create_user(self):
        # Substitua com os dados de teste relevantes
        response = client.post(
            "/users/", json={"username": "Teste", "password": "Teste"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())

    # Adicione métodos de teste para read, update e delete


if __name__ == "__main__":
    unittest.main()
