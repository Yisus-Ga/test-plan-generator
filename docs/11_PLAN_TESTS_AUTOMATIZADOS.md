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

### Semana 2: Tests de servicios con mocks

- Mock del `AIService` para no llamar a OpenAI
- Tests de `TestPlanService` (sin DB real)
- Tests de `ProjectService`, `ChatService` con mocks

---

### Semana 3: Tests de endpoints con BD en memoria

- Fixture de base de datos SQLite en memoria
- Tests de `POST /api/v1/test-plans/generate`
- Tests de `GET /api/v1/test-plans`
- Tests de `GET /api/v1/projects`

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
