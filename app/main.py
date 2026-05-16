from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Agents & Skills BV - API",
    description="API de orquestração de agentes de IA com governança comportamental e RAG.",
    version="0.1.0"
)

class AgentRequest(BaseModel):
    user_input: str
    session_id: str | None = None

class AgentResponse(BaseModel):
    response: str
    status: str

@app.get("/")
async def root():
    return {"message": "API de Agentes BV está online. Acesse /docs para a documentação Swagger."}

@app.post("/api/v1/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Endpoint principal para interação com os agentes.
    Aqui integraremos a chamada para o LangGraph e o ChromaDB.
    """
    try:
        # TODO: Integrar a lógica do LangGraph e Langfuse aqui
        
        # Mock temporário
        agent_reply = f"Mock: Recebi sua mensagem -> '{request.user_input}'. Em breve o LangGraph assumirá esta resposta."
        
        return AgentResponse(response=agent_reply, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
