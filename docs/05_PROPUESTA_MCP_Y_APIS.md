# Propuesta MCP y APIs

## 🎯 Objetivo

Definir una estrategia de evolución desde APIs tradicionales hacia **MCP (Model Context Protocol)** y proponer una arquitectura híbrida que aproveche lo mejor de ambos enfoques.

---

## 📚 Contexto: ¿Qué es MCP?

**MCP (Model Context Protocol)** es un protocolo desarrollado por Anthropic para estandarizar la comunicación entre aplicaciones y modelos de IA. Permite:

- ✅ Integración más directa con LLMs
- ✅ Contexto enriquecido y persistente
- ✅ Capacidades (tools) que los modelos pueden invocar
- ✅ Mejor manejo de estado y sesiones
- ✅ Flujo más natural de interacción

---

## 🏗️ Arquitectura Propuesta: Híbrida

### Estrategia: Convivencia Gradual

**Fase 1 (Actual)**: APIs REST tradicionales
**Fase 2 (Corto plazo)**: APIs REST + Servicios MCP internos
**Fase 3 (Mediano plazo)**: APIs REST + MCP Server público
**Fase 4 (Largo plazo)**: MCP nativo como protocolo principal

---

## 🔄 Arquitectura Híbrida Propuesta

```
┌─────────────────────────────────────────────────────────┐
│ Frontend (Web App)                                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├──────────────────┬─────────────────────┐
                 │                  │                     │
                 ▼                  ▼                     ▼
        ┌─────────────┐    ┌──────────────┐    ┌──────────────┐
        │ REST API    │    │ MCP Client   │    │ WebSocket    │
        │ (FastAPI)   │    │ (Interno)    │    │ (Real-time)  │
        └─────┬───────┘    └──────┬───────┘    └──────┬───────┘
              │                   │                    │
              │                   │                    │
              ▼                   ▼                    ▼
    ┌──────────────────────────────────────────────────────────┐
    │ Backend Services                                         │
    │                                                          │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │ MCP Server                                      │    │
    │  │ - Test Plan Generation Tool                     │    │
    │  │ - User Story Analysis Tool                      │    │
    │  │ - Export Format Converter Tool                  │    │
    │  └─────────────────────────────────────────────────┘    │
    │                                                          │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │ Business Services (Domain Layer)                │    │
    │  │ - UserStoryService                              │    │
    │  │ - TestPlanService                               │    │
    │  │ - AIService                                     │    │
    │  └─────────────────────────────────────────────────┘    │
    │                                                          │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │ Repositories (Data Layer)                       │    │
    │  │ - UserStoryRepository                           │    │
    │  │ - TestPlanRepository                            │    │
    │  └─────────────────────────────────────────────────┘    │
    └──────────────────────────────────────────────────────────┘
              │
              ▼
    ┌─────────────────────────────────────────┐
    │ Database (PostgreSQL)                   │
    └─────────────────────────────────────────┘
```

---

## 🔧 Implementación: MCP Server

### Estructura del MCP Server

```
mcp_server/
├── __init__.py
├── server.py                 # Servidor MCP principal
├── config.py                 # Configuración MCP
│
├── tools/                    # Tools (capacidades) disponibles
│   ├── __init__.py
│   ├── generate_test_plan.py
│   ├── analyze_user_story.py
│   ├── translate_content.py
│   └── export_test_plan.py
│
├── resources/                # Recursos (contexto disponible)
│   ├── __init__.py
│   ├── user_story_template.py
│   ├── test_plan_template.py
│   └── export_formats.py
│
└── prompts/                  # Prompts predefinidos
    ├── test_plan_generation.prompt
    ├── user_story_analysis.prompt
    └── translation.prompt
```

---

### Implementación Base del MCP Server

```python
# mcp_server/server.py
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
from typing import Any

from mcp_server.tools.generate_test_plan import generate_test_plan_tool
from mcp_server.tools.analyze_user_story import analyze_user_story_tool
from mcp_server.tools.translate_content import translate_content_tool

# Crear servidor MCP
server = Server("test-plan-generator-mcp")

# Registrar herramientas (tools)
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Listar herramientas disponibles"""
    return [
        Tool(
            name="generate_test_plan",
            description="Genera un Test Plan completo desde una Historia de Usuario",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_story_id": {
                        "type": "string",
                        "description": "ID de la Historia de Usuario"
                    },
                    "user_story_data": {
                        "type": "object",
                        "description": "Datos completos de la HU",
                        "properties": {
                            "story_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "acceptance_criteria": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["user_story_data"]
            }
        ),
        Tool(
            name="analyze_user_story",
            description="Analiza una Historia de Usuario y detecta su tipo (Backend/Frontend/UI-UX)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_story_data": {
                        "type": "object",
                        "description": "Datos de la HU"
                    }
                },
                "required": ["user_story_data"]
            }
        ),
        Tool(
            name="translate_content",
            description="Traduce contenido entre español e inglés",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "from_lang": {"type": "string", "enum": ["es", "en"]},
                    "to_lang": {"type": "string", "enum": ["es", "en"]}
                },
                "required": ["content", "from_lang", "to_lang"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Ejecutar herramienta"""
    if name == "generate_test_plan":
        return await generate_test_plan_tool(arguments)
    elif name == "analyze_user_story":
        return await analyze_user_story_tool(arguments)
    elif name == "translate_content":
        return await translate_content_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

# Inicializar servidor
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="test-plan-generator-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Tool: Generate Test Plan

```python
# mcp_server/tools/generate_test_plan.py
from mcp.types import TextContent
from typing import Any
from app.services.ai_service import AIService
from app.services.test_plan_service import TestPlanService
from app.repositories.interfaces.user_story_repository import UserStoryRepository
from app.repositories.interfaces.test_plan_repository import TestPlanRepository

