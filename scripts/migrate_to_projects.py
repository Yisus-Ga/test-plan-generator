"""
Script para migrar datos existentes a proyectos.
Crea el proyecto AEROMAN y asigna todos los Test Plans existentes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy import text, inspect
from app.db.session import SessionLocal, engine
from app.db.models import ProjectORM, UserStoryORM
from app.core.logging import setup_logging

setup_logging()

def migrate_to_projects():
    """Migrar datos existentes a proyectos"""
    db = SessionLocal()
    
    try:
        # 1. Verificar si la tabla projects existe
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'projects' not in tables:
            print("❌ La tabla 'projects' no existe. Ejecuta primero la migración de Alembic.")
            return
        
        # 2. Verificar si el proyecto AEROMAN existe
        aeroman = db.query(ProjectORM).filter(ProjectORM.code == 'AEROMAN').first()
        
        if not aeroman:
            print("Creando proyecto AEROMAN...")
            aeroman = ProjectORM(
                code='AEROMAN',
                name='AEROMAN',
                description='Proyecto por defecto para Test Plans existentes'
            )
            db.add(aeroman)
            db.commit()
            db.refresh(aeroman)
            print(f"Proyecto AEROMAN creado con ID: {aeroman.id}")
        else:
            print(f"Proyecto AEROMAN ya existe con ID: {aeroman.id}")
        
        # 3. Verificar si user_stories tiene project_id
        columns = [col['name'] for col in inspector.get_columns('user_stories')]
        
        if 'project_id' not in columns:
            print("ADVERTENCIA: La columna 'project_id' no existe en 'user_stories'.")
            print("   Ejecuta primero: alembic upgrade head")
            return
        
        # 4. Asignar todos los user_stories sin proyecto al proyecto AEROMAN
        user_stories = db.query(UserStoryORM).filter(
            (UserStoryORM.project_id == None) | (UserStoryORM.project_id == 0)
        ).all()
        
        if user_stories:
            print(f"Asignando {len(user_stories)} Historias de Usuario al proyecto AEROMAN...")
            for us in user_stories:
                us.project_id = aeroman.id
            db.commit()
            print(f"{len(user_stories)} Historias de Usuario asignadas al proyecto AEROMAN")
        else:
            print("Todas las Historias de Usuario ya tienen proyecto asignado")
        
        # 5. Verificar resultado
        total_stories = db.query(UserStoryORM).count()
        stories_with_project = db.query(UserStoryORM).filter(UserStoryORM.project_id == aeroman.id).count()
        
        print(f"\nResumen:")
        print(f"   Total de Historias de Usuario: {total_stories}")
        print(f"   Asignadas a AEROMAN: {stories_with_project}")
        
        if total_stories == stories_with_project:
            print("\nMigracion completada exitosamente")
        else:
            print(f"\nADVERTENCIA: Hay {total_stories - stories_with_project} HUs sin proyecto asignado")
        
    except Exception as e:
        print(f"ERROR durante la migracion: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_to_projects()
