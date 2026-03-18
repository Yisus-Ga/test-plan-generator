"""
Interface para repositorio de Historias de Usuario.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user_story import UserStory


class UserStoryRepository(ABC):
    """Interface para repositorio de User Stories"""
    
    @abstractmethod
    async def create(self, user_story: UserStory) -> UserStory:
        """Crear una nueva HU"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[UserStory]:
        """Obtener HU por ID interno"""
        pass
    
    @abstractmethod
    async def get_by_story_id(self, story_id: str) -> Optional[UserStory]:
        """Obtener HU por story_id (ID de negocio)"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserStory]:
        """Obtener todas las HUs con paginación"""
        pass
    
    @abstractmethod
    async def update(self, user_story: UserStory) -> UserStory:
        """Actualizar una HU"""
        pass
