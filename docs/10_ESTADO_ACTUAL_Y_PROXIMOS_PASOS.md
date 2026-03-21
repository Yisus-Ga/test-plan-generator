# Estado Actual del Proyecto y Próximos Pasos

**Documento de referencia** — Describe cómo está constituido el proyecto en la actualidad y el plan de trabajo acordado.

---

## 📦 Estado Actual del Proyecto

### Arquitectura Implementada

| Aspecto | Estado |
|---------|--------|
| **Backend** | FastAPI + Clean Architecture (capas separadas) |
| **Base de datos** | SQLite + SQLAlchemy ORM + Alembic |
| **Frontend** | HTML/CSS/JS vanilla modular (ES6 modules) |
| **Autenticación** | Modo single-user (sin login) |
| **IA** | OpenAI (gpt-4.1-mini para traducción, gpt-4.1 para generación) |

### Estructura del Código Actual

```
app/
├── api/v1/endpoints/     # user_stories, test_plans, projects, chat
├── core/                 # config, logging, exceptions
├── db/                   # models ORM, session, base
├── domain/               # entities, value_objects
├── repositories/         # interfaces + sqlalchemy implementations
├── schemas/              # Pydantic (user_story, project, test_plan, chat)
├── services/             # ai_service, test_plan_service, project_service, chat_service, export_service
├── utils/                # markdown_parser, excel_generator, csv_generator, json_generator, jira_generator
static/
├── assets/js/            # pages (generator, history, projects), api, components (chatModal), utils
├── assets/css/           # themes, components, navigation, analysis
├── index.html            # SPA con router
```

### Modelos de Datos Implementados

- **Project** (code, name, description)
- **UserStory** (project_id, story_id, title, description, acceptance_criteria)
- **TestPlan** (user_story_id, objective, summary, analysis_markdown, test_plan_markdown)
- **TestCase** (test_plan_id, priority, tc_id, title, precondition, expected_validation)

### Funcionalidades en Producción

| Funcionalidad | Estado |
|---------------|--------|
| Generar Test Plan desde HU | ✅ |
| Proyectos (crear, listar, seleccionar) | ✅ |
| Historial de Test Plans (listar, filtrar, eliminar) | ✅ |
| Chat con contexto (proyecto + HU + test plan) | ✅ |
| Exportación: Excel, CSV, JSON, Jira | ✅ |
| Validaciones en tiempo real | ✅ |
| Configuración vía .env | ✅ |

### Lo que NO está implementado aún

- Tests automatizados (Semana 1 en curso: pytest configurado, tests de utilidades)
- Plantillas de prompts (personalización sin tocar código)
- Imágenes en Historias de Usuario
- MCP Server
- Autenticación multi-usuario
- Persistencia del historial de chat

---

## 🗺️ Plan de Próximos Pasos (Acordado)

### Paso 1: Publicar en GitHub (sin exponer API Key) ✅ Preparado

- [x] `.gitignore` con `.env`
- [x] `.env.example` con placeholders
- [x] Guía en [09_GUIA_PUBLICAR_EN_GITHUB.md](./09_GUIA_PUBLICAR_EN_GITHUB.md)
- [ ] Ejecutar: `git init`, `git add .`, `git commit`, `git push`

---

### Paso 2: Tests Automatizados

| Semana | Enfoque | Estado |
|--------|---------|--------|
| **Semana 1** | Configurar pytest, estructura `tests/`, tests de utilidades (parsers, validaciones) | ✅ En curso |
| **Semana 2** | Tests de servicios (TestPlanService, etc.) con mocks (sin DB real) | Pendiente |
| **Semana 3** | Tests de endpoints con BD en memoria | Pendiente |

Objetivo: cobertura progresiva (unitario → integración → E2E).

**Implementado (Semana 1)**:
- [x] pytest + pytest-asyncio en `requirements.txt`
- [x] Estructura `tests/unit/`, `tests/conftest.py`, `pytest.ini`
- [x] Tests de `markdown_parser` (14 tests pasando)
- [x] Tests de `excel_generator` (clean_filename)
- [x] Tests de schemas (UserStoryCreate validaciones)
- [x] Documentación en [11_PLAN_TESTS_AUTOMATIZADOS.md](./11_PLAN_TESTS_AUTOMATIZADOS.md)

---

### Paso 3: Plantillas de Prompts

Objetivo: que personas sin tocar código puedan ajustar cómo se generan los Test Plans (prioridades, formato, tipo de casos).

Enfoque inicial: archivos de plantillas (rápido). Ejemplo: `prompts/template_test_plan.txt`.

---

### Paso 4: Imágenes en la Historia de Usuario (Nueva idea)

Objetivo: enviar capturas de pantalla u otras imágenes al cargar la HU para que la IA proponga casos considerando la interfaz real.

- Soporte: URL de imagen o subida local desde PC
- Diseñar: modelo, formato y flujo de incorporación

---

### Paso 5: MCP Server

Planificar el MCP Server como evolución posterior.

Referencia: [08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md](./08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md)

---

## 📚 Referencia a Otros Documentos

| Documento | Uso |
|-----------|-----|
| [00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md) | Configuración local (SQLite, CORS, etc.) |
| [01_DIAGNOSTICO_SISTEMA_ACTUAL.md](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) | Análisis del MVP inicial (contexto histórico) |
| [02_PROPUESTA_MODELOS_DATOS.md](./02_PROPUESTA_MODELOS_DATOS.md) | Modelos propuestos (muchos ya implementados) |
| [03_ARQUITECTURA_BACKEND.md](./03_ARQUITECTURA_BACKEND.md) | Clean Architecture y estructura |
| [07_ESCALADO_PROYECTO.md](./07_ESCALADO_PROYECTO.md) | Fases completadas y futuras |
| [08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md](./08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md) | Opciones para MCP |
| [09_GUIA_PUBLICAR_EN_GITHUB.md](./09_GUIA_PUBLICAR_EN_GITHUB.md) | Guía para publicar sin exponer claves |
| [11_PLAN_TESTS_AUTOMATIZADOS.md](./11_PLAN_TESTS_AUTOMATIZADOS.md) | Plan y configuración de tests |

---

**Última actualización**: Marzo 2026  
**Versión del proyecto**: 2.0.0
