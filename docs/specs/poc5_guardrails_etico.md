# PoC 5: Guardrails Éticos e Mitigação de Risco

## Objetivo
Bloquear alucinações e evitar quebra de regras corporativas.

## Tarefas
- [x] Definir 3 regras críticas de negócio (ex: o agente nunca pode aprovar crédito diretamente; não pode usar linguajar ofensivo; não pode dar dicas de investimento externo).
- [x] Desenvolver um nó de *Guardrail* na cadeia do LangChain/LangGraph que verifica a resposta gerada *antes* de enviá-la ao usuário.
- [x] Implementar a lógica de recusa elegante caso a saída viole a regra ("Desculpe, não posso fazer isso...").
- [x] Rodar testes de *Prompt Injection* (tentar enganar o modelo) para avaliar a robustez das proteções.
