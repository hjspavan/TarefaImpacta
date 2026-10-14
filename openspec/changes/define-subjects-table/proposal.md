<<<<<<< HEAD
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
=======
# Proposal

## Why

Para que o sistema EduTrack AI permita o gerenciamento de disciplinas acadêmicas vinculadas aos alunos, é necessário definir a estrutura da tabela `subjects` no backend Xano. Esta tabela viabiliza o armazenamento persistente das disciplinas, associando cada registro ao respectivo usuário autenticado.

## What Changes

- Criação e definição do esquema da tabela `subjects` no backend Xano.
- Configuração dos campos essenciais:
  - `id`: identificador único da disciplina (auto-increment integer / PK).
  - `name`: nome da disciplina/matéria (text, obrigatório).
  - `teacher`: nome do professor responsável (text).
  - `hours`: carga horária total da disciplina em horas (integer).
  - `user_id`: chave estrangeira (FK / table reference) apontando para a tabela de autenticação de usuários do Xano (`user`/`users`).
- Estabelecimento do relacionamento de pertencimento (ownership) para garantir que cada usuário gerencie suas próprias disciplinas.
>>>>>>> e43102d (feat: insercao do banco de dados xanoscript)

## Capabilities

### New Capabilities
<<<<<<< HEAD
- `subjects`: Especificação do esquema de dados da tabela `subjects` e seus relacionamentos no Xano.

### Modified Capabilities
<!-- Nenhuma capacidade existente modificada -->

## Impact
- Esquema de banco de dados no Xano.
- Criação dos artefatos de especificação e definição técnica (.xs / specs).
- Sem geração automática de APIs CRUD, testes ou interface frontend, respeitando as restrições de escopo de `AGENTES.md`.
=======
- `subjects`: Modela o esquema, regras de integridade e tipos de dados da tabela `subjects` no backend Xano associada ao usuário autenticado.

### Modified Capabilities

## Impact

- **Backend / Xano**: Nova tabela `subjects` adicionada ao catálogo de tabelas do workspace (`tables/`).
- **Segurança e Integridade**: Os registros de disciplinas estarão vinculados à tabela de autenticação (`user`/`users`), permitindo regras de controle de acesso (RBAC) e filtros por usuário.
- **Frontend (Streamlit)**: Preparação para integração de consumo dos dados de matérias em `app.py` (seção "Disciplinas").
>>>>>>> e43102d (feat: insercao do banco de dados xanoscript)

