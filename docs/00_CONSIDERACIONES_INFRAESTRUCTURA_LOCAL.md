# 00 · Entorno, Configuración y Puesta en Marcha

> **Objetivo del documento:** dejar corriendo el proyecto en local y explicar cómo se configura, incluyendo las piezas que habilita la evolución hacia **perfiles de dominio** (proveedor de IA intercambiable y selección de perfil por proyecto).

Índice de la documentación: ver [README.md](./README.md).
Visión y arquitectura de perfiles: ver [01](./01_DIAGNOSTICO_SISTEMA_ACTUAL.md) y [03](./03_ARQUITECTURA_BACKEND.md).

---

## 1. Contexto de infraestructura

Todo corre **en local**, sin dependencias de nube:

- **Base de datos:** SQLite (`test_plan_generator.db`), archivo único, sin servidor.
- **Backend:** FastAPI servido con Uvicorn.
- **Frontend:** estático (HTML/CSS/JS) servido por el mismo FastAPI en `/static`.
- **IA:** hoy vía API de OpenAI. La abstracción de proveedor (para sumar Claude) es parte del roadmap — ver [06](./06_ROADMAP_IMPLEMENTACION.md), Fase 1.

Esta simplicidad es deliberada: baja la barrera de entrada para el equipo. La migración a PostgreSQL, autenticación real y despliegue se contemplan como escalado posterior, no como bloqueo.

## 2. Requisitos

- Python 3.11+ (el proyecto se probó con 3.13).
- Una API Key de OpenAI.
- Windows con PowerShell (los comandos de ejemplo usan PowerShell; en otros SO son equivalentes).

## 3. Puesta en marcha

```powershell
# 1. Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env
#   Editar .env y completar OPENAI_API_KEY

# 4. Preparar la base de datos (aplica migraciones)
alembic upgrade head

# 5. Levantar la aplicación
uvicorn app.main:app --reload
```

- App: http://127.0.0.1:8000
- Documentación interactiva de la API (Swagger): http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

El listado completo de comandos está en [`comandos.txt`](../comandos.txt) (raíz del proyecto).

## 4. Configuración (`app/config.py` + `.env`)

La configuración está centralizada en `app/config.py` (Pydantic `BaseSettings`) y se sobreescribe con `.env`. Variables relevantes:

| Variable | Default | Descripción |
|---|---|---|
| `OPENAI_API_KEY` | — (obligatoria) | Clave de OpenAI. |
| `OPENAI_MODEL_TRANSLATION` | `gpt-4.1-mini` | Modelo para traducción. |
| `OPENAI_MODEL_GENERATION` | `gpt-4.1` | Modelo para generación del test plan. |
| `DATABASE_URL` | `sqlite:///./test_plan_generator.db` | Conexión a la BD. |
| `AUTH_REQUIRED` | `False` | Modo single-user (sin login). |
| `CORS_ORIGINS` | `["*"]` | Permisivo para desarrollo local. |
| `EXPORT_STORAGE_PATH` | `./exports` | Carpeta de exportaciones. |
| `LOG_LEVEL` / `LOG_FILE` | `INFO` / `./logs/app.log` | Logging. |

### Configuración prevista para perfiles (roadmap)

La evolución a perfiles introduce configuración nueva (aún no implementada, se documenta para dimensionar el trabajo — ver [03](./03_ARQUITECTURA_BACKEND.md) y [06](./06_ROADMAP_IMPLEMENTACION.md)):

- **Proveedor de IA** intercambiable: `AI_PROVIDER` (`openai` | `anthropic`) + claves y modelos por proveedor.
- **Perfil por defecto** para proyectos sin perfil asignado.
- **Credenciales de conectores** de grounding (por ejemplo, el MCP de Bantotal), gestionadas fuera del código y **nunca** versionadas.

## 5. Seguridad de secretos (importante antes de compartir el repo)

- `.env`, `*.db`, `logs/` y `exports/` están en `.gitignore`: **no se suben**.
- Nunca commitear claves reales. El archivo de referencia es `.env.example` (con placeholders).
- El perfil bancario (Bantotal) trabaja sobre **definiciones y estructuras**, nunca sobre datos productivos de clientes ni credenciales reales (ver [05](./05_PROPUESTA_MCP_Y_APIS.md)).
