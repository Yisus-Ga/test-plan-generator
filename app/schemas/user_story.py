"""
Schemas Pydantic para Historias de Usuario.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.domain.value_objects.story_type import StoryType


class UserStoryCreate(BaseModel):
    """Schema para crear una HU"""
    story_id: str = Field(..., description="ID único de la HU (ej: AER25-101)")
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    acceptance_criteria: List[str] = Field(..., min_length=1)


class UserStoryUpdate(BaseModel):
    """Schema para actualizar una HU"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    acceptance_criteria: Optional[List[str]] = Field(None, min_length=1)


class UserStoryResponse(BaseModel):
    """Schema de respuesta para HU"""
    id: int
    story_id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    story_type: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
