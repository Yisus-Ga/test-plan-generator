# Consideraciones de Infraestructura Local

## 🖥️ Contexto

**Situación actual**: Toda la infraestructura está en la computadora local del desarrollador.

Esto simplifica significativamente muchas decisiones arquitectónicas y cambia las recomendaciones en varios aspectos clave.

---

## 🔄 Cambios en Recomendaciones

### 1. Base de Datos: SQLite ÚNICAMENTE

**Recomendación Original**: PostgreSQL (producción) / SQLite (desarrollo)

**Recomendación Actualizada**: **SQLite exclusivamente**

**Justificación**:
- ✅ Sin necesidad de instalar/servir PostgreSQL
- ✅ Archivo único, fácil de respaldar
- ✅ Sin configuración de servidor
- ✅ Suficiente para uso local (soporta hasta GB de datos)
- ✅ Compatible con SQLAlchemy sin cambios
- ✅ Fácil migración futura a PostgreSQL si es necesario

**Implementación**:
```python
# app/config.py
class Settings(BaseSettings):
    # Database - SQLite para local
    DATABASE_URL: str = "sqlite:///./test_plan_generator.db"
    # Sin necesidad de usuario/contraseña/host
```

**Consideraciones**:
- ✅ SQLite maneja bien hasta cientos de MB de datos
- ✅ Para miles de registros funciona perfectamente
- ✅ Si en el futuro necesitas PostgreSQL, la migración es directa (mismo código SQLAlchemy)

---

### 2. Autenticación: Simplificada u Opcional

**Recomendación Original**: Autenticación completa con JWT y usuarios

**Recomendación Actualizada**: **Autenticación simplificada o modo "single-user"**

**Opciones**:

#### Opción A: Modo Single-User (Recomendada para empezar)

```python
# app/config.py
class Settings(BaseSettings):
    # Autenticación simplificada
    AUTH_REQUIRED: bool = False  # Desactivar autenticación para desarrollo local
    DEFAULT_USER_ID: int = 1     # Usuario por defecto
```

**Ventajas**:
- ✅ Sin complejidad de login/registro
- ✅ Enfocado en funcionalidad core
- ✅ Puede activarse después fácilmente

#### Opción B: Autenticación Mínima

```python
# Usuario único hardcodeado o en .env
DEFAULT_USER_EMAIL = "user@local.dev"
DEFAULT_USER_PASSWORD = "local"  # En .env, no hardcoded
```

**Ventajas**:
- ✅ Mantiene estructura de usuarios
- ✅ Fácil activar autenticación completa después
- ✅ Menos complejidad que JWT completo

**Recomendación**: Empezar con **Opción A** (single-user), activar autenticación cuando sea necesario.

---

### 3. CORS: Permisivo para Local

**Recomendación Original**: CORS restrictivo para producción

**Recomendación Actualizada**: **CORS permisivo para desarrollo local**

```python
# app/main.py
from app.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Consideraciones**:
- ✅ Permite probar desde cualquier puerto (3000, 8080, 8000, etc.)
- ✅ Sin problemas de CORS en desarrollo
- ⚠️ Cambiar cuando se despliegue en producción

---

### 4. URLs y Puertos: Todo Local

**Recomendación Original**: URLs configurables para múltiples entornos

**Recomendación Actualizada**: **URLs hardcodeadas a localhost**

```python
# app/config.py
class Settings(BaseSettings):
    # URLs locales
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"  # O puerto que uses
    
    # Base de datos local
    DATABASE_URL: str = "sqlite:///./test_plan_generator.db"
```

**Frontend**:
```javascript
// assets/js/config.js
export const config = {
  API_URL: "http://localhost:8000",
  // Sin necesidad de variables de entorno complejas
};
```

---

### 5. MCP Server: Ejecución Local

**Recomendación Original**: MCP Server como servicio separado

**Recomendación Actualizada**: **MCP Server ejecutándose localmente en el mismo proceso o puerto**

#### Opción A: MCP Server integrado (Recomendada)

```python
# Ejecutar MCP Server en el mismo proceso FastAPI
# app/main.py
from mcp_server.server import mcp_server

# Iniciar MCP Server en thread separado o proceso
async def startup():
    # Iniciar MCP Server
    await mcp_server.start()
```

#### Opción B: MCP Server en proceso separado (misma máquina)

```bash
# Terminal 1: Backend FastAPI
uvicorn app.main:app --reload --port 8000

# Terminal 2: MCP Server
python -m mcp_server.main --port 8001
```

**Recomendación**: **Opción A** (integrado) para simplicidad.

---

### 6. Almacenamiento de Archivos: Local

**Recomendación Original**: Almacenamiento en cloud o servicio externo

**Recomendación Actualizada**: **Archivos en carpeta local**

```python
# app/config.py
class Settings(BaseSettings):
    # Almacenamiento local
    EXPORT_STORAGE_PATH: str = "./exports"  # Carpeta relativa al proyecto
    UPLOAD_STORAGE_PATH: str = "./uploads"  # Si se necesita subir archivos
```

**Estructura**:
```
proyecto/
├── app/
├── static/
├── exports/          # Archivos Excel/CSV generados
├── uploads/          # Archivos subidos (si aplica)
├── test_plan_generator.db  # Base de datos SQLite
└── .env
```

**Ventajas**:
- ✅ Sin dependencias externas
- ✅ Fácil de respaldar (copiar carpeta)
- ✅ Acceso directo a archivos

---

### 7. Logging: Archivos Locales

**Recomendación Original**: Logging a servicios externos (Sentry, CloudWatch, etc.)

**Recomendación Actualizada**: **Logging a archivos locales**

```python
# app/core/logging.py
import logging
from pathlib import Path

