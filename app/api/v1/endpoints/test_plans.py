"""
Endpoints para Test Plans.
"""
from fastapi import APIRouter, Form, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.services.test_plan_service import TestPlanService
from app.services.export_service import ExportService
from app.domain.entities.test_plan import TestPlan
from app.core.exceptions import handle_app_exception, AIServiceError
from app.api.v1.dependencies import get_test_plan_service
from app.db.session import get_db
from app.schemas.test_plan import TestPlanListItem, TestPlanResponse
from app.repositories.interfaces.test_plan_repository import TestPlanRepository
from app.repositories.sqlalchemy.test_plan_repository import SQLAlchemyTestPlanRepository
from app.db.models import TestPlanORM, UserStoryORM, ProjectORM
from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/api/v1", tags=["test-plans"])


def get_test_plan_repository(db: Session = Depends(get_db)) -> TestPlanRepository:
    """Factory para TestPlanRepository"""
    return SQLAlchemyTestPlanRepository(db)


@router.post("/analyze/")
async def analyze(
    hu_id: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    acceptance_criteria: str = Form(...),
    project_code: str = Form(...),  # Código del proyecto
    service: TestPlanService = Depends(get_test_plan_service)
):
    """
    Analiza una Historia de Usuario y genera un Test Plan.
    Los datos se guardan en la base de datos.
    Requiere project_code (obligatorio).
    """
    try:
        # Validar que todos los campos estén presentes
        if not all([hu_id, title, description, acceptance_criteria, project_code]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos: hu_id, title, description, acceptance_criteria, project_code"
            )
        
        # Generar Test Plan (ahora con proyecto)
        result = await service.generate_test_plan(
            story_id=hu_id,
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            project_code=project_code
        )
        
        return JSONResponse(result)
        
    except AIServiceError as e:
        http_exception = handle_app_exception(e)
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/test-plans/", response_model=List[TestPlanListItem])
async def list_test_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_code: Optional[str] = Query(None, description="Filtrar por código de proyecto"),
    story_id: Optional[str] = Query(None, description="Filtrar por ID de HU"),
    search: Optional[str] = Query(None, description="Búsqueda por texto (en título de HU o proyecto)"),
    date_from: Optional[datetime] = Query(None, description="Fecha desde (ISO format)"),
    date_to: Optional[datetime] = Query(None, description="Fecha hasta (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Listar Test Plans con filtros opcionales.
    Filtros disponibles: project_code, story_id, search (texto), date_from, date_to
    """
    try:
        # Query base con joins y eager loading de relaciones
        query = db.query(TestPlanORM).options(
            joinedload(TestPlanORM.user_story).joinedload(UserStoryORM.project)
        ).join(UserStoryORM).join(ProjectORM)
        
        # Aplicar filtros
        if project_code:
            query = query.filter(ProjectORM.code.ilike(f"%{project_code}%"))
        
        if story_id:
            query = query.filter(UserStoryORM.story_id.ilike(f"%{story_id}%"))
        
        if search:
            search_filter = or_(
                UserStoryORM.title.ilike(f"%{search}%"),
                UserStoryORM.story_id.ilike(f"%{search}%"),
                ProjectORM.name.ilike(f"%{search}%"),
                ProjectORM.code.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if date_from:
            query = query.filter(TestPlanORM.created_at >= date_from)
        
        if date_to:
            query = query.filter(TestPlanORM.created_at <= date_to)
        
        # Ordenar por fecha descendente (más recientes primero)
        query = query.order_by(TestPlanORM.created_at.desc())
        
        # Paginación
        test_plans = query.offset(skip).limit(limit).all()
        
        # Convertir a schema de respuesta
        result = []
        for tp in test_plans:
            # Asegurar que las relaciones estén cargadas
            if not hasattr(tp, 'user_story') or tp.user_story is None:
                continue
            if not hasattr(tp.user_story, 'project') or tp.user_story.project is None:
                continue
                
            result.append(TestPlanListItem(
                id=tp.id,
                user_story_id=tp.user_story_id,
                user_story_story_id=tp.user_story.story_id,
                user_story_title=tp.user_story.title,
                project_code=tp.user_story.project.code,
                project_name=tp.user_story.project.name,
                total_cases=tp.total_cases,
                created_at=tp.created_at
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar Test Plans: {str(e)}"
        )


@router.get("/test-plans/{test_plan_id}", response_model=TestPlanResponse)
async def get_test_plan(
    test_plan_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un Test Plan completo por ID"""
    test_plan_orm = db.query(TestPlanORM).filter(TestPlanORM.id == test_plan_id).first()
    if not test_plan_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test Plan no encontrado"
        )
    
    # Obtener test cases
    from app.schemas.test_plan import TestCaseResponse
    test_cases = [
        TestCaseResponse(
            priority=tc.priority,
            tc_id=tc.tc_id,
            title=tc.title,
            precondition=tc.precondition or "",
            expected_validation=tc.expected_validation,
            obtained_result=tc.obtained_result or ""
        )
        for tc in test_plan_orm.test_cases
    ]
    
    try:
        return TestPlanResponse(
            id=test_plan_orm.id,
            user_story_id=test_plan_orm.user_story_id,
            objective=test_plan_orm.objective,
            summary=test_plan_orm.summary,
            total_cases=test_plan_orm.total_cases,
            high_priority_count=test_plan_orm.high_priority_count,
            medium_priority_count=test_plan_orm.medium_priority_count,
            low_priority_count=test_plan_orm.low_priority_count,
            notes=test_plan_orm.notes,
            analysis=test_plan_orm.analysis_markdown,
            test_cases=test_cases,
            download_token=test_plan_orm.download_token,
            created_at=test_plan_orm.created_at,
            updated_at=test_plan_orm.updated_at
        )
    except Exception as e:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error al obtener Test Plan {test_plan_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener Test Plan: {str(e)}"
        )


