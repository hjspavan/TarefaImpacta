# Proposal: Define Subjects Table Schema

## Why
Definir a estrutura de dados da tabela `subjects` no Xano para armazenamento de disciplinas associadas aos usuários autenticados da aplicação. Esta definição estabelece o contrato do esquema de dados necessário para persistência de matérias/disciplinas.

## What Changes
- Definição da estrutura e tipos de campos da tabela `subjects`:
  - `id` (auto): identificador primário auto-incremental.
  - `name` (text): nome da disciplina.
  - `teacher` (text): nome do professor responsável.
  - `hours` (int): carga horária da disciplina.
  - `user_id` (FK): referência à tabela de autenticação de usuários do Xano (`user`/`users`).

## Capabilities

### New Capabilities
- `subjects`: Especificação do esquema de dados da tabela `subjects` e seus relacionamentos no Xano.

### Modified Capabilities
<!-- Nenhuma capacidade existente modificada -->

## Impact
- Esquema de banco de dados no Xano.
- Criação dos artefatos de especificação e definição técnica (.xs / specs).
- Sem geração automática de APIs CRUD, testes ou interface frontend, respeitando as restrições de escopo de `AGENTES.md`.

