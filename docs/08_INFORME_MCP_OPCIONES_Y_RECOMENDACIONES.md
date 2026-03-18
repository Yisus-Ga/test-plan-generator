# Informe: MCP (Model Context Protocol) – Opciones y Recomendaciones

## 1. Objetivo de este documento

Evaluar cómo avanzar con MCP en el proyecto de Generador de Test Plans, considerando:
- Contexto de proyecto y historias relacionadas generadas anteriormente.
- Uso de la descripción del proyecto (y otros campos) como contexto.
- No solo recibir un Test Plan generado, sino poder hacer consultas al modelo (por ejemplo vía chat) sobre la historia que se va a probar, casos concretos o cómo ejecutar una prueba.
- Restricción actual: solo se dispone de acceso al modelo vía API Key de OpenAI de la compañía.

---

## 2. Qué es MCP y para qué sirve en tu caso

**Model Context Protocol (MCP)** es un estándar abierto que permite que aplicaciones expongan “recursos” y “herramientas” a clientes de IA (por ejemplo Claude Desktop, Cursor, IDEs, o un chat propio). Así, el modelo puede:
- Leer contexto (proyectos, HUs, Test Plans ya generados).
- Ejecutar acciones (generar test plan, analizar HU, traducir).
- Mantener una conversación apoyada en ese contexto.

En tu visión:
- El modelo tendría **contexto del proyecto** (descripción, nombre, etc.) y de las **historias y test plans ya generados**.
- El usuario podría, en un **chat**, preguntar cosas como: “¿Cómo pruebo el caso CP-003?”, “¿Qué precondiciones tiene la HU AER25-101?”, “Dame ideas de casos para el criterio de aceptación X”.
- Sigue existiendo el flujo actual: cargar HU → generar Test Plan → descargar. El chat sería un **complemento** para consultas y asistencia.

---

## 3. Opciones de arquitectura con solo API OpenAI

Con **solo API Key de OpenAI** (sin obligación de usar hoy un servidor MCP “estándar”), hay varias formas de acercarse a esto.

### Opción A: Chat con contexto en tu backend (sin MCP estándar aún)

**Idea:** En tu FastAPI actual:
- Nuevo endpoint, por ejemplo: `POST /api/v1/chat` que recibe: `project_id` o `test_plan_id`, y el **mensaje del usuario**.
- El backend arma un **prompt con contexto**:
  - Descripción del proyecto.
  - HU asociada (título, descripción, criterios).
  - Test Plan ya generado (resumen, tabla de casos, etc.).
- Llama a **OpenAI API** (Chat Completions) con ese contexto + historial de mensajes y devuelve la respuesta.

**Ventajas:**
- No requiere implementar MCP ni nuevas infraestructuras.
- Reutilizas tu API Key de OpenAI y tu stack actual.
- Escalable: luego puedes sumar más contexto (varias HUs del proyecto, otros Test Plans).
- Puedes guardar conversaciones en DB si quieres historial por proyecto/HU.

**Desventajas:**
- No es “MCP estándar”; si más adelante quieres conectar con Claude Desktop u otras apps MCP, habría que añadir un servidor MCP que use este backend por detrás.

**Recomendación:** Es la opción más práctica para **empezar ya** con “chat con contexto” y validar el valor con usuarios.

---

### Opción B: Servidor MCP integrado que usa OpenAI por detrás

**Idea:** Implementar un **servidor MCP** (por ejemplo con el SDK de MCP en Python) dentro del mismo proyecto:
- El servidor expone **tools**: `get_project_context`, `get_user_story`, `get_test_plan`, `generate_test_plan`, `ask_about_test` (o similar).
- Los **recursos** pueden ser: “proyecto X”, “HU Y”, “Test Plan Z”.
- Un **cliente MCP** (Cursor, Claude Desktop, o un frontend tuyo que hable MCP) se conecta al servidor; cuando el usuario escribe en el chat, el cliente llama a las tools y el modelo usa ese contexto.
- Las tools, por dentro, llaman a tu backend (o directamente a DB) y, cuando hace falta, a la **API de OpenAI** para generar respuestas.

**Ventajas:**
- Alineado con el estándar MCP: luego puedes reutilizar el mismo servidor con otros clientes (IDE, escritorio, etc.).
- Separa “quién tiene el contexto” (servidor MCP) de “quién genera texto” (OpenAI).

**Desventajas:**
- Más trabajo inicial: servidor MCP, transporte (stdio/SSE), definición de tools/recursos.
- Para “solo tu app web” no es estrictamente necesario; tiene más sentido si quieres que Cursor/Claude Desktop usen ese contexto.

**Recomendación:** Útil como **segunda fase** una vez que el chat con contexto (Opción A) esté validado y quieras abrir la puerta a clientes MCP estándar.

---

### Opción C: Solo frontend con OpenAI (sin backend de chat)

**Idea:** Un chat en el frontend que llame **directo** a OpenAI desde el navegador (con API Key oculta vía proxy o solo desde backend).

**Problema:** Si la API Key está en el frontend, se expone. Si la llamada va siempre a tu backend (que luego llama a OpenAI), en la práctica estás en la **Opción A**. Por tanto, no es una opción distinta si quieres seguridad; es Opción A con UI de chat.

