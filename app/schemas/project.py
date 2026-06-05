"""
Schemas Pydantic para Proyectos.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    """Schema para crear un proyecto"""
    code: str = Field(..., description="Código único del proyecto (ej: AEROMAN)")
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ProjectUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ProjectResponse(BaseModel):
    """Schema de respuesta para proyecto"""
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectStatusUpdate(BaseModel):
    """Schema para cambiar el estado activo/inactivo de un proyecto"""
    is_active: bool
