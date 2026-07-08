# Test Plan Generator — Evolución hacia Perfiles de Dominio

**Documento:** Propuesta de arquitectura y roadmap
**Autor:** Equipo QA / Jesús Gallardo
**Fecha:** Julio 2026
**Estado:** Borrador para revisión con el equipo

---

## 1. Objetivo del documento

Presentar la propuesta para hacer crecer el **Test Plan Generator** de modo que, a partir del mismo motor, pueda analizar y generar documentación de calidad (resumen del proyecto, planes de prueba y casos de prueba) para **distintos tipos de aplicaciones y tecnologías** — desde sistemas web (GeneXus u otros) hasta el core bancario (Bantotal) — sin duplicar el sistema.

Este documento sirve de base para la discusión con el equipo y para definir el plan de trabajo.

---

## 2. Resumen ejecutivo

Hoy el Test Plan Generator toma una Historia de Usuario (HU), la analiza con IA y produce un plan de pruebas estructurado bajo normas ISO/IEC 25010, ISO/IEC/IEEE 29119 e ISTQB, con exportación a Excel/CSV/Jira. Funciona bien para el caso general, pero fue pensado para un tipo de aplicación.

La empresa testea realidades muy distintas: **sistemas web** (construidos en GeneXus u otras tecnologías) y la **rama bancaria**, que corre sobre un core distinto y usa **Bantotal**. Cada mundo tiene reglas, riesgos y normativa propias. La pregunta es si adaptamos el sistema, lo migramos o construimos algo nuevo.

**La decisión propuesta es extender, no migrar ni bifurcar.** Se mantiene un **único motor de QA** (los roles de IA, los 7 escenarios de prueba, las normas ISO/ISTQB y la exportación que ya existen) y se le agregan **"Perfiles de Dominio" enchufables**. Un perfil ajusta tres cosas: *de dónde saca el contexto real de lo que se va a testear*, *qué conocimiento y normativa se inyecta al análisis*, y *cómo se ponderan los escenarios y prioridades*. El resultado: un solo sistema que cubre web, GeneXus, Bantotal y cualquier stack futuro, agregando un pack de conocimiento en lugar de reescribir el motor.

Un punto clave que reduce el esfuerzo: **Bantotal está desarrollado sobre GeneXus**, de modo que el perfil bancario reutiliza una capa base común con el perfil GeneXus y solo suma encima el paquete de dominio bancario. Además, la empresa ya cuenta con un conector **MCP hacia Bantotal**, que puede usarse para "aterrizar" los planes de prueba en las transacciones y el modelo de datos reales del core, en lugar de trabajar solo con el texto de la HU.

Como mejoras transversales se propone **repensar el flujo de traducción** actual (traducir la HU al inglés, generar y volver a traducir al español introduce pérdida de fidelidad, latencia y costo innecesarios) y **sumar un segundo proveedor de IA** (Claude, con contexto de 1M tokens) para ganar calidad, redundancia y capacidad de ingerir contexto extenso.

---

## 3. Punto de partida (situación actual)

El sistema hoy:

- Recibe Historias de Usuario y genera **resumen + plan de pruebas + casos** priorizados.
- Aplica **los 7 escenarios de prueba** (positivo, negativo, límite/exploratorio, no funcional, compatibilidad, seguridad, regresión).
- Inyecta estándares **ISO/IEC 25010, ISO/IEC/IEEE 29119 e ISTQB** en el análisis.
- Exporta a **Excel/CSV/Jira/JSON** con formato amigable.
- Ya organiza el trabajo por **Proyecto** (con estado activo/inactivo).
- Usa un flujo de IA que **traduce al inglés, genera y traduce de vuelta al español**, sobre un único proveedor (OpenAI).

Limitación central: el conocimiento y la ponderación están pensados para un tipo de aplicación. No distingue si lo que se testea es un web GeneXus o una transacción bancaria crítica.

---

## 4. Propuesta de arquitectura: un motor, muchos perfiles

Se mantiene el motor actual como núcleo y se introduce el concepto de **Perfil de Dominio**. Cada Proyecto elige un perfil, y ese perfil condiciona cómo el motor genera los entregables.