---

## 4. Qué necesitas para cada opción

### Para Opción A (Chat con contexto en backend)

| Necesidad | Estado / Acción |
|-----------|------------------|
| API Key OpenAI | Ya la tienes. |
| Modelo OpenAI | Usar mismo modelo que hoy (p.ej. gpt-4.1) o uno más barato para chat (gpt-4.1-mini). |
| Contexto en backend | Proyecto (descripción, nombre, código), HU (título, descripción, criterios), Test Plan (objetivo, resumen, tabla de casos). Todo ya está en tu dominio/DB. |
| Endpoint de chat | Nuevo: `POST /api/v1/chat` con body: `project_id` o `test_plan_id`, `message`, opcional `conversation_id` para historial. |
| Prompt de sistema | Definir un prompt que diga: “Eres un asistente de QA. Tienes el contexto del proyecto, la HU y el Test Plan. Responde preguntas sobre cómo probar, precondiciones, casos concretos, etc.” |
| Frontend | Nueva vista o panel “Chat” donde el usuario elige proyecto/HU o Test Plan y escribe; se muestran respuestas del modelo. |
| Persistencia (opcional) | Tabla `conversations` y `messages` si quieres guardar historial por proyecto/usuario. |

No necesitas:
- Servidor MCP.
- Nuevos protocolos.
- Cambiar cómo generas hoy el Test Plan (sigue siendo tu flujo actual).

---

### Para Opción B (Servidor MCP)

| Necesidad | Estado / Acción |
|-----------|------------------|
| Todo lo de Opción A | Como base de contexto y lógica. |
| SDK MCP (Python) | Instalar y configurar servidor MCP (p.ej. `mcp` en Python). |
| Definición de tools | Implementar tools que lean proyecto, HU, Test Plan y que llamen a tu servicio de OpenAI donde corresponda. |
| Transporte | Decidir: stdio (para Cursor/Claude Desktop) o SSE (para un frontend web que hable MCP). |
| Cliente | Cursor, Claude Desktop, o un cliente web que consuma tu servidor MCP. |

---

## 5. Recomendación de camino

### Fase 1 (corto plazo): Opción A – Chat con contexto en tu backend

1. **Implementar en tu FastAPI:**
   - `POST /api/v1/chat`: recibe `project_id` y/o `test_plan_id` (o `user_story_id`) y el mensaje del usuario.
   - Armar contexto desde DB: descripción del proyecto, HU asociada, Test Plan (resumen + casos).
   - Llamar a OpenAI Chat Completions con:
     - System prompt fijo (rol de asistente QA + instrucción de usar solo el contexto dado).
     - Mensajes: historial (si lo guardas) + mensaje actual.
   - Devolver la respuesta al frontend.

2. **En el frontend:**
   - Añadir una pestaña o panel “Consultas” / “Chat”:
     - Selector de proyecto y/o de Test Plan (o HU).
     - Caja de texto y envío de mensaje.
     - Área de respuestas (y opcional historial de la conversación).

3. **Opcional pero útil:**
   - Guardar en DB las conversaciones por proyecto (o por test_plan_id) para poder retomar después y para que el modelo tenga historial en la misma sesión.

Con esto tienes ya “un MCP conceptual”: **contexto del proyecto + historias/Test Plans + chat con el modelo**, usando solo tu stack actual y la API de OpenAI.

### Fase 2 (medio plazo): Opción B – Servidor MCP estándar

Cuando quieras que **Cursor, Claude Desktop u otras herramientas** usen el mismo contexto:
- Implementar servidor MCP que exponga **tools** y **recursos**.
- Esas tools/recursos pueden llamar a los mismos servicios que ya uses en la Opción A (obtener proyecto, HU, Test Plan, y hasta “preguntar al modelo”).
- Así, el “cerebro” (OpenAI) y la “fuente de verdad” (tu backend/DB) siguen siendo los mismos; solo añades la capa MCP estándar para otros clientes.

---

## 6. Resumen de respuestas directas

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué necesito para tener “MCP con contexto de proyecto e historias”? | Con solo API OpenAI: un **chat en backend** (Opción A) que arme contexto con proyecto + HU + Test Plan y llame a OpenAI. No es obligatorio implementar MCP estándar al principio. |
| ¿Puedo hacer consultas tipo chat sobre la historia o un caso concreto? | Sí, con la Opción A: el usuario elige proyecto/Test Plan, escribe la pregunta y el backend inyecta ese contexto en la llamada a OpenAI y devuelve la respuesta. |
| ¿Necesito algo más que la API Key de OpenAI? | Para la Opción A no. Para un servidor MCP estándar (Opción B) necesitas además el SDK MCP y definir tools/recursos. |
| ¿Es mejor empezar por MCP estándar o por chat en backend? | Recomendable **empezar por chat en backend** (Opción A): menos riesgo, entrega valor pronto y deja la puerta abierta a MCP estándar después (Opción B). |

Si quieres, el siguiente paso puede ser bajar esto a **tareas concretas** (endpoints, esquema de prompt, campos de contexto y diseño mínimo del panel de chat en el frontend) para la Fase 1.
