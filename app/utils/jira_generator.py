"""
Generador de exportación en formato compatible con Jira/Xray (CSV para importación).
Columnas típicas para Test issue type: Summary, Description, Priority, Steps.
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


def generate_jira_from_test_plan(hu_md: str, test_plan_md: str) -> Tuple[io.BytesIO, str]:
    """
    Genera un CSV listo para importar en Jira (Test issue type).
    Columnas: Summary, Description, Priority, Precondition, Expected Result, Test Key (opcional).
    """
    hu_id = extract_hu_id_from_markdown(hu_md)
    hu_title = extract_hu_title_from_markdown(hu_md)
    clean_title = clean_filename(hu_title)
    filename = f"{hu_id}_{clean_title}_jira.csv"

    test_cases = parse_markdown_table_to_dict(test_plan_md)
    # Formato compatible con importación Jira: Summary (obligatorio), Description, Priority
    columns = [
        "Summary",
        "Description",
        "Priority",
        "Precondition",
        "Expected Result",
        "Test ID",
    ]

    bio = io.BytesIO()
    text_buffer = io.TextIOWrapper(bio, encoding="utf-8-sig", newline="")
    writer = csv.writer(text_buffer)
    writer.writerow(columns)
    for tc in test_cases:
        tc_id = tc.get("tc_id", "") or ""
        title = tc.get("title", "") or ""
        summary = f"{tc_id} - {title}".strip(" - ") if tc_id or title else "Test case"
        precondition = tc.get("precondition", "") or ""
        expected = tc.get("expected_validation", "") or ""
        description = f"{precondition}\n\nValidación esperada: {expected}".strip()
        writer.writerow([
            summary,
            description,
            tc.get("priority", "Medium"),
            precondition,
            expected,
            tc_id,
        ])
    text_buffer.flush()
    # Devolver un BytesIO nuevo con los bytes ya escritos (evita problemas al hacer streaming)
    content = bio.getvalue()
    return io.BytesIO(content), filename
