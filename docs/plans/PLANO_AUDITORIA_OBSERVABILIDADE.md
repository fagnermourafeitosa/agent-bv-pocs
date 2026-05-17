# ADR 001: Ferramenta de Observabilidade e Auditoria de Agentes

**Status:** Aceito
**Data:** 16 de Maio de 2026
**Autor:** Especialista de Inteligência Artificial

## 1. Contexto e Problema
A arquitetura de agentes autônomos baseada em LangGraph e integrações complexas de RAG (com ChromaDB) gera uma "caixa preta" de decisões cognitivas. Precisamos de uma solução capaz de:
- Monitorar e rastrear a execução de cadeias (chains) e passos dos agentes (loops).
- Mensurar custos e latência de uso da API de LLMs.
- Auditar prompts, gerenciar suas versões de forma desacoplada da base de código.
- Obter métricas claras de governança e *feedback* em tempo real para os ajustes de comportamento (identidade de marca).

## 2. Decisão
Decidimos adotar o **Langfuse** como a ferramenta principal de Observabilidade, Tracing e Prompt Management.
O DeepEval permanecerá sendo usado (como biblioteca auxiliar de CI/CD), mas o monitoramento em produção e auditoria contínua será focado no Langfuse.

## 3. Justificativa
A escolha recaiu sobre o Langfuse pelos seguintes diferenciais alinhados aos nossos objetivos:
- **Tracing Profundo de Agentes:** A capacidade de visualizar a árvore hierárquica de chamadas, inputs e outputs de cada nó do *LangGraph* é superior e essencial para *debugging* de engenharia.
- **Métricas de Produção Focadas:** Oferece painéis *out-of-the-box* robustos de custo financeiro, consumo de tokens e latência, que são gargalos comuns na escalabilidade.
- **Feedback Loop Nativo:** Permite conectar avaliações geradas por usuários (ex.: *thumbs up/down* da API) diretamente ao *trace* específico que gerou a resposta, fornecendo insumo riquíssimo para a governança comportamental atuar de forma pontual.
- **Arquitetura Self-Hosted (Privacidade):** Por ser open source e distribuído via Docker, permite que os dados (possivelmente sensíveis de clientes bancários) não trafeguem em SaaS de terceiros, garantindo compliance de segurança.

## 4. Consequências
### Positivas:
- Visibilidade total em tempo real das ações do agente.
- Desacoplamento da gestão de Prompts da base de código da API.
- Facilidade de instrumentar (integração nativa via *callbacks* do LangChain).

### Negativas / Riscos Mitigados:
- Custo de infraestrutura interna para manter o banco PostgreSQL do Langfuse rodando de forma resiliente.
- Necessidade de adicionar decoradores/callbacks em todas as funções da nossa API para garantir o rastreamento, o que exige disciplina do time de engenharia.
