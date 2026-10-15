# academic-tasks Specification

## Purpose
Define a estrutura de dados e as regras de integridade da tabela `academic_tasks` no backend Xano, permitindo que os alunos registrem e gerenciem suas obrigações acadêmicas vinculadas às disciplinas.

## Requirements

### Requirement: Academic tasks table schema definition
O sistema SHALL definir o esquema da tabela `academic_tasks` no backend Xano contendo os seguintes campos:
- `id`: identificador primário auto-incremental (integer, auto-increment, primary key).
- `title`: título da obrigação acadêmica (text, obrigatório).
- `description`: descrição ou orientações detalhadas da tarefa (text, opcional).
- `due_date`: data de entrega ou realização da tarefa (date / timestamp, opcional).
- `status`: situação da tarefa (text, obrigatório, ex.: pendente, em andamento, concluída).
- `subject_id`: chave estrangeira (integer, foreign key / table reference) apontando para a tabela `subjects`.

#### Scenario: Valid table schema structure
- **WHEN** o esquema da tabela `academic_tasks` é inspecionado ou sincronizado no backend Xano
- **THEN** a tabela deve conter as colunas `id`, `title`, `description`, `due_date`, `status` e `subject_id` com seus respectivos tipos e restrições.

### Requirement: Association of academic tasks with subjects
O sistema SHALL vincular cada obrigação acadêmica a uma disciplina existente por meio do campo `subject_id`.

#### Scenario: Creating an academic task linked to an existing subject
- **WHEN** um aluno cria uma nova tarefa informando um `subject_id` válido
- **THEN** a tarefa é persistida com o vínculo relacional correto com a disciplina correspondente.

#### Scenario: Rejecting academic task creation with non-existent subject
- **WHEN** a criação de uma tarefa for solicitada com um `subject_id` inexistente na tabela `subjects`
- **THEN** o sistema SHALL recusar a operação garantindo a integridade referencial.

### Requirement: Task status tracking
O sistema SHALL registrar e manter atualizado o estado de conclusão de cada obrigação acadêmica por meio do campo `status`.

#### Scenario: Updating status of an academic task
- **WHEN** o aluno altera a situação de uma tarefa (ex.: de "pendente" para "concluída")
- **THEN** o sistema SHALL persistir o novo valor de `status` para o registro correspondente.
