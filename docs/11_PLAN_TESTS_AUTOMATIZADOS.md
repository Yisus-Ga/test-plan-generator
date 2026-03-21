# Plan de Tests Automatizados

Documento de referencia para la estrategia de testing del proyecto.

---

## Estructura de Carpetas

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidas (BD en memoria, mocks, etc.)
├── unit/                    # Tests unitarios (Semana 1)
│   ├── test_markdown_parser.py
│   ├── test_excel_generator.py
│   └── test_schemas.py
├── integration/             # Tests de integración (Semana 2-3)
│   ├── test_services.py     # Servicios con mocks
│   └── test_endpoints.py    # Endpoints con BD en memoria
└── e2e/                     # Tests end-to-end (futuro)
    └── ...
```

---

## Roadmap por Semana

### Semana 1: Configuración y tests de utilidades ✅

| Tarea | Estado | Descripción |
|-------|--------|-------------|
| pytest + pytest-asyncio | ✅ | En `requirements.txt` |
| pytest.ini | ✅ | Configuración (pythonpath, asyncio) |
| Estructura tests/ | ✅ | tests/unit/, conftest.py |
| test_markdown_parser | ✅ | 14 tests para parse_markdown_table_to_dict, clean_markdown_for_display, extract_hu_id/title |
| test_excel_generator | ✅ | clean_filename, generate_excel_from_test_plan |
| test_schemas | ✅ | UserStoryCreate validación (Pydantic) |

**Corrección aplicada**: El parser de markdown ignoraba la línea separadora (`|---|`) y la trataba como fila de datos. Se agregó filtro para omitir líneas donde todas las celdas son solo guiones.

**Corrección aplicada**: Schemas Pydantic v2 usan `min_length` en lugar de `min_items` para listas.

---

### Semana 2: Tests de servicios con mocks ✅

| Tarea | Estado | Descripción |
|-------|--------|-------------|
| Estructura `tests/integration/` | ✅ | Carpeta y `test_services.py` |
| Tests de `UserStoryService` | ✅ | 3 tests sin mocks (lógica pura) |
| Tests de `TestPlanService` | ✅ | 3 tests con mock de AIService y repos |
| Mock AIService | ✅ | `patch()` devuelve markdown falso |
| Mock repositorios | ✅ | `AsyncMock` para project_repo, user_story_repo, test_plan_repo |

**Técnica usada**: `unittest.mock.patch` para reemplazar AIService; `AsyncMock` para métodos async de repositorios.

---

### Semana 3: Tests de endpoints con BD en memoria ✅

| Tarea | Estado | Descripción |
|-------|--------|-------------|
| `tests/integration/conftest.py` | ✅ | Fixture `client` con BD SQLite en memoria compartida |
| `tests/integration/test_endpoints.py` | ✅ | 6 tests para endpoints de la API |
| GET `/api/v1/projects/` | ✅ | Devuelve AEROMAN precargado, valida estructura |
| GET `/api/v1/test-plans/` | ✅ | Lista vacía inicial, filtros |
| POST `/api/v1/analyze/` | ✅ | Con mock de AIService, devuelve token y download_url |

**Detalles técnicos**: Se usa `DATABASE_URL=sqlite:///file:testdb?mode=memory&cache=shared` para que todas las conexiones compartan la misma BD en memoria. El `client` fixture hace drop/create de tablas y crea proyecto AEROMAN antes de cada test. Para `/analyze/` se mockea `AIService` con `patch()`.

---

## Cómo ejecutar los tests

### Requisitos

Activar el entorno virtual donde están las dependencias del proyecto (`pip install -r requirements.txt`).

### Comandos

```bash
# Todos los tests
python -m pytest tests/

# Solo tests unitarios
python -m pytest tests/unit/

# Un archivo específico
python -m pytest tests/unit/test_markdown_parser.py -v

# Solo tests de integración (Semanas 2 y 3)
python -m pytest tests/integration/ -v

# Solo tests de endpoints (BD en memoria)
python -m pytest tests/integration/test_endpoints.py -v

# Con cobertura (opcional, requiere pytest-cov)
python -m pytest tests/ --cov=app
```

### Nota sobre entornos

Si `pytest` no está en el PATH, usar siempre `python -m pytest`. Si aparecen errores de `ModuleNotFoundError` (pandas, pydantic), asegurarse de estar en el entorno virtual correcto.

---

## Referencias

- [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) - Plan general
- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
