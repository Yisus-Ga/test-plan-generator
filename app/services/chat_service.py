"""
Servicio de chat con contexto del Test Plan (OpenAI Chat Completions).
"""
import logging
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError

logger = get_logger(__name__)

CHAT_MODEL = "gpt-4.1-mini"
OFF_TOPIC_RESPONSE = "Por favor, haz una consulta relacionada al test plan."


class ChatService:
    """Servicio para chat con contexto de Test Plan / HU / Proyecto."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _build_system_prompt(self, context: str) -> str:
        return f"""Eres un asistente de QA. Tienes el siguiente contexto sobre un proyecto, una Historia de Usuario (HU) y el Test Plan generado. Responde únicamente a consultas relacionadas con este proyecto, la HU o el Test Plan (casos de prueba, prioridades, cobertura, criterios de aceptación, etc.).

Si el usuario hace una pregunta o comentario que NO esté relacionado con el proyecto, la HU o el Test Plan, responde exactamente: "{OFF_TOPIC_RESPONSE}"

## Contexto

{context}
"""

    def chat(self, context: str, messages: List[Dict[str, str]]) -> str:
        """
        Envía los mensajes a OpenAI Chat Completions con el contexto en el system prompt.

        Args:
            context: Texto con descripción del proyecto, HU completa y Test Plan completo.
            messages: Lista de dicts con "role" ("user" | "assistant") y "content".

        Returns:
            Contenido de la respuesta del asistente.
        """
        try:
            system_content = self._build_system_prompt(context)
            openai_messages = [{"role": "system", "content": system_content}]

            for m in messages:
                role = m.get("role")
                content = m.get("content", "")
                if role in ("user", "assistant") and content:
                    openai_messages.append({"role": role, "content": content})

            response = self.client.chat.completions.create(
                model=CHAT_MODEL,
                messages=openai_messages,
            )
            choice = response.choices[0] if response.choices else None
            if not choice or not getattr(choice, "message", None):
                raise AIServiceError("Respuesta vacía del modelo de chat")
            return (choice.message.content or "").strip()
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            raise AIServiceError(f"Error en chat: {str(e)}")
