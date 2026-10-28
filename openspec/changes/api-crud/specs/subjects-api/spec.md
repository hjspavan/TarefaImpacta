# Spec Delta

## Purpose

Define a especificação dos endpoints REST de CRUD para a tabela `subjects` no backend Xano com autenticação obrigatória e isolamento de dados por usuário.

## ADDED Requirements

### Requirement: Authenticated creation of subjects
O sistema SHALL disponibilizar o endpoint `POST /subjects` que cria uma nova disciplina associada automaticamente ao usuário autenticado (`user_id = $auth.id`).

#### Scenario: Creating a subject successfully
- **WHEN** um usuário autenticado envia uma requisição POST para `/subjects` com os campos `name`, `teacher` e `hours`
- **THEN** o sistema cria o registro na tabela `subjects` vinculando o campo `user_id` ao ID do usuário autenticado e retorna o registro criado com status 200.

#### Scenario: Unauthorized creation attempt
- **WHEN** uma requisição POST para `/subjects` é realizada sem token de autenticação válido
- **THEN** o sistema recusa a requisição retornando erro de não autorizado (401).

### Requirement: Listing user subjects with isolation
O sistema SHALL disponibilizar o endpoint `GET /subjects` que retorna exclusivamente as disciplinas pertencentes ao usuário autenticado (`where user_id == $auth.id`).

#### Scenario: Querying subjects list
- **WHEN** o usuário autenticado envia uma requisição GET para `/subjects`
- **THEN** o sistema retorna uma lista contendo apenas as disciplinas cujo `user_id` corresponde ao ID do usuário logado.

### Requirement: Retrieve single subject with ownership verification
O sistema SHALL disponibilizar o endpoint `GET /subjects/{subjects_id}` para obter os detalhes de uma disciplina específica, garantindo que o registro pertença ao usuário autenticado.

#### Scenario: Accessing own subject by ID
- **WHEN** o usuário autenticado solicita os dados de uma disciplina de sua propriedade através de `GET /subjects/{subjects_id}`
- **THEN** o sistema retorna os dados completos da disciplina solicitada.

#### Scenario: Attempting to access another user's subject
- **WHEN** o usuário autenticado solicita uma disciplina pertencente a outro usuário
- **THEN** o sistema retorna erro de registro não encontrado (404) ou acesso proibido (403), impedindo o vazamento de dados.

### Requirement: Update user subject with ownership verification
O sistema SHALL disponibilizar o endpoint `PATCH /subjects/{subjects_id}` para atualização parcial dos campos (`name`, `teacher`, `hours`) de uma disciplina pertencente ao usuário autenticado.

#### Scenario: Updating own subject
- **WHEN** o usuário autenticado envia campos atualizados para uma disciplina de sua propriedade
- **THEN** o sistema atualiza o registro na tabela `subjects` e retorna a entidade atualizada.

#### Scenario: Attempting to update another user's subject
- **WHEN** o usuário tenta atualizar uma disciplina que não pertence ao seu `user_id`
- **THEN** o sistema rejeita a alteração e mantém os dados originais inalterados.

### Requirement: Delete user subject with ownership verification
O sistema SHALL disponibilizar o endpoint `DELETE /subjects/{subjects_id}` para remover uma disciplina pertencente ao usuário autenticado.

#### Scenario: Deleting own subject
- **WHEN** o usuário autenticado solicita a exclusão de uma disciplina de sua propriedade
- **THEN** o sistema remove o registro da tabela `subjects` e retorna confirmação de sucesso.

#### Scenario: Attempting to delete another user's subject
- **WHEN** o usuário tenta excluir uma disciplina que pertence a outro usuário
- **THEN** o sistema recusa a exclusão mantendo o registro intacto.

