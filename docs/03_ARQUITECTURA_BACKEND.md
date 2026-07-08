# 03 · Arquitectura Backend: Motor QA + Perfiles de Dominio

> **Objetivo del documento:** describir la arquitectura backend **actual** (por capas) y cómo se extiende para soportar **perfiles de dominio** manteniendo un único motor de QA.

Modelo de datos: [02](./02_PROPUESTA_MODELOS_DATOS.md) · Integraciones (MCP/APIs/n8n): [05](./05_PROPUESTA_MCP_Y_APIS.md) · Roadmap: [06](./06_ROADMAP_IMPLEMENTACION.md).

---

## 1. Arquitectura actual (implementada)

FastAPI con separación por capas (Clean Architecture / DDD ligero). Estructura real en `app/`:

```
app/
├── main.py                 # Bootstrap FastAPI, middleware, monta /static y el router
├── config.py               # Settings (Pydantic) + .env
├── api/v1/
│   ├── router.py           # Agrupa endpoints
│   ├── dependencies.py     # Inyección de dependencias (repos/servicios)
│   └── endpoints/          # test_plans, projects, chat, bug_report
├── domain/
│   ├── entities/           # Project, UserStory, TestPlan (lógica de negocio)
│   └── value_objects/      # StoryType
├── repositories/
│   ├── interfaces/         # Contratos (puertos)
│   └── sqlalchemy/         # Implementaciones (adaptadores de persistencia)
├── services/               # ai_service, test_plan_service, project_service,
│                           #   chat_service, bug_report_service, export_service,
│                           #   user_story_service
├── schemas/                # DTOs Pydantic (entrada/salida de la API)
├── core/                   # standards.py (ISO/ISTQB), logging, exceptions
├── db/                     # models.py (ORM), session, base
└── utils/                  # excel/csv/jira/json generators, markdown_parser
```

### Flujo de una generación de test plan (hoy)

```
Frontend ──POST /api/v1/analyze──▶ endpoint ──▶ test_plan_service
                                                     │
                                                     ▼
                                               ai_service  (pipeline 3 pasos)
                                          1) traduce HU a inglés (gpt-4.1-mini)
                                          2) genera TP en inglés (gpt-4.1) + core/standards.py
                                          3) traduce TP a español
                                                     │
                          markdown_parser ◀──────────┘   (extrae casos → TestCase)
                                                     │
                         repositorios ──▶ SQLite   ·   export_service ──▶ xlsx/csv/jira/json
```

Los estándares ISO/IEC 25010 y 29119 se inyectan al prompt desde `app/core/standards.py`
(`ISO_25010_CHARACTERISTICS`, `ISO_29119_TEST_PLAN_STRUCTURE`). El rol de IA es un
**Senior QA Analyst / Test Designer** que aplica los 7 escenarios y prioriza Alta/Media/Baja.

## 2. Extensión a Perfiles: principio de diseño

> **Un motor, muchos perfiles.** El motor (roles, 7 escenarios, normas, export) no cambia por dominio. Lo que cambia es *de dónde sale el contexto*, *qué conocimiento se inyecta* y *cómo se ponderan escenarios y prioridades*.

Un **Perfil** se compone de 4 piezas enchufables. Todas ya tienen un "hueco" natural en la arquitectura actual:

| Pieza del perfil | Dónde vive | Cómo se implementa |
|---|---|---|
| **Adaptador de entrada** | nuevo `app/adapters/input/` | Normaliza el artefacto a testear a un formato interno común (HU texto / KB GeneXus / transacción Bantotal). |
| **Paquete de conocimiento** | `app/core/domain_packs/` (evolución de `standards.py`) | Bloques de texto/reglas que se **componen**: base ISO/ISTQB + pack de dominio. |
| **Perfil de escenarios** | `app/core/profiles/` | Ponderación de los 7 escenarios y mapa de prioridades por dominio. |
| **Salida / conector** | `app/services/export_service.py` + nuevos conectores | Formato y destino (xlsx, Jira, test management, RTM). |

### 2.1 Composición del conocimiento (clave del refactor)

Hoy `standards.py` es un módulo plano. Se propone convertirlo en **packs componibles**:

```
app/core/
├── domain_packs/
│   ├── iso_base.py       # ISO 25010 + 29119 + ISTQB  (lo que ya existe)
│   ├── genexus.py        # patrones GeneXus, integridad referencial
│   └── banking.py        # contabilidad, integridad transaccional, PCI-DSS, AML, ...
└── profiles/
    ├── web_generic.py    # usa iso_base
    ├── genexus.py        # usa iso_base + genexus
    └── bantotal.py       # usa iso_base + genexus + banking   ← reutiliza la capa GeneXus
```

El `ai_service.generate_test_plan(...)` pasa a recibir un `profile` y **arma el prompt componiendo** el pack correspondiente + la ponderación de escenarios correspondiente. Un solo método, parametrizado por perfil.

### 2.2 Abstracción del proveedor de IA

Hoy `ai_service` está acoplado a OpenAI. Se introduce un **puerto** `LLMProvider` con implementaciones `OpenAIProvider` y `AnthropicProvider`, seleccionable por config (`AI_PROVIDER`). Esto habilita:

- Sumar **Claude** (contexto extenso, útil para grounding con KB/transacciones grandes).
- **Repensar el pipeline de traducción**: generar directamente en español cuando el proveedor lo permite con buena calidad, y usar traducción solo si aporta. Se valida con evaluación de calidad (ver [06](./06_ROADMAP_IMPLEMENTACION.md), Fase 5).

### 2.3 Grounding (contexto real del sistema)

El adaptador de entrada puede enriquecer el análisis con el sistema real, no solo el texto de la HU:

- **GeneXus:** parseo del export de la Knowledge Base (transacciones, atributos, reglas, Web Panels).
- **Bantotal:** consulta vía **MCP** (definiciones de transacciones, modelo de datos, servicios). Detalle en [05](./05_PROPUESTA_MCP_Y_APIS.md).

## 3. Flujo objetivo (con perfiles)

```
Proyecto(profile) ──▶ Adaptador de entrada(profile)
                            │  (HU texto | KB GeneXus | MCP Bantotal)
                            ▼
                   Motor QA  ─── compone ───▶  iso_base + pack de dominio(profile)
                            │                   + ponderación de escenarios(profile)
                            ▼
                   LLMProvider(config)  (OpenAI | Anthropic)
                            │
                            ▼
             Test plan + casos ──▶ persistencia (con profile + grounding_source)
                            │
                            ▼
             export_service ──▶ xlsx/csv/jira/json  ·  (roadmap) Xray/Zephyr/RTM
```

## 4. Principios a respetar

- **Retrocompatibilidad:** `web_generic` reproduce el comportamiento actual; ningún proyecto existente se rompe.
- **Aditivo:** perfiles, packs y proveedores se agregan sin reescribir el motor.
- **Puertos y adaptadores:** entrada, IA y salida se acceden por interfaces, no por implementaciones concretas.
- **Sin secretos en el código:** credenciales de conectores y proveedores viven en configuración, nunca versionadas.
