# Diagnóstico del Sistema Actual

> **Nota de contexto**: Este documento describe el **estado inicial del MVP** (antes de la refactorización). Muchas de las limitaciones indicadas ya fueron abordadas: el proyecto tiene persistencia (SQLite), proyectos, historial, chat, exportación múltiple y arquitectura modular. Ver [10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md](./10_ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md) para el estado actual real.

---

## 📊 Resumen Ejecutivo

El sistema actual es un **MVP funcional** que cumple su objetivo básico: analizar Historias de Usuario mediante IA y generar casos de prueba estructurados en formato Excel. Sin embargo, presenta limitaciones arquitectónicas y de diseño que deben abordarse para escalar a una plataforma productiva.

---

## ✅ Fortalezas

### 1. Funcionalidad Core Operativa
- **Pipeline de procesamiento IA funcional**: El flujo de traducción → generación → traducción funciona correctamente
- **Integración con OpenAI**: Uso correcto de la API con manejo de modelos diferenciados (gpt-4.1-mini para traducción, gpt-4.1 para generación)
- **Generación de Excel**: Implementación eficiente en memoria usando pandas y openpyxl
- **Separación de responsabilidades**: Lógica de negocio separada en funciones modulares

### 2. Decisiones Técnicas Acertadas
- **FastAPI como framework**: Moderno, asíncrono, con documentación automática
- **Markdown como formato interno**: Flexible y estándar para documentación técnica
- **Tokens temporales**: Mecanismo simple para manejo de estado sin persistencia
- **Procesamiento asíncrono**: Uso de `run_in_threadpool` para operaciones bloqueantes

### 3. UX Básica Funcional
- **Formulario intuitivo**: Campos claros (ID, Título, Descripción, Criterios)
- **Feedback visual**: Estados de carga y mensajes de error/success
- **Descarga automática**: Mejora la experiencia del usuario

---

## ❌ Limitaciones Técnicas

### 1. Arquitectura Monolítica Sin Separación de Capas

**Problema**: Todo el código está en un solo archivo (`main.py`), sin separación entre:
- Lógica de negocio
- Acceso a datos
- Presentación (API endpoints)
- Servicios externos (IA)

**Impacto**:
- Difícil de testear
- Imposible reutilizar componentes
- Escalabilidad limitada
- Mantenimiento complejo

**Evidencia**:
```12:332:main.py
# Todo mezclado: config, funciones, endpoints en el mismo archivo
```

### 2. Sin Persistencia de Datos

**Problema**: 
- Almacenamiento temporal en memoria (`results_store: dict`)
- Sin base de datos
- No hay historial de análisis
- No hay gestión de usuarios/proyectos

**Impacto**:
- Pérdida de datos al reiniciar el servidor
- Imposible auditar o revisar análisis previos
- No se puede trabajar colaborativamente
- No hay versionado de HUs o Test Plans

### 3. Sin Autenticación ni Autorización

**Problema**:
- CORS abierto (`allow_origins=["*"]`)
- Sin control de acceso
- Sin identificación de usuarios

**Impacto**:
- Inseguro para producción
- Imposible rastrear quién generó qué análisis
- No se puede personalizar experiencias por usuario
- Riesgo de abuso de recursos (API de IA)

### 4. Modelo de Datos Implícito y Frágil

**Problema**:
- No hay modelos de datos explícitos (Pydantic models)
- Parsing manual con regex frágil
- Validación mínima de entrada
- Estructura de datos acoplada al formato markdown

**Ejemplo de fragilidad**:
```177:197:main.py
def parse_markdown_table_to_df(test_plan_md_es: str) -> pd.DataFrame:
    # Busca con regex - puede fallar con variaciones de formato
    if re.match(r"\| *Prioridad *\|", line, re.IGNORECASE):
```

**Impacto**:
- Errores silenciosos si el formato cambia
- Difícil validar calidad de datos
- Imposible hacer queries estructuradas

### 5. Frontend Básico sin Framework

**Problema**:
- JavaScript vanilla sin organización
- Sin gestión de estado
- Sin componentes reutilizables
- CSS básico sin diseño system
- Hardcodeado `BASE_URL = "http://127.0.0.1:8000"`

**Evidencia**:
```63:293:static/index.html
// Todo el JS inline en el HTML, sin modularización
```

**Impacto**:
- Difícil agregar nuevas funcionalidades
- No hay reutilización de componentes
- Mantenimiento costoso
- UX limitada

### 6. Manejo de Errores Débil

**Problema**:
- Errores genéricos sin contexto
- Sin logging estructurado
- Sin manejo de timeouts en llamadas a IA
- Errores de parsing silenciosos

**Impacto**:
- Debugging difícil
- Usuario ve mensajes poco útiles
- No se puede monitorear problemas en producción

### 7. Sin Tests

