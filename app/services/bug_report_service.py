"""
Servicio para generación de reportes de bugs formales con IA (GPT-4.1).
"""
import logging
from openai import OpenAI
from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError
from app.core.standards import ISO_25010_CHARACTERISTICS

logger = get_logger(__name__)

BUG_REPORT_MODEL = "gpt-4.1"

SYSTEM_PROMPT = f"""Sos un QA técnico senior especializado en redacción de incidencias. \
El usuario te va a describir informalmente un bug o mejora encontrado durante el testing. \
Tu tarea es redactar un reporte técnico y formal en español, usando el contexto de la historia de usuario provisto.

{ISO_25010_CHARACTERISTICS}

Respondé SIEMPRE con el siguiente formato exacto, sin agregar texto fuera de él:

**Título:** [título corto, descriptivo y técnico]
**Tipo:** Bug | Mejora
**Severidad:** Crítica | Alta | Media | Baja
**Prioridad sugerida:** Alta | Media | Baja
**Característica ISO 25010 afectada:** [nombre de la característica según el marco de calidad provisto]

**Descripción:**
[explicación técnica y formal del problema o mejora]

**Pasos para reproducir:**
1. [paso]
2. [paso]
3. [paso]

**Resultado actual:**
[qué comportamiento se observa hoy]

**Resultado esperado:**
[cuál es el comportamiento correcto según los criterios de aceptación]

**Criterio de aceptación afectado:**
[indicá cuál criterio se viola o cuál funcionalidad no está contemplada. Si es una mejora y no viola ningún criterio, indicá 'No aplica']

**Notas adicionales:**
[cualquier observación técnica relevante, o 'Ninguna']"""


class BugReportService:
    """Servicio para generar reportes de bugs formales a partir de descripciones informales."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _build_user_message(
        self,
        descripcion_informal: str,
        historia_definicion: str,
        criterios_aceptacion: str,
        resumen_test_plan: str,
    ) -> str:
        return f"""## Descripción informal del tester
{descripcion_informal}

## Historia de Usuario
{historia_definicion}

## Criterios de Aceptación
{criterios_aceptacion}

## Resumen del Test Plan
{resumen_test_plan}"""

    def generar_reporte(
        self,
        descripcion_informal: str,
        historia_definicion: str,
        criterios_aceptacion: str,
        resumen_test_plan: str,
    ) -> str:
        try:
            user_message = self._build_user_message(
                descripcion_informal,
                historia_definicion,
                criterios_aceptacion,
                resumen_test_plan,
            )
            response = self.client.chat.completions.create(
                model=BUG_REPORT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            choice = response.choices[0] if response.choices else None
            if not choice or not getattr(choice, "message", None):
                raise AIServiceError("Respuesta vacía del modelo de reporte de bug")
            return (choice.message.content or "").strip()
        except Exception as e:
            logger.error(f"Error generando reporte de bug: {e}")
            raise AIServiceError(f"Error generando reporte de bug: {str(e)}")
