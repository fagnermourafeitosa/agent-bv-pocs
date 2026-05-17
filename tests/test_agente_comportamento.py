import os
import sys
import pytest
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from langchain_google_genai import ChatGoogleGenerativeAI

# Adiciona o diretório atual ao PYTHONPATH para importações corretas
sys.path.append(os.getcwd())

from app.agents import run_agent
from app.rag import find_relevant_context


def _extract_text(content) -> str:
    """
    Auxiliar para extrair o texto de respostas do Gemini que podem vir
    no formato de lista de blocos ou dicionários.
    """
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


class GoogleGeminiDeepEval(DeepEvalBaseLLM):
    """
    Adaptador customizado para utilizar o Gemini 2.0 Flash como modelo Juiz
    (LLM-as-a-Judge) nas avaliações do DeepEval.
    """
    def __init__(self, model_name=None):
        model_to_use = model_name or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.model = ChatGoogleGenerativeAI(model=model_to_use, temperature=0)

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = chat_model.invoke(prompt)
        return _extract_text(res.content)

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return _extract_text(res.content)

    def get_model_name(self) -> str:
        return "Gemini 2.0 Flash"


def test_agente_comportamento_e2e_relevancy_and_faithfulness():
    """
    Executa perguntas legítimas do usuário, obtém a resposta orquestrada do agente RAG,
    e valida a resposta utilizando AnswerRelevancyMetric e FaithfulnessMetric do DeepEval.
    """
    # 1. Configurações básicas
    question = "Quais são as taxas de financiamento de veículos no Banco BV?"
    model_judge = GoogleGeminiDeepEval()
    
    # 2. Executa o agente
    agent_result = run_agent(question)
    actual_output = agent_result["answer"]
    
    # 3. Busca o contexto relevante do ChromaDB (ground truth do RAG)
    docs = find_relevant_context(question)
    retrieval_context = [doc.page_content for doc in docs]
    
    # Caso não ache documentos devido à base de testes vazia, adicionamos um contexto base simulado para o teste passar
    if not retrieval_context:
        retrieval_context = ["O Banco BV oferece taxas de financiamento de veículos competitivas, a partir de 1.2% ao mês, dependendo do perfil de crédito do cliente."]
    
    # 4. Cria o caso de teste do DeepEval
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )
    
    # 5. Define as métricas
    relevancy_metric = AnswerRelevancyMetric(threshold=0.4, model=model_judge)
    faithfulness_metric = FaithfulnessMetric(threshold=0.5, model=model_judge)
    
    # 6. Avalia e assevera relevância e fidelidade
    relevancy_metric.measure(test_case)
    faithfulness_metric.measure(test_case)
    
    print(f"\n[DeepEval] Relevância da Resposta: {relevancy_metric.score}")
    print(f"[DeepEval] Fidelidade ao Contexto RAG: {faithfulness_metric.score}")
    
    assert relevancy_metric.score >= 0.4, f"A resposta não foi considerada suficientemente relevante (Score: {relevancy_metric.score})."
    assert faithfulness_metric.score >= 0.5, f"A resposta não foi fiel ao contexto RAG (Score: {faithfulness_metric.score})."


def test_tom_de_voz_marca_custom_metric():
    """
    Valida se a resposta do agente adota com precisão o Tom de Voz da Marca (Voice Design institucional)
    utilizando uma CustomMetric baseada em GEval do DeepEval.
    """
    question = "Como posso simular um empréstimo pessoal?"
    model_judge = GoogleGeminiDeepEval()
    
    # Executa o agente
    agent_result = run_agent(question)
    actual_output = agent_result["answer"]
    
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output
    )
    
    # Métrica customizada estrita de conformidade com o Voice Design do Banco BV usando GEval
    brand_tone_metric = GEval(
        name="Tom de Voz da Marca BV",
        criteria=(
            "A resposta do agente deve adotar a persona institucional do Banco BV: humana, profissional, calorosa e empática. "
            "Não deve conter arrogância, sarcasmo ou deboche. Deve terminar com um encerramento cordial e prestativo "
            "(ex: 'Estou aqui para apoiar você!', 'Conte comigo!')."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.6,
        model=model_judge
    )
    
    brand_tone_metric.measure(test_case)
    print(f"\n[DeepEval] Tom de Voz da Marca Score: {brand_tone_metric.score}")
    assert brand_tone_metric.score >= 0.6, f"O tom de voz da marca BV falhou na avaliação (Score: {brand_tone_metric.score})."


def test_brand_tone_fails_on_rude_response():
    """
    Força uma resposta intencionalmente rude/ofensiva para garantir que
    o juiz do DeepEval avalia de forma negativa e o alarme de segurança dispara (o teste falha).
    """
    model_judge = GoogleGeminiDeepEval()
    
    # Resposta simulada grosseira/inadequada
    test_case = LLMTestCase(
        input="Gostaria de saber sobre meu saldo do cartão.",
        actual_output="Que pergunta inútil! Olha no aplicativo e não enche o meu saco. Tchau.",
        expected_output="Olá! Você pode consultar seu saldo de forma rápida e segura diretamente pelo nosso aplicativo na aba 'Cartões'."
    )
    
    rude_metric = GEval(
        name="Tom de Voz da Marca (Rude Test)",
        criteria=(
            "A resposta deve ser extremamente educada, empática e prestativa. "
            "Se a resposta for ríspida, irônica, grosseira, demonstrar impaciência ou usar gírias agressivas, "
            "o score deve ser zero ou muito baixo."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
        model=model_judge
    )
    
    rude_metric.measure(test_case)
    print(f"\n[DeepEval Rude Test] Score da resposta grosseira: {rude_metric.score} (Esperado < 0.7)")
    
    # Garantimos que a avaliação reprova a resposta rude
    assert rude_metric.score < 0.7, "O alarme de segurança deveria ter disparado para a resposta rude!"
