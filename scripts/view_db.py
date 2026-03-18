"""
Script simple para ver los datos de la base de datos SQLite.
"""
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.db.models import UserStoryORM, TestPlanORM, TestCaseORM


def view_user_stories(db):
    """Ver todas las Historias de Usuario"""
    print("\n" + "="*80)
    print("HISTORIAS DE USUARIO")
    print("="*80)
    
    stories = db.query(UserStoryORM).all()
    
    if not stories:
        print("No hay Historias de Usuario en la base de datos.")
        return
    
    for story in stories:
        print(f"\n[ID: {story.id}]")
        print(f"   Story ID: {story.story_id}")
        print(f"   Titulo: {story.title}")
        print(f"   Tipo: {story.story_type or 'N/A'}")
        print(f"   Version: {story.version}")
        print(f"   Criterios de Aceptacion: {len(story.acceptance_criteria)}")
        print(f"   Creado: {story.created_at}")
        print(f"   Test Plans asociados: {len(story.test_plans)}")


def view_test_plans(db):
    """Ver todos los Test Plans"""
    print("\n" + "="*80)
    print("TEST PLANS")
    print("="*80)
    
    test_plans = db.query(TestPlanORM).all()
    
    if not test_plans:
        print("No hay Test Plans en la base de datos.")
        return
    
    for tp in test_plans:
        print(f"\n[ID: {tp.id}]")
        print(f"   User Story ID: {tp.user_story_id}")
        print(f"   Token: {tp.download_token}")
        print(f"   Objetivo: {tp.objective[:80]}..." if len(tp.objective) > 80 else f"   Objetivo: {tp.objective}")
        print(f"   Total Casos: {tp.total_cases}")
        print(f"   - Alta: {tp.high_priority_count}")
        print(f"   - Media: {tp.medium_priority_count}")
        print(f"   - Baja: {tp.low_priority_count}")
        print(f"   Casos de Prueba: {len(tp.test_cases)}")
        print(f"   Creado: {tp.created_at}")


def view_test_cases(db, test_plan_id=None):
    """Ver casos de prueba"""
    print("\n" + "="*80)
    print("CASOS DE PRUEBA")
    print("="*80)
    
    if test_plan_id:
        test_cases = db.query(TestCaseORM).filter(TestCaseORM.test_plan_id == test_plan_id).all()
    else:
        test_cases = db.query(TestCaseORM).limit(20).all()
    
    if not test_cases:
        print("No hay casos de prueba en la base de datos.")
        return
    
    print(f"Mostrando {len(test_cases)} casos de prueba:")
    
    for tc in test_cases:
        print(f"\n[ID: {tc.id}]")
        print(f"   TC ID: {tc.tc_id}")
        print(f"   Prioridad: {tc.priority}")
        print(f"   Titulo: {tc.title[:60]}..." if len(tc.title) > 60 else f"   Titulo: {tc.title}")
        print(f"   Test Plan ID: {tc.test_plan_id}")


def view_summary(db):
    """Ver resumen general"""
    print("\n" + "="*80)
    print("RESUMEN DE LA BASE DE DATOS")
    print("="*80)
    
    total_stories = db.query(UserStoryORM).count()
    total_test_plans = db.query(TestPlanORM).count()
    total_test_cases = db.query(TestCaseORM).count()
    
    print(f"\nHistorias de Usuario: {total_stories}")
    print(f"Test Plans: {total_test_plans}")
    print(f"Casos de Prueba: {total_test_cases}")
    
    if total_test_plans > 0:
        avg_cases = total_test_cases / total_test_plans
        print(f"\nPromedio de casos por Test Plan: {avg_cases:.1f}")


def main():
    """Función principal"""
    import sys
    # Configurar encoding UTF-8 para Windows
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("VISOR DE BASE DE DATOS - Test Plan Generator")
    print(f"Base de datos: {settings.DATABASE_URL}")
    
    # Crear sesión
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar si la base de datos existe
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            
            if not tables:
                print("\nADVERTENCIA: La base de datos no tiene tablas. Ejecuta las migraciones primero:")
                print("   alembic upgrade head")
                return
        
        # Mostrar resumen
        view_summary(db)
        
        # Mostrar datos
        view_user_stories(db)
        view_test_plans(db)
        view_test_cases(db)
        
        print("\n" + "="*80)
        print("Consulta completada")
        print("="*80)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
