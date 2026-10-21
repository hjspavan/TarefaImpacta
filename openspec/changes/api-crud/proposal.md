# Proposal

## Why

Para viabilizar a persistência e manipulação dinâmica dos dados acadêmicos dos alunos nas páginas do Streamlit (disciplinas e tarefas), é necessário criar os endpoints REST de CRUD (POST, GET, PATCH, DELETE) para as tabelas `subjects` e `academic_tasks` no backend Xano. É fundamental assegurar o isolamento dos dados por usuário (multitenancy por aluno), garantindo que cada usuário autenticado tenha acesso estritamente aos seus próprios registros.

## What Changes

- Criação dos endpoints CRUD autenticados para a tabela `subjects`:
  - `POST /subjects`: Criação de disciplina associando automaticamente `user_id = $auth.id`.
  - `GET /subjects`: Listagem de todas as disciplinas pertencentes ao usuário autenticado (`user_id == $auth.id`).
  - `GET /subjects/{subjects_id}`: Consulta detalhada de uma disciplina específica com validação de propriedade (`user_id == $auth.id`).
  - `PATCH /subjects/{subjects_id}`: Atualização parcial dos campos (`name`, `teacher`, `hours`) de uma disciplina do usuário.
  - `DELETE /subjects/{subjects_id}`: Exclusão de uma disciplina pertencente ao usuário.
- Criação dos endpoints CRUD autenticados para a tabela `academic_tasks`:
  - `POST /academic_tasks`: Criação de tarefa vinculada a uma disciplina (`subject_id`) que pertença ao usuário autenticado.
  - `GET /academic_tasks`: Listagem das tarefas acadêmicas pertencentes ao usuário autenticado (filtradas por disciplina do usuário).
  - `GET /academic_tasks/{academic_tasks_id}`: Consulta detalhada de uma tarefa específica do usuário.
  - `PATCH /academic_tasks/{academic_tasks_id}`: Atualização parcial (`title`, `description`, `due_date`, `status`) de uma tarefa do usuário.
  - `DELETE /academic_tasks/{academic_tasks_id}`: Remoção de uma tarefa pertencente ao usuário.
- Exigência de autenticação obrigatória via Bearer Token (`auth = "User"`) em todos os endpoints das duas tabelas.

## Capabilities

### New Capabilities
- `subjects-api`: Endpoints CRUD autenticados no Xano para gerenciamento de disciplinas com isolamento e segurança por usuário.
- `academic-tasks-api`: Endpoints CRUD autenticados no Xano para gerenciamento de tarefas acadêmicas vinculadas às disciplinas do usuário.

### Modified Capabilities

## Impact

- **Backend / Xano**: Novos arquivos de definição de endpoints XanoScript sob o diretório `api/` (ex: `api/subjects/` e `api/academic_tasks/`).
- **Segurança**: Bloqueio de acesso a registros de terceiros em todas as operações de leitura, edição e exclusão.
- **Frontend (Streamlit)**: Disponibilização dos endpoints para consumo nas abas "Disciplinas" e "Tarefas" do EduTrack AI.

