"""
Router: Agente Multiagente (PoC 2)

Endpoint único que executa o grafo de orquestração LangGraph,
retornando o domínio identificado, a resposta do especialista
e o resultado da validação pelo Supervisor.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents import run_agent

router = APIRouter(prefix="/api/agent", tags=["agent"])


class AgentRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_agent(request: AgentRequest):
    """
    Envia uma pergunta ao sistema multiagente.

    O Supervisor identifica o domínio, delega ao especialista correto
    e valida a resposta antes de retornar.
    """
    try:
        return run_agent(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
