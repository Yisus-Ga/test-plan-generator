# Arquitectura Backend Propuesta

## 🎯 Objetivo

Definir una arquitectura backend escalable, mantenible y preparada para producción, siguiendo principios SOLID y separación de responsabilidades.

---

## 🏗️ Arquitectura Propuesta: Clean Architecture + DDD

### Estructura de Directorios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── config.py               # Configuración centralizada
│   │
│   ├── api/                    # Capa de presentación (API endpoints)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── projects.py
│   │   │   │   ├── user_stories.py
│   │   │   │   ├── test_plans.py
│   │   │   │   └── exports.py
│   │   │   └── router.py       # Agrupa todos los routers
│   │   └── dependencies.py     # Dependencies de FastAPI (auth, etc.)
│   │
│   ├── core/                   # Configuración core (security, exceptions)
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, password hashing
│   │   ├── exceptions.py       # Excepciones customizadas
│   │   └── logging.py          # Configuración de logging
│   │
│   ├── domain/                 # Capa de dominio (entidades de negocio)
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── user_story.py
│   │   │   └── test_plan.py
│   │   └── value_objects/
│   │       ├── story_type.py
│   │       └── test_case_priority.py
│   │
│   ├── services/               # Lógica de negocio (use cases)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_story_service.py
│   │   ├── test_plan_service.py
│   │   ├── ai_service.py       # Integración con OpenAI
│   │   └── export_service.py   # Generación de Excel, CSV, etc.
│   │
│   ├── repositories/           # Capa de acceso a datos (abstracción)
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   ├── user_repository.py
│   │   │   ├── project_repository.py
│   │   │   ├── user_story_repository.py
│   │   │   └── test_plan_repository.py
│   │   └── sqlalchemy/
│   │       ├── __init__.py
│   │       ├── user_repository.py
│   │       ├── project_repository.py
│   │       ├── user_story_repository.py
│   │       └── test_plan_repository.py
│   │
│   ├── db/                     # Configuración de base de datos
│   │   ├── __init__.py
│   │   ├── base.py            # Base class SQLAlchemy
│   │   ├── session.py         # Session factory
│   │   └── models.py          # Modelos SQLAlchemy ORM
│   │
│   ├── schemas/                # Pydantic schemas (DTOs)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── user_story.py
│   │   ├── test_plan.py
│   │   └── common.py
│   │
│   └── utils/                  # Utilidades
│       ├── __init__.py
│       ├── markdown_parser.py
│       ├── excel_generator.py
│       └── validators.py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── alembic/                    # Migraciones de DB
│   ├── versions/
│   └── env.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Componentes Principales

### 1. Configuración Centralizada (`app/config.py`)

**Propósito**: Centralizar todas las configuraciones del sistema.

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Test Plan Generator"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # Database - SQLite para entorno local
    # Nota: Si en el futuro necesitas PostgreSQL, solo cambiar esta URL
    DATABASE_URL: str = "sqlite:///./test_plan_generator.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_TRANSLATION: str = "gpt-4.1-mini"
    OPENAI_MODEL_GENERATION: str = "gpt-4.1"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # File Storage (opcional para exports)
    EXPORT_STORAGE_PATH: str = "./exports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**Ventajas**:
- ✅ Validación automática de variables de entorno
- ✅ Type hints para IDE
- ✅ Valores por defecto
- ✅ Fácil testing (mock de settings)

---

### 2. Capa de Dominio (`app/domain/`)

**Propósito**: Entidades de negocio puras, sin dependencias de infraestructura.

```python
# app/domain/entities/user_story.py
from dataclasses import dataclass
from datetime import datetime
from typing import List
from app.domain.value_objects.story_type import StoryType

@dataclass
class UserStory:
    """Entidad de dominio pura (sin ORM)"""
    id: int
    story_id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    story_type: StoryType
    project_id: int
    created_by_id: int
    version: int = 1
    created_at: datetime = None
    updated_at: datetime = None
    
    def is_valid(self) -> bool:
        """Validación de reglas de negocio"""
        return (
            bool(self.story_id.strip()) and
            bool(self.title.strip()) and
            bool(self.description.strip()) and
            len(self.acceptance_criteria) > 0
        )
    
    def detect_type(self) -> StoryType:
        """Lógica de detección de tipo (regla de negocio)"""
        content = f"{self.title} {self.description}".lower()
        if any(word in content for word in ["backend", "endpoint", "api", "database"]):
            return StoryType.BACKEND
        elif any(word in content for word in ["frontend", "view", "component"]):
            return StoryType.FRONTEND
        elif any(word in content for word in ["design", "ui/ux", "interface"]):
            return StoryType.UI_UX
        return StoryType.UNKNOWN
```

