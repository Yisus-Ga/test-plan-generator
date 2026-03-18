"""
Entidad de dominio: Historia de Usuario
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from app.domain.value_objects.story_type import StoryType


@dataclass
class UserStory:
    """Entidad de dominio pura (sin ORM)"""
    id: Optional[int] = None
    project_id: int = 0  # Proyecto obligatorio
    story_id: str = ""
    title: str = ""
    description: str = ""
    acceptance_criteria: List[str] = None
    story_type: Optional[StoryType] = None
    version: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.acceptance_criteria is None:
            self.acceptance_criteria = []
    
    def is_valid(self) -> bool:
        """Validación de reglas de negocio"""
        return (
            bool(self.story_id.strip()) and
            bool(self.title.strip()) and
            bool(self.description.strip()) and
            len(self.acceptance_criteria) > 0
        )
    
    def detect_type(self) -> StoryType:
        """Lógica de detección de tipo (regla de negocio)"""
        content = f"{self.title} {self.description}".lower()
        if any(word in content for word in ["backend", "endpoint", "api", "database"]):
            return StoryType.BACKEND
        elif any(word in content for word in ["frontend", "view", "component"]):
            return StoryType.FRONTEND
        elif any(word in content for word in ["design", "ui/ux", "interface"]):
            return StoryType.UI_UX
        return StoryType.UNKNOWN
    
    def to_markdown(self) -> str:
        """Construye markdown de la HU"""
        ac_md = "\n".join(f"- {ac}" for ac in self.acceptance_criteria)
        return f"""User Story Data:
- ID: {self.story_id}
- Title: {self.title}

## Description
{self.description}

## Acceptance Criteria
{ac_md}
"""
