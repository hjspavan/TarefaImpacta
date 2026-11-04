# Proposal

## Why

O EduTrack AI já possui endpoints CRUD para disciplinas e tarefas acadêmicas, e o frontend exibe as tarefas com seus status. Porém, não há uma lógica centralizada que calcule a porcentagem de progresso de uma disciplina com base em suas tarefas concluídas. Ter esse cálculo em um script reutilizável permite que qualquer parte do sistema (páginas Streamlit, relatórios, dashboards) consuma o percentual de progresso de forma padronizada.

## What Changes

- Criação do script Python `scripts/calculate_progress.py` que:
  - Recebe um `subject_id` e um token de autenticação.
  - Consulta as tarefas da disciplina via `GET /academic_tasks?subject_id=<id>` no Xano.
  - Calcula a porcentagem de progresso: `(tarefas concluídas / total de tarefas) * 100`.
  - Trata divisão por zero (zero tarefas → retorna 0%).
  - Retorna um JSON com a chave `percentage`.

## Capabilities

### New Capabilities
- `progress-calculation`: Lógica Python para cálculo da porcentagem de progresso de uma disciplina baseada no status de suas tarefas acadêmicas.

### Modified Capabilities

## Impact

- **Frontend / Scripts**: Novo arquivo `scripts/calculate_progress.py` disponível para importação por páginas Streamlit ou execução direta.
- **Backend / Xano**: Nenhuma alteração — consome o endpoint `GET /academic_tasks` já existente.
- **Dependências**: Utiliza a biblioteca `requests` (já presente no projeto).

