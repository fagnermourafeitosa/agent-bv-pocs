import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from poc1_task2_load_documents import load_and_split_document
import chromadb

# Carrega as variáveis de ambiente
load_dotenv()

def vectorize_documents():
    """
    Vetoriza os documentos e salva no ChromaDB usando Embeddings do Gemini.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    doc_path = os.path.join(base_dir, "docs", "politica_bv.md")
    
    # 1. Carrega e divide os documentos usando o script da Tarefa 2
    chunks = load_and_split_document(doc_path)
    
    # 2. Configura os Embeddings do Gemini
    # O langchain procura pela env GOOGLE_API_KEY
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # 3. Conecta ao Chroma local via HttpClient
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    
    # 4. Salva no banco vetorial
    vector_store = Chroma(
        client=chroma_client,
        collection_name="politicas_bv",
        embedding_function=embeddings,
    )
    
    print(f"Vetorizando e adicionando {len(chunks)} chunks ao ChromaDB...")
    vector_store.add_documents(documents=chunks)
    print("Sucesso! Documentos vetorizados e salvos.")

if __name__ == "__main__":
    vectorize_documents()
