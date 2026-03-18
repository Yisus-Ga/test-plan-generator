"""
Generador de exportación JSON para Test Plans.
"""
import io
import json
from typing import Tuple, List, Dict, Any
from app.utils.markdown_parser import (
    parse_markdown_table_to_dict,
    extract_hu_id_from_markdown,
    extract_hu_title_from_markdown,
)
from app.utils.excel_generator import clean_filename


def generate_json_from_test_plan(hu_md: str, test_plan_md: str) -> Tuple[io.BytesIO, str]:
    """
    Genera un archivo JSON en memoria con la estructura del Test Plan y casos de prueba.
    """
    hu_id = extract_hu_id_from_markdown(hu_md)
    hu_title = extract_hu_title_from_markdown(hu_md)
    clean_title = clean_filename(hu_title)
    filename = f"{hu_id}_{clean_title}.json"

    test_cases = parse_markdown_table_to_dict(test_plan_md)
    payload: Dict[str, Any] = {
        "user_story": {
            "id": hu_id,
            "title": hu_title,
        },
        "test_cases": [
            {
                "priority": tc.get("priority", ""),
                "tc_id": tc.get("tc_id", ""),
                "title": tc.get("title", ""),
                "precondition": tc.get("precondition", ""),
                "expected_validation": tc.get("expected_validation", ""),
                "obtained_result": tc.get("obtained_result", ""),
            }
            for tc in test_cases
        ],
    }

    bio = io.BytesIO()
    bio.write(json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"))
    bio.seek(0)
    return bio, filename
