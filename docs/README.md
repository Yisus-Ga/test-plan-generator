# Documentación Arquitectónica del Proyecto

## 📚 Índice de Documentos

Esta documentación está organizada en documentos especializados que cubren diferentes aspectos del proyecto. Cada documento es independiente pero se relaciona con los demás para dar una visión completa.

**⚠️ IMPORTANTE**: Toda la infraestructura está en la computadora local. Ver [Consideraciones de Infraestructura Local](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md) para recomendaciones específicas de este contexto.

---

### 0. [Consideraciones de Infraestructura Local](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md)

**Contenido**:
- Configuración optimizada para entorno local
- SQLite como base de datos principal
- Autenticación simplificada
- URLs y puertos locales
- Comandos de inicio rápido

**Cuándo leerlo**: 
- **PRIMERO** - Para entender las decisiones específicas para infraestructura local
- Antes de configurar el proyecto
- Para entender por qué ciertas decisiones fueron simplificadas

---

## 📄 Documentos Disponibles

---

### 1. [Diagnóstico del Sistema Actual](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md)

**Contenido**:
- Resumen ejecutivo del sistema actual
- Fortalezas del MVP
- Limitaciones técnicas y de diseño
- Análisis detallado del código
- Conclusiones y prioridades de mejora

**Cuándo leerlo**: 
- Para entender el estado actual del proyecto
- Antes de hacer cambios significativos
- Para identificar áreas de mejora

---

### 2. [Propuesta de Modelos de Datos](./02_PROPUESTA_MODELOS_DATOS.md)

**Contenido**:
- Arquitectura de modelos propuesta
- Modelos core (User, Project, UserStory, TestPlan)
- Modelos de relación y soporte
- Esquema de base de datos
- Migraciones necesarias

**Cuándo leerlo**:
- Al diseñar la base de datos
- Para entender la estructura de datos
- Antes de implementar persistencia

---

### 3. [Arquitectura Backend](./03_ARQUITECTURA_BACKEND.md)

**Contenido**:
- Arquitectura Clean Architecture + DDD
- Estructura de directorios
- Componentes principales (servicios, repositorios, endpoints)
- Ejemplos de código
- Tecnologías recomendadas

**Cuándo leerlo**:
- Al refactorizar el backend
- Para entender la arquitectura propuesta
- Al implementar nuevas funcionalidades
- Para guía de implementación

---

### 4. [Arquitectura Frontend y UX/UI](./04_ARQUITECTURA_FRONTEND_UX_UI.md)

**Contenido**:
- Arquitectura frontend modular
- Sistema de diseño (colores, tipografía, componentes)
- Diseño de pantallas propuesto
- Componentes reutilizables
- Mejoras de UX específicas

**Cuándo leerlo**:
- Al refactorizar el frontend
- Para diseño de interfaces
- Al implementar componentes
- Para guía de estilo y UX

---

### 5. [Propuesta MCP y APIs](./05_PROPUESTA_MCP_Y_APIS.md)

**Contenido**:
- Introducción a MCP (Model Context Protocol)
- Arquitectura híbrida (REST + MCP)
- Implementación de MCP Server
- Integración con APIs REST
- Roadmap de migración a MCP

**Cuándo leerlo**:
- Al planificar integraciones avanzadas con IA
- Para entender la evolución hacia MCP
- Al implementar capacidades MCP
- Para guía de integración MCP

---

### 6. [Roadmap de Implementación](./06_ROADMAP_IMPLEMENTACION.md)

**Contenido**:
- Fases de implementación detalladas
- Timeline y prioridades
- Tareas específicas por fase
- Criterios de éxito
- Riesgos y mitigaciones

**Cuándo leerlo**:
- Al planificar el trabajo
- Para entender el orden de implementación
- Para estimar tiempos
- Para seguimiento de progreso

---

### 7. [Escalado del Proyecto](./07_ESCALADO_PROYECTO.md)

**Contenido**:
- Estado actual vs. futuras fases
- Matriz de priorización
- Recomendaciones de orden de implementación
- Cuándo escalar infraestructura
- Indicadores de cuándo agregar funcionalidades

**Cuándo leerlo**:
- **AHORA** - Para entender próximos pasos
- Al planificar desarrollo futuro
- Para decidir qué implementar primero
- Para entender cuándo escalar infraestructura

---

### 8. [Informe MCP - Opciones y Recomendaciones](./08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md)

