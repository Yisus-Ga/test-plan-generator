"""
Schemas Pydantic para Test Plans.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TestCaseResponse(BaseModel):
    """Schema para un caso de prueba"""
    priority: str
    tc_id: str
    title: str
    precondition: str
    expected_validation: str
    obtained_result: str = ""


class TestPlanListItem(BaseModel):
    """Schema para item en listado de Test Plans"""
    id: int
    user_story_id: int
    user_story_story_id: str  # ID de negocio de la HU
    user_story_title: str
    project_code: str
    project_name: str
    total_cases: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestPlanResponse(BaseModel):
    """Schema de respuesta para Test Plan completo"""
    id: int
    user_story_id: int
    objective: str
    summary: str
    total_cases: int = 0
    high_priority_count: int = 0
    medium_priority_count: int = 0
    low_priority_count: int = 0
    notes: Optional[str] = None
    analysis: str  # Análisis completo sin tabla
    test_cases: List[TestCaseResponse] = []
    download_token: Optional[str] = None  # Token para descarga
    created_at: datetime
    updated_at: Optional[datetime] = None  # Puede ser None si nunca se actualizó
    
    class Config:
        from_attributes = True
