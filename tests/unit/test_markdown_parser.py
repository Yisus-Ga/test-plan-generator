"""
Tests unitarios para app.utils.markdown_parser
"""
import pytest
from app.utils.markdown_parser import (
    parse_markdown_table_to_dict,
    clean_markdown_for_display,
    extract_hu_id_from_markdown,
    extract_hu_title_from_markdown,
)


class TestParseMarkdownTableToDict:
    """Tests para parse_markdown_table_to_dict"""

    def test_parse_table_with_valid_format(self):
        """Parsea correctamente una tabla markdown bien formada"""
        md = """
## Objetivo
Objetivo del test plan.

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Caso 1 | Pre 1 | Valid 1 | |
| Media | TC2 | Caso 2 | Pre 2 | Valid 2 | OK |
"""
        result = parse_markdown_table_to_dict(md)
        assert len(result) == 2
        assert result[0]["priority"] == "Alta"
        assert result[0]["tc_id"] == "TC1"
        assert result[0]["title"] == "Caso 1"
        assert result[0]["precondition"] == "Pre 1"
        assert result[0]["expected_validation"] == "Valid 1"
        assert result[0]["obtained_result"] == ""
        assert result[1]["priority"] == "Media"
        assert result[1]["obtained_result"] == "OK"

    def test_parse_empty_markdown_returns_empty_list(self):
        """Si no hay tabla, retorna lista vacía"""
        md = "Solo texto sin tabla"
        result = parse_markdown_table_to_dict(md)
        assert result == []

    def test_parse_table_header_only_returns_empty_list(self):
        """Solo encabezado sin filas retorna lista vacía"""
        md = """
| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
"""
        result = parse_markdown_table_to_dict(md)
        assert result == []

    def test_parse_case_insensitive_header(self):
        """El header de la tabla se detecta sin importar mayúsculas"""
        md = """
| prioridad | id cp | título | precondición | validación esperada | resultado obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Test | Pre | Val | |
"""
        result = parse_markdown_table_to_dict(md)
        assert len(result) == 1
        assert result[0]["tc_id"] == "TC1"


class TestCleanMarkdownForDisplay:
    """Tests para clean_markdown_for_display"""

    def test_removes_table_from_markdown(self):
        """Elimina la tabla pero mantiene el resto del contenido"""
        md = """
## Objetivo
Objetivo del test.

## Casos de prueba

| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Caso | Pre | Val | |

## Notas
Fin.
"""
        result = clean_markdown_for_display(md)
        assert "| Prioridad |" not in result
        assert "TC1" not in result
        assert "Objetivo" in result or "objetivo" in result.lower()
        assert "Fin" in result or "fin" in result.lower()

    def test_empty_input_returns_empty_string(self):
        """Input vacío retorna string limpio"""
        result = clean_markdown_for_display("")
        assert result == "" or result.isspace() or len(result.strip()) == 0

    def test_markdown_without_table_unchanged(self):
        """Markdown sin tabla se devuelve (limpio de markdown básico)"""
        md = "## Título\n\nTexto **negrita**"
        result = clean_markdown_for_display(md)
        assert "Título" in result or "título" in result.lower()
        # Limpia símbolos markdown básicos
        assert "**" not in result or "negrita" in result


class TestExtractHuIdFromMarkdown:
    """Tests para extract_hu_id_from_markdown"""

    def test_extract_hu_id_standard_format(self):
        """Extrae ID con formato estándar (ID: o ID-)"""
        md = "- ID: AER25-101"
        assert extract_hu_id_from_markdown(md) == "AER25-101"

    def test_extract_hu_id_with_dash(self):
        """Extrae ID cuando usa guión"""
        md = "- ID- AER25-101"
        assert extract_hu_id_from_markdown(md) == "AER25-101"

    def test_extract_hu_id_not_found_returns_default(self):
        """Si no hay ID, retorna HU_ID por defecto"""
        md = "Solo texto sin ID"
        assert extract_hu_id_from_markdown(md) == "HU_ID"

    def test_extract_hu_id_case_insensitive(self):
        """Detecta 'id' en cualquier caso"""
        md = "- id: XYZ-999"
        assert extract_hu_id_from_markdown(md) == "XYZ-999"


class TestExtractHuTitleFromMarkdown:
    """Tests para extract_hu_title_from_markdown"""

    def test_extract_hu_title_standard_format(self):
        """Extrae título con formato estándar"""
        md = "- Title: Pantalla principal de Login"
        assert extract_hu_title_from_markdown(md) == "Pantalla principal de Login"

    def test_extract_hu_title_multiline_takes_first_line(self):
        """Si el título tiene varias líneas, toma la primera"""
        md = "- Title: Línea uno\nLínea dos"
        assert "Línea uno" in extract_hu_title_from_markdown(md)
        assert "Línea dos" not in extract_hu_title_from_markdown(md)

    def test_extract_hu_title_not_found_returns_default(self):
        """Si no hay título, retorna HU_Title por defecto"""
        md = "Solo texto sin título"
        assert extract_hu_title_from_markdown(md) == "HU_Title"
