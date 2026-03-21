"""
Configuración global de pytest.
Fixtures compartidas para todos los tests.
"""
import pytest


@pytest.fixture
def sample_test_plan_markdown():
    """Markdown de ejemplo con tabla de casos de prueba."""
    return """
# Test Plan - Ejemplo

## Objetivo
Validar el login del usuario.

## Análisis
Se deben probar los flujos de autenticación.

## Tabla de Casos de Prueba

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Login con credenciales válidas | Usuario registrado | Redirección a dashboard | |
| Media | TC2 | Login con contraseña incorrecta | Usuario registrado | Mensaje de error | |
| Baja | TC3 | Login con campos vacíos | Navegador abierto | Validación de campos requeridos | |

## Notas
Cada caso debe ejecutarse manualmente.
"""


@pytest.fixture
def sample_hu_markdown():
    """Markdown de ejemplo de Historia de Usuario."""
    return """
- ID: AER25-101
- Title: Login de usuario en pantalla principal
- Description: El usuario debe poder autenticarse...
- Acceptance Criteria:
  - Ingresar usuario y contraseña
  - Ver mensaje de error si falla
"""