**Contenido**:
- Evaluación de MCP para el proyecto
- Opciones con solo API OpenAI
- Chat con contexto (implementado)
- Recomendaciones para evolución MCP

**Cuándo leerlo**:
- Al planificar integración MCP (Paso 5 del plan)
- Para entender el enfoque actual de chat con contexto

---

### 9. [Guía: Publicar en GitHub](./09_GUIA_PUBLICAR_EN_GITHUB.md)

**Contenido**:
- Paso a paso para publicar sin exponer la API Key
- Configuración de .gitignore y .env.example
- Checklist de seguridad

**Cuándo leerlo**:
- Antes de subir el proyecto a GitHub
- Para verificar que .env no se suba

---

### 10. [Estado Actual y Próximos Pasos](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) ⭐

**Contenido**:
- **Fuente de verdad** del estado actual del proyecto
- Estructura real del código (backend, frontend, BD)
- Funcionalidades implementadas
- Plan de trabajo acordado (GitHub → Tests → Plantillas → Imágenes → MCP)

**Cuándo leerlo**:
- **PRIMERO** - Para saber qué existe hoy y qué sigue
- Antes de tomar decisiones de desarrollo

---

## 🗺️ Flujo de Lectura Recomendado

### Para nuevos en el proyecto (empezar aquí)

1. **[Estado Actual y Próximos Pasos](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)** → Qué existe hoy y qué sigue
2. **[Consideraciones Infraestructura Local](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md)** → Configuración local

### Para Arquitectos/Tech Leads

1. **Estado Actual** → [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)
2. **Diagnóstico** → [01_DIAGNOSTICO](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) (contexto histórico)
3. **Roadmap** → [06_ROADMAP](./06_ROADMAP_IMPLEMENTACION.md)
4. **Modelos de Datos** → [02_PROPUESTA_MODELOS](./02_PROPUESTA_MODELOS_DATOS.md)
5. **Arquitectura Backend** → [03_ARQUITECTURA](./03_ARQUITECTURA_BACKEND.md)
6. **Arquitectura Frontend** → [04_ARQUITECTURA](./04_ARQUITECTURA_FRONTEND_UX_UI.md)
7. **MCP** → [08_INFORME_MCP](./08_INFORME_MCP_OPCIONES_Y_RECOMENDACIONES.md)

### Para Desarrolladores Backend

1. **Estado Actual** → [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)
2. **Modelos de Datos** → [02_PROPUESTA_MODELOS](./02_PROPUESTA_MODELOS_DATOS.md)
3. **Arquitectura Backend** → [03_ARQUITECTURA](./03_ARQUITECTURA_BACKEND.md)
4. **Escalado** → [07_ESCALADO](./07_ESCALADO_PROYECTO.md)

### Para Desarrolladores Frontend

1. **Estado Actual** → [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)
2. **Arquitectura Frontend** → [04_ARQUITECTURA](./04_ARQUITECTURA_FRONTEND_UX_UI.md)
3. **Modelos de Datos** → [02_PROPUESTA_MODELOS](./02_PROPUESTA_MODELOS_DATOS.md)
4. **Escalado** → [07_ESCALADO](./07_ESCALADO_PROYECTO.md)

### Para Product Managers

1. **Estado Actual** → [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)
2. **Escalado** → [07_ESCALADO](./07_ESCALADO_PROYECTO.md)
3. **Arquitectura Frontend** → [04_ARQUITECTURA](./04_ARQUITECTURA_FRONTEND_UX_UI.md)

---

## 🎯 Visión General del Proyecto

### Estado Actual (Implementado)

- **Backend**: FastAPI con Clean Architecture (servicios, repositorios, schemas)
- **Base de datos**: SQLite con SQLAlchemy + Alembic
- **Modelos**: Project, UserStory, TestPlan, TestCase
- **Frontend**: HTML/CSS/JS modular con navegación por páginas
- **Funcionalidades**: Generación de Test Plans, Proyectos, Historial, Chat con contexto
- **Exportación**: Excel, CSV, JSON, formato Jira
- **IA**: OpenAI (traducción + generación)
- **Autenticación**: Modo single-user (sin login)

Ver [Estado Actual y Próximos Pasos](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) para detalle completo.

### Próximos Pasos (Plan Acordado)

1. Publicar en GitHub (sin exponer API Key)
2. Tests automatizados (unitario, integración, E2E)
3. Plantillas de prompts
4. Imágenes en la Historia de Usuario
5. MCP Server (evolución posterior)

