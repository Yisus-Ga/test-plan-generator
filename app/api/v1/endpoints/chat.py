"""
Endpoint de chat con contexto del Test Plan.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.api.v1.dependencies import get_db
from app.db.models import TestPlanORM, UserStoryORM, ProjectORM
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.exceptions import handle_app_exception, AIServiceError

router = APIRouter(prefix="/api/v1", tags=["chat"])


def _build_chat_context(
    project: ProjectORM,
    user_story: UserStoryORM,
    test_plan: TestPlanORM,
) -> str:
    """Construye el texto de contexto para el modelo: proyecto, HU y Test Plan."""
    ac_list = user_story.acceptance_criteria or []
    ac_text = "\n".join(f"- {ac}" for ac in ac_list)

    cases_lines = []
    for tc in test_plan.test_cases:
        cases_lines.append(
            f"- [{tc.priority}] {tc.tc_id}: {tc.title}\n  Precondición: {tc.precondition or '-'}\n  Validación esperada: {tc.expected_validation}\n  Resultado: {tc.obtained_result or '-'}"
        )
    cases_text = "\n".join(cases_lines) if cases_lines else "(Sin casos)"

    return f"""### Proyecto
- Código: {project.code}
- Nombre: {project.name}
- Descripción: {project.description or 'Sin descripción'}

### Historia de Usuario
- ID: {user_story.story_id}
- Título: {user_story.title}
- Descripción: {user_story.description}
- Criterios de aceptación:
{ac_text}

### Test Plan
- Objetivo: {test_plan.objective or '-'}
- Resumen: {test_plan.summary or '-'}
- Análisis (resumen): {test_plan.analysis_markdown[:4000] if test_plan.analysis_markdown else '-'}

### Casos de prueba
{cases_text}
"""


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Envía un mensaje al chat con contexto del Test Plan.
    El modelo solo responde a consultas relacionadas con el proyecto, la HU o el Test Plan.
    """
    # Cargar Test Plan con HU, proyecto y casos
    test_plan_orm = (
        db.query(TestPlanORM)
        .options(
            joinedload(TestPlanORM.user_story).joinedload(UserStoryORM.project),
            joinedload(TestPlanORM.test_cases),
        )
        .filter(TestPlanORM.id == body.test_plan_id)
        .first()
    )
    if not test_plan_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test Plan no encontrado",
        )
    user_story = test_plan_orm.user_story
    if not user_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historia de Usuario no encontrada para este Test Plan",
        )
    project = user_story.project
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado para esta HU",
        )

    context = _build_chat_context(project, user_story, test_plan_orm)
    messages = [{"role": m.role, "content": m.content} for m in body.messages]

    try:
        content = ChatService().chat(context, messages)
        return ChatResponse(content=content)
    except AIServiceError as e:
        raise handle_app_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}",
        )
