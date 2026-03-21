"""
Archivo de EJEMPLO con tests que fallan intencionalmente.
Sirve para practicar: ejecutar, ver el fallo, entender el mensaje de error.

Una vez que los hayas visto fallar, podemos corregirlos para que pasen.

NOTA: Solo usa markdown_parser (no excel_generator) para que funcione sin pandas.
"""
import pytest
from app.utils.markdown_parser import (
    extract_hu_id_from_markdown,
    extract_hu_title_from_markdown,
    parse_markdown_table_to_dict,
)


class TestEjemploFallidos:
    """
    Tests que fallan A PROPOSITO para que puedas ver cómo se ve un fallo.
    """

    def test_fallo_1_valor_incorrecto(self):
        """
        FALLO: El assert espera "XYZ" pero la función devuelve "AER25-101".
        Verás algo como: AssertionError: assert 'AER25-101' == 'XYZ'
        """
        md = "- ID: AER25-101"
        result = extract_hu_id_from_markdown(md)
        assert result == "XYZ"  # ← Incorrecto a propósito

    def test_fallo_2_esperamos_lista_con_3_elementos_pero_tiene_2(self):
        """
        FALLO: Verás: AssertionError: assert 2 == 3
        El markdown tiene solo 2 casos de prueba, no 3.
        """
        md = """
| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Caso 1 | Pre | Val | |
| Media | TC2 | Caso 2 | Pre | Val | |
"""
        result = parse_markdown_table_to_dict(md)
        assert len(result) == 3  # ← Incorrecto: hay 2 filas, no 3

    def test_fallo_3_parse_table_esperamos_tc3_pero_no_existe(self):
        """
        FALLO: El primer caso tiene tc_id "TC1", no "TC3".
        Verás: AssertionError: assert 'TC1' == 'TC3'
        """
        md = """
| Prioridad | ID CP | Título | Precondición | Validación Esperada | Resultado Obtenido |
|-----------|-------|--------|--------------|---------------------|-------------------|
| Alta | TC1 | Caso 1 | Pre | Val | |
"""
        result = parse_markdown_table_to_dict(md)
        assert result[0]["tc_id"] == "TC3"  # ← Incorrecto: es "TC1"

    def test_fallo_4_extract_title_caso_default(self):
        """
        FALLO: Cuando no hay título, la función devuelve "HU_Title".
        Aquí esperamos "SIN_TITULO" (que no existe).
        """
        md = "Texto sin título definido"
        result = extract_hu_title_from_markdown(md)
        assert result == "SIN_TITULO"  # ← Incorrecto: devuelve "HU_Title"

    def test_paso_este_sirve_de_referencia(self):
        """
        Este test SÍ pasa. Usalo como referencia de cómo se ve un test exitoso.
        """
        result = extract_hu_id_from_markdown("- ID: AER25-101")
        assert result == "AER25-101"  # ← Correcto
