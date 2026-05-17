"""Entry point da API — registro de routers e configuração geral."""
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.knowledge import router as knowledge_router
from app.routers.agent import router as agent_router
from app.routers.behavior import router as behavior_router

import app.langchain_compatibility
from dotenv import load_dotenv
load_dotenv()

from langfuse.callback import CallbackHandler
langfuse_handler = CallbackHandler()

app = FastAPI(
    title="Agents & Skills BV",
    description="API de agentes de IA com RAG, governança comportamental e observabilidade.",
    version="1.0.0",
)

app.include_router(knowledge_router)
app.include_router(agent_router)
app.include_router(behavior_router)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")
