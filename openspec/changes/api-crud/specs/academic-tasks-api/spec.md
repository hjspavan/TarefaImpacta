# Spec Delta

## Purpose

Define a especificação dos endpoints REST de CRUD para a tabela `academic_tasks` no backend Xano com autenticação obrigatória e isolamento de dados por usuário baseado nas disciplinas pertencentes.

## ADDED Requirements

### Requirement: Authenticated creation of academic tasks
O sistema SHALL disponibilizar o endpoint `POST /academic_tasks` que cria uma nova tarefa associada a uma disciplina (`subject_id`) pertencente ao usuário autenticado.

#### Scenario: Creating an academic task successfully
- **WHEN** um usuário autenticado envia uma requisição POST para `/academic_tasks` com `title`, `description`, `due_date`, `status` e um `subject_id` pertencente ao usuário
- **THEN** o sistema cria o registro na tabela `academic_tasks` e retorna os dados da tarefa criada com status 200.

#### Scenario: Rejecting creation with subject owned by another user
- **WHEN** um usuário autenticado tenta criar uma tarefa informando um `subject_id` pertencente a outro usuário ou inexistente
- **THEN** o sistema recusa a criação retornando erro de autorização ou recurso não encontrado (403/404).

#### Scenario: Unauthorized creation attempt
- **WHEN** uma requisição POST para `/academic_tasks` é enviada sem token de autenticação válido
- **THEN** o sistema recusa a requisição com erro de não autorizado (401).

### Requirement: Listing user academic tasks with isolation
O sistema SHALL disponibilizar o endpoint `GET /academic_tasks` que retorna exclusivamente as tarefas vinculadas às disciplinas pertencentes ao usuário autenticado.

#### Scenario: Querying academic tasks list
- **WHEN** o usuário autenticado envia uma requisição GET para `/academic_tasks`
- **THEN** o sistema retorna a lista de tarefas associadas às disciplinas de propriedade do usuário autenticado.

#### Scenario: Filtering tasks by subject
- **WHEN** o usuário autenticado envia uma requisição GET para `/academic_tasks` com o parâmetro opcional `subject_id` de uma disciplina de sua propriedade
- **THEN** o sistema retorna apenas as tarefas correspondentes àquela disciplina específica.

### Requirement: Retrieve single academic task with ownership verification
O sistema SHALL disponibilizar o endpoint `GET /academic_tasks/{academic_tasks_id}` para consultar uma tarefa específica, garantindo que ela pertença a uma disciplina do usuário autenticado.

#### Scenario: Accessing own task by ID
- **WHEN** o usuário autenticado solicita os dados de uma tarefa através de `GET /academic_tasks/{academic_tasks_id}` cuja disciplina pertença a ele
- **THEN** o sistema retorna os dados detalhados da tarefa solicitada.

#### Scenario: Attempting to access another user's task
- **WHEN** o usuário autenticado tenta consultar uma tarefa vinculada a uma disciplina de outro usuário
- **THEN** o sistema recusa o acesso retornando erro de registro não encontrado (404) ou acesso proibido (403).

### Requirement: Update academic task with ownership verification
O sistema SHALL disponibilizar o endpoint `PATCH /academic_tasks/{academic_tasks_id}` para atualização parcial dos dados da tarefa (`title`, `description`, `due_date`, `status`, `subject_id`), assegurando que tanto a tarefa quanto a nova disciplina pertençam ao usuário autenticado.

#### Scenario: Updating own academic task
- **WHEN** o usuário autenticado envia dados parciais válidos para atualizar uma tarefa vinculada a uma disciplina de sua propriedade
- **THEN** o sistema atualiza o registro na tabela `academic_tasks` e retorna o registro atualizado.

#### Scenario: Attempting to update another user's task
- **WHEN** o usuário tenta atualizar uma tarefa associada a uma disciplina de outro usuário
- **THEN** o sistema rejeita a alteração e mantém os dados originais inalterados.

### Requirement: Delete academic task with ownership verification
O sistema SHALL disponibilizar o endpoint `DELETE /academic_tasks/{academic_tasks_id}` para remover uma tarefa pertencente ao usuário autenticado.

#### Scenario: Deleting own task
- **WHEN** o usuário autenticado solicita a exclusão de uma tarefa associada a uma disciplina de sua propriedade
- **THEN** o sistema remove o registro da tabela `academic_tasks` e retorna confirmação de sucesso.

#### Scenario: Attempting to delete another user's task
- **WHEN** o usuário tenta excluir uma tarefa que pertence às disciplinas de outro usuário
- **THEN** o sistema rejeita a exclusão mantendo o registro intacto.

