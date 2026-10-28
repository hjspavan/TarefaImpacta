# Tasks

## 1. Subjects API Endpoints

- [x] 1.1 Criar a definição do grupo de API `api/subjects/subjects.xs` e verificar a criação do arquivo.
- [x] 1.2 Criar o endpoint `POST /subjects` em `api/subjects/subjects_POST.xs` com `auth = "User"` e vinculação automática de `user_id = $auth.id`, verificando os campos de entrada e saída.
- [x] 1.3 Criar o endpoint `GET /subjects` em `api/subjects/subjects_GET.xs` com `auth = "User"` e filtro `where user_id == $auth.id`, verificando a consulta filtrada.
- [x] 1.4 Criar o endpoint `GET /subjects/{subjects_id}` em `api/subjects/subjects/subjects_id_GET.xs` com `auth = "User"` e verificação de propriedade (`user_id == $auth.id`), verificando a lógica de recuperação e retorno 404/403.
- [x] 1.5 Criar o endpoint `PATCH /subjects/{subjects_id}` em `api/subjects/subjects/subjects_id_PATCH.xs` com `auth = "User"` e validação de propriedade (`user_id == $auth.id`), verificando os campos atualizáveis.
- [x] 1.6 Criar o endpoint `DELETE /subjects/{subjects_id}` em `api/subjects/subjects/subjects_id_DELETE.xs` com `auth = "User"` e validação de propriedade (`user_id == $auth.id`), verificando a lógica de remoção.

## 2. Academic Tasks API Endpoints

- [x] 2.1 Criar a definição do grupo de API `api/academic_tasks/academic_tasks.xs` e verificar a criação do arquivo.
- [x] 2.2 Criar o endpoint `POST /academic_tasks` em `api/academic_tasks/academic_tasks_POST.xs` com `auth = "User"` e validação prévia de propriedade da disciplina (`subject_id` pertencente a `$auth.id`), verificando a inserção da tarefa.
- [x] 2.3 Criar o endpoint `GET /academic_tasks` em `api/academic_tasks/academic_tasks_GET.xs` com `auth = "User"` e filtro das tarefas vinculadas às disciplinas do usuário (`subjects.user_id == $auth.id`), verificando o retorno da listagem.
- [x] 2.4 Criar o endpoint `GET /academic_tasks/{academic_tasks_id}` em `api/academic_tasks/academic_tasks/academic_tasks_id_GET.xs` com `auth = "User"` e validação de propriedade da disciplina associada, verificando o retorno da tarefa.
- [x] 2.5 Criar o endpoint `PATCH /academic_tasks/{academic_tasks_id}` em `api/academic_tasks/academic_tasks/academic_tasks_id_PATCH.xs` com `auth = "User"` e validação de propriedade da disciplina associada, verificando a atualização parcial dos campos.
- [x] 2.6 Criar o endpoint `DELETE /academic_tasks/{academic_tasks_id}` em `api/academic_tasks/academic_tasks/academic_tasks_id_DELETE.xs` com `auth = "User"` e validação de propriedade da disciplina associada, verificando a lógica de exclusão.

