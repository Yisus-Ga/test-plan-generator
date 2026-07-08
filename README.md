# Test Plan Generator

Plataforma que analiza **Historias de Usuario (HU)** con IA y genera documentación de QA estructurada: **resumen/análisis**, **plan de pruebas priorizado** y **casos de prueba** cubriendo los 7 escenarios (positivo, negativo, límite, no funcional, compatibilidad, seguridad, regresión), bajo las normas **ISO/IEC 25010**, **ISO/IEC/IEEE 29119** e **ISTQB**. Exporta a **Excel, CSV, Jira y JSON**.

**Stack:** FastAPI + SQLAlchemy/Alembic (SQLite) · frontend SPA en JS vanilla modular · IA vía OpenAI.

> **Hacia dónde va el proyecto:** evolucionar hacia **perfiles de dominio** para cubrir distintos tipos de aplicaciones (web/GeneXus, core bancario/Bantotal) con un único motor. Resumen ejecutivo: [`PROPUESTA_PERFILES_DOMINIO.md`](PROPUESTA_PERFILES_DOMINIO.md). Detalle técnico y plan: [`docs/`](docs/README.md).

## Puesta en marcha rápida

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
copy .env.example .env      # editar .env y completar OPENAI_API_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

- App: http://127.0.0.1:8000 · API docs: http://127.0.0.1:8000/docs

Detalle completo en [docs/00 — Entorno y Puesta en Marcha](docs/00_CONSIDERACIONES_INFRAESTRUCTURA_LOCAL.md) y en [`comandos.txt`](comandos.txt).

## Seguridad de secretos

> ⚠️ **Nunca** subas tu archivo `.env` (ni la base de datos). Ya están excluidos en `.gitignore`.
> Usá `.env.example` como plantilla. Las claves reales de API y los datos productivos no se versionan.

## Documentación

- [Índice de documentación](docs/README.md)
- [Propuesta de Perfiles de Dominio (resumen ejecutivo)](PROPUESTA_PERFILES_DOMINIO.md)

## Estructura del proyecto

```
app/            Backend FastAPI (dominio, repositorios, servicios, API, core/standards)
static/         Frontend SPA (router, pages, components, api)
alembic/        Migraciones de base de datos
tests/          Tests unitarios y de integración (pytest)
docs/           Documentación del proyecto y del roadmap de perfiles
scripts/        Utilidades (ver scripts/README.md)
```
