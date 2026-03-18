"""
Implementación SQLAlchemy del repositorio de Historias de Usuario.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities.user_story import UserStory
from app.domain.value_objects.story_type import StoryType
from app.db.models import UserStoryORM
from app.repositories.interfaces.user_story_repository import UserStoryRepository


class SQLAlchemyUserStoryRepository(UserStoryRepository):
    """Implementación SQLAlchemy del repositorio de User Stories"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _orm_to_entity(self, orm: UserStoryORM) -> UserStory:
        """Convertir modelo ORM a entidad de dominio"""
        return UserStory(
            id=orm.id,
            project_id=orm.project_id if hasattr(orm, 'project_id') else 0,
            story_id=orm.story_id,
            title=orm.title,
            description=orm.description,
            acceptance_criteria=orm.acceptance_criteria or [],
            story_type=StoryType(orm.story_type) if orm.story_type else StoryType.UNKNOWN,
            version=orm.version,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )
    
    def _entity_to_orm(self, entity: UserStory) -> UserStoryORM:
        """Convertir entidad de dominio a modelo ORM"""
        if entity.id:
            # Actualizar existente
            orm = self.db.query(UserStoryORM).filter(UserStoryORM.id == entity.id).first()
            if not orm:
                orm = UserStoryORM()
        else:
            # Crear nuevo
            orm = UserStoryORM()
        
        orm.project_id = entity.project_id
        orm.story_id = entity.story_id
        orm.title = entity.title
        orm.description = entity.description
        orm.acceptance_criteria = entity.acceptance_criteria
        orm.story_type = entity.story_type.value if entity.story_type else None
        orm.version = entity.version
        
        return orm
    
    async def create(self, user_story: UserStory) -> UserStory:
        """Crear una nueva HU"""
        orm = self._entity_to_orm(user_story)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._orm_to_entity(orm)
    
    async def get_by_id(self, id: int) -> Optional[UserStory]:
        """Obtener HU por ID interno"""
        orm = self.db.query(UserStoryORM).filter(UserStoryORM.id == id).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_by_story_id(self, story_id: str) -> Optional[UserStory]:
        """Obtener HU por story_id (ID de negocio)"""
        orm = self.db.query(UserStoryORM).filter(UserStoryORM.story_id == story_id).first()
        return self._orm_to_entity(orm) if orm else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserStory]:
        """Obtener todas las HUs con paginación"""
        orms = self.db.query(UserStoryORM).offset(skip).limit(limit).all()
        return [self._orm_to_entity(orm) for orm in orms]
    
    async def update(self, user_story: UserStory) -> UserStory:
        """Actualizar una HU"""
        if not user_story.id:
            raise ValueError("UserStory debe tener ID para actualizar")
        
        orm = self._entity_to_orm(user_story)
        self.db.commit()
        self.db.refresh(orm)
        return self._orm_to_entity(orm)
