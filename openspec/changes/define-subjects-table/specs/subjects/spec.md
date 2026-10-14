# Spec Delta

## Purpose

<<<<<<< HEAD
Define a estrutura de dados e relacionamentos da tabela subjects no Xano para gerenciamento de disciplinas de usuários.

## ADDED Requirements

### Requirement: Subjects Table Schema Definition
The system SHALL define a `subjects` database table in Xano with fields `id` (auto-increment integer), `name` (text), `teacher` (text), `hours` (integer), and `user_id` (foreign key to Xano auth table).

#### Scenario: Validating fields and types in subjects table
- **WHEN** the `subjects` table schema is evaluated
- **THEN** it contains `id` as auto-increment primary key, `name` as text, `teacher` as text, `hours` as integer, and `user_id` referencing the `user`/`users` table

### Requirement: User Authentication Reference
The system SHALL link records in the `subjects` table to the authenticated user using the `user_id` foreign key reference.

#### Scenario: Referential relationship with user table
- **WHEN** a record is created or verified in `subjects`
- **THEN** the `user_id` field must reference a valid entry in the Xano authentication table (`user`/`users`)
=======
Define a estrutura de dados e as regras de integridade da tabela `subjects` no backend Xano, permitindo armazenar disciplinas acadêmicas vinculadas aos usuários autenticados.

## ADDED Requirements

### Requirement: Subjects table schema definition
O sistema SHALL definir o esquema da tabela `subjects` no backend Xano com os seguintes campos:
- `id`: identificador primário auto-incremental (integer, auto-increment, primary key).
- `name`: nome da disciplina (text, obrigatório).
- `teacher`: nome do professor responsável (text, opcional).
- `hours`: carga horária da disciplina em horas (integer, obrigatório).
- `user_id`: chave estrangeira (integer, foreign key) com referência direta à tabela de autenticação de usuários do Xano (`user`/`users`).

#### Scenario: Valid table schema structure
- **WHEN** o esquema da tabela `subjects` é consultado ou sincronizado no backend Xano
- **THEN** a tabela deve conter os campos `id`, `name`, `teacher`, `hours` e `user_id` com os respectivos tipos e identificadores configurados.

### Requirement: User association and data isolation
O sistema SHALL associar cada registro de disciplina a um usuário específico por meio do campo `user_id`, garantindo que cada usuário acesse e gerencie apenas suas próprias disciplinas.

#### Scenario: Associating a subject with an authenticated user
- **WHEN** um novo registro de disciplina é criado para um usuário autenticado
- **THEN** o campo `user_id` deve armazenar o identificador do usuário correspondente na tabela de autenticação.

#### Scenario: Rejecting invalid user reference
- **WHEN** for solicitada a inserção de uma disciplina com um `user_id` inexistente na tabela de autenticação
- **THEN** o sistema SHALL rejeitar a operação para manter a integridade referencial.

### Requirement: Field validation for subjects
O sistema SHALL validar que o campo `name` seja uma string não vazia e que o campo `hours` seja um número inteiro positivo ou igual a zero.

#### Scenario: Subject payload meets validation constraints
- **WHEN** um registro de disciplina é enviado com nome válido e carga horária em horas como inteiro positivo
- **THEN** os dados são aceitos e validados com sucesso pelo backend.

#### Scenario: Subject payload with invalid hours value
- **WHEN** um registro de disciplina é enviado com carga horária negativa ou em formato inválido
- **THEN** o sistema SHALL retornar erro de validação e recusar o salvamento.
>>>>>>> e43102d (feat: insercao do banco de dados xanoscript)

