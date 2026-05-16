# PoC 3: Observabilidade com Langfuse na API

## Objetivo
Garantir que o comportamento (latência, custo, tokens e rastreabilidade) das cadeias seja monitorado.

## Tarefas
- [ ] Subir os containers do Langfuse e PostgreSQL (via `docker-compose up -d`).
- [ ] Configurar as variáveis de ambiente com as chaves locais do Langfuse (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`).
- [ ] Integrar o *Callback Handler* do Langfuse na API do FastAPI (`app/main.py`).
- [ ] Enviar requisições de teste para a API e verificar se o *Trace* foi registrado corretamente no painel local do Langfuse.
- [ ] Validar a visualização de métricas de custo de tokens na dashboard.
