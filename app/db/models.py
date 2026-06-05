"""
Modelos SQLAlchemy ORM para la base de datos.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.domain.value_objects.story_type import StoryType
import enum


class ProjectORM(Base):
    """Modelo ORM para Proyectos"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)  # Ej: "AEROMAN", "AER25"
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user_stories = relationship("UserStoryORM", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ProjectORM(id={self.id}, code={self.code})>"


class UserStoryORM(Base):
    """Modelo ORM para Historias de Usuario"""
    __tablename__ = "user_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    story_id = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    acceptance_criteria = Column(JSON, nullable=False)  # Lista de strings como JSON
    story_type = Column(String(50), nullable=True)  # BACKEND, FRONTEND, UI_UX, etc.
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    project = relationship("ProjectORM", back_populates="user_stories")
    test_plans = relationship("TestPlanORM", back_populates="user_story", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserStoryORM(id={self.id}, story_id={self.story_id})>"


class TestPlanORM(Base):
    """Modelo ORM para Test Plans"""
    __tablename__ = "test_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"), nullable=False, index=True)
    
    # Metadatos del Test Plan
    objective = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Conteos
    total_cases = Column(Integer, default=0)
    high_priority_count = Column(Integer, default=0)
    medium_priority_count = Column(Integer, default=0)
    low_priority_count = Column(Integer, default=0)
    
    # Análisis completo (markdown)
    analysis_markdown = Column(Text, nullable=False)  # Análisis sin tabla
    test_plan_markdown = Column(Text, nullable=False)  # Test Plan completo con tabla
    
    # Token para descarga (temporal, puede eliminarse después de migrar completamente)
    download_token = Column(String(100), unique=True, nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user_story = relationship("UserStoryORM", back_populates="test_plans")
    test_cases = relationship("TestCaseORM", back_populates="test_plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<TestPlanORM(id={self.id}, user_story_id={self.user_story_id})>"


class TestCaseORM(Base):
    """Modelo ORM para Casos de Prueba individuales"""
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    test_plan_id = Column(Integer, ForeignKey("test_plans.id"), nullable=False, index=True)
    
    # Datos del caso de prueba
    tc_id = Column(String(200), nullable=False)  # Ej: "AER25-101: TC1"
    priority = Column(String(20), nullable=False)  # HIGH, MEDIUM, LOW
    title = Column(String(500), nullable=False)
    precondition = Column(Text, nullable=True)
    expected_validation = Column(Text, nullable=False)
    obtained_result = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    test_plan = relationship("TestPlanORM", back_populates="test_cases")
    
    def __repr__(self):
        return f"<TestCaseORM(id={self.id}, tc_id={self.tc_id})>"