**Ventajas**:
- ✅ Independiente de frameworks
- ✅ Fácil de testear
- ✅ Lógica de negocio clara

---

### 3. Servicios de Negocio (`app/services/`)

**Propósito**: Orquestar la lógica de negocio y casos de uso.

#### Ejemplo: TestPlanService

```python
# app/services/test_plan_service.py
from typing import Optional
from app.domain.entities.user_story import UserStory
from app.domain.entities.test_plan import TestPlan
from app.repositories.interfaces.test_plan_repository import TestPlanRepository
from app.repositories.interfaces.user_story_repository import UserStoryRepository
from app.services.ai_service import AIService
from app.services.export_service import ExportService

class TestPlanService:
    def __init__(
        self,
        test_plan_repo: TestPlanRepository,
        user_story_repo: UserStoryRepository,
        ai_service: AIService,
        export_service: ExportService
    ):
        self.test_plan_repo = test_plan_repo
        self.user_story_repo = user_story_repo
        self.ai_service = ai_service
        self.export_service = export_service
    
    async def generate_test_plan(
        self,
        user_story_id: int,
        user_id: int
    ) -> TestPlan:
        """
        Caso de uso principal: Generar Test Plan desde una HU.
        
        Flujo:
        1. Obtener HU
        2. Generar Test Plan con IA
        3. Guardar Test Plan
        4. Retornar resultado
        """
        # 1. Obtener HU
        user_story = await self.user_story_repo.get_by_id(user_story_id)
        if not user_story:
            raise ValueError(f"User Story {user_story_id} not found")
        
        # 2. Generar con IA (orquestación del proceso completo)
        test_plan = await self.ai_service.generate_test_plan_from_story(
            user_story=user_story,
            generated_by_id=user_id
        )
        
        # 3. Guardar
        saved_test_plan = await self.test_plan_repo.create(test_plan)
        
        return saved_test_plan
    
    async def export_test_plan(
        self,
        test_plan_id: int,
        format: str,
        user_id: int
    ) -> bytes:
        """Exportar Test Plan en el formato solicitado"""
        test_plan = await self.test_plan_repo.get_by_id(test_plan_id)
        if not test_plan:
            raise ValueError(f"Test Plan {test_plan_id} not found")
        
        return await self.export_service.export(
            test_plan=test_plan,
            format=format,
            exported_by_id=user_id
        )
```

---

### 4. Servicio de IA (`app/services/ai_service.py`)

**Propósito**: Encapsular toda la lógica de interacción con OpenAI.

