"""
Entidad de dominio: Proyecto
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """Entidad de dominio pura (sin ORM)"""
    id: Optional[int] = None
    code: str = ""  # Ej: "AEROMAN", "AER25"
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_valid(self) -> bool:
        """Validación de reglas de negocio"""
        return (
            bool(self.code.strip()) and
            bool(self.name.strip())
        )