@router.delete("/test-plans/{test_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_plan(
    test_plan_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un Test Plan por ID"""
    test_plan = db.query(TestPlanORM).filter(TestPlanORM.id == test_plan_id).first()
    if not test_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test Plan no encontrado"
        )
    
    try:
        db.delete(test_plan)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar Test Plan: {str(e)}"
        )


@router.get("/download/{token}")
async def download(
    token: str,
    export_format: Optional[str] = Query("xlsx", alias="format", description="Formato: xlsx, csv, jira, json"),
    service: TestPlanService = Depends(get_test_plan_service),
):
    """
    Descarga el Test Plan en el formato indicado (xlsx, csv, jira, json).
    Por defecto devuelve Excel (.xlsx). Query param: format=xlsx|csv|jira|json
    """
    try:
        from app.services.export_service import ExportService, EXPORT_FORMATS

        fmt = (export_format or "xlsx").lower().strip()
        if fmt not in EXPORT_FORMATS:
            fmt = "xlsx"

        export_service = ExportService()

        test_plan = await service.get_test_plan_by_token(token)
        if not test_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token no válido o expirado",
            )

        from app.api.v1.dependencies import get_user_story_repository
        from app.db.session import SessionLocal

        db = SessionLocal()
        try:
            user_story_repo = get_user_story_repository(db)
            user_story = await user_story_repo.get_by_id(test_plan.user_story_id)
            if not user_story:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia de Usuario no encontrada",
                )
            hu_md = user_story.to_markdown()
        finally:
            db.close()

        bio, filename, media_type = await run_in_threadpool(
            export_service.export,
            hu_md,
            test_plan.test_plan_markdown,
            fmt,
        )

        if not filename.endswith((".xlsx", ".csv", ".json")):
            filename = filename.rstrip("_") + (".xlsx" if fmt == "xlsx" else ".csv" if fmt in ("csv", "jira") else ".json")

        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

        return StreamingResponse(bio, media_type=media_type, headers=headers)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar archivo: {str(e)}",
        )
