"""
Interface para repositorio de Proyectos.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.project import Project


class ProjectRepository(ABC):
    """Interface para repositorio de Projects"""
    
    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Crear un nuevo proyecto"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Project]:
        """Obtener proyecto por ID"""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Project]:
        """Obtener proyecto por código"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Obtener todos los proyectos con paginación"""
        pass
    
    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Actualizar un proyecto"""
        pass
    
    @abstractmethod
    async def delete(self, project_id: int) -> bool:
        """Eliminar un proyecto por ID. Retorna True si se eliminó, False si no existía"""
        pass
    
    @abstractmethod
    async def update_status(self, project_id: int, is_active: bool) -> Optional[Project]:
        """Cambiar el estado activo/inactivo de un proyecto"""
        pass

    @abstractmethod
    async def get_all_active(self) -> List[Project]:
        """Obtener solo proyectos activos"""
        pass

    @abstractmethod
    async def count_user_stories(self, project_id: int) -> int:
        """Contar cuántas HUs tiene asociadas un proyecto"""
        pass
