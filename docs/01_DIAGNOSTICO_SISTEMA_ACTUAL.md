# 01 · Punto de Partida y Visión de Perfiles de Dominio

> **Objetivo del documento:** describir qué hace hoy el sistema (estado real) y explicar la dirección estratégica acordada: evolucionar hacia **perfiles de dominio** para cubrir distintos tipos de aplicaciones (web/GeneXus, core bancario/Bantotal) sin duplicar el sistema.
>
> Resumen ejecutivo para compartir con el equipo/negocio: [`../PROPUESTA_PERFILES_DOMINIO.md`](../PROPUESTA_PERFILES_DOMINIO.md).

---

## 1. Qué es el sistema hoy

**Test Plan Generator** es una plataforma que toma una **Historia de Usuario (HU)**, la analiza con IA y produce documentación de QA estructurada:

- **Resumen/análisis** de la HU.
- **Plan de pruebas** priorizado (Alta / Media / Baja).
- **Casos de prueba** cubriendo los **7 escenarios**: positivo, negativo, límite/exploratorio, no funcional, compatibilidad, seguridad, regresión.
- **Exportación** a Excel, CSV, Jira y JSON.

Todo bajo el marco de normas **ISO/IEC 25010**, **ISO/IEC/IEEE 29119** e **ISTQB**, que se inyectan en el prompt desde `app/core/standards.py`.

### Estado real de la implementación

Ya está construido y operativo (a diferencia de lo que decían versiones viejas de esta documentación, la refactorización a arquitectura limpia **ya se completó**):

- **Backend:** FastAPI con arquitectura por capas (dominio, repositorios, servicios, API). Ver [03](./03_ARQUITECTURA_BACKEND.md).
- **Persistencia:** SQLite + SQLAlchemy + Alembic. Modelos: Project, UserStory, TestPlan, TestCase. Ver [02](./02_PROPUESTA_MODELOS_DATOS.md).
- **Gestión por Proyecto:** con estado activo/inactivo.
- **Frontend:** SPA en JS vanilla modular (router, páginas, componentes). Ver [04](./04_ARQUITECTURA_FRONTEND_UX_UI.md).
- **Funcionalidades adicionales:** chat con contexto sobre la HU/Test Plan, y generación de reportes de bug (bajo ISO 25010).
- **Tests:** unitarios y de integración con pytest.

### Pipeline de IA actual (y su punto débil)

Hoy la generación sigue tres pasos (`app/services/ai_service.py`): **traduce la HU al inglés → genera el test plan en inglés → traduce el resultado al español**. Este ida y vuelta agrega latencia, costo y pérdida de fidelidad. Repensarlo (generar directamente en español y sumar un segundo proveedor de IA) es parte del roadmap — ver [06](./06_ROADMAP_IMPLEMENTACION.md), Fase 1.

## 2. La limitación central

El conocimiento QA, la ponderación de escenarios y la fuente de contexto están pensados para **un solo tipo de aplicación**. El sistema no distingue si lo que se prueba es:

- un **sistema web** (por ejemplo hecho en **GeneXus** u otra tecnología), o
- una **transacción crítica del core bancario** que corre sobre **Bantotal**,

cuando en realidad cada mundo tiene reglas, riesgos y normativa muy distintos. Además, el análisis parte solo del **texto** de la HU, sin "aterrizar" en el sistema real (código, modelo de datos, transacciones).

## 3. La decisión: extender vía perfiles (no migrar ni bifurcar)

Se mantiene **un único motor de QA** (roles de IA, 7 escenarios, normas ISO/ISTQB, exportación) y se le agregan **Perfiles de Dominio enchufables**.

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

Un **Perfil** ajusta cuatro cosas (detalle técnico en [03](./03_ARQUITECTURA_BACKEND.md)):

| Pieza | Qué define |
|---|---|
| **Adaptador de entrada** | De dónde sale el artefacto a testear (HU en texto, export de KB de GeneXus, transacciones vía MCP Bantotal). |
| **Paquete de conocimiento** | Normativa y reglas de dominio inyectadas al análisis, por encima de la base ISO/ISTQB. |
| **Perfil de escenarios** | Ponderación de los 7 escenarios y de las prioridades según el dominio. |
| **Salida / conector** | Formato y destino de los entregables (Excel, Jira, herramienta de test management, matriz de trazabilidad). |

### Palanca clave que reduce el esfuerzo

**Bantotal está desarrollado sobre GeneXus.** Por eso el perfil bancario **reutiliza la capa base del perfil GeneXus** y solo suma encima el paquete de dominio bancario: el segundo perfil es incremental, no un desarrollo desde cero.

## 4. Perfiles iniciales objetivo

| Perfil | Grounding (contexto real) | Énfasis de conocimiento | Escenarios que más pesan |
|---|---|---|---|
| **Web genérico** | HU en texto | ISO/ISTQB base | Funcional, compatibilidad, UX |
| **GeneXus** | Export de la Knowledge Base (transacciones, atributos, reglas, Web Panels) | Patrones GeneXus, integridad referencial | Validación de transacciones, integridad, compatibilidad del web generado |
| **Bantotal** | Transacciones y modelo de datos reales vía **MCP Bantotal** | Contabilidad (cuadre), integridad transaccional, concurrencia, batch/cierre, conciliación, segregación de funciones, no repudio, PCI-DSS, AML, normativa del regulador | Seguridad, integridad de datos, regresión, negativo (habitualmente Alta) |

## 5. Fortalezas a preservar

- Motor de generación probado y con normas ISO/ISTQB ya integradas.
- Arquitectura por capas que **ya admite** la extensión por perfiles sin reescrituras (ver [03](./03_ARQUITECTURA_BACKEND.md)).
- Exportación múltiple con formato amigable.
- Cobertura de tests como red de seguridad para refactors.

## 6. Próximos pasos

El plan de implementación por fases está en el [Roadmap (06)](./06_ROADMAP_IMPLEMENTACION.md). El primer incremento (Fase 1) sienta la base de perfiles y moderniza el motor de IA sin romper el comportamiento actual para web.
