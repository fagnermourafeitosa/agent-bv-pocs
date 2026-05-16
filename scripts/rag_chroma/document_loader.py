import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_document(file_path: str):
    """
    Carrega um arquivo de texto/markdown e divide em chunks 
    preparando-os para a vetorização.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    
    # Dividindo em blocos menores de 500 caracteres
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    doc_path = os.path.join(base_dir, "docs", "politica_bv.md")
    
    chunks = load_and_split_document(doc_path)
    print(f"Documento dividido em {len(chunks)} chunks.")
    for i, doc in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content)
