# 05 · Integración: API-first, MCP (Bantotal) y Orquestación (n8n)

> **Objetivo del documento:** definir cómo el sistema se integra con el mundo exterior — como **API/servicio**, como consumidor de **grounding vía MCP** (en especial Bantotal), y como pieza orquestada por **n8n** junto a Jira/Confluence.

Backend: [03](./03_ARQUITECTURA_BACKEND.md) · Roadmap: [06](./06_ROADMAP_IMPLEMENTACION.md).

---

## 1. API REST actual

El backend ya expone una API REST versionada bajo `/api/v1` (documentada en `/docs`). Endpoints principales:

| Método | Ruta | Función |
|---|---|---|
| POST | `/api/v1/analyze/` | Genera análisis + test plan a partir de una HU. |
| GET | `/api/v1/test-plans/` · `/{id}` | Lista y detalle de test plans. |
| DELETE | `/api/v1/test-plans/{id}` | Elimina un test plan. |
| GET | `/api/v1/download/{token}` | Descarga del export. |
| CRUD | `/api/v1/projects/...` | Gestión de proyectos (+ `PATCH .../status`). |
| POST | `/api/v1/chat` | Chat con contexto sobre HU/Test Plan. |
| POST | `/api/v1/reporte-bug` | Generación de reporte de bug (ISO 25010). |

Esta API es la base del enfoque **API-first**: cualquier integración externa (n8n, Jira, CI) consume estos endpoints; la lógica QA **no se replica afuera**.

## 2. Grounding vía MCP — el caso Bantotal

**MCP (Model Context Protocol)** permite que el sistema consulte de forma programática una fuente externa y use esa información como contexto del análisis. Aquí el uso central es **grounding**: aterrizar los test plans en el sistema real, no solo en el texto de la HU.

### 2.1 Bantotal

La organización ya cuenta con un conector **MCP AP Bantotal**. El **adaptador de entrada** del perfil Bantotal (ver [03](./03_ARQUITECTURA_BACKEND.md)) lo usaría para traer, como contexto:

- Definiciones de **transacciones** del core.
- **Modelo de datos** y relaciones relevantes.
- **Servicios** expuestos.

Con eso, el motor diseña casos que referencian transacciones y reglas reales, con foco en integridad, seguridad y regresión.

### 2.2 Consideraciones críticas (a resolver con el equipo antes de la Fase 3)

- **Autorización:** el conector MCP debe estar habilitado y autorizado. Confirmar **qué expone exactamente** (transacciones / modelo de datos / servicios), porque de eso depende cuánto grounding real es posible.
- **Datos sensibles:** trabajar **solo con definiciones y estructuras**, nunca con datos productivos de clientes. Definir política de manejo de información bancaria.
- **GeneXus por debajo:** Bantotal corre sobre GeneXus, así que el adaptador reutiliza la comprensión de objetos GeneXus del perfil correspondiente.

### 2.3 GeneXus

Para el perfil GeneXus, el "grounding" equivalente es el **export de la Knowledge Base** (transacciones, atributos, reglas, Web Panels). Puede empezar como lectura de archivo (offline) antes de integrar contra GeneXus Server.

## 3. Orquestación con n8n

**Principio rector:** n8n **orquesta y mueve datos; no contiene la lógica QA.** El motor sigue siendo el "cerebro"; n8n es el "plumbing".

```
Jira (webhook: nueva/actualizada HU)
        │
        ▼
      n8n  ──llama──▶  API del Test Plan Generator  (/api/v1/analyze, etc.)
        │                        │
        │                  genera resumen + test plan (+ manual de usuario)
        ▼                        ▼
Jira / Confluence / Slack  ◀── publica resultados (adjuntos, comentarios, tickets)
```

Beneficios:
- Un flujo editable por perfiles no-dev (QA/PM) sin tocar el backend.
- Reintentos, agendado y notificaciones resueltos por n8n.
- El motor permanece como única fuente de verdad de la calidad.

Prerrequisito: **exponer el motor como API/webhook estable** (ya casi cubierto) antes de conectar n8n. Los conectores de Jira/Confluence requieren autorización previa.

## 4. Destinos de salida (evolución)

Además del export actual (xlsx/csv/jira/json), los perfiles habilitan destinos ricos:

- **Herramientas de test management:** Xray / Zephyr / TestRail (donde vive el equipo QA).
- **Matriz de trazabilidad (RTM):** HU ↔ casos ↔ requisitos ↔ defectos — especialmente valiosa para auditoría en banca.
- **Manual de usuario:** publicado a Confluence/PDF (mismo pipeline: entrada → IA → documento → export).

## 5. Resumen de decisiones

- **API-first:** la inteligencia vive en el backend; todo lo demás la consume.
- **MCP para grounding**, empezando por Bantotal (con las salvaguardas de datos).
- **n8n como orquestador**, no como dueño de la lógica.
- Evolución de salidas hacia test management + RTM + manual de usuario.
