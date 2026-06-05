"""
Servicio para gestión de Proyectos.
"""
from app.domain.entities.project import Project
from app.repositories.interfaces.project_repository import ProjectRepository
from app.core.logging import get_logger
from app.core.exceptions import ValidationError, AppException

logger = get_logger(__name__)


class ProjectService:
    """Servicio para operaciones con Proyectos"""
    
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo
    
    async def get_or_create_aeroman(self) -> Project:
        """
        Obtiene el proyecto AEROMAN o lo crea si no existe.
        Útil para asignar proyectos por defecto.
        """
        aeroman = await self.project_repo.get_by_code("AEROMAN")
        if not aeroman:
            aeroman = Project(
                code="AEROMAN",
                name="AEROMAN",
                description="Proyecto por defecto"
            )
            aeroman = await self.project_repo.create(aeroman)
            logger.info("Proyecto AEROMAN creado")
        return aeroman
    
    async def create_project(self, code: str, name: str, description: str = None) -> Project:
        """Crear un nuevo proyecto"""
        # Verificar si ya existe un proyecto con ese código
        existing = await self.project_repo.get_by_code(code)
        if existing:
            raise ValueError(f"Ya existe un proyecto con el código '{code}'")
        
        project = Project(
            code=code.strip(),
            name=name.strip(),
            description=description.strip() if description and description.strip() else None
        )
        
        if not project.is_valid():
            raise ValueError("El proyecto no es válido. Verifique que code y name estén completos.")
        
        created = await self.project_repo.create(project)
        logger.info(f"Proyecto creado: {code}")
        return created
    
    async def update_project(self, project_id: int, name: str = None, description: str = None) -> Project:
        """Actualizar un proyecto existente"""
        # Verificar que el proyecto existe
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Proyecto con ID {project_id} no encontrado")
        
        # Actualizar campos si se proporcionan
        if name is not None:
            project.name = name.strip()
        if description is not None:
            project.description = description.strip() if description and description.strip() else None
        
        # Validar
        if not project.is_valid():
            raise ValueError("El proyecto no es válido. Verifique que name esté completo.")
        
        # Actualizar
        updated = await self.project_repo.update(project)
        logger.info(f"Proyecto actualizado: {updated.code} (ID: {project_id})")
        return updated
    
    async def toggle_status(self, project_id: int) -> Project:
        """Alternar estado activo/inactivo de un proyecto"""
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Proyecto con ID {project_id} no encontrado")
        updated = await self.project_repo.update_status(project_id, not project.is_active)
        action = "activado" if updated.is_active else "inactivado"
        logger.info(f"Proyecto {action}: {updated.code} (ID: {project_id})")
        return updated

    async def delete_project(self, project_id: int) -> bool:
        """
        Eliminar un proyecto.
        No permite eliminar proyectos que tengan HUs asociadas.
        Retorna True si se eliminó, False si no existía.
        """
        # Verificar que el proyecto existe
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            return False
        
        # Verificar si tiene HUs asociadas
        user_stories_count = await self.project_repo.count_user_stories(project_id)
        if user_stories_count > 0:
            raise ValueError(
                f"No se puede eliminar el proyecto '{project.code}' porque tiene {user_stories_count} "
                f"historia(s) de usuario asociada(s). Elimine primero las HUs o asígnelas a otro proyecto."
            )
        
        # Eliminar el proyecto
        deleted = await self.project_repo.delete(project_id)
        if deleted:
            logger.info(f"Proyecto eliminado: {project.code} (ID: {project_id})")
        return deleted
