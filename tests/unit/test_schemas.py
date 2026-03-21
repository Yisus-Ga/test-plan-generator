"""
Tests unitarios para schemas Pydantic (validaciones)
"""
import pytest
from pydantic import ValidationError
from app.schemas.user_story import UserStoryCreate, UserStoryUpdate


class TestUserStoryCreate:
    """Tests para UserStoryCreate schema"""

    def test_valid_data_creates_successfully(self):
        """Datos válidos crean el schema correctamente"""
        data = {
            "story_id": "AER25-101",
            "title": "Pantalla de Login",
            "description": "Como usuario quiero... con al menos 20 caracteres para pasar validación",
            "acceptance_criteria": ["Criterio 1", "Criterio 2"],
        }
        hu = UserStoryCreate(**data)
        assert hu.story_id == "AER25-101"
        assert hu.title == "Pantalla de Login"
        assert len(hu.acceptance_criteria) == 2

    def test_story_id_required(self):
        """story_id es obligatorio"""
        with pytest.raises(ValidationError) as exc_info:
            UserStoryCreate(
                title="Título",
                description="Descripción larga suficiente",
                acceptance_criteria=["C1"],
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("story_id",) for e in errors)

    def test_title_min_length(self):
        """title debe tener al menos 1 carácter"""
        with pytest.raises(ValidationError):
            UserStoryCreate(
                story_id="AER-1",
                title="",
                description="Descripción larga suficiente",
                acceptance_criteria=["C1"],
            )

    def test_title_max_length(self):
        """title no puede exceder 200 caracteres"""
        with pytest.raises(ValidationError):
            UserStoryCreate(
                story_id="AER-1",
                title="a" * 201,
                description="Descripción larga suficiente",
                acceptance_criteria=["C1"],
            )

    def test_description_required(self):
        """description es obligatorio"""
        with pytest.raises(ValidationError):
            UserStoryCreate(
                story_id="AER-1",
                title="Título",
                description="",
                acceptance_criteria=["C1"],
            )

    def test_acceptance_criteria_min_one(self):
        """acceptance_criteria debe tener al menos un elemento"""
        with pytest.raises(ValidationError):
            UserStoryCreate(
                story_id="AER-1",
                title="Título",
                description="Descripción larga suficiente",
                acceptance_criteria=[],
            )


class TestUserStoryUpdate:
    """Tests para UserStoryUpdate schema (parcial)"""

    def test_all_fields_optional(self):
        """Todos los campos pueden ser None"""
        update = UserStoryUpdate()
        assert update.title is None
        assert update.description is None
        assert update.acceptance_criteria is None

    def test_partial_update_valid(self):
        """Actualización parcial con un solo campo"""
        update = UserStoryUpdate(title="Nuevo título")
        assert update.title == "Nuevo título"
        assert update.description is None
        assert update.acceptance_criteria is None

    def test_acceptance_criteria_min_one_when_provided(self):
        """Si se provee acceptance_criteria, debe tener al menos un elemento"""
        with pytest.raises(ValidationError):
            UserStoryUpdate(acceptance_criteria=[])
