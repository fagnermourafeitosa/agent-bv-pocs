import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from scripts.rag_chroma.retriever import test_retriever

load_dotenv()

def get_rag_chain():
    """
    Monta e retorna a cadeia (Chain) do RAG usando LangChain.
    """
    # 1. Instancia o LLM do Gemini
    # O langchain vai ler a variável GOOGLE_API_KEY do .env e GEMINI_MODEL
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    llm = ChatGoogleGenerativeAI(model=gemini_model, temperature=0.2)
    
    # 2. Obtém o Retriever que já configuramos na Tarefa 4
    # Vamos reusar a logica instanciando o chroma db e o retriever.
    # Mas como o test_retriever faz a busca, melhor extrairmos o retriever lá.
    # Para simplificar e isolar a execução, vamos recriar o retriever aqui:
    from scripts.rag_chroma.vectorizer import get_embeddings
    from langchain_chroma import Chroma
    import chromadb
    
    embeddings = get_embeddings()
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    vector_store = Chroma(
        client=chroma_client,
        collection_name="politicas_bv",
        embedding_function=embeddings,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # 3. Cria o Prompt com Guardrails
    template = """Você é um assistente virtual do Banco BV, atuando de forma "Simples, Parceira, Segura e Inovadora".
    
    REGRAS CRÍTICAS DE GUARDRAIL:
    1. Baseie sua resposta EXCLUSIVAMENTE no contexto fornecido abaixo. Se a resposta não estiver no contexto, diga "Desculpe, não tenho essa informação nas diretrizes do Banco."
    2. Nunca faça promessas de taxas ou aprovações sem validação sistêmica.
    3. Recuse-se terminantemente, de forma polida, a responder qualquer pergunta com palavras de baixo calão, ofensiva, inapropriada ou fora do escopo bancário.

    Contexto:
    {context}
    
    Pergunta do Usuário:
    {question}
    
    Sua Resposta:"""
    
    prompt = PromptTemplate.from_template(template)
    
    # 4. Formata os documentos recuperados
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    # 5. Monta a Cadeia (Chain)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    chain = get_rag_chain()
    pergunta = "Quais as regras para limite de crédito?"
    print(f"Pergunta: {pergunta}")
    resposta = chain.invoke(pergunta)
    print(f"\nResposta do Gemini:\n{resposta}")
