import chromadb

def get_chroma_client():
    """
    Retorna o cliente HTTP do ChromaDB conectado ao container local.
    """
    try:
        # Tenta conectar ao ChromaDB rodando no docker-compose
        client = chromadb.HttpClient(host='localhost', port=8000)
        return client
    except Exception as e:
        print(f"Erro ao conectar ao ChromaDB: {e}")
        return None

if __name__ == "__main__":
    client = get_chroma_client()
    if client:
        print("Conexão com ChromaDB bem sucedida! Versão:", client.get_version())
        print("Heartbeat:", client.heartbeat())
