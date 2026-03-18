# Escalado del Proyecto - Roadmap Futuro

> **Referencia actual**: Ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) para el plan de trabajo acordado (GitHub → Tests → Plantillas → Imágenes → MCP).

---

## 🎯 Estado Actual del Proyecto

### ✅ Completado

**Fase 1: Fundamentos**
- ✅ Estructura de capas (Clean Architecture)
- ✅ Configuración centralizada
- ✅ Modelos de datos (Pydantic + SQLAlchemy)
- ✅ Manejo de errores estructurado
- ✅ Código muerto eliminado

**Fase 2: Persistencia y Base de Datos**
- ✅ SQLite configurado
- ✅ Modelos SQLAlchemy ORM
- ✅ Migraciones con Alembic
- ✅ Repositorios implementados
- ✅ Almacenamiento migrado a DB

**Fase 3: Mejoras de UX y Frontend**
- ✅ Frontend modularizado (ES6 modules)
- ✅ Sistema de diseño (CSS variables)
- ✅ Validaciones en tiempo real
- ✅ Componentes reutilizables

**Fase 4: Funcionalidades Core (completada)**
- ✅ **4.1 Gestión de Proyectos** — Proyectos con CRUD, selector en formulario
- ✅ **4.2 Historial de Test Plans** — Listado, filtros, eliminación, vista detallada
- ✅ **4.3 Múltiples formatos de exportación** — Excel, CSV, JSON, formato Jira
- ✅ **Chat con contexto** — Modal de chat sobre proyecto + HU + test plan (generador e historial)

---

## 🚀 Próximas Fases de Escalado

> **Plan acordado**: GitHub → Tests → Plantillas → Imágenes → MCP. Ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md).

### Próximas Fases (Plan Acordado)

Ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) para el detalle. Resumen:

#### Paso 1: Publicar en GitHub ✅ Preparado
- `.gitignore` y `.env.example` configurados
- Guía en [09_GUIA_PUBLICAR_EN_GITHUB.md](./09_GUIA_PUBLICAR_EN_GITHUB.md)

#### Paso 2: Tests automatizados (3 semanas)
- Semana 1: pytest, tests de utilidades
- Semana 2: tests de servicios con mocks
- Semana 3: tests de endpoints con BD en memoria

#### Paso 3: Plantillas de prompts
- Personalización sin tocar código
- Enfoque inicial: archivos de plantillas

#### Paso 4: Imágenes en HUs
- Capturas para que la IA considere la interfaz real
- URL o subida local

#### Paso 5: MCP Server
- Evolución posterior

---

### Fases ya implementadas (referencia)

Las secciones siguientes describen funcionalidades **ya implementadas** o planes de **largo plazo**. Para el plan actual, ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md).

#### 4.3 Mejoras en Exportación ✅ Implementado

**Objetivo**: Agregar múltiples formatos de exportación.

**Implementado**: Excel, CSV, JSON, formato Jira. TestRail pendiente si se requiere.

**Formatos descritos originalmente**:
1. **CSV** - Para Excel básico o importación genérica
2. **JSON** - Para integración con otras herramientas
3. **Jira** - Formato para importar directamente a Jira
4. **TestRail** - Formato para importar a TestRail

**Implementación**:
- Crear servicios de exportación por formato
- Agregar selector de formato en frontend
- Generar archivos según formato seleccionado

**Valor agregado**:
- Integración con herramientas de QA existentes
- Mayor flexibilidad
- Mejor interoperabilidad

**Impacto**: Medio - Valor agregado importante

---

### Fase 5: Funcionalidades Avanzadas (Prioridad Media)

#### 5.1 Edición y Actualización de HUs (Semana 1-2)

**Objetivo**: Permitir editar HUs existentes y regenerar Test Plans.

**Implementación**:
- Endpoint para actualizar HUs
- Frontend: Formulario de edición
- Regenerar Test Plans desde HUs actualizadas
- Versionado de HUs (ya implementado en modelo)

