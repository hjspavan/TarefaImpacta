# Proposal

## Why

Para que os estudantes possam registrar, organizar e acompanhar o cumprimento de suas obrigações acadêmicas (como lições de casa, provas, seminários e trabalhos) no EduTrack AI, é necessário estruturar a entidade de tarefas vinculadas às matérias cadastradas. A criação da tabela `academic_tasks` no backend Xano provê a persistência necessária para associar cada obrigação à sua respectiva disciplina (`subjects`).

## What Changes

- Definição do esquema da tabela `academic_tasks` no backend Xano.
- Especificação dos campos da tabela:
  - `id`: identificador primário auto-incremental (auto-increment integer / PK).
  - `title`: título da obrigação acadêmica (text, obrigatório).
  - `description`: descrição ou instruções complementares da tarefa (text).
  - `due_date`: data limite ou data de realização da tarefa/prova (date / timestamp).
  - `status`: status atual da obrigação acadêmica (text, ex.: pendente, em andamento, concluída).
  - `subject_id`: chave estrangeira (FK / table reference) apontando para a tabela `subjects`.
- Estabelecimento do relacionamento relacional para que as tarefas estejam diretamente associadas a uma disciplina.

## Capabilities

### New Capabilities
- `academic-tasks`: Modela o esquema, regras de integridade e campos da tabela `academic_tasks` no backend Xano, vinculando tarefas acadêmicas a disciplinas (`subjects`).

### Modified Capabilities

## Impact

- **Backend / Xano**: Nova tabela `academic_tasks` no catálogo de tabelas do workspace (`tables/academic_tasks.xs`).
- **Modelo de Dados**: Relacionamento 1:N entre a tabela `subjects` e a tabela `academic_tasks`.
- **Frontend (Streamlit)**: Suporte para futura listagem e gerenciamento de tarefas na aba "Tarefas" do aplicativo `app.py`.

