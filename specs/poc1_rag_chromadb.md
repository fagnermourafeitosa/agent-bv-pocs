# PoC 1: Motor RAG Básico (ChromaDB + LangChain)

## Objetivo
Validar a capacidade de injetar conhecimento externo no agente utilizando buscas semânticas de alta performance.

## Tarefas
- [x] Configurar conexão inicial com o ChromaDB no projeto.
- [ ] Criar um script para carregar um documento Markdown ou PDF (ex: mock de políticas do Banco BV).
- [ ] Vetorizar o conteúdo do documento e salvar no ChromaDB usando *Embeddings*.
- [ ] Criar uma função de *retriever* para buscar fragmentos de texto baseados em uma query de usuário.
- [ ] Configurar uma cadeia simples (*Chain*) no LangChain que use o LLM para responder à pergunta baseando-se exclusivamente no contexto retornado.
