"""
Utilidades para parsear Markdown de Test Plans.
"""
import re
from typing import List, Dict


def parse_markdown_table_to_dict(test_plan_md: str) -> List[Dict[str, str]]:
    """
    Parsea una tabla markdown del Test Plan y retorna lista de diccionarios.
    
    Args:
        test_plan_md: Markdown completo del Test Plan
        
    Returns:
        Lista de diccionarios con los casos de prueba
    """
    table_lines = []
    capture = False
    
    for line in test_plan_md.splitlines():
        if re.match(r"\| *Prioridad *\|", line, re.IGNORECASE):
            capture = True
            continue
        if capture:
            if line.strip() == "" or line.strip().startswith("---"):
                continue
            if line.startswith("|"):
                table_lines.append(line)
    
    # Patrón para detectar línea separadora de tabla (|----|----|...|)
    separator_pattern = re.compile(r"^[-:\s]+$")

    test_cases = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6:
            # Saltar línea separadora (todas las celdas son guiones/espacios)
            if all(separator_pattern.match(cell) for cell in cells):
                continue
            test_cases.append({
                "priority": cells[0],
                "tc_id": cells[1],
                "title": cells[2],
                "precondition": cells[3],
                "expected_validation": cells[4],
                "obtained_result": cells[5] if len(cells) > 5 else ""
            })

    return test_cases


def clean_markdown_for_display(test_plan_md: str) -> str:
    """
    Limpia el markdown del Test Plan para mostrar en el frontend (sin tabla).
    
    Args:
        test_plan_md: Markdown completo del Test Plan
        
    Returns:
        Markdown limpio sin la tabla de casos de prueba
    """
    lines = test_plan_md.splitlines()
    filtered_lines = []
    in_table = False
    
    for line in lines:
        # Detectar el inicio de la tabla
        if re.match(r"\| *Prioridad *\|", line, re.IGNORECASE):
            in_table = True
            continue
        # Si estamos dentro de la tabla, saltar esas líneas
        if in_table:
            if not line.strip():  # Si hay una línea vacía después de la tabla, termina
                in_table = False
            continue
        filtered_lines.append(line)
    
    # Limpiar el markdown básico para que se vea más "texto plano"
    clean_analysis = re.sub(r"[*_#>`]", "", "\n".join(filtered_lines))
    clean_analysis = re.sub(r"\n{3,}", "\n\n", clean_analysis).strip()
    
    return clean_analysis


def extract_hu_id_from_markdown(hu_md: str) -> str:
    """Extrae el ID de la HU del markdown"""
    match = re.search(r"[-\s]*ID[:\-]\s*([A-Za-z0-9_-]+)", hu_md, re.IGNORECASE)
    return match.group(1).strip() if match else "HU_ID"


def extract_hu_title_from_markdown(hu_md: str) -> str:
    """Extrae el título de la HU del markdown"""
    match = re.search(r"[-\s]*Title[:\-]\s*(.+)", hu_md, re.IGNORECASE)
    if match:
        return match.group(1).strip().splitlines()[0].strip()
    return "HU_Title"
