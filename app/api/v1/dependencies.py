"""
Dependencias para endpoints de la API v1.
"""
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.repositories.interfaces.user_story_repository import UserStoryRepository
from app.repositories.interfaces.test_plan_repository import TestPlanRepository
from app.repositories.interfaces.project_repository import ProjectRepository
from app.repositories.sqlalchemy.user_story_repository import SQLAlchemyUserStoryRepository
from app.repositories.sqlalchemy.test_plan_repository import SQLAlchemyTestPlanRepository
from app.repositories.sqlalchemy.project_repository import SQLAlchemyProjectRepository
from app.services.test_plan_service import TestPlanService


def get_user_story_repository(db: Session = Depends(get_db)) -> UserStoryRepository:
    """Factory para UserStoryRepository"""
    return SQLAlchemyUserStoryRepository(db)


def get_test_plan_repository(db: Session = Depends(get_db)) -> TestPlanRepository:
    """Factory para TestPlanRepository"""
    return SQLAlchemyTestPlanRepository(db)


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    """Factory para ProjectRepository"""
    return SQLAlchemyProjectRepository(db)


def get_test_plan_service(
    db: Session = Depends(get_db),
    user_story_repo: UserStoryRepository = Depends(get_user_story_repository),
    test_plan_repo: TestPlanRepository = Depends(get_test_plan_repository),
    project_repo: ProjectRepository = Depends(get_project_repository)
) -> TestPlanService:
    """Factory para TestPlanService con todas sus dependencias"""
    return TestPlanService(
        db=db,
        user_story_repo=user_story_repo,
        test_plan_repo=test_plan_repo,
        project_repo=project_repo
    )
