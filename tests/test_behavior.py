import json
import os
import pytest
from app.agents.persona import generate_persona_response

def carregar_perguntas():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "perguntas_desafiadoras.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("item", carregar_perguntas())
def test_comportamento_agente(item):
    """Testa o agente com base no conjunto de perguntas desafiadoras definidas em JSON."""
    pergunta = item["pergunta"]
    expected_tags = item["expected_tags"]
    forbidden_tags = item["forbidden_tags"]
    
    response = generate_persona_response(pergunta)
    content = response.lower()
    
    # Pelo menos uma das tags esperadas deve estar na resposta
    assert any(tag in content for tag in expected_tags), (
        f"A resposta deveria conter algum dos termos: {expected_tags}. "
        f"Resposta recebida: {response}"
    )
    
    # Nenhuma das tags proibidas deve estar na resposta
    for tag in forbidden_tags:
        assert tag not in content, (
            f"A resposta contém um termo proibido '{tag}'. "
            f"Resposta recebida: {response}"
        )
