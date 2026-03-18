"""
Configuración de logging estructurado.
"""
import logging
import sys
from pathlib import Path
from app.config import settings


def setup_logging():
    """Configurar logging de la aplicación"""
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True, parents=True)
    
    # Configurar formato
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configurar nivel
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Handlers
    handlers = [
        logging.StreamHandler(sys.stdout),  # Consola
    ]
    
    # Agregar archivo si está configurado
    if settings.LOG_FILE:
        handlers.append(logging.FileHandler(settings.LOG_FILE))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )
    
    # Reducir verbosidad de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Obtener logger con nombre"""
    return logging.getLogger(name)