**Valor agregado**:
- Flexibilidad para corregir errores
- Mejor iteración sobre análisis

**Impacto**: Medio - Mejora workflow

---

#### 5.2 Comparación de Test Plans (Semana 2-3)

**Objetivo**: Comparar diferentes versiones de Test Plans.

**Implementación**:
- Endpoint para comparar dos Test Plans
- Algoritmo de diferencia (casos agregados/eliminados/modificados)
- Frontend: Vista de comparación side-by-side

**Valor agregado**:
- Ver cambios entre versiones
- Tracking de evolución

**Impacto**: Bajo - Nice to have

---

#### 5.3 Plantillas y Configuración de Prompts (Semana 3-4)

**Objetivo**: Permitir personalizar prompts de IA.

**Implementación**:
- Modelo `PromptTemplate` en base de datos
- UI para editar templates
- Guardar templates como favoritos
- Selector de template al generar Test Plan

**Valor agregado**:
- Personalización según necesidades
- Mejor control sobre resultados de IA

**Impacto**: Medio - Mayor control sobre generación

---

### Fase 6: MCP y APIs Avanzadas (Prioridad Media-Baja)

#### 6.1 Implementación MCP Server (Mes 1-2)

**Objetivo**: Integrar Model Context Protocol para mejor integración con IA.

**Implementación**:
- Crear servidor MCP integrado
- Implementar tools básicos:
  - `generate_test_plan`
  - `analyze_user_story`
  - `translate_content`
- Migrar servicios de IA a usar MCP
- Mantener compatibilidad con APIs REST

**Valor agregado**:
- Mejor integración con modelos de IA
- Contexto persistente
- Capacidades más avanzadas

**Impacto**: Medio - Preparación para futuro

---

#### 6.2 API REST Pública (Semana 2-3)

**Objetivo**: Documentar y exponer APIs para integraciones externas.

**Implementación**:
- Mejorar documentación OpenAPI/Swagger
- Agregar autenticación API Key (opcional)
- Endpoints adicionales:
  - `GET /api/v1/user-stories`
  - `GET /api/v1/test-plans`
  - `POST /api/v1/projects`

**Valor agregado**:
- Integración con herramientas externas
- Automatización de workflows
- API-first approach

**Impacto**: Bajo - Si no hay necesidad inmediata

---

### Fase 7: Optimizaciones y Performance (Prioridad Baja)

#### 7.1 Caché de Resultados de IA (Semana 1-2)

**Objetivo**: Evitar regenerar Test Plans para HUs similares.

**Implementación**:
- Algoritmo de similitud de HUs (hash, embedding, etc.)
- Buscar Test Plans similares antes de generar
- Ofrecer reutilizar o regenerar

**Valor agregado**:
- Ahorro de costos de API de IA
- Respuestas más rápidas

**Impacto**: Medio - Si hay mucho uso repetitivo

---

#### 7.2 Optimización de Queries (Semana 2)

**Objetivo**: Mejorar performance de consultas a base de datos.

**Implementación**:
- Agregar índices adicionales
- Optimizar queries N+1
- Implementar paginación eficiente
- Caché de resultados frecuentes

**Valor agregado**:
- Respuestas más rápidas
- Mejor escalabilidad

**Impacto**: Bajo - SQLite es rápido para uso local

---

#### 7.3 Background Jobs (Semana 3-4)

**Objetivo**: Procesar generación de Test Plans en background.

**Implementación**:
- Sistema de colas (Celery o similar)
- Jobs asíncronos para generación
- Notificaciones cuando esté listo

**Valor agregado**:
- No bloquear interfaz durante generación
- Mejor experiencia de usuario

**Impacto**: Bajo - Solo si hay muchos usuarios simultáneos

---

## 📊 Matriz de Priorización

