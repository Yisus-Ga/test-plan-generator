"""
Interface para repositorio de Test Plans.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.test_plan import TestPlan


class TestPlanRepository(ABC):
    """Interface para repositorio de Test Plans"""
    
    @abstractmethod
    async def create(self, test_plan: 'TestPlan') -> 'TestPlan':
        """Crear un nuevo Test Plan"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional['TestPlan']:
        """Obtener Test Plan por ID"""
        pass
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional['TestPlan']:
        """Obtener Test Plan por token de descarga"""
        pass
    
    @abstractmethod
    async def get_by_user_story_id(self, user_story_id: int) -> List['TestPlan']:
        """Obtener todos los Test Plans de una HU"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List['TestPlan']:
        """Obtener todos los Test Plans con paginación"""
        pass
