"""
Endpoints para Proyectos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectStatusUpdate
from app.services.project_service import ProjectService
from app.repositories.interfaces.project_repository import ProjectRepository
from app.repositories.sqlalchemy.project_repository import SQLAlchemyProjectRepository
from app.db.session import get_db

router = APIRouter(prefix="/api/v1", tags=["projects"])


def _to_response(p) -> ProjectResponse:
    return ProjectResponse(
        id=p.id,
        code=p.code,
        name=p.name,
        description=p.description,
        is_active=p.is_active,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    """Factory para ProjectRepository"""
    return SQLAlchemyProjectRepository(db)


def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository)
) -> ProjectService:
    """Factory para ProjectService"""
    return ProjectService(project_repo)


@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Crear un nuevo proyecto"""
    try:
        project = await service.create_project(
            code=project_data.code,
            name=project_data.name,
            description=project_data.description
        )
        return _to_response(project)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/projects/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Listar proyectos. Con active_only=true devuelve solo los activos."""
    try:
        if active_only:
            projects = await project_repo.get_all_active()
        else:
            projects = await project_repo.get_all(skip=skip, limit=limit)
        return [_to_response(p) for p in projects]
    except Exception as e:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error al listar proyectos: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar proyectos: {str(e)}"
        )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Obtener un proyecto por ID"""
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return _to_response(project)


@router.get("/projects/code/{code}", response_model=ProjectResponse)
async def get_project_by_code(
    code: str,
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Obtener un proyecto por código"""
    project = await project_repo.get_by_code(code)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return _to_response(project)


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Actualizar un proyecto existente"""
    try:
        project = await service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        return _to_response(project)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error al actualizar proyecto {project_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar proyecto: {str(e)}"
        )


@router.patch("/projects/{project_id}/status", response_model=ProjectResponse)
async def toggle_project_status(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Alternar estado activo/inactivo de un proyecto."""
    try:
        project = await service.toggle_status(project_id)
        return _to_response(project)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error al cambiar estado del proyecto {project_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar estado: {str(e)}"
        )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Eliminar un proyecto. No permite eliminar proyectos con HUs asociadas."""
    try:
        deleted = await service.delete_project(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
    except ValueError as e:
        # Error de validación (tiene HUs asociadas)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error al eliminar proyecto {project_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar proyecto: {str(e)}"
        )
