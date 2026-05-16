# Plano de Auditoria e Observabilidade para Agentes de IA

Este documento detalha as ferramentas *Open Source* escolhidas para garantir o monitoramento, a qualidade, a segurança e a governança (auditoria) das nossas soluções baseadas em LLMs e LangGraph.

## 1. Ferramenta de Auditoria de LLM (Avaliação e Governança)

Para atender ao requisito de auditoria (incluindo testes de *LLM-as-a-judge*, controle de qualidade das respostas e mitigação de alucinações/vieses), adotaremos o **DeepEval** (ou alternativamente o **Giskard**).

### Por que o DeepEval?
- **Foco em LLMs e RAG**: É um framework open source altamente especializado em testar e auditar pipelines RAG e Agentes.
- **Métricas Baseadas em LLM-as-a-Judge**: Fornece métricas prontas como relevância da resposta, fidelidade ao contexto, toxicidade e alucinação.
- **Integração CI/CD**: Permite rodar baterias de testes automatizados na esteira, bloqueando deploys de agentes que não atinjam o *score* comportamental mínimo (essencial para a governança comportamental definida nos objetivos).
- **Integração LangChain/LangGraph**: Funciona perfeitamente em conjunto com nossa stack principal.

*(Alternativa forte: **Giskard**, excelente para testes de segurança e detecção de vulnerabilidades e vieses em LLMs).*

## 2. Ferramenta de Observabilidade e Métricas (Tracing e Monitoramento)

Para observar o comportamento dos agentes em tempo real, rastrear o estado das decisões (LangGraph) e coletar métricas, adotaremos o **Langfuse** (ou alternativamente o **Phoenix by Arize**).

### Por que o Langfuse?
- **Tracing de Agentes (LangGraph)**: Permite visualizar exatamente o caminho cognitivo que o agente tomou (quais *tools* chamou, loops de reflexão, tempo em cada etapa).
- **Métricas de Custo e Latência**: Calcula automaticamente tokens consumidos e latência por requisição, fundamental para escalar a arquitetura.
- **Feedback Loop**: Possui suporte nativo para coletar feedback do usuário final (thumbs up/down) e vincular isso ao trace da execução, alimentando a área de governança com dados reais.
- **Open Source e Self-Hosted**: Pode ser hospedado na própria infraestrutura do banco, garantindo privacidade dos dados.

## Próximos Passos de Integração
1. Subir instâncias locais (via Docker) do Langfuse/Phoenix para iniciar a instrumentação.
2. Adicionar os *callbacks* do Langfuse na inicialização da nossa API FastAPI e nas cadeias do LangChain.
3. Criar a primeira suíte de testes de auditoria com DeepEval simulando o tom de voz do Banco BV.
