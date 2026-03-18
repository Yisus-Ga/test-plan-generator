"""
Servicio para gestión de Test Plans.
"""
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.services.ai_service import AIService
from app.services.user_story_service import UserStoryService
from app.domain.entities.user_story import UserStory
from app.domain.entities.test_plan import TestPlan, TestCase
from app.repositories.interfaces.user_story_repository import UserStoryRepository
from app.repositories.interfaces.test_plan_repository import TestPlanRepository
from app.repositories.interfaces.project_repository import ProjectRepository
from app.utils.markdown_parser import clean_markdown_for_display, parse_markdown_table_to_dict
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError, ValidationError

logger = get_logger(__name__)


class TestPlanService:
    """Servicio para operaciones con Test Plans"""
    
    def __init__(
        self,
        db: Session,
        user_story_repo: UserStoryRepository,
        test_plan_repo: TestPlanRepository,
        project_repo: ProjectRepository
    ):
        self.db = db
        self.ai_service = AIService()
        self.user_story_service = UserStoryService()
        self.user_story_repo = user_story_repo
        self.test_plan_repo = test_plan_repo
        self.project_repo = project_repo
    
    async def generate_test_plan(
        self,
        story_id: str,
        title: str,
        description: str,
        acceptance_criteria: str,
        project_code: str
    ) -> dict:
        """
        Genera un Test Plan desde datos de formulario y lo guarda en la base de datos.
        
        Args:
            story_id: ID de la HU
            title: Título
            description: Descripción
            acceptance_criteria: Criterios de aceptación
            project_code: Código del proyecto (obligatorio)
            
        Returns:
            Diccionario con token, analysis, download_url, filename
        """
        try:
            # 1. Obtener o validar proyecto
            project = await self.project_repo.get_by_code(project_code)
            if not project:
                raise ValidationError(f"Proyecto con código '{project_code}' no encontrado")
            
            # 2. Crear UserStory desde formulario
            user_story = self.user_story_service.create_user_story_from_form(
                story_id=story_id,
                title=title,
                description=description,
                acceptance_criteria=acceptance_criteria
            )
            
            # 3. Asignar proyecto a la UserStory
            user_story.project_id = project.id
            
            # 4. Verificar si ya existe una HU con este story_id
            existing_hu = await self.user_story_repo.get_by_story_id(story_id)
            if existing_hu:
                user_story.id = existing_hu.id
                user_story.version = existing_hu.version + 1
                user_story = await self.user_story_repo.update(user_story)
            else:
                # 5. Guardar UserStory en base de datos
                user_story = await self.user_story_repo.create(user_story)
            
            # 4. Generar Test Plan con IA
            test_plan_md_es = await self.ai_service.generate_test_plan_from_story(user_story)
            
            # 5. Parsear test cases de la tabla markdown
            test_cases_dict = parse_markdown_table_to_dict(test_plan_md_es)
            test_cases = [
                TestCase(
                    tc_id=tc["tc_id"],
                    priority=tc["priority"],
                    title=tc["title"],
                    precondition=tc["precondition"],
                    expected_validation=tc["expected_validation"],
                    obtained_result=tc["obtained_result"]
                )
                for tc in test_cases_dict
            ]
            
            # 8. Contar casos por prioridad
            high_count = sum(1 for tc in test_cases if tc.priority.upper() == "HIGH" or tc.priority.upper() == "ALTA")
            medium_count = sum(1 for tc in test_cases if tc.priority.upper() == "MEDIUM" or tc.priority.upper() == "MEDIA")
            low_count = sum(1 for tc in test_cases if tc.priority.upper() == "LOW" or tc.priority.upper() == "BAJA")
            
            # 9. Extraer objetivo y resumen del markdown
            clean_analysis = clean_markdown_for_display(test_plan_md_es)
            lines = clean_analysis.splitlines()
            objective = ""
            summary = ""
            
            # Buscar objetivo y resumen en el markdown
            for i, line in enumerate(lines):
                if "objetivo" in line.lower() or "objective" in line.lower():
                    # Tomar las siguientes líneas hasta encontrar un título o fin
                    j = i + 1
                    while j < len(lines) and (not lines[j].startswith("#") or len(lines[j].strip()) == 0):
                        if lines[j].strip():
                            objective += lines[j].strip() + " "
                        j += 1
                    break
            
            # Resumen es típicamente la primera sección
            if lines:
                summary = lines[0] if len(lines[0]) < 200 else lines[0][:200] + "..."
            
            # 10. Crear entidad TestPlan
            test_plan = TestPlan(
                user_story_id=user_story.id,
                objective=objective.strip() or "Test Plan generado automáticamente",
                summary=summary.strip() or "Análisis de Test Plan",
                total_cases=len(test_cases),
                high_priority_count=high_count,
                medium_priority_count=medium_count,
                low_priority_count=low_count,
                analysis_markdown=clean_analysis,
                test_plan_markdown=test_plan_md_es,
                test_cases=test_cases,
                download_token=uuid.uuid4().hex
            )
            
            # 11. Guardar TestPlan en base de datos
            saved_test_plan = await self.test_plan_repo.create(test_plan)
            
            # 12. Generar nombre de archivo
            filename = f"{story_id}_{title[:50]}.xlsx"
            filename = filename.replace(" ", "_").replace("/", "_")
            filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-", "."))
            
            logger.info(f"Test Plan generado y guardado en DB: ID={saved_test_plan.id}, HU={story_id}")
            
            return {
                "token": saved_test_plan.download_token,
                "test_plan_id": saved_test_plan.id,
                "analysis": saved_test_plan.analysis_markdown,
                "download_url": f"/api/v1/download/{saved_test_plan.download_token}",
                "filename": filename
            }
            
        except AIServiceError as e:
            logger.error(f"Error en servicio de IA: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generando Test Plan: {e}")
            raise AIServiceError(f"Error al generar Test Plan: {str(e)}")
    
    async def get_test_plan_by_token(self, token: str) -> Optional[TestPlan]:
        """
        Obtiene un Test Plan por token.
        
        Args:
            token: Token del Test Plan
            
        Returns:
            Entidad TestPlan o None
        """
        return await self.test_plan_repo.get_by_token(token)
