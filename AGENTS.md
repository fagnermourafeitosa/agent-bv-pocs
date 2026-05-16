# Agentes e Skills - Banco BV

Este repositório consolida as definições, arquitetura e implementação das soluções de Inteligência Artificial com foco em Agentes Inteligentes, englobando desde a governança comportamental até a arquitetura técnica de sistemas distribuídos.

## 🎯 Objetivos do Projeto

Nossa estratégia está dividida em dois perfis e áreas de atuação fundamentais:

1. **[Governança Comportamental e Soft Skills](objetivos_governanca_comportamental.md)**: 
   Foco na definição do tom de voz, humanização, mitigação de riscos (uso ético de IA), e avaliações comportamentais dos agentes utilizando técnicas como *LLM-as-a-Judge*.
   
2. **[Arquitetura e Soluções de IA](objetivos_arquitetura_solucoes.md)**:
   Foco na construção da infraestrutura técnica, orquestração de LLMs e sistemas multiagentes, garantindo resiliência e alta escalabilidade em ambientes distribuídos.

---

## 🛠️ Stack Tecnológica

Para atingir esses objetivos de forma robusta e escalável, adotamos as seguintes tecnologias:

### Orquestração e Agentes
- **[LangChain](https://python.langchain.com/)**: Framework base para a construção e interconexão de cadeias com LLMs, ferramentas e *prompts*.
- **[LangGraph](https://python.langchain.com/docs/langgraph/)**: Utilizado para a criação de sistemas multiagentes com fluxos complexos, controle de estado, ciclos (loops) de reflexão e autonomia progressiva.

### API
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework Python de alta performance para a construção da API que servirá os agentes, gerenciando requisições, segurança e rotas assíncronas com excelente documentação nativa (Swagger/OpenAPI).

### Banco de Dados Vetorial (Vector Store)
- **[Chroma](https://www.trychroma.com/) (ChromaDB)**: Banco de dados vetorial focado em IA, ideal para as implementações de arquitetura *RAG (Retrieval-Augmented Generation)*, permitindo buscas semânticas rápidas e armazenamento de embeddings em alta performance.

---

## 🚀 Próximos Passos
- Configurar a estrutura base do FastAPI.
- Integrar a conexão inicial com o ChromaDB.
- Modelar o primeiro fluxo de agente no LangGraph focando em uma *skill* comportamental básica.
