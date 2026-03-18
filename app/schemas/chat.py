"""
Schemas Pydantic para Chat.
"""
from pydantic import BaseModel
from typing import List, Literal


class ChatMessage(BaseModel):
    """Un mensaje del chat (usuario o asistente)."""
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Request para enviar mensaje(s) al chat con contexto del Test Plan."""
    test_plan_id: int
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    """Respuesta del modelo en el chat."""
    content: str
