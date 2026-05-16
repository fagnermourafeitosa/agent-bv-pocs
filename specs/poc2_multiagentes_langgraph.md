# PoC 2: Orquestração Multiagentes com LangGraph

## Objetivo
Criar um sistema onde agentes autônomos colaboram para resolver um problema complexo, testando roteamento e controle de estado.

## Tarefas
- [ ] Inicializar a estrutura do grafo (*StateGraph*) com um estado compartilhado para o agente.
- [ ] Desenvolver o nó do *Agente Supervisor*, responsável por interpretar a entrada do usuário e delegar a tarefa.
- [ ] Desenvolver o nó do *Especialista em Crédito* (responde apenas sobre limites e taxas).
- [ ] Desenvolver o nó do *Especialista em Atendimento* (responde sobre dúvidas gerais e rotinas).
- [ ] Configurar as *conditional edges* no LangGraph para rotear a conversa entre o Supervisor e os Especialistas.
- [ ] Implementar um loop simples de validação (reflexão) onde o Supervisor confere a resposta do especialista antes de finalizar.
