"""
Tests unitarios para app.utils.excel_generator
"""
import pytest
from app.utils.excel_generator import clean_filename, generate_excel_from_test_plan


class TestCleanFilename:
    """Tests para clean_filename"""

    def test_replaces_spaces_with_underscores(self):
        """Reemplaza espacios por guiones bajos"""
        assert clean_filename("Nombre con espacios") == "Nombre_con_espacios"

    def test_removes_invalid_chars(self):
        """Elimina caracteres inválidos para nombres de archivo"""
        invalid = 'archivo<>:"/\\|?*'
        result = clean_filename(invalid)
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result
        assert "/" not in result
        assert "\\" not in result
        assert "|" not in result
        assert "?" not in result
        assert "*" not in result

    def test_strips_leading_trailing_underscores(self):
        """Elimina guiones bajos al inicio y final"""
        assert clean_filename("___nombre___") == "nombre"
        assert clean_filename("  nombre  ") == "nombre"

    def test_valid_filename_unchanged(self):
        """Nombre válido (letras, números, guiones) se mantiene"""
        assert clean_filename("AER25-101_Login") == "AER25-101_Login"

    def test_empty_string_returns_empty(self):
        """String vacío retorna vacío"""
        assert clean_filename("") == ""

    def test_only_invalid_chars_returns_empty(self):
        """Solo caracteres inválidos retorna string vacío"""
        result = clean_filename('<>:"/\\|?*  ')
        assert result == "" or len(result.strip()) == 0


class TestGenerateExcelFromTestPlan:
    """Tests para generate_excel_from_test_plan"""

    def test_generates_excel_bytes_and_filename(self):
        """Genera BytesIO y nombre de archivo correcto"""
        hu_md = """
- ID: AER25-101
- Title: Pantalla de Login
"""
        test_plan_md = """
| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Login válido | Usuario existe | Muestra dashboard | |
"""
        bio, filename = generate_excel_from_test_plan(hu_md, test_plan_md)
        assert bio is not None
        assert bio.read(4) == b"PK\x03\x04"  # Zip/Excel magic bytes
        assert filename.startswith("AER25-101")
        assert filename.endswith(".xlsx")
        assert "Login" in filename

    def test_empty_test_plan_generates_empty_excel(self):
        """Test plan sin tabla genera Excel con columnas vacías"""
        hu_md = "- ID: XY-1\n- Title: Test"
        test_plan_md = "Solo texto, sin tabla"
        bio, filename = generate_excel_from_test_plan(hu_md, test_plan_md)
        assert bio is not None
        assert "XY-1" in filename
        assert filename.endswith(".xlsx")

    def test_excel_contains_expected_columns(self):
        """El Excel generado tiene las columnas esperadas"""
        import pandas as pd
        hu_md = "- ID: T1\n- Title: T"
        test_plan_md = """
| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | T | P | V | |
"""
        bio, _ = generate_excel_from_test_plan(hu_md, test_plan_md)
        bio.seek(0)
        df = pd.read_excel(bio)
        expected = ["Prioridad", "ID CP", "Título", "Precondición", "Validación Esperada", "Resultado Obtenido"]
        for col in expected:
            assert col in df.columns
