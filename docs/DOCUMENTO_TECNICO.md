# Documento Técnico: Test Plan Generator v2.0

**Versión del documento**: 1.0  
**Fecha**: Abril 2026  
**Audiencia**: Equipos técnicos de IT — desarrolladores, arquitectos, tech leads, QA engineers  
**Fuente**: Análisis del código fuente, documentación arquitectónica y archivos de configuración del repositorio

---

## Tabla de Contenidos

1. [Descripción General del Proyecto](#1-descripción-general-del-proyecto)
2. [Arquitectura y Tecnología](#2-arquitectura-y-tecnología)
3. [Modelos de IA y Agentes](#3-modelos-de-ia-y-agentes)
4. [Flujo de Datos End-to-End](#4-flujo-de-datos-end-to-end)
5. [Potencialidades Actuales](#5-potencialidades-actuales)
6. [Limitaciones Conocidas](#6-limitaciones-conocidas)
7. [Roadmap y Mejoras Futuras Posibles](#7-roadmap-y-mejoras-futuras-posibles)
8. [Decisiones de Diseño Relevantes](#8-decisiones-de-diseño-relevantes)

---

## 1. Descripción General del Proyecto

### ¿Qué problema resuelve?

La generación manual de planes de testing a partir de historias de usuario (HU) es una tarea repetitiva, que consume tiempo considerable y cuya calidad depende fuertemente de la experiencia y disponibilidad del analista QA. Un analista de testing puede tardar entre 1 y 3 horas en elaborar un plan de pruebas completo para una historia de usuario de complejidad media, incluyendo casos positivos, negativos, de borde, de seguridad y no funcionales.

**Test Plan Generator** automatiza este proceso mediante inteligencia artificial. A partir de los datos de una Historia de Usuario (ID, título, descripción y criterios de aceptación), el sistema genera automáticamente un plan de testing estructurado, priorizado y exportable en múltiples formatos.

### Flujo Principal

```
[Formulario Web / Jira (manual)]
         ↓
   Historia de Usuario
 (ID + Título + Descripción + Criterios de Aceptación)
         ↓
  [Pipeline de IA - 3 pasos]
  1. Traducción al inglés
  2. Generación del Test Plan (en inglés)
  3. Traducción al español
         ↓
  Markdown estructurado con tabla de casos de prueba
         ↓
  Persistencia en base de datos (SQLite)
         ↓
  [Exportación multi-formato]
  Excel (.xlsx) | CSV | JSON | CSV Jira/Xray
```

> **Nota sobre la integración con Jira**: en la versión actual (v2.0), los datos de la HU se ingresan manualmente a través del formulario web. La integración automática con Jira (lectura bidireccional vía API) está contemplada en el roadmap como evolución futura.

### Valor que aporta al equipo de QA

- **Reducción de tiempo estimada**: de 1-3 horas por HU a 30-60 segundos de procesamiento de IA + revisión humana de 10-15 minutos.
- **Cobertura sistemática**: el sistema genera siempre casos de prueba para todos los tipos (positivos, negativos, borde, no funcionales, compatibilidad, seguridad, regresión), eliminando omisiones involuntarias.
- **Estandarización**: todos los planes de testing siguen el mismo formato, nomenclatura y estructura de columnas, lo que facilita la comunicación entre equipos.
- **Historial persistente**: todos los planes generados quedan almacenados en la base de datos, con su HU asociada, el proyecto al que pertenecen y la fecha de creación.
- **Chat contextual con IA**: el analista puede consultar al asistente de IA sobre el plan generado, pidiendo explicaciones, ajustes o consultas de cobertura sin salir de la interfaz.
- **Exportación flexible**: los planes se pueden exportar en Excel (para uso offline), CSV (para procesamiento), JSON (para integraciones) o formato Jira/Xray (para importación directa).

---

## 2. Arquitectura y Tecnología

### Stack Tecnológico

| Capa | Tecnología | Versión mínima | Propósito |
|------|-----------|---------------|-----------|
| Backend | Python + FastAPI | FastAPI ≥ 0.104.1 | API REST asíncrona |
| Servidor ASGI | Uvicorn | ≥ 0.24.0 | Servidor de aplicación |
| ORM | SQLAlchemy | ≥ 2.0.23 | Mapeo objeto-relacional |
| Migraciones | Alembic | ≥ 1.13.0 | Gestión de esquema de BD |
| Base de datos | SQLite | (nativa Python) | Persistencia local |
| Validación | Pydantic + pydantic-settings | ≥ 2.5.0 | Schemas y configuración |
| IA | OpenAI Python SDK | ≥ 1.3.0 | Llamadas a modelos LLM |
| Exportación | pandas + openpyxl | pandas ≥ 2.1.0 | Generación de Excel/CSV |
| Frontend | HTML + CSS + Vanilla JS | — | SPA sin framework |
| Renderer Markdown | marked.js | (CDN) | Render del plan en UI |
| Testing | pytest + pytest-asyncio + httpx | pytest ≥ 7.4.0 | Tests unitarios e integración |

### Estructura de Carpetas y Módulos

```
v5/
├── app/                          # Núcleo de la aplicación
│   ├── main.py                   # Punto de entrada FastAPI (lifespan, CORS, rutas estáticas)
│   ├── config.py                 # Configuración centralizada (pydantic-settings)
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # Registro de sub-routers
│   │       ├── dependencies.py   # Inyección de dependencias (servicios, repos)
│   │       └── endpoints/
│   │           ├── test_plans.py # Endpoints: analyze, list, get, delete, download
│   │           ├── projects.py   # CRUD de proyectos
│   │           └── chat.py       # Endpoint de chat contextual
│   ├── core/
│   │   ├── exceptions.py         # Excepciones de dominio (AIServiceError, ValidationError)
│   │   └── logging.py            # Configuración de logging centralizado
│   ├── db/
│   │   ├── base.py               # Base declarativa SQLAlchemy
│   │   ├── models.py             # Modelos ORM (ProjectORM, UserStoryORM, TestPlanORM, TestCaseORM)
│   │   └── session.py            # Sesión de base de datos y factory
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── project.py        # Entidad de dominio Project
│   │   │   ├── test_plan.py      # Entidades TestPlan y TestCase
│   │   │   └── user_story.py     # Entidad UserStory (con método to_markdown())
│   │   └── value_objects/
│   │       └── story_type.py     # Enum StoryType: BACKEND, FRONTEND, UI_UX
│   ├── repositories/
│   │   ├── interfaces/           # Contratos abstractos (patrón Repository)
│   │   └── sqlalchemy/           # Implementaciones concretas con SQLAlchemy
│   ├── schemas/                  # Schemas Pydantic para request/response
│   │   ├── test_plan.py          # TestPlanListItem, TestPlanResponse, TestCaseResponse
│   │   ├── project.py            # ProjectCreate, ProjectUpdate, ProjectResponse
│   │   ├── user_story.py         # UserStoryCreate, UserStoryResponse
│   │   └── chat.py               # ChatRequest, ChatResponse, ChatMessage
│   ├── services/
│   │   ├── ai_service.py         # Pipeline IA: traducción + generación + traducción
│   │   ├── chat_service.py       # Chat contextual con OpenAI Chat Completions
│   │   ├── export_service.py     # Orquestador de exportación (xlsx/csv/jira/json)
│   │   ├── test_plan_service.py  # Orquestador principal: HU → IA → parse → DB
│   │   ├── project_service.py    # Lógica de negocio para proyectos
│   │   └── user_story_service.py # Creación de entidades UserStory desde formulario
│   └── utils/
│       ├── markdown_parser.py    # Parser de tabla Markdown → lista de dicts
│       ├── excel_generator.py    # Generación de .xlsx en memoria (BytesIO)
│       ├── csv_generator.py      # Generación de .csv en memoria
│       ├── jira_generator.py     # Generación de CSV compatible con Jira/Xray
│       └── json_generator.py     # Serialización JSON del plan de testing
├── static/                       # Frontend SPA
│   ├── index.html                # Shell HTML con navegación hash (#/, #/history, #/projects)
│   ├── style.css                 # Estilos globales
│   └── assets/
│       ├── css/                  # Módulos CSS (analysis, components, navigation, themes)
│       └── js/
│           ├── config.js         # API_URL dinámica (window.location.origin)
│           ├── main.js           # Entrada y bootstrapping
│           ├── router.js         # Enrutador SPA por hash
│           ├── api/              # Clientes HTTP por entidad (chat, projects, test_plans)
│           ├── components/       # Componentes reutilizables (Button, FormInput, chatModal)
│           ├── pages/            # Vistas: generator, history, projects
│           └── utils/            # DOM helpers, validación
├── docs/                         # Documentación arquitectónica (12 documentos)
├── tests/
│   ├── unit/                     # Tests de utilidades y schemas
│   └── integration/              # Tests de servicios y endpoints (BD en memoria)
├── alembic/                      # Migraciones de base de datos
├── scripts/                      # Utilitarios de administración de BD
├── .env.example                  # Plantilla de variables de entorno
├── requirements.txt              # Dependencias del proyecto
├── pytest.ini                    # Configuración de pytest
└── alembic.ini                   # Configuración de Alembic
```

### Modelo de Datos

El esquema de base de datos está compuesto por cuatro tablas relacionadas:

```
projects
  ├── id (PK)
  ├── code (único, indexado) — ej: "AEROMAN", "AER25"
  ├── name
  ├── description
  └── timestamps (created_at, updated_at)

user_stories
  ├── id (PK)
  ├── project_id (FK → projects.id)
  ├── story_id (único, indexado) — ej: "AER25-101"
  ├── title
  ├── description
  ├── acceptance_criteria (JSON — lista de strings)
  ├── story_type — BACKEND | FRONTEND | UI_UX
  ├── version (incrementa al regenerar)
  └── timestamps

test_plans
  ├── id (PK)
  ├── user_story_id (FK → user_stories.id)
  ├── objective, summary, notes
  ├── total_cases, high_priority_count, medium_priority_count, low_priority_count
  ├── analysis_markdown (texto sin tabla)
  ├── test_plan_markdown (texto completo con tabla)
  ├── download_token (UUID hex, único)
  └── timestamps

test_cases
  ├── id (PK)
  ├── test_plan_id (FK → test_plans.id)
  ├── tc_id — ej: "AER25-101: TC1"
  ├── priority — HIGH | MEDIUM | LOW
  ├── title
  ├── precondition
  ├── expected_validation
  ├── obtained_result
  └── created_at
```

### APIs Externas Consumidas

| API | Propósito | Modelo utilizado |
|-----|-----------|-----------------|
| OpenAI Responses API (`client.responses.create`) | Traducción HU al inglés y Test Plan al español | `gpt-4.1-mini` |
| OpenAI Responses API (`client.responses.create`) | Generación del Test Plan en inglés | `gpt-4.1` |
| OpenAI Chat Completions API (`client.chat.completions.create`) | Chat contextual con el Test Plan | `gpt-4.1-mini` |

No se consume la API de Jira en la versión actual. La integración con Jira está planificada como mejora futura.

### Endpoints de la API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Sirve el frontend (index.html) |
| `GET` | `/health` | Estado de la aplicación y versión |
| `POST` | `/api/v1/analyze/` | Recibe formulario HU, ejecuta pipeline IA, guarda en DB |
| `GET` | `/api/v1/test-plans/` | Lista Test Plans con filtros (project, story_id, search, fechas) |
| `GET` | `/api/v1/test-plans/{id}` | Detalle completo de un Test Plan |
| `DELETE` | `/api/v1/test-plans/{id}` | Elimina un Test Plan |
| `GET` | `/api/v1/download/{token}?format=` | Descarga en xlsx, csv, jira o json |
| `GET/POST/PUT/DELETE` | `/api/v1/projects/` | CRUD completo de proyectos |
| `POST` | `/api/v1/chat` | Chat con contexto (project + HU + Test Plan) |

---

## 3. Modelos de IA y Agentes

### Modelos de Lenguaje Utilizados

El sistema usa dos modelos de OpenAI, seleccionados deliberadamente para cada tarea:

| Modelo | Tarea | Justificación |
|--------|-------|---------------|
| `gpt-4.1` | Generación del Test Plan en inglés | Modelo de máxima capacidad para razonamiento complejo, análisis de criterios de aceptación y generación exhaustiva de casos de prueba de diferentes tipos |
| `gpt-4.1-mini` | Traducción EN→ES y ES→EN, Chat contextual | Modelo rápido y económico para tareas de transformación de texto y conversación, donde no se requiere razonamiento de alto nivel |

Los modelos son configurables vía variables de entorno (`OPENAI_MODEL_GENERATION` y `OPENAI_MODEL_TRANSLATION`), lo que permite actualizarlos sin cambiar código.

### Cadena de Agentes (Pipeline de 3 Pasos)

El núcleo del sistema es una cadena secuencial de 3 llamadas a la API de OpenAI, implementada en `AIService.generate_test_plan_from_story()`:

```
[UserStory entity]
      ↓
  PASO 1: translate_to_english()
      ↓
  [HU en inglés (Markdown)]
      ↓
  PASO 2: generate_test_plan()
      ↓
  [Test Plan en inglés (Markdown con tabla)]
      ↓
  PASO 3: translate_to_spanish()
      ↓
  [Test Plan en español (Markdown con tabla)]
```

#### Paso 1: Traducción al inglés (`gpt-4.1-mini`)

**Recibe**: Markdown de la HU en español (generado por `UserStory.to_markdown()`), con campos ID, Título, Descripción, Criterios de Aceptación.

**Prompt del sistema** (inferido del código):
```
You are a professional translator specialized in software development documentation. 
Translate the following User Story into English, keeping the same structure 
with the labels in English (ID, Title, Description, Acceptance Criteria).

{hu_es}
```

**Devuelve**: El mismo Markdown de la HU, traducido al inglés, manteniendo la estructura de labels.

**Justificación del paso**: Los modelos de OpenAI razonan con mayor profundidad y generan mejores casos de testing cuando se procesan instrucciones en inglés. Esta etapa maximiza la calidad de la generación subsiguiente.

---

#### Paso 2: Generación del Test Plan (`gpt-4.1`)

**Recibe**: Markdown de la HU en inglés.

**Prompt del sistema** (íntegro, extraído de `ai_service.py`):

```
User Story: {hu_en}   

## ROLE OF THE AI

### General Introduction  

Role: Act as a **Senior QA Analyst / Test Designer** and generate test cases based on the 
User Stories (US) provided, following the criteria specified in the sections below.  

Always write in a **formal and technical** tone.  

---

## CONTEXT  

We have **refined Acceptance Criteria (AC)** for a **User Story (US)**.  

The goal is to create the **Test Plan (TP)**, prioritizing the test cases according to:  

- **High**: Business-critical functionality, security, regulatory compliance, or high risk.  
- **Medium**: Important functionality, but not blocking.  
- **Low**: Edge cases, exploratory, UX/UI, accessibility, regression, or low impact.  

---

## User Story Analysis  

Analyze and classify the US based on **Title, Description, and Acceptance Criteria**:  

- **Backend**: If it contains words like "Backend", "Endpoint", "API", "Database", 
  "Business logic", "Microservice".  
- **Frontend**: If it contains words like "Frontend", "View", "Component", "Style", "Structure".  
- **UI/UX**: If it contains words like "Design", "UI/UX", "Interface", "Figma".  

---

## Test Plan (TP) Creation  

### Test Cases  

Generate cases **mapped to each Acceptance Criterion (AC)** to ensure coverage:  

- **Positive**: Validate the main functionality.  
- **Negative**: Error handling or invalid inputs.  
- **Boundary / Exploratory**: Limits and unforeseen situations.  
- **Non-Functional**: Performance, Usability, Accessibility ([NF]).  
- **Compatibility**: Different browsers, resolutions, OS.  
- **Security**: Authentication, roles, injection.  
- **Regression**: Identify previous functionalities that could be affected.  

## Format and Naming  

- **Test Case Format:**  
  `USID: TC#: FEATURE CONDITION`  

  Example:  
  `AER25-101: TC1: Validate Endpoint Job Type creation with valid data`  

- **List the test plan in tabular format with the following columns (use Markdown with | separators):**  

  Priority | TC ID | Title | Precondition | Expected Validation | Obtained Result  

### Input Data  

Include data variants:  
- Valid / Invalid / Null / Boundary (extreme values) / Special (UTF-8, symbols)  

### Environments and Compatibility  

Specify browsers, devices, resolutions, or relevant operating systems.  

### Estimation  

Summarize the **number of suggested cases** by priority (High, Medium, Low).  

## Jira Report  

Must include:  
- **Objective of the TP**  
- **Summary of the TP and number of test cases (by priority)**  
- **Relevant notes** (non-functional, regression, security)  
```

**Devuelve**: Markdown extenso con:
- Análisis del tipo de HU (Backend/Frontend/UI-UX)
- Tabla de casos de prueba (columnas: Prioridad, TC ID, Título, Precondición, Validación Esperada, Resultado Obtenido)
- Sección de datos de entrada con variantes
- Ambientes y compatibilidad
- Estimación por prioridad
- Reporte Jira (objetivo, resumen, notas relevantes)

---

#### Paso 3: Traducción al español (`gpt-4.1-mini`)

**Recibe**: Test Plan completo en inglés (Markdown).

**Prompt del sistema** (íntegro, extraído de `ai_service.py`):

```
You are a professional technical translator and Quality Assurance (QA) document writer.
Translate the following Test Plan from English to Spanish, keeping the order of the sections.
Specific instructions: The response must always begin with the title ("ID + tittle") of the 
analyzed user story (HU) and continue with the content of the first section. Additionally, 
the table containing the test cases must always be returned in clean Markdown format.
Test Plan (English):
{test_plan_en}
```

**Devuelve**: Test Plan completo en español, con la tabla Markdown preservada y el título de la HU como primera línea (requerimiento explícito del prompt para garantizar el parsing posterior correcto).

---

#### Agente de Chat Contextual (independiente del pipeline principal)

**Implementado en**: `ChatService` — usa `client.chat.completions.create` (API diferente a los pasos anteriores).

**Modelo**: `gpt-4.1-mini` (hardcoded).

**Prompt del sistema** (íntegro, extraído de `chat_service.py`):

```
Eres un asistente de QA. Tienes el siguiente contexto sobre un proyecto, una Historia de 
Usuario (HU) y el Test Plan generado. Responde únicamente a consultas relacionadas con 
este proyecto, la HU o el Test Plan (casos de prueba, prioridades, cobertura, criterios 
de aceptación, etc.).

Si el usuario hace una pregunta o comentario que NO esté relacionado con el proyecto, 
la HU o el Test Plan, responde exactamente: "Por favor, haz una consulta relacionada 
al test plan."

## Contexto

{context}
```

El campo `{context}` se construye dinámicamente en el endpoint de chat, inyectando los datos del proyecto, la HU completa y el Test Plan completo. Esto evita que el asistente responda consultas fuera del alcance del sistema.

---

## 4. Flujo de Datos End-to-End

A continuación se describe, paso a paso, qué ocurre desde que se ingresa una Historia de Usuario hasta que el usuario descarga el archivo Excel.

### Etapa 1: Entrada de datos

El usuario completa el formulario en la UI web (`static/assets/js/pages/generator.js`):
- **ID de HU** (ej: `AER25-101`)
- **Título** (ej: `Validar creación de tipo de trabajo`)
- **Descripción** (texto libre en español)
- **Criterios de Aceptación** (texto libre, puede ser lista numerada o con bullets)
- **Proyecto** (seleccionado de la lista de proyectos disponibles — dropdown poblado desde `/api/v1/projects/`)

El formulario envía un `POST` a `/api/v1/analyze/` como `multipart/form-data`.

### Etapa 2: Recepción y validación (endpoint)

`endpoints/test_plans.py → analyze()`:
1. Verifica que todos los campos estén presentes (validación HTTP 400 si faltan).
2. Delega en `TestPlanService.generate_test_plan()`.

### Etapa 3: Orquestación del servicio principal

`services/test_plan_service.py → generate_test_plan()`:

1. **Valida el proyecto**: busca en la BD por `project_code`. Si no existe → `ValidationError`.
2. **Construye la entidad `UserStory`**: mediante `UserStoryService.create_user_story_from_form()`, que parsea los criterios de aceptación (los divide por saltos de línea o numeración) y clasifica el tipo de historia (`StoryType.BACKEND`, `FRONTEND`, o `UI_UX`) basándose en palabras clave del título y descripción.
3. **Maneja versioning**: si ya existe una HU con ese `story_id` en la BD, incrementa el campo `version` y actualiza en lugar de crear un duplicado.
4. **Ejecuta el pipeline de IA** (ver Sección 3): `ai_service.generate_test_plan_from_story(user_story)`.

### Etapa 4: Pipeline de IA

Tres llamadas secuenciales a la API de OpenAI:

```
UserStory.to_markdown()
    → "## ID: AER25-101\n## Título: ...\n## Descripción: ...\n## Criterios de Aceptación:\n- ..."
    
    → [Llamada 1: gpt-4.1-mini] translate_to_english()
    → "## ID: AER25-101\n## Title: ...\n## Description: ...\n## Acceptance Criteria:\n- ..."
    
    → [Llamada 2: gpt-4.1] generate_test_plan()
    → Markdown extenso con tabla:
      "| Priority | TC ID | Title | Precondition | Expected Validation | Obtained Result |
       |----------|-------|-------|--------------|--------------------|-----------------| 
       | High | AER25-101: TC1 | Validate creation with valid data | ... | ... | |
       ..."
    
    → [Llamada 3: gpt-4.1-mini] translate_to_spanish()
    → Markdown en español con tabla:
      "| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
       |-----------|-------|--------|--------------|--------------------|--------------------|
       | Alta | AER25-101: TC1 | Validar creación con datos válidos | ... | ... | |
       ..."
```

### Etapa 5: Parsing del Markdown

`utils/markdown_parser.py → parse_markdown_table_to_dict()`:
- Busca la primera línea que matchee `| *Prioridad *|` (case-insensitive) en el Markdown resultante.
- Extrae todas las filas de la tabla (6 columnas exactamente).
- Ignora líneas separadoras (líneas con solo guiones).
- Devuelve una lista de diccionarios con claves: `priority`, `tc_id`, `title`, `precondition`, `expected_validation`, `obtained_result`.

Adicionalmente, `clean_markdown_for_display()` elimina la tabla del Markdown para el campo `analysis_markdown` mostrado en la UI (el análisis narrativo sin la tabla de casos).

### Etapa 6: Conteo y metadatos

El servicio cuenta los casos por prioridad buscando las variantes en español e inglés: `HIGH`/`ALTA`, `MEDIUM`/`MEDIA`, `LOW`/`BAJA`.

Extrae el objetivo del Test Plan buscando líneas que contengan las palabras "objetivo" u "objective" en el Markdown.

### Etapa 7: Persistencia en base de datos

Se crean y guardan en SQLite:
- `TestPlanORM` con todos los metadatos y el Markdown completo
- `TestCaseORM` (uno por cada caso de prueba parseado)
- Se genera un `download_token` (UUID hex) único para la descarga

### Etapa 8: Respuesta al frontend

El endpoint devuelve un JSON con:
```json
{
  "token": "<uuid_hex>",
  "test_plan_id": 42,
  "analysis": "<markdown_sin_tabla>",
  "download_url": "/api/v1/download/<uuid_hex>",
  "filename": "AER25-101_Validar_creacion_tipo_trabajo.xlsx"
}
```

El frontend renderiza el `analysis` con `marked.js` y muestra el botón de descarga.

### Etapa 9: Descarga del archivo

`GET /api/v1/download/{token}?format=xlsx`:
1. Recupera el `TestPlan` por token desde la BD.
2. Recupera la `UserStory` asociada y la convierte a Markdown (`to_markdown()`).
3. Llama a `ExportService.export(hu_md, test_plan_markdown, format)`.
4. El generador correspondiente (Excel, CSV, Jira, JSON) parsea nuevamente el Markdown, construye el DataFrame y lo serializa en memoria (`io.BytesIO`).
5. Devuelve un `StreamingResponse` con los headers correctos (`Content-Disposition: attachment`).

### Formato del archivo Excel

El archivo `.xlsx` generado tiene una sola hoja llamada `TestPlan` con las siguientes columnas:

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|--------------------|--------------------|
| Alta | AER25-101: TC1 | ... | ... | ... | (vacío para completar) |

---

## 5. Potencialidades Actuales

### ¿Qué hace bien el sistema hoy?

**Generación de cobertura exhaustiva**: el prompt de generación instruye explícitamente al modelo a cubrir 7 tipos de casos de prueba (positivos, negativos, de borde, no funcionales, compatibilidad, seguridad y regresión), lo que resulta en planes de testing más completos que los generados manualmente bajo presión de tiempo.

**Clasificación automática de HUs**: el sistema detecta si una historia es de tipo Backend, Frontend o UI/UX y ajusta el análisis y los casos generados en consecuencia. Para HUs de Backend genera más casos de API, validación de endpoints y manejo de errores; para Frontend genera más casos de compatibilidad de navegadores y UX.

**Nomenclatura consistente**: el formato de IDs de caso de prueba (`USID: TC#: CONDITION`) es consistente con la convención usada en el equipo (por ejemplo, `AER25-101: TC1: Validate endpoint...`), lo que facilita la trazabilidad entre HU y caso de prueba.

**Gestión multi-proyecto**: el sistema soporta múltiples proyectos activos con su código identificador (ej: `AEROMAN`, `AER25`), y todos los datos están segregados por proyecto. El historial puede filtrarse por proyecto, por ID de HU, por búsqueda de texto o por rango de fechas.

**Versionamiento de HUs**: si se regenera el plan para una HU que ya existe (mismo `story_id`), el sistema no duplica el registro sino que incrementa la versión de la HU, permitiendo rastrear la evolución de una historia a lo largo del sprint.

**Exportación multi-formato**: XLSX (para QA engineers), CSV estándar (para procesamiento), CSV compatible con Jira/Xray (para importación directa) y JSON (para integraciones con otras herramientas).

**Chat contextual del plan**: el asistente de IA recibe el contexto completo del proyecto, la HU y el Test Plan, permitiendo preguntas como "¿hay casos de prueba de seguridad cubiertos?", "¿qué precondiciones tiene el TC5?" o "generá un caso adicional para este criterio de aceptación".

### Tipos de proyectos o historias que maneja mejor

- **HUs de APIs y endpoints REST**: el modelo genera con alta precisión casos para validación de datos de entrada, manejo de errores HTTP, autenticación y casos de borde para campos obligatorios/opcionales.
- **HUs con criterios de aceptación bien definidos**: cuanto más detallados y específicos sean los criterios, más acertados son los casos generados. El sistema puede mapear explícitamente cada criterio a uno o más casos de prueba.
- **HUs de funcionalidades de formularios y validaciones**: el modelo genera sistemáticamente variantes de datos válidos/inválidos/nulos/borde para campos de formulario.
- **HUs con ID en formato Jira** (ej: `PROJ-123`): el naming automático de los casos de prueba funciona correctamente con este formato.

### Ahorro de tiempo estimado

| Actividad | Proceso manual | Con el sistema |
|-----------|---------------|----------------|
| Generación de casos de prueba básicos | 45-90 minutos | ~40 segundos (IA) |
| Escritura de tabla de test plan | 30-60 minutos | Incluido |
| Formateo y exportación a Excel | 15-30 minutos | ~5 segundos |
| Revisión y ajuste del plan | 30-60 minutos | 10-20 minutos |
| **Total estimado** | **2-4 horas** | **15-25 minutos** |

---

## 6. Limitaciones Conocidas

### Limitaciones técnicas

**Dependencia total de la calidad del input**: si los criterios de aceptación son vagos, incompletos o inconsistentes, el Test Plan generado reflejará esa vaguedad. El sistema no tiene mecanismo para solicitar aclaraciones al usuario ni para detectar criterios ambiguos.

**Parsing de Markdown frágil**: el parser de la tabla (`parse_markdown_table_to_dict`) depende de que la tabla generada por la IA tenga exactamente 6 columnas y comience con el header `Prioridad`. Si el modelo genera variaciones en el header (ej: usa inglés, o agrega/elimina columnas), el parser falla silenciosamente y devuelve una lista vacía. Esto puede resultar en un Test Plan guardado sin casos de prueba estructurados.

**Pipeline secuencial sin paralelismo**: las 3 llamadas a OpenAI son secuenciales. No hay paralelización posible en la arquitectura actual porque cada paso depende del output del anterior. Si una llamada falla, todo el pipeline falla sin mecanismo de reintento automático.

**Sin integración directa con Jira**: los datos de la HU se ingresan manualmente. No existe lectura automática desde Jira, lo que implica que el usuario debe copiar y pegar el contenido de la HU desde Jira al formulario web.

**No maneja imágenes**: si la HU en Jira incluye capturas de pantalla de mockups o wireframes, el sistema actual no las procesa. El modelo solo recibe texto.

**Sin autenticación multi-usuario**: el sistema opera en modo single-user (`AUTH_REQUIRED: bool = False`). No hay control de acceso, roles ni segregación de datos entre usuarios.

**Base de datos SQLite**: apropiado para uso local y equipos pequeños, pero no escalable para uso concurrente de múltiples usuarios o volúmenes grandes de datos. SQLite tiene limitaciones conocidas con escrituras concurrentes.

### Limitaciones de alcance

**HUs muy largas**: si la descripción y criterios de aceptación son muy extensos, el costo de tokens aumenta y hay riesgo de truncamiento o degradación de calidad en la respuesta del modelo.

**Ausencia de templates personalizables**: actualmente el prompt de generación es fijo en el código. No hay interfaz para que el equipo de QA pueda ajustar el estilo de escritura, la nomenclatura o los tipos de casos a generar sin modificar el código fuente.

**Sin validación del Test Plan generado**: no hay mecanismo automático para detectar si el plan generado es de baja calidad, tiene pocos casos para la complejidad de la HU, o si la tabla de casos se generó correctamente antes de persistirla.

**Sin escritura de vuelta a Jira**: los casos de prueba generados no se publican automáticamente como sub-tareas, comentarios o adjuntos en el ticket de Jira correspondiente.

---

## 7. Roadmap y Mejoras Futuras Posibles

Las siguientes mejoras están propuestas como evolución natural del sistema, basándose en la arquitectura actual y en los documentos de roadmap del repositorio (`06_ROADMAP_IMPLEMENTACION.md`, `07_ESCALADO_PROYECTO.md`, `05_PROPUESTA_MCP_Y_APIS.md`).

---

### 7.1 Integración Bidireccional con Jira

**Descripción**: implementar lectura automática de HUs desde Jira mediante la API REST de Jira Cloud o Server, y escritura de vuelta de los Test Plans como comentarios, adjuntos o issues vinculados.

**Componentes a implementar**:
- Nuevo servicio `jira_client.py` con autenticación OAuth o Basic Auth
- Endpoint `GET /api/v1/jira/stories/{project_key}` para listar HUs abiertas
- Selector de HU desde la UI (en lugar del formulario manual)
- Escritura de vuelta: publicar el Test Plan como comentario en el ticket o adjuntar el `.xlsx`
- Configuración de `JIRA_URL`, `JIRA_USER`, `JIRA_TOKEN` en `.env`

**Impacto**: elimina la necesidad de copiar/pegar datos de Jira al formulario, reduciendo el tiempo de entrada a casi cero y eliminando posibles errores de transcripción.

---

### 7.2 Integración con Herramientas de Gestión de Testing (Xray, Zephyr, TestRail)

**Descripción**: exportar los casos de prueba generados directamente a la herramienta de test management utilizada por el equipo, en lugar de solo generar archivos Excel/CSV.

**Opciones por herramienta**:

| Herramienta | Método de integración | Complejidad |
|-------------|----------------------|-------------|
| Xray for Jira | API REST de Xray + importación de JSON/CSV con formato específico | Media |
| Zephyr Scale | API REST de Zephyr + creación de test cases vía `POST /testcases` | Media |
| TestRail | API REST de TestRail + creación de casos con `add_case` | Baja-Media |

**Componentes a implementar**:
- Servicio `test_management_service.py` con adaptadores por herramienta
- Endpoint `POST /api/v1/test-plans/{id}/push?target=xray|zephyr|testrail`
- Mapeo de prioridades del sistema (Alta/Media/Baja) a las prioridades de la herramienta destino
- Configuración en `.env` y UI para seleccionar el destino

---

### 7.3 Generación Automática de Scripts de Automatización

**Descripción**: a partir de un Test Plan generado, producir esqueletos de scripts de automatización en el framework preferido del equipo.

**Casos de uso**:
- Generar esqueletos de tests con Selenium/Playwright para HUs de Frontend
- Generar schemas de Postman Collections o archivos `.http` para HUs de Backend/API
- Generar esqueletos de pruebas con Cypress o Robot Framework

**Implementación sugerida**:
- Nuevo paso opcional en el pipeline de IA: `generate_automation_scripts(test_plan_en, framework)`
- Prompt especializado que mapea cada caso de prueba a una función de test con assertions básicas
- Exportación como `.py`, `.spec.js`, `.robot` o colección de Postman (`.json`)
- Selector en la UI para el framework de automatización destino

**Impacto**: proporciona al equipo de automatización un punto de partida estructurado en lugar de empezar desde cero.

---

### 7.4 Dashboard de Métricas y Analítica

**Descripción**: agregar un panel de métricas que permita al equipo de QA y management visualizar el uso del sistema, la cobertura generada y la evolución de la calidad de testing.

**Métricas propuestas**:
- Cantidad de Test Plans generados por proyecto y por período
- Distribución de casos por prioridad (Alta/Media/Baja) globalmente y por proyecto
- HUs con mayor número de casos de prueba (más complejas)
- Tiempo promedio de procesamiento por plan
- Planes generados vs. planes eliminados (tasa de aceptación)
- Evolución de versiones de HUs (cuántas veces se regeneró un plan)

**Implementación**:
- Endpoints de analítica: `GET /api/v1/analytics/summary`, `/api/v1/analytics/by-project`
- Nueva página en el frontend (`#/analytics`)
- Uso de Chart.js o Recharts para visualizaciones
- Posible integración con Grafana si se migra a PostgreSQL

---

### 7.5 Soporte Multi-Proyecto con Roles y Autenticación

**Descripción**: agregar autenticación de usuarios y control de acceso por proyecto, permitiendo que múltiples analistas trabajen simultáneamente con datos segregados.

**Componentes**:
- Autenticación con JWT (FastAPI Security + python-jose)
- Modelo `User` con campos: email, password (hash), role (admin/analyst/viewer)
- Permisos por proyecto: cada usuario puede ser asignado a uno o más proyectos
- Migración de SQLite a PostgreSQL para soporte de escrituras concurrentes
- Variables de entorno para configurar `DATABASE_URL` con PostgreSQL

**Nota de implementación**: la base de datos ya tiene el campo `DEFAULT_USER_ID = 1` preparado en la configuración, y el modelo de datos ya tiene `project_id` en `UserStory`, lo que hace que esta migración sea relativamente directa.

---

### 7.6 Plantillas de Prompts Personalizables

**Descripción**: externalizar los prompts del sistema a archivos de plantilla editables, permitiendo que el equipo de QA ajuste el estilo, nomenclatura, tipos de casos y nivel de detalle sin modificar el código.

**Implementación**:
- Carpeta `prompts/` con archivos `template_generate.txt`, `template_translate_en.txt`, `template_translate_es.txt`
- Soporte de variables de template (ej: `{hu_content}`, `{project_name}`, `{naming_convention}`)
- Interfaz en la UI para editar y guardar plantillas por proyecto
- Persistencia de plantillas en la BD (nueva tabla `prompt_templates`)

---

### 7.7 Procesamiento de Imágenes en Historias de Usuario

**Descripción**: permitir adjuntar capturas de pantalla de mockups, wireframes o diseños Figma a la HU, para que el modelo de IA los analice junto con el texto al generar el Test Plan.

**Implementación**:
- Soporte de upload de imágenes en el formulario web
- Uso del modelo `gpt-4o` (visión) para procesar texto + imagen en el paso de generación
- Almacenamiento de imágenes en el filesystem local o S3
- Casos de prueba de UI más precisos al tener visibilidad del diseño real

---

### 7.8 Servidor MCP (Model Context Protocol)

**Descripción**: exponer las capacidades del sistema como un servidor MCP, permitiendo que herramientas como Cursor, Claude Desktop o cualquier cliente MCP puedan invocar la generación de Test Plans directamente desde el IDE o desde flujos de trabajo automatizados.

**Herramientas MCP a exponer**:
- `generate_test_plan(story_id, title, description, acceptance_criteria, project_code)`
- `get_test_plan(test_plan_id)`
- `list_test_plans(project_code, limit)`
- `chat_with_test_plan(test_plan_id, message)`

**Valor**: permite que el desarrollador genere un Test Plan para la HU que está implementando directamente desde su IDE, sin cambiar de contexto.

---

## 8. Decisiones de Diseño Relevantes

### 8.1 ¿Por qué FastAPI y no Django, Flask u otro framework?

**Decisión**: FastAPI como framework principal del backend.

**Justificación**:
- **Asincronismo nativo**: el pipeline de IA involucra múltiples llamadas HTTP a OpenAI que pueden durar varios segundos. FastAPI con `async/await` permite atender otras solicitudes durante esas esperas sin bloquear el servidor.
- **Validación automática con Pydantic**: los schemas de request/response se definen una sola vez en Python y FastAPI genera automáticamente documentación OpenAPI, validación de tipos y serialización/deserialización. Esto elimina código boilerplate.
- **Performance**: FastAPI es uno de los frameworks Python más rápidos, basado en Starlette y comparable en performance a frameworks de Node.js.
- **OpenAPI/Swagger integrado**: la interfaz de documentación interactiva (`/docs`) es útil para desarrollo y testing sin herramientas adicionales.

**Trade-off**: FastAPI tiene una curva de aprendizaje moderada para desarrolladores acostumbrados a Django. La ausencia de ORM incluido (requiere SQLAlchemy por separado) añade algo de complejidad de configuración.

---

### 8.2 ¿Por qué Clean Architecture + DDD (Domain-Driven Design)?

**Decisión**: separar el código en capas: `domain` (entidades puras), `repositories` (interfaces + implementaciones), `services` (lógica de negocio), `api` (HTTP).

**Justificación**:
- **Testabilidad**: los servicios no dependen directamente de la base de datos, sino de interfaces de repositorio. En los tests se inyectan repositorios en memoria en lugar de SQLite, lo que hace los tests unitarios independientes de la BD y mucho más rápidos.
- **Reemplazabilidad**: si en el futuro se migra de SQLite a PostgreSQL, se reemplaza solo la implementación del repositorio (`sqlalchemy/`), sin tocar los servicios ni la lógica de dominio.
- **Legibilidad**: la estructura de carpetas refleja la arquitectura conceptual del sistema, facilitando la comprensión a nuevos desarrolladores.

**Trade-off**: para un proyecto de tamaño pequeño-mediano como este, Clean Architecture introduce algo de indirección (interfaces, entidades separadas de modelos ORM, factories de dependencias). Es una inversión en mantenibilidad a largo plazo que puede sentirse como overhead en las primeras etapas.

---

### 8.3 ¿Por qué SQLite y no PostgreSQL?

**Decisión**: SQLite como base de datos principal en la versión actual.

**Justificación**:
- **Sin infraestructura adicional**: no requiere instalar, configurar ni mantener un servidor de base de datos separado. El archivo `.db` es portable y fácilmente respaldable.
- **Suficiente para el caso de uso actual**: el sistema opera en modo single-user o equipo pequeño (< 10 usuarios), con volúmenes de datos que están lejos de los límites de SQLite (gigabytes).
- **Alembic ya está configurado**: la migración a PostgreSQL es posible simplemente cambiando la variable `DATABASE_URL` en `.env` sin cambiar ninguna otra línea de código, gracias a que SQLAlchemy abstrae el dialecto de BD.

**Trade-off**: SQLite no soporta escrituras concurrentes múltiples. En un escenario multi-usuario real (> 5 usuarios simultáneos generando planes), se podrían producir errores de contención. La migración a PostgreSQL es el paso natural cuando se escale el sistema.

---

### 8.4 ¿Por qué un pipeline de 3 llamadas y no una sola llamada en inglés?

**Decisión**: traducir al inglés → generar en inglés → traducir al español, en lugar de generar directamente en español.

**Justificación empírica**: los modelos de OpenAI (GPT-4 y familia) fueron entrenados predominantemente en inglés. Los prompts de QA técnicos en inglés producen consistentemente mejores resultados en:
- Cobertura de tipos de casos de prueba
- Precisión en la nomenclatura de testing
- Calidad del Reporte Jira incluido en el output

**Trade-off**: 3 llamadas API implica 3x el tiempo de espera y 3x el costo de tokens respecto a una sola llamada. Los modelos más rápidos (`gpt-4.1-mini`) para las traducciones compensan parcialmente este costo.

---

### 8.5 ¿Por qué Vanilla JS y no React/Vue/Angular?

**Decisión**: frontend con HTML + CSS + JavaScript puro, sin framework.

**Justificación**:
- **Sin proceso de build**: el frontend se sirve directamente como archivos estáticos desde FastAPI (`StaticFiles`). No requiere Node.js, npm, webpack ni proceso de compilación.
- **Cero dependencias externas**: el único JS de terceros es `marked.js` cargado desde CDN para renderizar Markdown.
- **Suficiente para el caso de uso actual**: la SPA tiene 3 vistas (generador, historial, proyectos) y complejidad de interacción moderada, manejable con Vanilla JS modular.
- **Facilidad de mantenimiento**: cualquier desarrollador con conocimientos básicos de HTML/CSS/JS puede modificar el frontend sin aprender un framework adicional.

**Trade-off**: a medida que la UI crezca (dashboard de métricas, editor de plantillas, gestión de usuarios), el mantenimiento de Vanilla JS se vuelve más complejo que con un framework con gestión de estado. El roadmap contempla migración a React o Vue como siguiente paso de madurez del frontend.

---

### 8.6 ¿Por qué parsear Markdown en lugar de pedir un JSON directamente a la IA?

**Decisión**: el modelo genera Markdown con tabla de casos de prueba, y el backend lo parsea en lugar de solicitar JSON estructurado.

**Justificación**: el output en Markdown con tabla es más legible para el usuario final cuando se renderiza en la UI web, y mantiene el documento completo (análisis narrativo + tabla) en un único campo que se puede almacenar, mostrar y exportar. El formato JSON directo de la IA tiende a ser menos consistente para documentos largos.

**Trade-off**: el parser de Markdown es más frágil que parsear JSON. Cambios en el formato de salida del modelo (por ejemplo, variaciones en el header de la tabla) pueden romper el parsing. Como mejora futura, se podría usar Structured Outputs de OpenAI (respuestas tipadas con JSON Schema) para la parte tabular, manteniendo el Markdown para el análisis narrativo.

---

*Documento generado a partir del análisis del código fuente, documentación arquitectónica y archivos de configuración del repositorio. Los apartados marcados con "(inferido del código)" corresponden a decisiones identificadas por análisis estático del código, no documentadas explícitamente.*
