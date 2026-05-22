"""
Endpoint para generación de reportes de bugs formales con IA.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.v1.dependencies import get_db
from app.db.models import TestPlanORM, UserStoryORM
from app.schemas.bug_report import BugReportRequest, BugReportResponse
from app.services.bug_report_service import BugReportService
from app.core.exceptions import handle_app_exception, AIServiceError

router = APIRouter(prefix="/api/v1", tags=["bug-report"])


@router.post("/reporte-bug", response_model=BugReportResponse)
async def reporte_bug(
    body: BugReportRequest,
    db: Session = Depends(get_db),
):
    """
    Genera un reporte de bug técnico y formal a partir de una descripción informal del tester.
    Obtiene el contexto (HU, criterios, resumen) desde la BD usando el test_plan_id.
    """
    test_plan_orm = (
        db.query(TestPlanORM)
        .options(joinedload(TestPlanORM.user_story))
        .filter(TestPlanORM.id == body.test_plan_id)
        .first()
    )
    if not test_plan_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test Plan no encontrado",
        )
    user_story: UserStoryORM = test_plan_orm.user_story
    if not user_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historia de Usuario no encontrada para este Test Plan",
        )

    ac_list = user_story.acceptance_criteria or []
    criterios = "\n".join(f"- {ac}" for ac in ac_list) if ac_list else "Sin criterios definidos"
    historia_definicion = user_story.description or user_story.title or ""
    resumen_test_plan = test_plan_orm.summary or test_plan_orm.objective or ""

    try:
        content = BugReportService().generar_reporte(
            descripcion_informal=body.descripcion_informal,
            historia_definicion=historia_definicion,
            criterios_aceptacion=criterios,
            resumen_test_plan=resumen_test_plan,
        )
        return BugReportResponse(content=content)
    except AIServiceError as e:
        raise handle_app_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando reporte de bug: {str(e)}",
        )
