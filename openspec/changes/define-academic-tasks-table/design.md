# Design

## Context

O sistema EduTrack AI gerencia a vida acadêmica dos estudantes utilizando o backend Xano. A tabela `subjects` já foi estruturada (`tables/subjects.xs`), representando as matérias em que o aluno está matriculado. A tabela `academic_tasks` complementa esse domínio permitindo registrar lições, provas e trabalhos vinculados a essas disciplinas. Veja `proposal.md` para a motivação geral.

## Goals / Non-Goals

**Goals:**
- Definir tecnicamente o esquema da tabela `academic_tasks` no formato XanoScript (`tables/academic_tasks.xs`).
- Configurar todos os campos solicitados: `id` (PK auto-increment), `title` (text), `description` (text), `due_date` (date/timestamp), `status` (text) e `subject_id` (FK para `subjects`).
- Estabelecer a integridade referencial com a tabela `subjects`.

**Non-Goals:**
- Criação de endpoints de API REST no Xano nesta mudança.
- Integração ou telas de gerenciamento no frontend Streamlit (`app.py`).
- Implementação de notificações ou alertas de prazos.

## Decisions

### 1. Modelagem dos Campos em XanoScript
- **Decisão**:
  - `id`: Integer, auto-increment, chave primária indexada (`int id`).
  - `title`: Text, obrigatório (`text title`).
  - `description`: Text, opcional (`text description?`).
  - `due_date`: Timestamp/Date para representação de prazos e datas de entrega (`timestamp due_date?`).
  - `status`: Text para armazenar o estado da tarefa (`text status`), suportando estados como "pendente", "em andamento" e "concluída".
  - `subject_id`: Integer com atributo `table = "subjects"`, estabelecendo a chave estrangeira (FK) relacional com a tabela de disciplinas.
- **Alternativas consideradas**:
  - `enum` para o status: Descartado em favor de `text` simples para manter flexibilidade nos fluxos de trabalho do usuário e compatibilidade direta com a solicitação.

### 2. Relacionamento com a Tabela subjects
- **Decisão**: Configurar `subject_id` como Table Reference para a tabela `subjects`.
- **Racional**: Garante consistência referencial, impedindo tarefas orfãs de disciplinas inexistentes e viabilizando agrupamentos e consultas conjuntas por disciplina.

## Risks / Trade-offs

- **[Integridade na remoção de disciplina]** → Mitigação: Recomenda-se configurar regra de exclusão restrita ou remoção em cascata no Xano caso uma disciplina seja deletada.

## Migration Plan

1. Definir o esquema em `tables/academic_tasks.xs`.
2. Sincronizar/criar a tabela no workspace do Xano (`148582`, branch `v1`).
3. Verificar a associação da chave estrangeira apontando para `subjects`.

