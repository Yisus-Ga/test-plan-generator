"""
Servicio para gestión de Historias de Usuario.
"""
from app.domain.entities.user_story import UserStory
from app.core.logging import get_logger
from app.core.exceptions import ValidationError

logger = get_logger(__name__)


class UserStoryService:
    """Servicio para operaciones con Historias de Usuario"""
    
    def create_user_story_from_form(
        self,
        story_id: str,
        title: str,
        description: str,
        acceptance_criteria: str
    ) -> UserStory:
        """
        Crea una entidad UserStory desde datos del formulario.
        
        Args:
            story_id: ID de la HU
            title: Título
            description: Descripción
            acceptance_criteria: Criterios de aceptación (texto con líneas separadas)
            
        Returns:
            Entidad UserStory
        """
        # Convertir acceptance_criteria de texto a lista
        ac_list = [
            line.strip() 
            for line in acceptance_criteria.splitlines() 
            if line.strip()
        ]
        
        # Crear entidad
        user_story = UserStory(
            story_id=story_id.strip(),
            title=title.strip(),
            description=description.strip(),
            acceptance_criteria=ac_list
        )
        
        # Detectar tipo
        user_story.story_type = user_story.detect_type()
        
        # Validar
        if not user_story.is_valid():
            raise ValidationError("La Historia de Usuario no es válida. Verifique que todos los campos estén completos y tenga al menos un criterio de aceptación.")
        
        logger.info(f"User Story creada: {story_id}")
        return user_story
