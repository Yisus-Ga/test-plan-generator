"""
Router principal que agrupa todos los endpoints de la API v1.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import test_plans, projects, chat

api_router = APIRouter()

api_router.include_router(test_plans.router)
api_router.include_router(projects.router)
api_router.include_router(chat.router)
