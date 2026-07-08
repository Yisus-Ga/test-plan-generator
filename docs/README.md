# Documentación del Proyecto — Test Plan Generator

Esta carpeta documenta el sistema **y su evolución hacia perfiles de dominio** (soporte para distintos tipos de aplicaciones: web/GeneXus, core bancario/Bantotal), manteniendo un único motor de QA.

> **¿Buscás el resumen ejecutivo para compartir con el equipo/negocio?**
> Está en la raíz: [`../PROPUESTA_PERFILES_DOMINIO.md`](../PROPUESTA_PERFILES_DOMINIO.md).

---

## Índice

| # | Documento | Contenido |
|---|---|---|
| 00 | [Entorno, Configuración y Puesta en Marcha](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md) | Cómo instalar y correr el proyecto; configuración y secretos. |
| 01 | [Punto de Partida y Visión de Perfiles](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) | Qué hace el sistema hoy y por qué evolucionamos a perfiles de dominio. |
| 02 | [Modelo de Datos](./02_PROPUESTA_MODELOS_DATOS.md) | Modelo actual (Project/UserStory/TestPlan/TestCase) + extensión para perfiles. |
| 03 | [Arquitectura Backend](./03_ARQUITECTURA_BACKEND.md) | Motor QA por capas + cómo se enchufan los perfiles (packs, adaptadores, proveedor de IA). |
| 04 | [Arquitectura Frontend y UX](./04_ARQUITECTURA_FRONTEND_UX_UI.md) | SPA actual + selección de perfil en la interfaz. |
| 05 | [Integración: API-first, MCP y n8n](./05_PROPUESTA_MCP_Y_APIS.md) | API REST, grounding vía MCP (Bantotal) y orquestación con n8n/Jira. |
| 06 | [Roadmap de Implementación](./06_ROADMAP_IMPLEMENTACION.md) | Plan por fases para construir los perfiles. |

---

## Rutas de lectura sugeridas

- **Para entender el rumbo (management/PM):** [`../PROPUESTA_PERFILES_DOMINIO.md`](../PROPUESTA_PERFILES_DOMINIO.md) → [01](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) → [06](./06_ROADMAP_IMPLEMENTACION.md).
- **Para empezar a desarrollar:** [00](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md) → [01](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) → [03](./03_ARQUITECTURA_BACKEND.md) → [02](./02_PROPUESTA_MODELOS_DATOS.md).
- **Frontend:** [04](./04_ARQUITECTURA_FRONTEND_UX_UI.md) → [03](./03_ARQUITECTURA_BACKEND.md).
- **Integraciones:** [05](./05_PROPUESTA_MCP_Y_APIS.md) → [06](./06_ROADMAP_IMPLEMENTACION.md).

---

## Estado

- El sistema base (generación de test plans, proyectos, historial, chat, exportación) está **implementado y operativo**.
- La documentación describe ese estado actual **y** el diseño acordado de **perfiles de dominio**, que es la próxima etapa (ver [06](./06_ROADMAP_IMPLEMENTACION.md)).
- Las secciones marcadas como "roadmap" o "propuesta" aún no están implementadas: son el plan a construir con el equipo.
