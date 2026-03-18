"""
Value objects para tipos de Historia de Usuario.
"""
from enum import Enum


class StoryType(str, Enum):
    """Tipo de Historia de Usuario"""
    BACKEND = "backend"
    FRONTEND = "frontend"
    UI_UX = "ui_ux"
    API = "api"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    UNKNOWN = "unknown"
