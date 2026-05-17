# PoC 6: Avaliação Automatizada com DeepEval

## Objetivo
Usar *LLM-as-a-Judge* para validar o agente automaticamente.

## Tarefas
- [x] Instalar e configurar a biblioteca *DeepEval* no projeto.
- [x] Criar o script de teste (`test_agente_comportamento.py`).
- [x] Configurar métricas prontas do DeepEval: `AnswerRelevancyMetric` e `FaithfulnessMetric`.
- [x] Criar uma métrica customizada (Custom Metric) para avaliar estritamente o "Tom de Voz da Marca".
- [x] Executar o *pytest* para rodar a suíte de avaliação com um modelo avançado como Juiz.
- [x] Fazer a avaliação quebrar intencionalmente (forçando o agente a ser rude) para verificar se o alarme de segurança dispara.
