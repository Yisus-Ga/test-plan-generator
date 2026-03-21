"""
Tests de integración para servicios.

Semana 2: Usamos MOCKS para no llamar a OpenAI ni a la base de datos real.
- AIService se reemplaza por un "doble" que devuelve respuestas falsas
- Los repositorios se reemplazan por objetos que simulan respuestas
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.user_story_service import UserStoryService
from app.services.test_plan_service import TestPlanService
from app.domain.entities.user_story import UserStory
from app.domain.entities.project import Project
from app.domain.entities.test_plan import TestPlan
from app.domain.value_objects.story_type import StoryType
from app.core.exceptions import ValidationError, AIServiceError


# Markdown falso que devolverá el AIService mockeado (debe tener formato de tabla válido)
FAKE_TEST_PLAN_MD = """
## Objetivo
Validar el login del usuario.

## Resumen
Se generaron 2 casos de prueba.

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Login con credenciales válidas | Usuario registrado | Redirección a dashboard | |
| Media | TC2 | Login con contraseña incorrecta | Usuario registrado | Mensaje de error | |
"""


# ========== UserStoryService - Sin mocks (lógica pura) ==========

class TestUserStoryService:
    """UserStoryService no necesita mocks: no llama a APIs ni a BD."""

    def test_create_user_story_from_form_valid(self):
        """Crea una UserStory correctamente desde datos del formulario."""
        service = UserStoryService()
        criteria = "Criterio 1\nCriterio 2\nCriterio 3"

        hu = service.create_user_story_from_form(
            story_id="AER25-101",
            title="Pantalla de Login",
            description="Como usuario quiero autenticarme en el sistema",
            acceptance_criteria=criteria
        )

        assert isinstance(hu, UserStory)
        assert hu.story_id == "AER25-101"
        assert hu.title == "Pantalla de Login"
        assert len(hu.acceptance_criteria) == 3
        assert hu.acceptance_criteria[0] == "Criterio 1"

    def test_create_user_story_detect_type_backend(self):
        """Detecta tipo BACKEND cuando la descripción menciona API."""
        service = UserStoryService()
        hu = service.create_user_story_from_form(
            story_id="AER-1",
            title="Endpoint API",
            description="Crear endpoint de backend para validar datos",
            acceptance_criteria="C1"
        )
        assert hu.story_type == StoryType.BACKEND

    def test_create_user_story_empty_criteria_raises(self):
        """Criterios vacíos deben lanzar ValidationError."""
        service = UserStoryService()
        with pytest.raises(ValidationError):
            service.create_user_story_from_form(
                story_id="AER-1",
                title="Título",
                description="Descripción suficiente",
                acceptance_criteria=""
            )


# ========== TestPlanService - Con mocks (no llama a OpenAI ni BD) ==========

class TestTestPlanService:
    """TestPlanService con AIService y repositorios mockeados."""

    @pytest.fixture
    def mock_project(self):
        """Proyecto falso para el mock."""
        p = Project(id=1, code="AEROMAN", name="Proyecto AEROMAN")
        return p

    @pytest.fixture
    def mock_user_story(self):
        """UserStory falso con ID asignado."""
        hu = UserStory(
            id=10,
            project_id=1,
            story_id="AER25-101",
            title="Login",
            description="Desc",
            acceptance_criteria=["C1"]
        )
        return hu

    @pytest.fixture
    def mock_saved_test_plan(self):
        """TestPlan que simula el guardado en DB."""
        tp = TestPlan(
            id=100,
            user_story_id=10,
            download_token="abc123token456"
        )
        return tp

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def mock_project_repo(self, mock_project):
        """Repositorio de proyectos que devuelve el proyecto falso."""
        repo = MagicMock()
        repo.get_by_code = AsyncMock(return_value=mock_project)
        return repo

    @pytest.fixture
    def mock_user_story_repo(self, mock_user_story):
        """Repositorio de HUs: get_by_story_id devuelve None (HU nueva), create devuelve HU con ID."""
        repo = MagicMock()
        repo.get_by_story_id = AsyncMock(return_value=None)  # HU nueva
        created_hu = UserStory(
            id=10,
            project_id=1,
            story_id="AER25-101",
            title="Login",
            description="Desc",
            acceptance_criteria=["C1"]
        )
        repo.create = AsyncMock(return_value=created_hu)
        repo.update = AsyncMock(return_value=created_hu)
        return repo

    @pytest.fixture
    def mock_test_plan_repo(self, mock_saved_test_plan):
        """Repositorio de Test Plans que devuelve el TP guardado."""
        repo = MagicMock()
        repo.create = AsyncMock(return_value=mock_saved_test_plan)
        repo.get_by_token = AsyncMock(return_value=mock_saved_test_plan)
        return repo

    @pytest.mark.asyncio
    async def test_generate_test_plan_returns_expected_structure(
        self,
        mock_db,
        mock_project_repo,
        mock_user_story_repo,
        mock_test_plan_repo
    ):
        """
        Al generar un Test Plan con AIService mockeado,
        el servicio devuelve token, analysis, download_url y filename.
        """
        with patch("app.services.test_plan_service.AIService") as MockAIService:
            mock_ai_instance = MagicMock()
            mock_ai_instance.generate_test_plan_from_story = AsyncMock(
                return_value=FAKE_TEST_PLAN_MD
            )
            MockAIService.return_value = mock_ai_instance

            service = TestPlanService(
                db=mock_db,
                user_story_repo=mock_user_story_repo,
                test_plan_repo=mock_test_plan_repo,
                project_repo=mock_project_repo
            )

            result = await service.generate_test_plan(
                story_id="AER25-101",
                title="Pantalla de Login",
                description="Como usuario quiero autenticarme",
                acceptance_criteria="C1\nC2",
                project_code="AEROMAN"
            )

            assert "token" in result
            assert "test_plan_id" in result
            assert "analysis" in result
            assert "download_url" in result
            assert "filename" in result
            assert result["token"] == "abc123token456"
            assert "/api/v1/download/" in result["download_url"]
            assert result["filename"].endswith(".xlsx")

    @pytest.mark.asyncio
    async def test_generate_test_plan_calls_ai_service_once(
        self,
        mock_db,
        mock_project_repo,
        mock_user_story_repo,
        mock_test_plan_repo
    ):
        """Verifica que el AIService se llame exactamente una vez."""
        with patch("app.services.test_plan_service.AIService") as MockAIService:
            mock_ai_instance = MagicMock()
            mock_ai_instance.generate_test_plan_from_story = AsyncMock(
                return_value=FAKE_TEST_PLAN_MD
            )
            MockAIService.return_value = mock_ai_instance

            service = TestPlanService(
                db=mock_db,
                user_story_repo=mock_user_story_repo,
                test_plan_repo=mock_test_plan_repo,
                project_repo=mock_project_repo
            )

            await service.generate_test_plan(
                story_id="AER25-101",
                title="Login",
                description="Desc",
                acceptance_criteria="C1",
                project_code="AEROMAN"
            )

            mock_ai_instance.generate_test_plan_from_story.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_test_plan_project_not_found_raises(
        self,
        mock_db,
        mock_user_story_repo,
        mock_test_plan_repo
    ):
        """
        Si el proyecto no existe, debe lanzar error.
        Nota: El servicio envuelve ValidationError en AIServiceError.
        """
        project_repo = MagicMock()
        project_repo.get_by_code = AsyncMock(return_value=None)

        with patch("app.services.test_plan_service.AIService") as MockAIService:
            service = TestPlanService(
                db=mock_db,
                user_story_repo=mock_user_story_repo,
                test_plan_repo=mock_test_plan_repo,
                project_repo=project_repo
            )

            with pytest.raises(AIServiceError) as exc_info:
                await service.generate_test_plan(
                    story_id="AER25-101",
                    title="Login",
                    description="Desc",
                    acceptance_criteria="C1",
                    project_code="PROYECTO_INEXISTENTE"
                )

            assert "no encontrado" in str(exc_info.value).lower()