| Fase | Prioridad | Impacto | Esfuerzo | Valor |
|------|-----------|---------|----------|-------|
| **4.1 Gestión de Proyectos** | 🔴 Alta | Alto | Medio | Alto |
| **4.2 Historial de Test Plans** | 🔴 Alta | Alto | Medio | Alto |
| **4.3 Múltiples Formatos** | 🟡 Media | Medio | Bajo | Alto |
| **5.1 Edición de HUs** | 🟡 Media | Medio | Medio | Medio |
| **5.3 Plantillas de Prompts** | 🟡 Media | Medio | Alto | Medio |
| **6.1 MCP Server** | 🟡 Media | Medio | Alto | Medio |
| **7.1 Caché de IA** | 🟢 Baja | Medio | Alto | Medio |
| **5.2 Comparación** | 🟢 Baja | Bajo | Alto | Bajo |

---

## 🎯 Recomendación de Orden de Implementación

### Corto Plazo (Próximas 4-6 semanas)

1. **Fase 4.2: Historial de Test Plans** (2 semanas)
   - Esencial para uso real
   - Permite consultar trabajos previos
   - Base para otras funcionalidades

2. **Fase 4.1: Gestión de Proyectos** (2 semanas)
   - Organización fundamental
   - Mejora significativa la utilidad

3. **Fase 4.3: Múltiples Formatos** (2 semanas)
   - Alto valor con esfuerzo relativamente bajo
   - Mejora integración con herramientas existentes

---

### Mediano Plazo (Semanas 7-12)

4. **Fase 5.1: Edición de HUs** (2 semanas)
   - Mejora workflow significativamente

5. **Fase 5.3: Plantillas de Prompts** (2 semanas)
   - Mayor control sobre generación

6. **Fase 6.1: MCP Server** (4 semanas)
   - Preparación para futuro
   - Mejor integración con IA

---

### Largo Plazo (Semanas 13+)

7. **Fase 7.1: Caché de IA** (2 semanas)
   - Solo si hay uso intensivo repetitivo

8. **Fase 5.2: Comparación de Test Plans** (2 semanas)
   - Nice to have

9. **Fase 7.2-7.3: Optimizaciones** (4 semanas)
   - Solo si hay problemas de performance

---

## 🔄 Consideraciones de Escalado

### Escalado Horizontal vs. Vertical

**Situación actual**: Uso local, un solo usuario

**Futuro próximo**: 
- **Vertical**: Optimizar para manejar más datos (miles de HUs/Test Plans)
  - ✅ SQLite soporta bien hasta varios GB
  - ✅ Suficiente para uso individual o pequeño equipo

**Si necesitas escalar horizontalmente** (múltiples usuarios simultáneos):
- **Migrar a PostgreSQL** (misma estructura, solo cambiar DATABASE_URL)
- Agregar autenticación completa
- Implementar background jobs
- Load balancing (si es necesario)

---

### Migración de SQLite a PostgreSQL

**Cuándo considerar**:
- Más de 5-10 usuarios simultáneos
- Más de 100,000 registros
- Necesidad de conexiones concurrentes múltiples

**Cómo migrar**:
1. Cambiar `DATABASE_URL` en `.env`
2. Ejecutar `alembic upgrade head`
3. ¡Listo! (el mismo código SQLAlchemy funciona)

---

### Arquitectura para Escalado

**Actual**:
```
Frontend (HTML/JS) → Backend (FastAPI) → SQLite
```

**Escalado sugerido** (si crece mucho):
```
Frontend (React/Vue) → Backend (FastAPI) → PostgreSQL → Redis (caché)
                                         ↓
                                    MCP Server
```

**Cuándo migrar a framework frontend**:
- Necesitas más de 5-10 páginas
- Necesitas estado complejo compartido
- Necesitas routing avanzado
- El código vanilla JS se vuelve difícil de mantener

**Recomendación**: Mantener vanilla JS modular hasta que realmente lo necesites.

---

## 📋 Checklist de Preparación para Escalado

### Infraestructura

- [ ] Monitoreo básico (logs estructurados ✅)
- [ ] Backup de base de datos (automático)
- [ ] Configuración de entorno (producción vs. desarrollo)
- [ ] Manejo de secretos (variables de entorno ✅)

