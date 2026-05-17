"""
Domínio: Persona e Tom de Voz
Implementa a injeção do System Prompt comportamental e gera respostas
usando as diretrizes de voz do Banco BV.
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.prompts import BV_BEHAVIORAL_SYSTEM_PROMPT
from app.agents.state import ConversationState

def _extract_text(response) -> str:
    """Extrai o texto da resposta do LLM independente do formato."""
    content = response.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)

def generate_persona_response(question: str) -> str:
    """
    Gera uma resposta aplicando as regras de tom de voz e taxonomia comportamental.
    (Utilizado de forma avulsa/router).
    """
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        temperature=0.7,
    )
    
    messages = [
        SystemMessage(content=BV_BEHAVIORAL_SYSTEM_PROMPT),
        HumanMessage(content=question)
    ]
    
    response = llm.invoke(messages)
    return _extract_text(response)

def persona_node(state: ConversationState) -> ConversationState:
    """
    Nó LangGraph: Recebe a resposta técnica gerada por um especialista e aplica 
    o tom de voz e diretrizes comportamentais do Banco BV.
    """
    original_answer = state.get("specialist_answer", "")
    question = state["messages"][-1].content if state.get("messages") else ""
    
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        temperature=0.7,
    )
    
    prompt = f"""Reescreva a seguinte resposta técnica de forma a aplicar estritamente as regras de tom de voz.
Pergunta do cliente: {question}
Resposta técnica original: {original_answer}
"""
    
    messages = [
        SystemMessage(content=BV_BEHAVIORAL_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    new_answer = _extract_text(response)
    
    return {
        **state,
        "specialist_answer": new_answer,
        "trace": [f"[Voice Design] Resposta reescrita com a persona institucional."]
    }
