# Propuesta de Modelos de Datos

## 🎯 Objetivo

Definir un modelo de datos robusto, escalable y orientado a objetos que soporte:
- Múltiples usuarios y proyectos
- Versionado de HUs y Test Plans
- Auditoría y trazabilidad
- Extensibilidad futura

---

## 📊 Arquitectura de Modelos Propuesta

### Nivel 1: Modelos Core (Base)

#### 1. User (Usuario)

**Propósito**: Identificar y autenticar usuarios del sistema.

```python
# models/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    QA_ANALYST = "qa_analyst"
    PROJECT_MANAGER = "project_manager"
    DEVELOPER = "developer"
    VIEWER = "viewer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.QA_ANALYST
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

**Campos**:
- `id`: Identificador único
- `email`: Email único (usuario de login)
- `full_name`: Nombre completo
- `role`: Rol en el sistema (para permisos futuros)
- `is_active`: Estado del usuario
- `created_at` / `updated_at`: Auditoría

---

#### 2. Project (Proyecto)

**Propósito**: Agrupar HUs y Test Plans por proyecto o contexto de trabajo.

```python
# models/project.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: str  # Código único del proyecto (ej: "AER25")

class ProjectCreate(ProjectBase):
    owner_id: int

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

**Campos**:
- `id`: Identificador único
- `name`: Nombre del proyecto
- `description`: Descripción opcional
- `code`: Código único (ej: "AER25")
- `owner_id`: Usuario propietario
- Timestamps de auditoría

**Relaciones**:
- `owner` → User (uno a muchos)
- `user_stories` → List[UserStory] (uno a muchos)

---

#### 3. UserStory (Historia de Usuario)

**Propósito**: Representar las HUs con toda su información estructurada.

```python
# models/user_story.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class StoryType(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    UI_UX = "ui_ux"
    API = "api"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    UNKNOWN = "unknown"

class UserStoryBase(BaseModel):
    story_id: str = Field(..., description="ID único de la HU (ej: AER25-101)")
    title: str
    description: str
    acceptance_criteria: List[str]  # Lista de criterios

class UserStoryCreate(UserStoryBase):
    project_id: int
    created_by_id: int

class UserStoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None

class UserStory(UserStoryBase):
    id: int
    project_id: int
    story_type: Optional[StoryType] = None
    created_by_id: int
    version: int = 1  # Para versionado
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserStoryVersion(BaseModel):
    """Modelo para historial de versiones"""
    id: int
    user_story_id: int
    version: int
    story_id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    created_at: datetime
    created_by_id: int
```

**Campos**:
- `id`: Identificador único interno
- `story_id`: ID de negocio (ej: "AER25-101")
- `title`: Título de la HU
- `description`: Descripción completa
- `acceptance_criteria`: Lista de criterios (estructurado, no texto plano)
- `story_type`: Tipo detectado (Backend/Frontend/UI-UX/etc.)
- `project_id`: Proyecto al que pertenece
- `created_by_id`: Usuario que creó la HU
- `version`: Número de versión (para versionado)
- Timestamps

**Mejoras vs. modelo actual**:
- ✅ Criterios de aceptación como lista estructurada (no texto)
- ✅ Tipo de historia detectado automáticamente
- ✅ Versionado incorporado
- ✅ Relación explícita con Proyecto

---

#### 4. TestPlan (Plan de Pruebas)

**Propósito**: Representar el análisis completo generado por IA.