async def generate_test_plan_tool(arguments: Any) -> list[TextContent]:
    """
    Tool MCP para generar Test Plan.
    
    Este tool puede ser invocado directamente por un modelo MCP
    con el contexto completo de la HU.
    """
    user_story_data = arguments.get("user_story_data")
    if not user_story_data:
        return [TextContent(
            type="text",
            text="Error: user_story_data es requerido"
        )]
    
    try:
        # Crear entidad UserStory desde datos
        user_story = UserStory(
            story_id=user_story_data["story_id"],
            title=user_story_data["title"],
            description=user_story_data["description"],
            acceptance_criteria=user_story_data["acceptance_criteria"],
            # ... otros campos
        )
        
        # Usar servicio de negocio existente
        # (Nota: Esto requiere inyección de dependencias,
        # simplificado aquí para ejemplo)
        ai_service = AIService(...)
        test_plan = await ai_service.generate_test_plan_from_story(
            user_story=user_story,
            generated_by_id=arguments.get("user_id")
        )
        
        # Retornar resultado como texto estructurado
        result_text = f"""
Test Plan generado exitosamente:
- ID: {test_plan.id}
- Total de casos: {test_plan.total_cases}
- Alta prioridad: {test_plan.high_priority_count}
- Media prioridad: {test_plan.medium_priority_count}
- Baja prioridad: {test_plan.low_priority_count}

Objetivo: {test_plan.objective}

Resumen: {test_plan.summary}
"""
        
        return [TextContent(
            type="text",
            text=result_text
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error generando Test Plan: {str(e)}"
        )]
```

---

## 🔄 Integración: APIs REST + MCP

### Caso de Uso: Generar Test Plan

#### Opción A: API REST tradicional (actual)

```python
# app/api/v1/endpoints/test_plans.py
@router.post("/", response_model=TestPlanResponse)
async def create_test_plan(
    user_story_id: int,
    current_user = Depends(get_current_user),
    service: TestPlanService = Depends(get_test_plan_service)
):
    """Generar Test Plan - API REST tradicional"""
    test_plan = await service.generate_test_plan(
        user_story_id=user_story_id,
        user_id=current_user.id
    )
    return TestPlanResponse.from_entity(test_plan)
```

#### Opción B: API REST que usa MCP internamente

```python
# app/api/v1/endpoints/test_plans.py
from mcp_client import MCPClient

@router.post("/", response_model=TestPlanResponse)
async def create_test_plan(
    user_story_id: int,
    current_user = Depends(get_current_user),
    service: TestPlanService = Depends(get_test_plan_service),
    mcp_client: MCPClient = Depends(get_mcp_client)
):
    """Generar Test Plan - Usando MCP internamente"""
    # Obtener HU
    user_story = await service.get_user_story(user_story_id)
    
    # Invocar MCP tool
    result = await mcp_client.call_tool(
        tool_name="generate_test_plan",
        arguments={
            "user_story_data": {
                "story_id": user_story.story_id,
                "title": user_story.title,
                "description": user_story.description,
                "acceptance_criteria": user_story.acceptance_criteria
            },
            "user_id": current_user.id
        }
    )
    
    # Procesar resultado y guardar
    test_plan = await service.process_mcp_result(result, user_story_id)
    
    return TestPlanResponse.from_entity(test_plan)
```

#### Opción C: MCP Client directo (futuro)

```python
# En el frontend o cliente directo MCP
from mcp_client import MCPClient

client = MCPClient(server_url="mcp://localhost:8000")

