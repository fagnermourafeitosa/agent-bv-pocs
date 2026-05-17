"""
Router: Comportamento e Tom de Voz
Endpoint para validar a aplicação da persona comportamental do Banco BV.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.persona import generate_persona_response

router = APIRouter(prefix="/api/behavior", tags=["behavior"])

class PersonaQueryRequest(BaseModel):
    query: str

@router.post("/test-persona")
async def test_persona(request: PersonaQueryRequest):
    """
    Testa a injeção do System Prompt comportamental no LangChain
    simulando a resposta do agente com a persona do Banco BV.
    """
    try:
        response_text = generate_persona_response(request.query)
        return {
            "query": request.query,
            "agent_response": response_text,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