```python
# models/test_plan.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TestPlanStatus(str, Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    ARCHIVED = "archived"

class TestCasePriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TestCaseType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BOUNDARY = "boundary"
    NON_FUNCTIONAL = "non_functional"
    COMPATIBILITY = "compatibility"
    SECURITY = "security"
    REGRESSION = "regression"

class TestCase(BaseModel):
    """Caso de prueba individual"""
    tc_id: str  # Ej: "AER25-101: TC1"
    title: str
    priority: TestCasePriority
    test_type: TestCaseType
    precondition: str
    expected_validation: str
    obtained_result: Optional[str] = None  # Para completar después
    
    class Config:
        from_attributes = True

class TestPlanBase(BaseModel):
    objective: str
    summary: str
    total_cases: int = 0
    high_priority_count: int = 0
    medium_priority_count: int = 0
    low_priority_count: int = 0
    notes: Optional[str] = None

class TestPlanCreate(BaseModel):
    user_story_id: int
    generated_by_id: int

class TestPlanUpdate(BaseModel):
    status: Optional[TestPlanStatus] = None
    notes: Optional[str] = None

class TestPlan(TestPlanBase):
    id: int
    user_story_id: int
    status: TestPlanStatus = TestPlanStatus.DRAFT
    test_cases: List[TestCase] = []
    generated_by_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

**Campos**:
- `id`: Identificador único
- `user_story_id`: HU asociada
- `objective`: Objetivo del plan
- `summary`: Resumen del análisis
- `test_cases`: Lista estructurada de casos de prueba
- `total_cases`: Conteo total
- `high_priority_count` / `medium_priority_count` / `low_priority_count`: Conteos por prioridad
- `status`: Estado del plan (borrador, generado, revisado, aprobado)
- `notes`: Notas adicionales
- `generated_by_id`: Usuario que generó el plan
- Timestamps

**Mejoras vs. modelo actual**:
- ✅ Casos de prueba estructurados (no solo tabla)
- ✅ Estado del plan (workflow)
- ✅ Tipo de caso explícito
- ✅ Metadatos de conteo

---

#### 5. AIAnalysis (Análisis de IA)

**Propósito**: Almacenar el proceso completo de análisis de IA para auditoría y mejora.

```python
# models/ai_analysis.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AnalysisStep(str, Enum):
    TRANSLATION_TO_EN = "translation_to_en"
    TEST_PLAN_GENERATION = "test_plan_generation"
    TRANSLATION_TO_ES = "translation_to_es"

class AIModel(str, Enum):
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4O = "gpt-4o"

class AIAnalysis(BaseModel):
    id: int
    test_plan_id: int
    step: AnalysisStep
    model_used: AIModel
    prompt_sent: str
    response_received: str
    tokens_used: Optional[int] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**Propósito**: 
- Auditoría completa del proceso de IA
- Análisis de costos (tokens)
- Mejora de prompts basada en historial
- Debugging de problemas

---

### Nivel 2: Modelos de Relación

#### 6. ProjectMember (Miembro de Proyecto)

**Propósito**: Relación many-to-many entre Users y Projects (permisos futuros).

```python
# models/project_member.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ProjectRole(str, Enum):
    OWNER = "owner"
    MEMBER = "member"
    VIEWER = "viewer"

class ProjectMember(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: ProjectRole
    added_at: datetime
    added_by_id: int
    
    class Config:
        from_attributes = True
```

---

### Nivel 3: Modelos de Soporte

#### 7. ExportFormat (Formato de Exportación)

**Propósito**: Metadatos sobre exportaciones realizadas.

```python
# models/export.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ExportFormat(str, Enum):
    EXCEL = "excel"
    CSV = "csv"
    JIRA = "jira"
    TESTRAIL = "testrail"
    JSON = "json"

class Export(BaseModel):
    id: int
    test_plan_id: int
    format: ExportFormat
    file_path: Optional[str] = None  # Si se guarda en disco
    file_size_bytes: Optional[int] = None
    exported_by_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

---

## 🗄️ Esquema de Base de Datos Propuesto

### ⚠️ IMPORTANTE: Infraestructura Local

**Situación**: Toda la infraestructura está en la computadora local del desarrollador.

**Recomendación**: **SQLite exclusivamente** para este contexto.

**Justificación para entorno local**:
- ✅ Sin necesidad de instalar/servir PostgreSQL
- ✅ Archivo único, fácil de respaldar
- ✅ Sin configuración de servidor
- ✅ Suficiente para uso local (soporta hasta GB de datos)
- ✅ Compatible con SQLAlchemy sin cambios
- ✅ Fácil migración futura a PostgreSQL si es necesario

### Opción A: SQLite (Recomendada para Local)

**Justificación**:
- ✅ Sin dependencias externas
- ✅ Fácil para desarrollo local
- ✅ Perfecto para un solo usuario
- ✅ Migración simple a PostgreSQL después (si es necesario)

**Consideraciones**:
- ⚠️ Solo 1 escritura simultánea (suficiente para uso local)
- ⚠️ Funciona bien hasta varios GB (más que suficiente)
- ✅ Migración a PostgreSQL es directa (mismo código SQLAlchemy)

### Opción B: PostgreSQL (Para Futuro/Escalabilidad)

**Justificación** (si en el futuro necesitas escalar):
- ✅ Robusto para producción
- ✅ Soporte completo de relaciones y constraints
- ✅ Múltiples escrituras simultáneas
- ✅ JSON fields para flexibilidad
- ✅ Escalable y maduro

**Nota**: La migración de SQLite a PostgreSQL es directa (mismo código SQLAlchemy, solo cambiar DATABASE_URL).

### Diagrama de Relaciones (Simplificado)

```
User (1) ────< (N) Project (owner_id)
User (1) ────< (N) ProjectMember ──> (N) Project
User (1) ────< (N) UserStory (created_by_id)
User (1) ────< (N) TestPlan (generated_by_id)
User (1) ────< (N) AIAnalysis
Project (1) ────< (N) UserStory (project_id)
UserStory (1) ────< (N) TestPlan (user_story_id)
TestPlan (1) ────< (N) TestCase (test_plan_id)
TestPlan (1) ────< (N) AIAnalysis (test_plan_id)
TestPlan (1) ────< (N) Export (test_plan_id)
```

---

## 📋 Migraciones Necesarias

### Migración 1: Estructura Base
1. Crear tabla `users`
2. Crear tabla `projects`
3. Crear tabla `user_stories`
4. Crear tabla `test_plans`
5. Crear tabla `test_cases` (como JSON o tabla separada según ORM)

### Migración 2: Relaciones y Auditoría
1. Agregar foreign keys
2. Agregar índices
3. Agregar timestamps

### Migración 3: Funcionalidades Avanzadas
1. Tabla `ai_analyses`
2. Tabla `exports`
3. Tabla `project_members`

---

## 🔄 Transformaciones Necesarias

### Del Modelo Actual al Nuevo

**Entrada actual (formulario)**:
```python
# Formulario HTML → FormData
{
    "hu_id": "AER25-101",
    "title": "Frontend -> Pantalla principal",
    "description": "...",
    "acceptance_criteria": "AC1\nAC2\nAC3"
}
```

**Transformación**:
```python
# En el servicio
def create_user_story_from_form(form_data, user_id, project_id):
    # Convertir acceptance_criteria de texto a lista
    ac_list = [
        line.strip() 
        for line in form_data["acceptance_criteria"].splitlines() 
        if line.strip()
    ]
    
    return UserStoryCreate(
        story_id=form_data["hu_id"],
        title=form_data["title"],
        description=form_data["description"],
        acceptance_criteria=ac_list,
        project_id=project_id,
        created_by_id=user_id
    )
