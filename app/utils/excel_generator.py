"""
Utilidades para generar archivos Excel.
"""
import io
import re
import pandas as pd
from typing import Tuple
from app.utils.markdown_parser import parse_markdown_table_to_dict, extract_hu_id_from_markdown, extract_hu_title_from_markdown


def clean_filename(name: str) -> str:
    """Limpia un nombre para que sea válido como nombre de archivo"""
    return re.sub(r'[\\/*?:"<>|\s]+', "_", name).strip("_")


def generate_excel_from_test_plan(
    hu_md: str,
    test_plan_md: str
) -> Tuple[io.BytesIO, str]:
    """
    Genera un archivo Excel en memoria a partir del Test Plan.
    
    Args:
        hu_md: Markdown de la Historia de Usuario
        test_plan_md: Markdown del Test Plan en español
        
    Returns:
        Tupla con (BytesIO del archivo, nombre del archivo)
    """
    # Extraer información de la HU
    hu_id = extract_hu_id_from_markdown(hu_md)
    hu_title = extract_hu_title_from_markdown(hu_md)
    
    # Limpiar título para nombre de archivo
    clean_title = clean_filename(hu_title)
    filename = f"{hu_id}_{clean_title}.xlsx"
    
    # Parsear tabla del Test Plan
    test_cases = parse_markdown_table_to_dict(test_plan_md)
    
    # Crear DataFrame
    if test_cases:
        df = pd.DataFrame(test_cases)
        # Renombrar columnas para Excel
        df.columns = ["Prioridad", "ID CP", "Título", "Precondición", "Validación Esperada", "Resultado Obtenido"]
    else:
        # DataFrame vacío con las columnas correctas
        df = pd.DataFrame(columns=[
            "Prioridad", "ID CP", "Título", "Precondición", 
            "Validación Esperada", "Resultado Obtenido"
        ])
    
    # Generar Excel en memoria
    bio = io.BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="TestPlan")
    bio.seek(0)
    
    return bio, filename
