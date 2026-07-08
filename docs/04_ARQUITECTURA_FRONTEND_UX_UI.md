# 04 · Arquitectura Frontend y UX (con selección de Perfil)

> **Objetivo del documento:** describir el frontend **actual** (SPA en JS vanilla modular) y los cambios de UX necesarios para exponer los **perfiles de dominio** al usuario.

Backend: [03](./03_ARQUITECTURA_BACKEND.md) · Roadmap: [06](./06_ROADMAP_IMPLEMENTACION.md).

---

## 1. Frontend actual (implementado)

SPA sin framework, servida por FastAPI en `/static`. Estructura real en `static/assets/js/`:

```
static/
├── index.html
├── style.css
└── assets/
    ├── css/            # themes, navigation, components, analysis
    └── js/
        ├── main.js         # arranque de la app
        ├── router.js       # ruteo entre páginas (SPA)
        ├── config.js       # base URL de la API, constantes
        ├── api/            # client + wrappers: projects, test_plans, chat, bug_report
        ├── pages/          # generator, history, projects
        ├── components/     # Button, FormInput, chatModal, confirmDialog, toast
        └── utils/          # dom, validation
```

Características:
- **Ruteo del lado del cliente** (`router.js`) entre páginas (generador, historial, proyectos).
- **Capa de API** (`api/`) que centraliza las llamadas al backend a través de un `client.js`.
- **Componentes reutilizables** (botones, inputs, modal de chat, diálogos de confirmación, toasts) — notificaciones y confirmaciones ya estandarizadas.
- **Temas** (CSS variables en `themes.css`).

## 2. Cambios de UX para Perfiles

El objetivo es que el perfil sea **explícito y visible**, porque condiciona qué se genera y con qué rigor.

### 2.1 Selección de perfil en el Proyecto

- Al **crear/editar un proyecto** (`pages/projects.js`), agregar un selector de **Perfil de dominio**: `Web genérico` · `GeneXus` · `Bantotal`.
- Mostrar el perfil como **badge** en el listado de proyectos y en el historial, para que el usuario sepa siempre bajo qué reglas se generó cada test plan.

### 2.2 Entrada según perfil (grounding)

La pantalla del generador (`pages/generator.js`) se adapta al perfil del proyecto:

| Perfil | Entrada mostrada |
|---|---|
| Web genérico | Formulario de HU actual (título, descripción, criterios). |
| GeneXus | Formulario de HU **+** opción de adjuntar/referenciar el export de la Knowledge Base. |
| Bantotal | Formulario de HU **+** selector de transacción/servicio del core (vía conector MCP). |

Las partes que dependen de conectores (KB, MCP) deben degradar con elegancia: si el conector no está disponible, el sistema cae al modo "solo texto de la HU" e informa al usuario.

### 2.3 Resultado y exportación

- Mostrar en el resultado la **procedencia**: perfil usado, proveedor/modelo de IA y fuente de grounding (trazabilidad — ver [02](./02_PROPUESTA_MODELOS_DATOS.md)).
- Mantener la exportación actual (xlsx/csv/jira/json) y prever destinos nuevos por perfil (ej. Xray/Zephyr, matriz de trazabilidad) — ver [06](./06_ROADMAP_IMPLEMENTACION.md).

## 3. Principios de UX

- **El perfil nunca es implícito:** siempre visible dónde y cómo afecta el resultado.
- **Retrocompatibilidad:** sin elegir perfil, la experiencia es la actual (perfil `web_generic` por defecto).
- **Degradación elegante:** la ausencia de un conector no bloquea; reduce capacidades e informa.
- **Consistencia:** reutilizar los componentes existentes (toasts, confirmDialog) para toda interacción nueva.