```

**Salida actual (Test Plan)**:
```python
# Markdown parseado → DataFrame → Excel
```

**Nueva salida**:
```python
# Estructura de TestPlan con TestCases → Múltiples formatos
def generate_excel_from_test_plan(test_plan: TestPlan) -> bytes:
    # Usar pandas con datos estructurados
    df = pd.DataFrame([
        {
            "Prioridad": tc.priority.value,
            "ID CP": tc.tc_id,
            "Título": tc.title,
            "Precondición": tc.precondition,
            "Validación Esperada": tc.expected_validation,
            "Resultado Obtenido": tc.obtained_result or ""
        }
        for tc in test_plan.test_cases
    ])
    # ... generar Excel
```

---

## 🎯 Ventajas del Nuevo Modelo

1. **Estructuración**: Datos organizados en entidades claras
2. **Validación**: Pydantic valida tipos y formatos automáticamente
3. **Extensibilidad**: Fácil agregar campos o relaciones
4. **Auditoría**: Timestamps y creadores en todas las entidades
5. **Versionado**: Soporte para versiones de HUs
6. **Relaciones**: Claves foráneas explícitas
7. **Tipado**: Enum para valores controlados
8. **Escalabilidad**: Preparado para múltiples usuarios y proyectos

---

## 📝 Notas de Implementación

### Uso de ORM (SQLAlchemy)

Los modelos Pydantic mostrados son para **validación y serialización** (API layer). Para persistencia, se necesita:

1. **Modelos SQLAlchemy** (database layer):
```python
# db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    # ...
```

2. **Modelos Pydantic** (API layer) - Ya mostrados arriba

3. **Conversión entre ambos**:
```python
# Usar from_attributes=True en Pydantic
user = User(...)  # SQLAlchemy
user_pydantic = UserPydantic.from_orm(user)  # Conversión
```

### Campos JSON vs. Tablas Relacionadas

Para `test_cases` dentro de `TestPlan`:
- **Opción A**: Campo JSON en PostgreSQL (más simple, menos flexible)
- **Opción B**: Tabla `test_cases` separada (más normalizado, más flexible)

**Recomendación**: Tabla separada para poder hacer queries y filtros sobre casos individuales.

---

## 🔐 Consideraciones de Seguridad

1. **Passwords**: Hash con bcrypt o similar
2. **Tokens JWT**: Para autenticación de sesiones
3. **Permisos**: Basados en roles (UserRole, ProjectRole)
4. **Validación**: Pydantic valida entrada antes de guardar
5. **Sanitización**: Limpiar inputs antes de usar en prompts de IA

---

Este modelo de datos proporciona una base sólida para escalar la plataforma manteniendo la flexibilidad necesaria para futuras funcionalidades.
