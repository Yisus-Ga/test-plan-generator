"""
Generador de exportación CSV para Test Plans.
"""
import io
import csv
from typing import Tuple
from app.utils.markdown_parser import (
    parse_markdown_table_to_dict,
    extract_hu_id_from_markdown,
    extract_hu_title_from_markdown,
)
from app.utils.excel_generator import clean_filename


def generate_csv_from_test_plan(hu_md: str, test_plan_md: str) -> Tuple[io.BytesIO, str]:
    """
    Genera un archivo CSV en memoria a partir del Test Plan.
    Columnas: Prioridad, ID CP, Título, Precondición, Validación Esperada, Resultado Obtenido
    """
    hu_id = extract_hu_id_from_markdown(hu_md)
    hu_title = extract_hu_title_from_markdown(hu_md)
    clean_title = clean_filename(hu_title)
    filename = f"{hu_id}_{clean_title}.csv"

    test_cases = parse_markdown_table_to_dict(test_plan_md)
    columns = [
        "Prioridad",
        "ID CP",
        "Título",
        "Precondición",
        "Validación Esperada",
        "Resultado Obtenido",
    ]

    bio = io.BytesIO()
    text_buffer = io.TextIOWrapper(bio, encoding="utf-8-sig", newline="")
    writer = csv.writer(text_buffer)
    writer.writerow(columns)
    for tc in test_cases:
        row = [
            tc.get("priority", ""),
            tc.get("tc_id", ""),
            tc.get("title", ""),
            tc.get("precondition", ""),
            tc.get("expected_validation", ""),
            tc.get("obtained_result", ""),
        ]
        writer.writerow(row)
    text_buffer.flush()
    # Devolver un BytesIO nuevo con los bytes ya escritos (evita problemas al hacer streaming)
    content = bio.getvalue()
    return io.BytesIO(content), filename