**Problema**:
- No hay tests unitarios
- No hay tests de integración
- No hay tests end-to-end

**Impacto**:
- Refactoring riesgoso
- Regresiones no detectadas
- Calidad de código no verificable

### 8. Flujo de Archivo en Desuso

**Problema**:
- Se mantiene código para subir archivos `.txt/.md` pero está en desuso
- Código muerto aumenta complejidad

**Evidencia**:
```26:28:static/index.html
<label for="fileInput">Subir archivo (.md / .txt)</label>
<input type="file" id="fileInput" accept=".md,.txt" />
```

---

## ⚠️ Limitaciones de Diseño

### 1. Flujo de Usuario Lineal

**Problema**:
- Solo permite: Cargar → Analizar → Descargar
- No se puede editar una HU después de analizar
- No se pueden comparar análisis
- No se puede iterar sobre el mismo análisis

### 2. Sin Gestión de Proyectos o Contexto

**Problema**:
- Cada análisis es independiente
- No se puede agrupar HUs por proyecto
- No hay contexto compartido entre análisis
- Imposible generar test plans consolidados

### 3. Output Limitado

**Problema**:
- Solo genera Excel
- No hay exportación a otros formatos (Jira, TestRail, CSV, etc.)
- No se puede personalizar el formato del Test Plan

### 4. Sin Personalización de Prompts

**Problema**:
- Prompts hardcodeados
- No se puede ajustar el estilo o profundidad del análisis
- No hay templates configurables

### 5. Sin Feedback Loop

**Problema**:
- No se puede calificar la calidad del análisis
- No hay mecanismo para mejorar prompts basado en feedback
- No hay aprendizaje del sistema

---

## 🔍 Análisis de Código Específico

### Backend: main.py

#### Fortalezas
- Funciones bien nombradas y con propósito único
- Uso correcto de async/await
- Manejo de archivos en memoria (eficiente)

#### Debilidades

**1. Configuración mezclada con lógica:**
```15:27:main.py
# Config mezclado con aplicación
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()
# ...
```

**2. Prompts hardcodeados:**
```55:64:main.py
def traducir_hu(hu_es: str) -> str:
    prompt = f"""..."""
    # El prompt está dentro de la función
```

**3. Parsing frágil:**
```177:197:main.py
# Regex matching que puede fallar con variaciones
def parse_markdown_table_to_df(test_plan_md_es: str) -> pd.DataFrame:
```

**4. Almacenamiento global:**
```28:30:main.py
# Variable global - no escalable
results_store: dict = {}
```

### Frontend: index.html

#### Fortalezas
- Código funcional y legible
- Manejo básico de estados de UI
- Feedback visual adecuado

#### Debilidades

**1. JavaScript inline:**
```63:293:static/index.html
// Todo el código JS en el HTML
```

**2. Sin gestión de estado:**
- Variables globales (`currentToken`, `currentFilename`)
- Estado distribuido entre funciones

**3. Hardcodeo de URLs:**
```85:85:static/index.html
const BASE_URL = "http://127.0.0.1:8000";
```

**4. Sin validación del lado del cliente:**
- Validación solo de "campos completos"
- No valida formato de ID, longitud de campos, etc.

---

## 📈 Métricas de Complejidad

- **Líneas de código backend**: ~332 (en un solo archivo)
- **Líneas de código frontend**: ~297 (HTML + JS inline)
- **Funciones backend**: 7 funciones
- **Endpoints API**: 3 endpoints
- **Dependencias externas**: FastAPI, OpenAI, pandas, openpyxl
- **Cobertura de tests**: 0%
- **Documentación**: Solo comentarios inline

---

## 🎯 Conclusiones del Diagnóstico

### Estado Actual
El sistema es un **MVP funcional** que cumple su objetivo básico, pero presenta limitaciones arquitectónicas significativas que impiden su escalabilidad y uso en producción.

### Principales Riesgos
1. **Técnico**: Arquitectura monolítica difícil de mantener y escalar
2. **Funcional**: Falta de persistencia y gestión de datos limita las capacidades
3. **Seguridad**: Sin autenticación/autorización, no es seguro para producción
4. **Experiencia**: Flujo limitado y sin personalización reduce utilidad
5. **Calidad**: Sin tests, riesgo alto de regresiones

### Prioridades de Mejora
1. **Corto plazo**: Separar capas, agregar modelos de datos, eliminar código muerto
2. **Mediano plazo**: Persistencia, autenticación, tests, mejor UX
3. **Largo plazo**: MCP, múltiples formatos de salida, colaboración, personalización

---

## 📝 Referencias al Código

- Backend principal: `main.py` (332 líneas)
- Frontend principal: `static/index.html` (297 líneas)
- Estilos: `static/style.css` (119 líneas)
- Sin base de datos
- Sin archivos de configuración estructurados (solo `.env`)
