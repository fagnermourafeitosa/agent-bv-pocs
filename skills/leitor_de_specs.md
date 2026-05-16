# Skill: Leitor e Executor de Specs

## Objetivo
Esta skill orienta o modelo assistente (eu) sobre como ler as especificações (specs) criadas no diretório `specs/`, executar cada tarefa de forma autônoma e iterativa, e marcar a tarefa como concluída diretamente no arquivo Markdown.

## Instruções de Execução

Quando o usuário solicitar algo como "Execute a PoC 1" ou "Inicie a spec X", você **DEVE** seguir exatamente o fluxo abaixo:

1. **Ler o Arquivo da Spec**:
   - Use a ferramenta `view_file` para carregar e ler o arquivo Markdown correspondente no diretório `specs/` (ex: `specs/poc1_rag_chromadb.md`).

2. **Identificar a Primeira Tarefa Pendente**:
   - Analise o arquivo e encontre a primeira ocorrência de uma tarefa não concluída, indicada pela sintaxe exata: `- [ ]`.
   - Se todas as tarefas estiverem marcadas com `[x]`, informe ao usuário que a spec já foi totalmente concluída.

3. **Executar a Tarefa**:
   - Proponha e execute o plano para resolver *apenas* essa tarefa específica.
   - Escreva o código, rode os comandos necessários, instale as dependências ou crie os arquivos solicitados pela tarefa.

4. **Marcar a Tarefa como Concluída**:
   - Assim que a tarefa for finalizada com sucesso, utilize a ferramenta `replace_file_content` para alterar **exatamente e unicamente** a linha da tarefa de `- [ ]` para `- [x]`.
   - Garanta que a linha atualizada reflita o texto exato da original, mudando apenas a checkbox.

5. **Aguardar Próxima Instrução ou Continuar**:
   - Salve o arquivo (caso tenha feito *replace*), faça o commit da tarefa se apropriado, informe ao usuário o que foi feito e pergunte se pode seguir para a próxima tarefa (o próximo `[ ]`).
   - Repita o processo até que o arquivo não tenha mais marcadores `- [ ]`.

## Regras Críticas
- **NUNCA** mude todas as tarefas para `[x]` de uma vez. A progressão deve ser iterativa e real. Só marque uma tarefa como `[x]` quando o código ou a configuração daquela etapa específica estiver pronta.
- Se travar em um erro ou precisar de uma decisão arquitetural, pare, explique o problema e peça permissão ao usuário antes de avançar para a próxima tarefa ou marcar com `[x]`.
