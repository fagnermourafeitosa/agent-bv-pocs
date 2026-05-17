import sys
import types
from langchain_core.documents import Document
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult
import langchain_core.callbacks.base

# Registra a compatibilidade com langchain.callbacks
sys.modules['langchain.callbacks'] = langchain_core.callbacks.base
sys.modules['langchain.callbacks.base'] = langchain_core.callbacks.base

# Registra a compatibilidade com langchain.schema e seus submódulos
schema = types.ModuleType('langchain.schema')
schema.Document = Document
schema.AgentAction = AgentAction
schema.AgentFinish = AgentFinish
schema.LLMResult = LLMResult
sys.modules['langchain.schema'] = schema

schema_document = types.ModuleType('langchain.schema.document')
schema_document.Document = Document
sys.modules['langchain.schema.document'] = schema_document

schema_agent = types.ModuleType('langchain.schema.agent')
schema_agent.AgentAction = AgentAction
schema_agent.AgentFinish = AgentFinish
sys.modules['langchain.schema.agent'] = schema_agent
