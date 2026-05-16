import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from scripts.rag_chroma.document_loader import load_and_split_document
import chromadb

# Carrega as variáveis de ambiente
load_dotenv()

def get_embeddings():
    print("Inicializando embeddings locais (HuggingFace all-MiniLM-L6-v2)...")
    try:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Erro no modelo local, ativando fallback Gemini ({e})...")
        return GoogleGenerativeAIEmbeddings(model="models/text-multilingual-embedding-002")

def vectorize_documents():
    """
    Vetoriza os documentos e salva no ChromaDB usando Embeddings.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    doc_path = os.path.join(base_dir, "docs", "politica_bv.md")
    
    # 1. Carrega e divide os documentos usando o script da Tarefa 2
    chunks = load_and_split_document(doc_path)
    
    # 2. Configura os Embeddings Local com Fallback Gemini
    embeddings = get_embeddings()

    
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