---

## 📋 Decisiones Arquitectónicas Clave

### 1. Backend: FastAPI + Clean Architecture

**Decisión**: Mantener FastAPI, reorganizar en capas limpias

**Justificación**:
- FastAPI es moderno y eficiente
- Clean Architecture permite escalabilidad
- Separación de capas facilita testing y mantenimiento

**Referencia**: [Arquitectura Backend](./03_ARQUITECTURA_BACKEND.md)

---

### 2. Base de Datos: SQLite (Infraestructura Local)

**Decisión**: SQLite exclusivamente (infraestructura local)

**Justificación**:
- Sin necesidad de instalar/servir PostgreSQL
- Suficiente para uso local (soporta hasta GB de datos)
- Fácil de respaldar (archivo único)
- Migración simple a PostgreSQL después si es necesario

**Referencia**: 
- [Propuesta de Modelos de Datos](./02_PROPUESTA_MODELOS_DATOS.md)
- [Consideraciones de Infraestructura Local](./00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md)

---

### 3. Frontend: Vanilla JS Modular (Corto plazo) → Framework (Largo plazo)

**Decisión**: Empezar con Vanilla JS modular, considerar framework después

**Justificación**:
- Sin dependencias pesadas inicialmente
- Fácil de entender y mantener
- Transición suave desde código actual
- Flexibilidad para migrar a React/Vue después

**Referencia**: [Arquitectura Frontend](./04_ARQUITECTURA_FRONTEND_UX_UI.md)

---

### 4. MCP: Convivencia Híbrida con APIs REST

**Decisión**: Implementar MCP gradualmente, mantener APIs REST

**Justificación**:
- MCP para integraciones avanzadas con IA
- APIs REST para compatibilidad y simplicidad
- Evolución gradual sin romper funcionalidad

**Referencia**: [Propuesta MCP y APIs](./05_PROPUESTA_MCP_Y_APIS.md)

---

## 🚀 Próximos Pasos

Ver el documento [Estado Actual y Próximos Pasos](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) como fuente de verdad. Resumen del plan acordado:

1. **Publicar en GitHub** → Sin exponer API Key (.gitignore, .env.example)
2. **Tests automatizados** → Pytest, unitarios → servicios → endpoints
3. **Plantillas de prompts** → Personalización sin tocar código
4. **Imágenes en HUs** → Capturas para que la IA considere la interfaz real
5. **MCP Server** → Evolución posterior

**Referencias**: [Guía GitHub](./09_GUIA_PUBLICAR_EN_GITHUB.md) | [Escalado](./07_ESCALADO_PROYECTO.md) | [Roadmap](./06_ROADMAP_IMPLEMENTACION.md)

---

## 📝 Notas Importantes

### Mantenimiento de Documentación

- **Actualizar** cuando haya cambios arquitectónicos significativos
- **Revisar** periódicamente para asegurar coherencia
- **Versionar** junto con el código

### Dependencias entre Documentos

- Los documentos están **interconectados** pero pueden leerse independientemente
- Hay **referencias cruzadas** para navegación fácil
- Algunos conceptos se repiten para **contexto completo** en cada documento

### Estado de la Documentación

- ✅ **Completa**: Documentos base creados
- 🔄 **En evolución**: Se actualizará con el proyecto
- 📋 **Revisión pendiente**: Validar con equipo antes de implementar

---

## 🤝 Contribución

### Cómo Usar Esta Documentación

1. **Leer** los documentos relevantes antes de empezar trabajo
2. **Consultar** cuando haya dudas de arquitectura
3. **Actualizar** cuando se implementen cambios significativos
4. **Proponer** mejoras o correcciones

### Cómo Actualizar

1. **Identificar** qué documento necesita actualización
2. **Hacer cambios** manteniendo el formato markdown
3. **Revisar** referencias cruzadas si es necesario
4. **Comunicar** cambios relevantes al equipo

---

## 📞 Contacto

Para preguntas o sugerencias sobre esta documentación:
- Revisar documentos relevantes primero
- Proponer mejoras en reuniones de arquitectura
- Documentar decisiones nuevas en documentos apropiados

---

**Última actualización**: Documentación alineada con estado actual del proyecto  
**Versión del proyecto**: v2.0 - Proyectos, Historial, Chat, Exportación múltiple  
**Estado**: Documentación actualizada - ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md)
