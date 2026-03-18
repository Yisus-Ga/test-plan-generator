"""
Implementación SQLAlchemy del repositorio de Proyectos.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities.project import Project
from app.db.models import ProjectORM
from app.repositories.interfaces.project_repository import ProjectRepository


class SQLAlchemyProjectRepository(ProjectRepository):
    """Implementación SQLAlchemy del repositorio de Projects"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _orm_to_entity(self, orm: ProjectORM) -> Project:
        """Convertir modelo ORM a entidad de dominio"""
        return Project(
            id=orm.id,
            code=orm.code,
            name=orm.name,
            description=orm.description,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: Project) -> ProjectORM:
        """Convertir entidad de dominio a modelo ORM"""
        if entity.id:
            orm = self.db.query(ProjectORM).filter(ProjectORM.id == entity.id).first()
            if not orm:
                orm = ProjectORM()
        else:
            orm = ProjectORM()
        
        orm.code = entity.code
        orm.name = entity.name
        orm.description = entity.description
        
        return orm
    
    async def create(self, project: Project) -> Project:
        """Crear un nuevo proyecto"""
        orm = self._entity_to_orm(project)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._orm_to_entity(orm)
    
    async def get_by_id(self, id: int) -> Optional[Project]:
        """Obtener proyecto por ID"""
        orm = self.db.query(ProjectORM).filter(ProjectORM.id == id).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_by_code(self, code: str) -> Optional[Project]:
        """Obtener proyecto por código"""
        orm = self.db.query(ProjectORM).filter(ProjectORM.code == code).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Obtener todos los proyectos con paginación"""
        orms = self.db.query(ProjectORM).offset(skip).limit(limit).all()
        return [self._orm_to_entity(orm) for orm in orms]
    
    async def update(self, project: Project) -> Project:
        """Actualizar un proyecto"""
        if not project.id:
            raise ValueError("Project debe tener ID para actualizar")
        
        orm = self._entity_to_orm(project)
        self.db.commit()
        self.db.refresh(orm)
        return self._orm_to_entity(orm)
    
    async def delete(self, project_id: int) -> bool:
        """Eliminar un proyecto por ID. Retorna True si se eliminó, False si no existía"""
        orm = self.db.query(ProjectORM).filter(ProjectORM.id == project_id).first()
        if not orm:
            return False
        
        self.db.delete(orm)
        self.db.commit()
        return True
    
    async def count_user_stories(self, project_id: int) -> int:
        """Contar cuántas HUs tiene asociadas un proyecto"""
        from app.db.models import UserStoryORM
        count = self.db.query(UserStoryORM).filter(UserStoryORM.project_id == project_id).count()
        return count