### Código

- [ ] Tests automatizados (pendiente - Fase 8)
- [ ] Documentación de APIs (Swagger/OpenAPI)
- [ ] Versionado de API (`/api/v1/` ✅)
- [ ] Manejo de errores robusto (✅)

### Funcionalidades

- [ ] Autenticación (opcional - modo single-user actual)
- [ ] Permisos y roles (si se necesita colaboración)
- [ ] Rate limiting (si se expone públicamente)
- [ ] Validación de entrada (✅)

---

## 🎯 Recomendación Estratégica

### Para Uso Individual/Pequeño Equipo

**Priorizar**:
1. ✅ Historial de Test Plans (esencial)
2. ✅ Gestión de Proyectos (organización)
3. ✅ Múltiples formatos de exportación (integración)

**Postergar**:
- MCP Server (hasta que realmente lo necesites)
- Optimizaciones avanzadas (SQLite es suficiente)
- Background jobs (no necesario con un usuario)

---

### Para Uso Empresarial/Múltiples Usuarios

**Además de lo anterior, considerar**:
1. Migración a PostgreSQL
2. Autenticación completa
3. Gestión de permisos
4. Monitoreo y logging avanzado
5. Backup automático
6. CI/CD básico

---

## 🔍 Indicadores de Cuándo Escalar

### Escalar Infraestructura

- **De SQLite a PostgreSQL**: 
  - Más de 3-5 usuarios simultáneos
  - Más de 10,000 registros
  - Necesitas replicación/backup avanzado

- **Agregar Redis/Caché**:
  - Más de 100 requests/minuto
  - Consultas repetitivas frecuentes
  - Necesitas sesiones compartidas

- **Background Jobs**:
  - Generaciones que tardan >30 segundos
  - Múltiples usuarios generando simultáneamente
  - Necesitas cola de procesamiento

---

### Escalar Funcionalidades

**Agregar gestión de proyectos**: Cuando tengas >20 HUs sin organización clara

**Agregar historial/consulta**: Inmediatamente - esencial para uso real

**Múltiples formatos**: Cuando necesites integrar con herramientas específicas

**Edición de HUs**: Cuando necesites corregir errores frecuentemente

**MCP Server**: Cuando quieras integración avanzada con IA o herramientas externas

---

## 📈 Roadmap Visual Simplificado

```
Ahora (Completado)
├── Fase 1: Fundamentos ✅
├── Fase 2: Persistencia ✅
└── Fase 3: Frontend ✅

Próximos 4-6 semanas (Prioridad Alta)
├── Historial de Test Plans
├── Gestión de Proyectos
└── Múltiples Formatos

Próximos 2-3 meses (Prioridad Media)
├── Edición de HUs
├── Plantillas de Prompts
└── MCP Server

Futuro (Prioridad Baja)
├── Optimizaciones
├── Background Jobs
└── Comparación de Test Plans
```

---

## 🎯 Conclusión y Recomendación

### Próximos Pasos Inmediatos

**Recomendación**: Enfocarse en **Fase 4** completa:

1. **Historial de Test Plans** (2 semanas) - Esencial
2. **Gestión de Proyectos** (2 semanas) - Organización fundamental
3. **Múltiples Formatos** (2 semanas) - Alto valor

**Total**: ~6 semanas para tener una plataforma completa y funcional

### Después

Evaluar según uso real:
- Si necesitas editar HUs frecuentemente → Fase 5.1
- Si necesitas personalizar prompts → Fase 5.3
- Si necesitas integración avanzada → Fase 6.1

### Escalado Infraestructura

**Mantener SQLite** hasta que realmente necesites PostgreSQL (múltiples usuarios simultáneos o >50k registros).

**No agregar complejidad innecesaria** - El sistema actual es sólido y escalable para uso local/pequeño equipo.

---

Este roadmap te da una hoja de ruta clara para escalar el proyecto de manera incremental, priorizando funcionalidades de alto valor y evitando sobre-ingeniería innecesaria.