result = await client.call_tool(
    tool_name="generate_test_plan",
    arguments={
        "user_story_data": {...}
    }
)
```

---

## 🎯 Ventajas de la Arquitectura Híbrida

### 1. Flexibilidad

- **APIs REST**: Mantienen compatibilidad con clientes existentes
- **MCP**: Permite integraciones más avanzadas y naturales con LLMs
- **Convivencia**: Ambos pueden coexistir sin conflictos

### 2. Evolución Gradual

- **Fase 1**: Migrar servicios internos a MCP
- **Fase 2**: Exponer MCP Server públicamente
- **Fase 3**: Migrar clientes a MCP nativo

### 3. Mejora de Capacidades

- **Contexto persistente**: MCP mantiene contexto entre llamadas
- **Tools composables**: Múltiples tools pueden trabajar juntos
- **Flujo natural**: Los modelos pueden usar tools automáticamente

---

## 📋 Roadmap de Migración a MCP

### Fase 1: Preparación (Mes 1-2)

**Objetivos**:
- Investigar e implementar servidor MCP base
- Crear tools básicos (generate_test_plan, analyze_user_story)
- Integrar MCP como servicio interno

**Tareas**:
1. Instalar dependencias MCP (`mcp` package)
2. Crear estructura del servidor MCP
3. Implementar tools básicos
4. Tests unitarios de tools

**Resultado**: MCP Server funcional, usado internamente por APIs REST

---

### Fase 2: Integración (Mes 3-4)

**Objetivos**:
- Migrar servicios de IA a usar MCP
- Exponer MCP Server para uso interno
- Mantener APIs REST como interfaz pública

**Tareas**:
1. Refactorizar AIService para usar MCP Client
2. Configurar MCP Server en producción
3. Monitorear performance y errores
4. Documentar uso interno de MCP

**Resultado**: APIs REST usan MCP internamente, transparencia para usuarios

---

### Fase 3: Expansión (Mes 5-6)

**Objetivos**:
- Agregar más tools (export, análisis avanzado)
- Exponer MCP Server públicamente
- Documentar API MCP para desarrolladores

**Tareas**:
1. Agregar tools adicionales
2. Configurar autenticación para MCP
3. Crear documentación de MCP API
4. Ejemplos de integración

**Resultado**: MCP Server público, múltiples tools disponibles

---

### Fase 4: Optimización (Mes 7+)

**Objetivos**:
- Optimizar performance
- Agregar capacidades avanzadas (streaming, etc.)
- Considerar migración completa a MCP

**Tareas**:
1. Optimizar llamadas MCP
2. Implementar streaming para respuestas largas
3. Evaluar migración completa
4. Roadmap futuro

---

## 🔐 Consideraciones de Seguridad

### Autenticación en MCP

```python
# mcp_server/auth.py
from mcp.server import Server
from mcp.types import ErrorCode, McpError

async def authenticate_request(request):
    """Autenticar request MCP"""
    token = request.headers.get("Authorization")
    if not token:
        raise McpError(
            code=ErrorCode.InvalidRequest,
            message="Token de autenticación requerido"
        )
    
    # Validar token (similar a APIs REST)
    user = verify_token(token)
    if not user:
        raise McpError(
            code=ErrorCode.Unauthorized,
            message="Token inválido"
        )
    
    return user
```

---

## 📊 Comparación: APIs REST vs MCP

| Característica | APIs REST | MCP |
|----------------|-----------|-----|
| **Compatibilidad** | ✅ Universal | ⚠️ Requiere cliente MCP |
| **Contexto** | ❌ Sin estado | ✅ Contexto persistente |
| **Integración con LLMs** | ⚠️ Manual | ✅ Nativa |
| **Tools/Capabilities** | ❌ No | ✅ Sí |
| **Complejidad** | ✅ Baja | ⚠️ Media |
| **Ecosistema** | ✅ Muy maduro | ⚠️ En crecimiento |
| **Performance** | ✅ Rápido | ✅ Rápido |

**Recomendación**: Usar ambos, APIs REST como interfaz pública, MCP para integraciones avanzadas con IA.

---

## 🛠️ Dependencias Necesarias

```txt
# requirements-mcp.txt
mcp>=0.9.0              # Servidor MCP
mcp-client>=0.9.0       # Cliente MCP (para integración)
anthropic>=0.18.0       # Si se usa Claude (opcional)
openai>=1.0.0           # Ya existe (OpenAI)
```

---

## ✅ Ventajas de esta Estrategia

1. **Flexibilidad**: Mantiene APIs REST mientras adopta MCP
2. **Evolución gradual**: Migración paso a paso sin romper funcionalidad
3. **Mejor integración IA**: MCP facilita integración con LLMs
4. **Escalabilidad**: MCP permite agregar capacidades fácilmente
5. **Futuro-proof**: Preparado para evoluciones del ecosistema MCP

---

Esta estrategia híbrida permite aprovechar lo mejor de ambos mundos mientras se evoluciona gradualmente hacia una arquitectura más moderna y orientada a IA.
