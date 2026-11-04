# Tasks

## 1. Script de cálculo de progresso

- [x] 1.1 Criar o arquivo `scripts/calculate_progress.py` com a função `calculate_progress(subject_id, auth_token)` que consulta `GET /academic_tasks?subject_id=<id>` via a URL base `URL_base_ACADEMIC_TASKS` do `.env`, calcula `(concluídas / total) * 100`, trata divisão por zero retornando `{"percentage": 0}`, e retorna um dicionário com a chave `percentage`. Verificar que o arquivo existe e que a função é importável sem erros de sintaxe executando `python -c "from scripts.calculate_progress import calculate_progress"`.

