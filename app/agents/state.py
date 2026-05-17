"""
Estado compartilhado do grafo multiagente.

Cada nó lê e escreve neste estado. O TypedDict garante
tipagem estática e documentação implícita dos campos.
"""
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


def _append_trace(left: list, right: list) -> list:
    """Reducer que acumula entradas de trace sem sobrescrever."""
    return (left or []) + (right or [])


class ConversationState(TypedDict):
    """Estado que flui entre os nós do grafo de agentes."""

    messages: Annotated[list, add_messages]
    domain: str
    specialist_answer: str
    answer_approved: bool

    # Log passo-a-passo da orquestração entre agentes
    trace: Annotated[list[str], _append_trace]
