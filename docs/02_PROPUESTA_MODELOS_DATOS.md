# 02 · Modelo de Datos (actual y extensión para Perfiles)

> **Objetivo del documento:** documentar el modelo de datos **implementado hoy** y la **extensión mínima** necesaria para soportar perfiles de dominio.

Arquitectura backend: [03](./03_ARQUITECTURA_BACKEND.md) · Roadmap: [06](./06_ROADMAP_IMPLEMENTACION.md).

---

## 1. Modelo actual (implementado)

Definido en `app/db/models.py` (SQLAlchemy ORM). Cuatro entidades principales:

```
Project 1───N UserStory 1───N TestPlan 1───N TestCase
```

### `projects`
| Campo | Tipo | Notas |
|---|---|---|
| `id` | int PK | |
| `code` | str único | Ej: `AEROMAN`, `AER25` |
| `name` | str | |
| `description` | text | |
| `is_active` | bool | Estado activo/inactivo (default `true`) |
| `created_at` / `updated_at` | datetime | |

### `user_stories`
| Campo | Tipo | Notas |
|---|---|---|
| `id` | int PK | |
| `project_id` | FK → projects | |
| `story_id` | str único | ID de negocio de la HU |
| `title` | str | |
| `description` | text | |
| `acceptance_criteria` | JSON | Lista de criterios |
| `story_type` | str | BACKEND / FRONTEND / UI_UX (ver `value_objects/story_type.py`) |
| `version` | int | |

### `test_plans`
Metadatos (`objective`, `summary`, `notes`), conteos por prioridad (`total_cases`, `high/medium/low_priority_count`), y los markdown generados (`analysis_markdown`, `test_plan_markdown`). Incluye `download_token` (temporal para descargas).

### `test_cases`
`tc_id` (ej. `AER25-101: TC1`), `priority` (HIGH/MEDIUM/LOW), `title`, `precondition`, `expected_validation`, `obtained_result`.

> Las entidades de dominio (`app/domain/entities/`) son la representación de negocio; los `*ORM` son la representación de persistencia. Los repositorios traducen entre ambas — ver [03](./03_ARQUITECTURA_BACKEND.md).

## 2. Extensión propuesta para Perfiles

La meta es que **cada proyecto tenga un perfil de dominio** y que ese perfil viaje con la HU y el test plan generados. La extensión es deliberadamente **mínima y aditiva** (no rompe lo existente).

### 2.1 Perfil a nivel de Proyecto

Agregar a `projects`:

| Campo | Tipo | Notas |
|---|---|---|
| `profile` | str (enum) | `web_generic` \| `genexus` \| `bantotal`. Default `web_generic` para retrocompatibilidad. |

Las HU heredan el perfil de su proyecto. Alternativamente, `user_stories` puede llevar un `profile` opcional que sobreescriba el del proyecto (decisión a confirmar con el equipo).

### 2.2 Trazabilidad del contexto usado (grounding)

Cuando un test plan se genera con grounding (KB de GeneXus o MCP de Bantotal), conviene registrar **qué fuente y versión** se usó, para auditoría y reproducibilidad. Propuesta en `test_plans`:

| Campo | Tipo | Notas |
|---|---|---|
| `profile` | str | Perfil con el que se generó (copia inmutable). |
| `grounding_source` | str/JSON | Origen del contexto (ej. `genexus_kb:vX`, `bantotal_mcp:txn=...`). Solo referencias/estructura, **sin datos sensibles**. |
| `ai_provider` / `ai_model` | str | Proveedor y modelo usados (OpenAI/Anthropic). |

### 2.3 Enriquecimiento del caso de prueba (opcional, recomendado)

Para mejorar la trazabilidad ISO/ISTQB, `test_cases` puede sumar columnas opcionales (nulas por defecto para no romper nada):

| Campo | Notas |
|---|---|
| `scenario_type` | Uno de los 7 escenarios. |
| `design_technique` | Técnica ISO 29119-4 (partición de equivalencia, valores límite, etc.). |
| `iso_characteristic` | Característica ISO 25010 afectada (para casos no funcionales). |

## 3. Migraciones

El proyecto usa **Alembic**. Cada cambio de esquema se versiona con una migración nueva:

```powershell
# Generar migración autodetectada tras cambiar los modelos ORM
alembic revision --autogenerate -m "add profile to projects"

# Aplicar
alembic upgrade head
```

Migraciones existentes en `alembic/versions/`:
- `initial_migration` — creación de user_stories/test_plans/test_cases.
- `add_projects_table_and_project_id` — incorporación de proyectos.

> Recomendación: los campos nuevos de perfil deben entrar como **nullable** o con `server_default`, para que las migraciones sean seguras sobre datos existentes.
