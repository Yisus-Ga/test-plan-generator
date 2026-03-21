"""
Tests de integración para endpoints de la API (Semana 3).
Usa BD SQLite en memoria y mock de AIService para no llamar a OpenAI.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock


FAKE_TEST_PLAN_MD = """
## Objetivo
Validar el login del usuario.

## Resumen
Se generaron 2 casos de prueba.

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Login con credenciales válidas | Usuario registrado | Redirección a dashboard | |
| Media | TC2 | Login con contraseña incorrecta | Usuario registrado | Mensaje de error | |
"""


class TestProjectsEndpoint:
    """Tests para GET /api/v1/projects/"""

    def test_list_projects_returns_aeroman(self, client):
        """GET /projects/ devuelve al menos el proyecto AEROMAN."""
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        codes = [p["code"] for p in data]
        assert "AEROMAN" in codes

    def test_list_projects_response_structure(self, client):
        """Cada proyecto tiene id, code, name, description."""
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        for p in response.json():
            assert "id" in p
            assert "code" in p
            assert "name" in p
            assert "description" in p


class TestTestPlansEndpoint:
    """Tests para GET /api/v1/test-plans/"""

    def test_list_test_plans_empty_initially(self, client):
        """Al inicio no hay Test Plans; devuelve lista vacía."""
        response = client.get("/api/v1/test-plans/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_test_plans_with_filter(self, client):
        """Filtro project_code=AEROMAN devuelve 200."""
        response = client.get("/api/v1/test-plans/?project_code=AEROMAN")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAnalyzeEndpoint:
    """Tests para POST /api/v1/analyze/ - con mock de AIService"""

    def test_analyze_returns_token_and_download_url(self, client):
        """POST /analyze/ con datos válidos devuelve token y download_url."""
        with patch("app.services.test_plan_service.AIService") as MockAIService:
            mock_ai = MagicMock()
            mock_ai.generate_test_plan_from_story = AsyncMock(
                return_value=FAKE_TEST_PLAN_MD
            )
            MockAIService.return_value = mock_ai

            response = client.post(
                "/api/v1/analyze/",
                data={
                    "hu_id": "AER25-101",
                    "title": "Login de usuario",
                    "description": "Como usuario quiero autenticarme",
                    "acceptance_criteria": "Criterio 1\nCriterio 2",
                    "project_code": "AEROMAN",
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "download_url" in data
        assert "/api/v1/download/" in data["download_url"]

    def test_analyze_missing_fields_returns_400(self, client):
        """POST /analyze/ sin project_code devuelve 400."""
        response = client.post(
            "/api/v1/analyze/",
            data={
                "hu_id": "AER25-101",
                "title": "Login",
                "description": "Desc",
                "acceptance_criteria": "C1",
                # project_code faltante
            },
        )
        assert response.status_code == 422  # Validación de Form
