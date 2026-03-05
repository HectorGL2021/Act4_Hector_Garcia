"""
Tests unitarios para la aplicación Flask.
Ejecutar con: pytest test_app.py -v
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_status_code(client):
    """Verifica que la ruta / devuelve status code 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_index_content_type(client):
    """Verifica que la respuesta es JSON."""
    response = client.get("/")
    assert response.content_type == "application/json"


def test_index_message(client):
    """Verifica que la respuesta contiene el mensaje de saludo."""
    response = client.get("/")
    data = response.get_json()
    assert "mensaje" in data
    assert "Bienvenido" in data["mensaje"]


def test_index_autor(client):
    """Verifica que la respuesta contiene el campo autor."""
    response = client.get("/")
    data = response.get_json()
    assert data["autor"] == "Héctor García"


def test_index_status_field(client):
    """Verifica que la respuesta contiene el campo status ok."""
    response = client.get("/")
    data = response.get_json()
    assert data["status"] == "ok"


def test_health_endpoint(client):
    """Verifica que el endpoint /health responde correctamente."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_not_found(client):
    """Verifica que rutas no definidas devuelven 404."""
    response = client.get("/ruta-inexistente")
    assert response.status_code == 404
