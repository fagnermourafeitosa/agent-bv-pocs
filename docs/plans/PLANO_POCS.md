# Plano de Provas de Conceito (PoCs)

Este documento descreve as etapas práticas (Provas de Conceito) que serão desenvolvidas para validar e tangibilizar os objetivos estabelecidos de Arquitetura e de Governança Comportamental para os Agentes de IA do Banco BV.

---

## 🏗️ 1. Trilha de Arquitetura e Soluções

Estas PoCs visam validar a fundação tecnológica, a escalabilidade e a orquestração dos agentes usando as ferramentas definidas (LangChain, LangGraph, FastAPI, ChromaDB, Langfuse).

### PoC 1: Motor RAG (Retrieval-Augmented Generation) Básico
- **Objetivo:** Validar a capacidade de injetar conhecimento externo no agente utilizando buscas semânticas de alta performance.
- **Implementação:**
  - Subir uma instância local do ChromaDB.
  - Criar um script para vetorizar e salvar documentos fictícios (ex: "Políticas do Banco BV" em PDF/Markdown).
  - Configurar uma cadeia no LangChain para recuperar a informação do ChromaDB e gerar a resposta com o LLM.

### PoC 2: Orquestração Multiagentes com LangGraph
- **Objetivo:** Criar um sistema onde agentes autônomos colaboram para resolver um problema complexo, testando o roteamento e controle de estado.
- **Implementação:**
  - Construir um fluxo no LangGraph com um **Agente Supervisor** e dois agentes especialistas (ex: "Especialista em Produtos de Crédito" e "Especialista em Atendimento").
  - Testar loops de reflexão (onde um agente corrige a própria resposta antes de devolver ao usuário).

### PoC 3: Observabilidade com Langfuse na API (FastAPI)
- **Objetivo:** Garantir que o comportamento de engenharia (latência, custo, tokens e rastreabilidade) não seja uma caixa-preta.
- **Implementação:**
  - Ligar o container Docker do Langfuse.
  - Implementar os callbacks do Langfuse na nossa FastAPI (`app/main.py`).
  - Realizar chamadas na API e validar se a árvore de execução (trace) do LangGraph aparece corretamente no painel do Langfuse.

---

## 🛡️ 2. Trilha de Governança Comportamental e Soft Skills

Estas PoCs visam garantir que a Inteligência Artificial obedeça a diretrizes éticas, mantenha o tom de voz da marca institucional (Banco BV) e tenha seus comportamentos avaliados automaticamente.

### PoC 4: Injeção de Persona e Tom de Voz (Voice Design)
- **Objetivo:** Estabelecer a "alma" do agente, garantindo que ele comunique os valores institucionais (simples, parceiro, seguro, inovador).
- **Implementação:**
  - Modelar um *System Prompt* (Contrato de Comportamento) blindado contra saídas genéricas de LLM.
  - Testar respostas do agente em cenários de tensão (ex: um cliente irritado por um atraso) e validar se a empatia e a resolução da IA se mantém dentro da taxonomia de soft skills definida.

### PoC 5: Guardrails e Mitigação de Risco Ético
- **Objetivo:** Bloquear alucinações perigosas, quebra de autonomia ou desvios do código de conduta (ex: o agente nunca deve conceder um crédito ou prometer uma taxa que não foi pré-aprovada pelo sistema).
- **Implementação:**
  - Criar regras de limitação de autonomia na cadeia do agente.
  - Testar injeções de prompt (*Prompt Injection*) para tentar forçar o agente a quebrar regras, validando a eficácia do guardrail.

### PoC 6: Avaliação Automatizada (*LLM-as-a-Judge* com DeepEval)
- **Objetivo:** Substituir a validação humana manual por uma avaliação sistêmica e escalável para aprovação de modelos e comportamentos.
- **Implementação:**
  - Criar um script com a biblioteca **DeepEval**.
  - Rodar 20 perguntas contra nosso Agente. Em seguida, usar um modelo (ex: GPT-4) atuando como "Juiz" para avaliar as respostas sob três métricas: *Relevância*, *Fidelidade ao Contexto* e *Aderência ao Tom de Voz Institucional*.
  - Gerar um relatório de KPIs e configurar um "alarme" (falhar o teste) se o Score Comportamental for menor que 80%.
