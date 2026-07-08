# 06 · Roadmap de Implementación (Perfiles de Dominio)

> **Objetivo del documento:** plan de implementación por fases para evolucionar el sistema hacia perfiles de dominio. Ordenado por dependencia: cada fase habilita la siguiente.

Visión: [01](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) · Backend: [03](./03_ARQUITECTURA_BACKEND.md) · Integraciones: [05](./05_PROPUESTA_MCP_Y_APIS.md).
Resumen ejecutivo para negocio: [`../PROPUESTA_PERFILES_DOMINIO.md`](../PROPUESTA_PERFILES_DOMINIO.md).

---

## Vista general

| Fase | Foco | Depende de |
|---|---|---|
| **1** | Base de perfiles + modernización del motor de IA | — |
| **2** | Perfil GeneXus (grounding en el modelo real) | 1 |
| **3** | Perfil Bantotal (core bancario) | 1, 2 |
| **4** | Manual de usuario + orquestación (n8n/Jira) | 1 (API), 3 |
| **5** | Calidad, trazabilidad y madurez de plataforma | transversal |

Las fases 1 y 2 son la base; 3 y 4 aportan el mayor salto de valor; 5 consolida calidad.

---

## Fase 1 — Base de perfiles y modernización del motor de IA
**Objetivo:** que el sistema entienda el concepto de perfil y quede desacoplado del proveedor de IA, sin romper el comportamiento actual para web.

**Tareas:**
- Agregar el atributo **`profile`** a `Project` (`web_generic` / `genexus` / `bantotal`), default `web_generic`. Migración Alembic nullable/con default (ver [02](./02_PROPUESTA_MODELOS_DATOS.md)).
- Refactorizar `core/standards.py` en **packs componibles** (`domain_packs/` + `profiles/`) — ver [03](./03_ARQUITECTURA_BACKEND.md).
- Introducir el puerto **`LLMProvider`** con `OpenAIProvider` y `AnthropicProvider`, seleccionable por config (`AI_PROVIDER`).
- **Rediseñar el pipeline de traducción:** generar directamente en español cuando la calidad lo permita; usar traducción solo si aporta.
- UI: selector de perfil en crear/editar proyecto + badge de perfil (ver [04](./04_ARQUITECTURA_FRONTEND_UX_UI.md)).

**Criterios de éxito:** proyectos existentes siguen funcionando idénticamente con `web_generic`; se puede cambiar de proveedor de IA por configuración; test plans en español sin doble traducción.

**Consideraciones:** medir calidad antes/después del cambio de traducción para evitar regresiones (base para el eval harness de la Fase 5).

---

## Fase 2 — Perfil GeneXus (grounding en el modelo real)
**Objetivo:** que los planes dejen de basarse solo en texto y usen los objetos reales del sistema.

**Tareas:**
- **Adaptador de entrada** para el **export de Knowledge Base de GeneXus** (transacciones, atributos, reglas, Web Panels).
- **Pack de conocimiento GeneXus** (`domain_packs/genexus.py`): patrones, integridad referencial.
- Ajustar la **ponderación de escenarios** para web generado.
- UI: adjuntar/referenciar el export de la KB en el generador.

**Criterios de éxito:** un test plan generado con perfil GeneXus referencia transacciones/atributos reales del export.

**Consideraciones:** definir con el equipo el formato de export de KB disponible. Empezar por lectura offline del export antes de integrar contra GeneXus Server.

---

## Fase 3 — Perfil Bantotal (core bancario)
**Objetivo:** cubrir la rama bancaria con el rigor que exige el dominio.

**Tareas:**
- **Pack de conocimiento bancario** (`domain_packs/banking.py`): contabilidad (cuadre), integridad transaccional, concurrencia, batch/cierre, conciliación, segregación de funciones, no repudio, PCI-DSS, AML, normativa del regulador.
- **Reponderación** de escenarios y prioridades hacia seguridad e integridad.
- **Adaptador vía MCP Bantotal** para traer transacciones y modelo de datos reales como contexto (ver [05](./05_PROPUESTA_MCP_Y_APIS.md)).
- Reutilizar la capa base GeneXus de la Fase 2.

**Criterios de éxito:** test plans bancarios con foco correcto (seguridad/integridad como Alta) y trazabilidad de la transacción de origen.

**Consideraciones (bloqueantes a gestionar en paralelo):**
- **Autorización del MCP Bantotal** y confirmación de qué expone.
- **Política de datos sensibles:** trabajar sobre definiciones/estructuras, nunca datos productivos.

---

## Fase 4 — Manual de usuario y orquestación (n8n + Jira)
**Objetivo:** cerrar el ciclo y automatizar el flujo end-to-end.

**Tareas:**
- Generación de **manual de usuario** a partir de HU, flujos y capturas (mismo pipeline: entrada → IA → documento → export).
- **Orquestación con n8n:** Jira dispara el análisis vía API, el motor genera los entregables y se publican en Jira/Confluence/Slack. El motor sigue siendo el cerebro (ver [05](./05_PROPUESTA_MCP_Y_APIS.md)).

**Criterios de éxito:** una HU nueva en Jira produce, sin intervención manual, su resumen + test plan publicados donde corresponde.

**Consideraciones:** estabilizar la API/webhook antes de conectar n8n; autorizar conectores Jira/Confluence.

---

## Fase 5 — Calidad, trazabilidad y madurez de plataforma
**Objetivo:** sostener la calidad a escala. Transversal, se incorpora incrementalmente.

**Tareas:**
- **Matriz de trazabilidad (RTM):** HU ↔ casos ↔ requisitos ↔ defectos.
- **Harness de evaluación de prompts:** medir cobertura de los 7 escenarios y fidelidad al cambiar prompt, perfil o modelo.
- **Procesos asíncronos** para generaciones largas y **seguimiento de costos** de IA.
- (Futuro) Generación de **tests ejecutables** (Playwright/pytest/Postman) e integración con **Xray/Zephyr/TestRail**.

**Criterios de éxito:** cada cambio de modelo/prompt/perfil se valida contra un set de referencia; trazabilidad completa disponible para auditoría.

---

## Consideraciones transversales

- **Retrocompatibilidad:** el perfil web genérico es el comportamiento por defecto; nada de lo actual se rompe.
- **Seguridad y datos bancarios:** definir política antes de la Fase 3.
- **Dependencias externas:** MCP Bantotal y conectores Jira/Confluence requieren autorización; gestionarlas en paralelo para no bloquear.
- **Esfuerzo incremental:** la sinergia GeneXus↔Bantotal hace que la Fase 3 sea aditiva sobre la 2.
- **Conocimiento de dominio:** los packs bancarios requieren input de especialistas de la rama bancaria; involucrarlos temprano.

## Próximos pasos inmediatos

1. Validar con el equipo la decisión de extender vía perfiles y el alcance de los 3 perfiles iniciales.
2. Confirmar qué expone el MCP Bantotal y gestionar su autorización.
3. Definir el formato de export de la Knowledge Base de GeneXus disponible.
4. Priorizar y estimar **Fase 1** como primer incremento.
5. Acordar la política de manejo de datos sensibles para el perfil bancario.
