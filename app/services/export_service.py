"""
Servicio para exportación de Test Plans.
"""
from typing import Tuple, Optional
import io
from app.utils.excel_generator import generate_excel_from_test_plan
from app.utils.csv_generator import generate_csv_from_test_plan
from app.utils.jira_generator import generate_jira_from_test_plan
from app.utils.json_generator import generate_json_from_test_plan

# Formatos soportados
EXPORT_FORMATS = ("xlsx", "csv", "jira", "json")

# Media types por formato
MEDIA_TYPES = {
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv; charset=utf-8",
    "jira": "text/csv; charset=utf-8",
    "json": "application/json; charset=utf-8",
}


class ExportService:
    """Servicio para exportar Test Plans a diferentes formatos"""

    def generate_excel(self, hu_md: str, test_plan_md_es: str) -> Tuple[io.BytesIO, str]:
        """Genera un archivo Excel desde un Test Plan."""
        return generate_excel_from_test_plan(hu_md, test_plan_md_es)

    def generate_csv(self, hu_md: str, test_plan_md_es: str) -> Tuple[io.BytesIO, str]:
        """Genera un archivo CSV desde un Test Plan."""
        return generate_csv_from_test_plan(hu_md, test_plan_md_es)

    def generate_jira(self, hu_md: str, test_plan_md_es: str) -> Tuple[io.BytesIO, str]:
        """Genera un CSV compatible con Jira/Xray desde un Test Plan."""
        return generate_jira_from_test_plan(hu_md, test_plan_md_es)

    def generate_json(self, hu_md: str, test_plan_md_es: str) -> Tuple[io.BytesIO, str]:
        """Genera un archivo JSON desde un Test Plan."""
        return generate_json_from_test_plan(hu_md, test_plan_md_es)

    def export(
        self,
        hu_md: str,
        test_plan_md_es: str,
        format: str = "xlsx",
    ) -> Tuple[io.BytesIO, str, str]:
        """
        Genera el archivo en el formato indicado.
        Returns:
            Tupla (BytesIO, filename, media_type)
        """
        fmt = (format or "xlsx").lower().strip()
        if fmt not in EXPORT_FORMATS:
            fmt = "xlsx"

        if fmt == "xlsx":
            bio, filename = self.generate_excel(hu_md, test_plan_md_es)
        elif fmt == "csv":
            bio, filename = self.generate_csv(hu_md, test_plan_md_es)
        elif fmt == "jira":
            bio, filename = self.generate_jira(hu_md, test_plan_md_es)
        else:  # json
            bio, filename = self.generate_json(hu_md, test_plan_md_es)

        media_type = MEDIA_TYPES.get(fmt, MEDIA_TYPES["xlsx"])
        return bio, filename, media_type
