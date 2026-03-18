"""
Implementación SQLAlchemy del repositorio de Test Plans.
"""
from typing import Optional, List
import uuid
from sqlalchemy.orm import Session
from app.domain.entities.test_plan import TestPlan, TestCase
from app.db.models import TestPlanORM, TestCaseORM
from app.repositories.interfaces.test_plan_repository import TestPlanRepository


class SQLAlchemyTestPlanRepository(TestPlanRepository):
    """Implementación SQLAlchemy del repositorio de Test Plans"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _orm_to_entity(self, orm: TestPlanORM) -> TestPlan:
        """Convertir modelo ORM a entidad de dominio"""
        test_cases = [
            TestCase(
                id=tc.id,
                tc_id=tc.tc_id,
                priority=tc.priority,
                title=tc.title,
                precondition=tc.precondition or "",
                expected_validation=tc.expected_validation,
                obtained_result=tc.obtained_result or ""
            )
            for tc in orm.test_cases
        ]
        
        return TestPlan(
            id=orm.id,
            user_story_id=orm.user_story_id,
            objective=orm.objective,
            summary=orm.summary,
            notes=orm.notes,
            total_cases=orm.total_cases,
            high_priority_count=orm.high_priority_count,
            medium_priority_count=orm.medium_priority_count,
            low_priority_count=orm.low_priority_count,
            analysis_markdown=orm.analysis_markdown,
            test_plan_markdown=orm.test_plan_markdown,
            test_cases=test_cases,
            download_token=orm.download_token,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: TestPlan) -> TestPlanORM:
        """Convertir entidad de dominio a modelo ORM"""
        if entity.id:
            orm = self.db.query(TestPlanORM).filter(TestPlanORM.id == entity.id).first()
            if not orm:
                orm = TestPlanORM()
        else:
            orm = TestPlanORM()
        
        orm.user_story_id = entity.user_story_id
        orm.objective = entity.objective
        orm.summary = entity.summary
        orm.notes = entity.notes
        orm.total_cases = entity.total_cases
        orm.high_priority_count = entity.high_priority_count
        orm.medium_priority_count = entity.medium_priority_count
        orm.low_priority_count = entity.low_priority_count
        orm.analysis_markdown = entity.analysis_markdown
        orm.test_plan_markdown = entity.test_plan_markdown
        orm.download_token = entity.download_token or uuid.uuid4().hex
        
        # Eliminar test cases antiguos si es actualización
        if entity.id:
            self.db.query(TestCaseORM).filter(TestCaseORM.test_plan_id == entity.id).delete()
        
        # Crear test cases
        orm.test_cases = [
            TestCaseORM(
                tc_id=tc.tc_id,
                priority=tc.priority,
                title=tc.title,
                precondition=tc.precondition,
                expected_validation=tc.expected_validation,
                obtained_result=tc.obtained_result
            )
            for tc in entity.test_cases
        ]
        
        return orm
    
    async def create(self, test_plan: TestPlan) -> TestPlan:
        """Crear un nuevo Test Plan"""
        orm = self._entity_to_orm(test_plan)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._orm_to_entity(orm)
    
    async def get_by_id(self, id: int) -> Optional[TestPlan]:
        """Obtener Test Plan por ID"""
        orm = self.db.query(TestPlanORM).filter(TestPlanORM.id == id).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_by_token(self, token: str) -> Optional[TestPlan]:
        """Obtener Test Plan por token de descarga"""
        orm = self.db.query(TestPlanORM).filter(TestPlanORM.download_token == token).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_by_user_story_id(self, user_story_id: int) -> List[TestPlan]:
        """Obtener todos los Test Plans de una HU"""
        orms = self.db.query(TestPlanORM).filter(TestPlanORM.user_story_id == user_story_id).all()
        return [self._orm_to_entity(orm) for orm in orms]
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TestPlan]:
        """Obtener todos los Test Plans con paginación"""
        orms = self.db.query(TestPlanORM).offset(skip).limit(limit).all()
        return [self._orm_to_entity(orm) for orm in orms]