def setup_logging():
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler()  # También a consola
        ]
    )
```

**Estructura**:
```
proyecto/
├── logs/
│   ├── app.log
│   └── error.log
```

---

### 8. Variables de Entorno: Simplificadas

**Recomendación Original**: Variables de entorno complejas para múltiples entornos

**Recomendación Actualizada**: **Variables mínimas necesarias**

```bash
# .env (local)
OPENAI_API_KEY=sk-...              # Obligatorio
SECRET_KEY=local-secret-key-123    # Simple para local
DEBUG=true                         # Activar debug
DATABASE_URL=sqlite:///./test_plan_generator.db  # Ya tiene valor por defecto
```

**Sin necesidad de**:
- ❌ Variables de base de datos (usuario, host, puerto)
- ❌ URLs de servicios externos (todos son localhost)
- ❌ Configuraciones de cloud
- ❌ Variables de autenticación complejas (si usas modo single-user)

---

### 9. Testing: Simplificado

**Recomendación Original**: Tests con bases de datos separadas, mocks complejos

**Recomendación Actualizada**: **Tests con SQLite en memoria**

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

@pytest.fixture
def db_session():
    # SQLite en memoria para tests (super rápido)
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
```

**Ventajas**:
- ✅ Tests rápidos (sin necesidad de DB real)
- ✅ Aislados (cada test tiene su propia DB)
- ✅ Sin configuración externa

---

### 10. Deployment: NO Aplicable

**Recomendación Original**: Consideraciones de deployment (Docker, nginx, etc.)

**Recomendación Actualizada**: **NO es necesario**

**Para ejecutar localmente**:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY

# Ejecutar backend
uvicorn app.main:app --reload

# El frontend se sirve desde FastAPI (static files)
# Abrir navegador en http://localhost:8000
```

**Sin necesidad de**:
- ❌ Docker / Docker Compose
- ❌ Nginx / Apache
- ❌ Gunicorn / uWSGI (uvicorn es suficiente)
- ❌ Scripts de deployment
- ❌ Variables de entorno de producción

---

## 📋 Checklist de Configuración Local

### Configuración Mínima Necesaria

- [ ] Python 3.9+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado con `OPENAI_API_KEY`
- [ ] Base de datos SQLite (se crea automáticamente)
- [ ] Carpeta `exports/` para archivos generados
- [ ] Carpeta `logs/` para logs (opcional)

### Estructura de Carpetas Local

```
proyecto/
├── app/                    # Código backend
├── static/                 # Frontend (HTML/CSS/JS)
├── exports/                # Archivos Excel/CSV generados
├── logs/                   # Logs de la aplicación
├── test_plan_generator.db  # Base de datos SQLite (auto-creada)
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias Python
└── README.md
```

---

## 🚀 Comandos de Inicio Rápido

### Iniciar la Aplicación

```bash
# 1. Clonar/configurar proyecto
cd proyecto

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env
echo "SECRET_KEY=local-secret-123" >> .env
echo "DEBUG=true" >> .env

# 4. Iniciar backend
uvicorn app.main:app --reload

# 5. Abrir navegador
# http://localhost:8000
```

### Iniciar con MCP Server (cuando se implemente)

```bash
# El MCP Server puede ejecutarse integrado o separado
# Ver sección de MCP para más detalles
```

---

## ⚠️ Consideraciones Importantes

### Limitaciones de SQLite

**Atención**: SQLite tiene algunas limitaciones que debes conocer:

1. **Concurrencia**: Solo 1 escritura simultánea
   - ✅ **OK para uso local** (un solo usuario)
   - ⚠️ Si planeas múltiples usuarios simultáneos, considerar PostgreSQL

2. **Tamaño**: Funciona bien hasta varios GB
   - ✅ **Más que suficiente para uso local**

3. **Características**: Algunas características avanzadas no disponibles
   - ✅ **No necesarias para este proyecto**

### Migración Futura

Si en el futuro necesitas escalar (múltiples usuarios, producción):

1. **SQLite → PostgreSQL**: Migración directa (mismo código SQLAlchemy)
2. **Cambiar DATABASE_URL** en `.env`
3. **Ejecutar migraciones** con Alembic
4. **¡Listo!**

---

## ✅ Resumen de Cambios

| Aspecto | Recomendación Original | Recomendación Local |
|---------|------------------------|---------------------|
| **Base de Datos** | PostgreSQL | **SQLite** |
| **Autenticación** | Completa con JWT | **Simplificada u opcional** |
| **CORS** | Restrictivo | **Permisivo** |
| **URLs** | Configurables | **Localhost fijo** |
| **MCP Server** | Servicio separado | **Integrado o local** |
| **Archivos** | Cloud storage | **Carpeta local** |
| **Logging** | Servicios externos | **Archivos locales** |
| **Variables ENV** | Múltiples entornos | **Mínimas necesarias** |
| **Testing** | DB externa | **SQLite en memoria** |
| **Deployment** | Docker, nginx, etc. | **NO necesario** |

---

## 📝 Notas Finales

Esta configuración es **perfecta para desarrollo y uso local personal**. Si en el futuro necesitas:

- **Múltiples usuarios simultáneos** → Considerar PostgreSQL
- **Deployment en producción** → Agregar Docker, nginx, etc.
- **Autenticación completa** → Activar sistema de usuarios/JWT
- **Logging centralizado** → Integrar con servicios externos

Pero para empezar y desarrollar, **SQLite + configuración simple es ideal**.

---

**Última actualización**: Para entorno local exclusivamente  
**Versión**: 1.0  
**Estado**: Recomendaciones para infraestructura local
