"""
Configuración de tests de integración (Semana 3).
BD SQLite en memoria para probar endpoints sin tocar la BD real.

IMPORTANTE: Variables de entorno deben fijarse ANTES de importar app.
"""
import os

# BD en memoria compartida (evita que cada conexión tenga DB vacía)
os.environ["DATABASE_URL"] = "sqlite:///file:testdb?mode=memory&cache=shared"
os.environ.setdefault("OPENAI_API_KEY", "test-fake-key")

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models import ProjectORM


@pytest.fixture
def client():
    """
    Cliente de prueba con BD SQLite en memoria.
    Cada test obtiene tablas limpias y proyecto AEROMAN precargado.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        aeroman = ProjectORM(
            code="AEROMAN",
            name="AEROMAN",
            description="Proyecto por defecto para tests",
        )
        db.add(aeroman)
        db.commit()
    finally:
        db.close()

    with TestClient(app) as c:
        yield c