```python
# app/services/ai_service.py
from openai import OpenAI
from typing import List
from app.config import settings
from app.domain.entities.user_story import UserStory
from app.domain.entities.test_plan import TestPlan
from app.repositories.interfaces.ai_analysis_repository import AIAnalysisRepository
from app.core.logging import get_logger

logger = get_logger(__name__)

class AIService:
    def __init__(
        self,
        client: OpenAI,
        ai_analysis_repo: AIAnalysisRepository
    ):
        self.client = client
        self.ai_analysis_repo = ai_analysis_repo
        self.prompt_templates = self._load_prompt_templates()
    
    def _load_prompt_templates(self) -> dict:
        """Cargar templates de prompts desde archivos o configuración"""
        return {
            "translate_to_en": self._get_translation_prompt(),
            "generate_test_plan": self._get_test_plan_prompt(),
            "translate_to_es": self._get_translation_prompt_es()
        }
    
    async def generate_test_plan_from_story(
        self,
        user_story: UserStory,
        generated_by_id: int
    ) -> TestPlan:
        """
        Proceso completo de generación de Test Plan.
        
        Pasos:
        1. Traducir HU al inglés
        2. Generar Test Plan en inglés
        3. Traducir Test Plan al español
        4. Parsear resultado a estructura TestPlan
        """
        import time
        
        # 1. Traducir al inglés
        start_time = time.time()
        hu_en_md = await self._translate_to_english(user_story)
        step1_time = int((time.time() - start_time) * 1000)
        
        # 2. Generar Test Plan
        start_time = time.time()
        test_plan_en = await self._generate_test_plan(hu_en_md)
        step2_time = int((time.time() - start_time) * 1000)
        
        # 3. Traducir al español
        start_time = time.time()
        test_plan_es = await self._translate_to_spanish(test_plan_en)
        step3_time = int((time.time() - start_time) * 1000)
        
        # 4. Parsear a entidad TestPlan
        test_plan = self._parse_test_plan_markdown(
            markdown=test_plan_es,
            user_story=user_story,
            generated_by_id=generated_by_id
        )
        
        return test_plan
    
    async def _translate_to_english(self, user_story: UserStory) -> str:
        """Traducir HU al inglés"""
        hu_md = self._build_hu_markdown(user_story)
        
        prompt = self.prompt_templates["translate_to_en"].format(hu_es=hu_md)
        
        try:
            response = self.client.responses.create(
                model=settings.OPENAI_MODEL_TRANSLATION,
                input=prompt
            )
            result = response.output[0].content[0].text
            
            # Guardar análisis para auditoría
            await self.ai_analysis_repo.create({
                "step": "translation_to_en",
                "prompt_sent": prompt,
                "response_received": result,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            })
            
            return result
        except Exception as e:
            logger.error(f"Error translating to English: {e}")
            raise
    
    def _build_hu_markdown(self, user_story: UserStory) -> str:
        """Construir markdown de HU desde entidad"""
        ac_md = "\n".join(f"- {ac}" for ac in user_story.acceptance_criteria)
        return f"""User Story Data:
- ID: {user_story.story_id}
- Title: {user_story.title}

## Description
{user_story.description}

## Acceptance Criteria
{ac_md}
"""
    
    def _parse_test_plan_markdown(
        self,
        markdown: str,
        user_story: UserStory,
        generated_by_id: int
    ) -> TestPlan:
        """Parsear markdown del Test Plan a entidad TestPlan"""
        from app.utils.markdown_parser import parse_test_plan_markdown
        return parse_test_plan_markdown(markdown, user_story, generated_by_id)
```

**Mejoras vs. código actual**:
- ✅ Separación de responsabilidades
- ✅ Manejo de errores robusto
- ✅ Auditoría completa (tokens, tiempos)
- ✅ Templates configurables
- ✅ Logging estructurado

---

### 5. Repositorios (`app/repositories/`)

**Propósito**: Abstraer el acceso a datos (Repository Pattern).

#### Interface (Contrato)

```python
# app/repositories/interfaces/test_plan_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.test_plan import TestPlan

class TestPlanRepository(ABC):
    @abstractmethod
    async def create(self, test_plan: TestPlan) -> TestPlan:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[TestPlan]:
        pass
    
    @abstractmethod
    async def get_by_user_story_id(self, user_story_id: int) -> List[TestPlan]:
        pass
    
    @abstractmethod
    async def update(self, test_plan: TestPlan) -> TestPlan:
        pass
```

#### Implementación SQLAlchemy

```python
# app/repositories/sqlalchemy/test_plan_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import TestPlan as TestPlanORM
from app.repositories.interfaces.test_plan_repository import TestPlanRepository
from app.domain.entities.test_plan import TestPlan

class SQLAlchemyTestPlanRepository(TestPlanRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, test_plan: TestPlan) -> TestPlan:
        # Convertir entidad de dominio a modelo ORM
        orm_model = TestPlanORM(
            user_story_id=test_plan.user_story_id,
            objective=test_plan.objective,
            # ... mapear todos los campos
        )
        self.session.add(orm_model)
        await self.session.commit()
        await self.session.refresh(orm_model)
        
        # Convertir de vuelta a entidad de dominio
        return self._orm_to_entity(orm_model)
    
    def _orm_to_entity(self, orm: TestPlanORM) -> TestPlan:
        """Convertir modelo ORM a entidad de dominio"""
        return TestPlan(
            id=orm.id,
            user_story_id=orm.user_story_id,
            # ... mapear todos los campos
        )
```

**Ventajas**:
- ✅ Fácil cambiar de base de datos (solo cambiar implementación)
- ✅ Testeable con mocks
- ✅ Separación de infraestructura y dominio

---

### 6. Endpoints API (`app/api/v1/endpoints/`)

**Propósito**: Puntos de entrada HTTP, solo validación y delegación a servicios.

