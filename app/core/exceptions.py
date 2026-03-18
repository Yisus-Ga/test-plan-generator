"""
Excepciones customizadas de la aplicación.
"""
from fastapi import HTTPException, status


class AppException(Exception):
    """Excepción base de la aplicación"""
    pass


class UserStoryNotFoundError(AppException):
    """Error cuando no se encuentra una Historia de Usuario"""
    pass


class TestPlanNotFoundError(AppException):
    """Error cuando no se encuentra un Test Plan"""
    pass


class AIServiceError(AppException):
    """Error en el servicio de IA"""
    pass


class ValidationError(AppException):
    """Error de validación de datos"""
    pass


def handle_app_exception(exception: AppException) -> HTTPException:
    """Convertir excepciones de aplicación a HTTPException"""
    if isinstance(exception, UserStoryNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception) or "Historia de Usuario no encontrada"
        )
    elif isinstance(exception, TestPlanNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception) or "Test Plan no encontrado"
        )
    elif isinstance(exception, AIServiceError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en servicio de IA: {str(exception)}"
        )
    elif isinstance(exception, ValidationError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(exception)}"
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(exception)}"
        )
