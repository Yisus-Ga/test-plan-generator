"""
Entidad de dominio: Test Plan
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class TestCase:
    """Caso de prueba individual"""
    id: Optional[int] = None
    tc_id: str = ""  # Ej: "AER25-101: TC1"
    priority: str = ""  # HIGH, MEDIUM, LOW
    title: str = ""
    precondition: str = ""
    expected_validation: str = ""
    obtained_result: str = ""


@dataclass
class TestPlan:
    """Entidad de dominio pura (sin ORM)"""
    id: Optional[int] = None
    user_story_id: int = 0
    objective: str = ""
    summary: str = ""
    notes: Optional[str] = None
    total_cases: int = 0
    high_priority_count: int = 0
    medium_priority_count: int = 0
    low_priority_count: int = 0
    analysis_markdown: str = ""  # Análisis sin tabla
    test_plan_markdown: str = ""  # Test Plan completo con tabla
    test_cases: List[TestCase] = None
    download_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.test_cases is None:
            self.test_cases = []