```python
# app/api/v1/endpoints/test_plans.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.test_plan import TestPlanCreate, TestPlanResponse
from app.services.test_plan_service import TestPlanService
from app.api.dependencies import get_current_user, get_test_plan_service

router = APIRouter(prefix="/test-plans", tags=["test-plans"])

@router.post("/", response_model=TestPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_test_plan(
    user_story_id: int,
    current_user = Depends(get_current_user),
    service: TestPlanService = Depends(get_test_plan_service)
):
    """Generar Test Plan desde una HU"""
    try:
        test_plan = await service.generate_test_plan(
            user_story_id=user_story_id,
            user_id=current_user.id
        )
        return TestPlanResponse.from_entity(test_plan)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{test_plan_id}/export")
async def export_test_plan(
    test_plan_id: int,
    format: str = "excel",
    current_user = Depends(get_current_user),
    service: TestPlanService = Depends(get_test_plan_service)
):
    """Exportar Test Plan en formato especificado"""
    from fastapi.responses import StreamingResponse
    import io
    
    try:
        file_bytes = await service.export_test_plan(
            test_plan_id=test_plan_id,
            format=format,
            user_id=current_user.id
        )
        
        filename = f"test_plan_{test_plan_id}.{format}"
        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

---

### 7. Dependency Injection (`app/api/dependencies.py`)

**Propósito**: Configurar inyección de dependencias de FastAPI.

```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from app.services.test_plan_service import TestPlanService
from app.repositories.sqlalchemy.test_plan_repository import SQLAlchemyTestPlanRepository
from app.db.session import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtener usuario actual desde JWT"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    # Obtener usuario de DB
    # ...
    return user

def get_test_plan_service(db = Depends(get_db_session)):
    """Factory para TestPlanService"""
    test_plan_repo = SQLAlchemyTestPlanRepository(db)
    # ... otras dependencias
    return TestPlanService(
        test_plan_repo=test_plan_repo,
        # ...
    )
```

---

## 🔄 Flujo de Datos (Ejemplo: Generar Test Plan)

```
1. Cliente → POST /api/v1/test-plans/ (con user_story_id)
   ↓
2. Endpoint (test_plans.py)
   - Valida autenticación (get_current_user)
   - Valida entrada (Pydantic schema)
   ↓
3. Service (test_plan_service.py)
   - Obtiene HU del repositorio
   - Llama a AI Service
   ↓
4. AI Service (ai_service.py)
   - Traduce HU
   - Genera Test Plan
   - Traduce resultado
   - Parsea a entidad TestPlan
   ↓
5. Service
   - Guarda TestPlan en repositorio
   ↓
6. Repository (test_plan_repository.py)
   - Convierte entidad → ORM
   - Guarda en DB
   - Convierte ORM → entidad
   ↓
7. Endpoint
   - Convierte entidad → Pydantic schema
   - Retorna JSON
```

---

## 🛠️ Tecnologías Recomendadas

### Core
- **FastAPI**: Framework web (mantener)
- **SQLAlchemy 2.0+**: ORM asíncrono
- **Alembic**: Migraciones de DB
- **Pydantic v2**: Validación y serialización
- **python-dotenv**: Variables de entorno

### Base de Datos
- **PostgreSQL**: Producción
- **SQLite**: Desarrollo (migración fácil a PostgreSQL)

### Autenticación
- **python-jose[cryptography]**: JWT
- **passlib[bcrypt]**: Hash de passwords

### Testing
- **pytest**: Framework de testing
- **pytest-asyncio**: Tests asíncronos
- **httpx**: Cliente HTTP para tests
- **factory-boy**: Factories para datos de test

### Logging y Monitoreo
- **structlog**: Logging estructurado
- **sentry-sdk**: Error tracking (opcional)

---

## 🚀 Migración desde Código Actual

### Fase 1: Estructura Base
1. Crear estructura de directorios
2. Mover código actual a módulos correspondientes
3. Mantener funcionalidad actual

### Fase 2: Separación de Capas
1. Extraer lógica de negocio a servicios
2. Crear repositorios
3. Separar endpoints

### Fase 3: Persistencia
1. Agregar SQLAlchemy
2. Crear modelos ORM
3. Migrar almacenamiento en memoria a DB

### Fase 4: Mejoras
1. Agregar autenticación
2. Agregar tests
3. Mejorar manejo de errores

---

## ✅ Ventajas de esta Arquitectura

1. **Escalabilidad**: Fácil agregar nuevos endpoints/servicios
2. **Testeable**: Cada capa se puede testear independientemente
3. **Mantenible**: Código organizado y con responsabilidades claras
4. **Flexible**: Fácil cambiar implementaciones (ej: cambiar de DB)
5. **Producción-ready**: Logging, manejo de errores, validación

---

Esta arquitectura proporciona una base sólida para escalar el sistema manteniendo la calidad del código y facilitando el mantenimiento futuro.
