import os
from langchain_chroma import Chroma
import chromadb
from scripts.rag_chroma.vectorizer import get_embeddings

def test_retriever(query: str):
    """
    Função para inicializar o retriever e fazer uma busca semântica na base de conhecimento.
    """
    # 1. Recupera a mesma função de embeddings (local com fallback)
    embeddings = get_embeddings()
    
    # 2. Conecta ao ChromaDB
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    vector_store = Chroma(
        client=chroma_client,
        collection_name="politicas_bv",
        embedding_function=embeddings,
    )
    
    # 3. Cria o retriever (retorna os 2 chunks mais relevantes)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    print(f"\nBuscando na base de conhecimento: '{query}'")
    
    # 4. Faz a busca semântica
    docs = retriever.invoke(query)
    
    if not docs:
        print("Nenhum documento encontrado.")
        return []
        
    print("\nResultados encontrados:")
    for i, doc in enumerate(docs):
        print(f"\n--- Resultado {i+1} ---")
        print(doc.page_content)
        
    return docs

if __name__ == "__main__":
    # Testando com duas perguntas diferentes
    test_retriever("Qual é o limite de crédito aprovado?")
    test_retriever("Posso pedir a senha do cliente por telefone?")
