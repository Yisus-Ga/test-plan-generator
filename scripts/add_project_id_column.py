"""
Script para agregar la columna project_id a user_stories manualmente.
"""
import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text, inspect
from app.db.session import SessionLocal, engine
from app.db.models import ProjectORM, UserStoryORM

def add_project_id_column():
    """Agregar columna project_id a user_stories"""
    db = SessionLocal()
    
    try:
        # 1. Verificar si project_id ya existe
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('user_stories')]
        
        if 'project_id' in columns:
            print("La columna project_id ya existe en user_stories")
        else:
            print("Agregando columna project_id a user_stories...")
            # SQLite no soporta ALTER TABLE ADD COLUMN con NOT NULL directamente
            # Necesitamos agregarlo como nullable primero
            db.execute(text("ALTER TABLE user_stories ADD COLUMN project_id INTEGER"))
            db.commit()
            print("Columna project_id agregada")
        
        # 2. Obtener proyecto AEROMAN
        aeroman = db.query(ProjectORM).filter(ProjectORM.code == 'AEROMAN').first()
        if not aeroman:
            print("ERROR: Proyecto AEROMAN no existe. Creandolo...")
            aeroman = ProjectORM(code='AEROMAN', name='AEROMAN', description='Proyecto por defecto')
            db.add(aeroman)
            db.commit()
            db.refresh(aeroman)
        
        # 3. Asignar todos los user_stories sin proyecto
        result = db.execute(text("""
            UPDATE user_stories 
            SET project_id = :project_id 
            WHERE project_id IS NULL
        """), {"project_id": aeroman.id})
        
        db.commit()
        print(f"Actualizadas {result.rowcount} Historias de Usuario")
        
        # 4. Verificar
        total = db.execute(text("SELECT COUNT(*) FROM user_stories")).scalar()
        with_project = db.execute(text("SELECT COUNT(*) FROM user_stories WHERE project_id = :pid"), 
                                  {"pid": aeroman.id}).scalar()
        
        print(f"\nResumen:")
        print(f"  Total HUs: {total}")
        print(f"  Con proyecto AEROMAN: {with_project}")
        
        if total == with_project:
            print("\nMigracion completada exitosamente")
        else:
            print(f"\nADVERTENCIA: {total - with_project} HUs sin proyecto")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_project_id_column()
