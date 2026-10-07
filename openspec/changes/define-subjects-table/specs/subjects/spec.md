# Spec Delta

## Purpose

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