```
                    ┌─────────────────────────────┐
                    │   MOTOR QA (lo que ya existe) │
                    │  roles · 7 escenarios · ISO   │
                    │  ISTQB · export · chat        │
                    └──────────────┬──────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           ▼                       ▼                       ▼
   Perfil Web genérico     Perfil GeneXus          Perfil Bantotal
   (React, .NET, etc.)     (capa base GeneXus)     (GeneXus + pack bancario)
```

### 4.1 Qué compone un Perfil

Cada perfil son cuatro piezas enchufables:

| Pieza | Qué define |
|---|---|
| **Adaptador de entrada** | De dónde obtiene el artefacto a testear (HU en texto, export de KB de GeneXus, transacciones del core vía MCP Bantotal). |
| **Paquete de conocimiento** | Reglas y normativa de dominio que se inyectan al análisis, por encima de la base ISO/ISTQB. |
| **Perfil de escenarios** | Ponderación y checklist de los 7 escenarios y de las prioridades Alta/Media/Baja según el dominio. |
| **Salida / conector** | Dónde y en qué formato se publican los resultados (Excel, Jira, herramienta de test management, matriz de trazabilidad para auditoría). |

### 4.2 Perfiles iniciales objetivo

| Perfil | Grounding (contexto real) | Énfasis de conocimiento | Escenarios que más pesan |
|---|---|---|---|
| **Web genérico** | HU en texto | ISO/ISTQB base | Funcional, compatibilidad, UX |
| **GeneXus** | Export de la Knowledge Base (transacciones, atributos, reglas, Web Panels) | Patrones GeneXus, integridad referencial | Validación de transacciones, integridad, compatibilidad del web generado |
| **Bantotal** | Transacciones y modelo de datos reales vía **MCP Bantotal** | Contabilidad (cuadre/partida doble), integridad transaccional, concurrencia, procesos batch de cierre, conciliación, segregación de funciones, no repudio, PCI-DSS, prevención de lavado, normativa del regulador | Seguridad, integridad de datos, regresión y negativo (habitualmente prioridad Alta) |

---

## 5. Decisiones ya acordadas

1. **Extender el sistema actual mediante perfiles** — no migrar ni crear un sistema paralelo.
2. El motor genera **resumen del proyecto, planes y casos de prueba según el perfil** indicado.
3. **Repensar el flujo de traducción** (evitar el ida y vuelta inglés↔español).
4. **Incorporar un segundo modelo de IA** (Claude) además del actual.

---

## 6. Roadmap propuesto

> El roadmap está ordenado por dependencia: cada fase habilita la siguiente. Las fases 1 y 2 son la base; las 3 y 4 aportan el mayor salto de valor; la 5 consolida calidad y trazabilidad.

### Fase 1 — Base de perfiles y modernización del motor de IA
**Objetivo:** que el sistema entienda el concepto de perfil y quede desacoplado del proveedor de IA.
- Agregar el atributo **Perfil** al Proyecto (web-genérico / genexus / bantotal).
- Refactorizar el conocimiento de normas en **paquetes componibles** (base ISO/ISTQB + pack de dominio).
- **Abstraer el proveedor de IA** para soportar OpenAI y Claude de forma intercambiable.
- **Rediseñar el flujo de traducción**: generar directamente en español (validado con evaluación de calidad) y usar la traducción solo cuando aporte.

*Consideraciones:* mantener 100% compatible el comportamiento actual para web mientras se introduce el perfil por defecto. Medir calidad antes/después del cambio de traducción para evitar regresiones.

### Fase 2 — Perfil GeneXus (grounding en el modelo real)
**Objetivo:** que los planes dejen de basarse solo en texto y usen los objetos reales del sistema.
- Adaptador de entrada para **export de Knowledge Base de GeneXus** (transacciones, atributos, reglas, Web Panels).
- Paquete de conocimiento GeneXus (patrones, integridad referencial).
- Ajuste de la ponderación de escenarios para web generado.

*Consideraciones:* definir con el equipo el formato de export de la KB disponible. Empezar por lectura del export (offline) antes de integración directa con GeneXus Server.

