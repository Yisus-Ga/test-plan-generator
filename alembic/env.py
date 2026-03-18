"""
Configuración de Alembic para migraciones de base de datos.
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Agregar el directorio raíz al path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar configuración y modelos
from app.config import settings
from app.db.base import Base
from app.db.models import UserStoryORM, TestPlanORM, TestCaseORM  # Importar todos los modelos

# this is the Alembic Config object
config = context.config

# Interpretar el archivo de configuración para logging de Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sobrescribir sqlalchemy.url con la configuración de la app
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Agregar el objeto MetaData del Base para 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
