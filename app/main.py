"""
Punto de entrada principal de la aplicación FastAPI.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router

# Configurar logging
setup_logging()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Inicializar base de datos (crear tablas si no existen)
@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos al iniciar la aplicación"""
    from app.db.base import Base
    from app.db.session import engine
    from sqlalchemy import inspect
    
    # Verificar si la tabla projects existe, si no, crear proyecto AEROMAN
    inspector = inspect(engine)
    if 'projects' in inspector.get_table_names():
        # Tabla existe, verificar si AEROMAN existe
        from app.db.session import SessionLocal
        from app.db.models import ProjectORM
        db = SessionLocal()
        try:
            aeroman = db.query(ProjectORM).filter(ProjectORM.code == 'AEROMAN').first()
            if not aeroman:
                # Crear proyecto AEROMAN si no existe
                aeroman = ProjectORM(code='AEROMAN', name='AEROMAN', description='Proyecto por defecto')
                db.add(aeroman)
                db.commit()
        finally:
            db.close()
    
    # Crear tablas si no existen (útil para desarrollo)
    # Nota: En producción, usar solo migraciones de Alembic
    Base.metadata.create_all(bind=engine)

# Configurar CORS (permisivo para desarrollo local)
# Permitir tanto localhost como 127.0.0.1 para evitar problemas de CORS
cors_origins = settings.CORS_ORIGINS
if cors_origins == ["*"]:
    # En desarrollo, permitir todos los orígenes
    cors_origins = ["*"]
else:
    # Agregar variantes comunes de localhost
    cors_origins.extend([
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de API
app.include_router(api_router)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint raíz para servir el frontend
@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "index.html"))

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}