### Fase 3 — Perfil Bantotal (core bancario)
**Objetivo:** cubrir la rama bancaria con el nivel de rigor que exige el dominio.
- **Paquete de conocimiento bancario** (contabilidad, integridad transaccional, concurrencia, batch/cierre, conciliación, segregación de funciones, PCI-DSS, AML, normativa).
- Reponderación de escenarios y prioridades hacia seguridad e integridad.
- **Adaptador vía MCP Bantotal** para traer transacciones y modelo de datos reales como contexto del análisis.

*Consideraciones:*
- **El conector MCP Bantotal debe estar autorizado**; hay que confirmar con el área responsable qué expone exactamente (transacciones, modelo de datos, servicios), porque de eso depende cuánto grounding real es posible.
- **Datos sensibles:** definir política de manejo de información bancaria (no exponer datos productivos ni secretos; trabajar sobre definiciones/estructuras, no sobre datos reales de clientes).
- Reutilizar la capa base GeneXus del perfil de Fase 2 (Bantotal corre sobre GeneXus).

### Fase 4 — Manual de usuario y orquestación (n8n + Jira)
**Objetivo:** cerrar el ciclo y automatizar el flujo end-to-end.
- Generación de **manual de usuario** a partir de HU, flujos y capturas.
- **Orquestación con n8n**: Jira dispara el análisis, el motor genera los entregables, y se publican en Jira/Confluence/Slack. *El motor sigue siendo el "cerebro"; n8n solo orquesta y mueve datos, no contiene la lógica QA.*

*Consideraciones:* exponer el motor como **API/webhook** estable antes de conectar n8n. Los conectores de Jira/Confluence requieren autorización previa.

### Fase 5 — Calidad, trazabilidad y madurez de plataforma
**Objetivo:** sostener la calidad a escala.
- **Matriz de trazabilidad (RTM):** HU ↔ casos ↔ requisitos ↔ defectos (clave para auditorías, sobre todo en banca).
- **Harness de evaluación de prompts:** medir cobertura de los 7 escenarios y fidelidad al cambiar prompts, perfiles o modelo.
- **Procesos asíncronos** para generaciones largas y **seguimiento de costos** de IA.
- (Opcional/futuro) Generación de **tests ejecutables** (Playwright/pytest/Postman) e integración con herramientas de test management (Xray/Zephyr/TestRail).

---

## 7. Consideraciones transversales

- **Compatibilidad hacia atrás:** todo lo que hoy funciona para web debe seguir funcionando; el perfil web genérico es el comportamiento por defecto.
- **Seguridad y datos bancarios:** el perfil Bantotal trabaja sobre definiciones y estructuras, nunca sobre datos productivos de clientes. Definir política antes de la Fase 3.
- **Dependencias externas:** el MCP Bantotal y los conectores Jira/Confluence requieren autorización y validación de alcance; conviene gestionarlas en paralelo para no bloquear las fases.
- **Evaluación de calidad:** cada cambio de modelo, prompt o perfil debe medirse contra un conjunto de referencia para evitar regresiones silenciosas.
- **Esfuerzo incremental:** la sinergia GeneXus↔Bantotal hace que el perfil bancario (Fase 3) sea aditivo sobre la Fase 2, no un desarrollo desde cero.
- **Gestión del conocimiento de dominio:** los paquetes bancarios requieren input de especialistas de la rama bancaria; conviene involucrarlos temprano.

---

## 8. Próximos pasos inmediatos

1. Validar con el equipo la **decisión de extender vía perfiles** y el alcance de los tres perfiles iniciales.
2. Confirmar **qué expone el MCP Bantotal** y gestionar su autorización.
3. Definir el **formato de export de la Knowledge Base de GeneXus** disponible.
4. Priorizar y estimar **Fase 1** como primer incremento.
5. Acordar la **política de manejo de datos sensibles** para el perfil bancario.

---

## Glosario breve

- **Perfil de Dominio:** configuración enchufable que adapta el motor QA a un tipo de aplicación (web, GeneXus, Bantotal).
- **Grounding:** alimentar el análisis con el contexto real del sistema (código, modelo de datos, transacciones) en lugar de solo el texto de la HU.
- **MCP:** protocolo/conector que permite al sistema consultar de forma programática una fuente externa (aquí, el core Bantotal).
- **RTM:** matriz de trazabilidad de requisitos.
- **Los 7 escenarios de prueba:** positivo, negativo, límite/exploratorio, no funcional, compatibilidad, seguridad, regresión.
