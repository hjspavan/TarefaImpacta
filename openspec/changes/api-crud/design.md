# Design

## Context

O sistema EduTrack AI necessita de endpoints de CRUD (Create, Read, Update, Delete) no backend Xano para gerenciar as disciplinas (`subjects`) e as tarefas acadêmicas (`academic_tasks`).
Atualmente, as definições das tabelas já existem no projeto em `table/subjects.xs` e `table/academic_tasks.xs`.
A tabela `subjects` possui os campos `id`, `name`, `teacher`, `hours` e `user_id`. A tabela `academic_tasks` possui os campos `id`, `title`, `description`, `due_date`, `status` e `subject_id` (com chave estrangeira apontando para `subjects`).
É requisito crítico de arquitetura e segurança que todas as operações sejam protegidas por autenticação de usuário (`auth = "User"`) e que nenhum usuário tenha permissão para ler, alterar ou excluir registros pertencentes a outro estudante.

Consulte `proposal.md` para mais detalhes de motivação e escopo.

## Goals / Non-Goals

**Goals:**
- Projetar endpoints CRUD padronizados para `subjects` (`POST`, `GET`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`) com `auth = "User"` e filtro direto por `user_id == $auth.id`.
- Projetar endpoints CRUD padronizados para `academic_tasks` (`POST`, `GET`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`) com `auth = "User"` e validação relacional de propriedade através de `subject_id` pertencente a `user_id == $auth.id`.
- Estruturar os arquivos XanoScript em diretórios dedicados (`api/subjects/` e `api/academic_tasks/`).

**Non-Goals:**
- Alterar o esquema ou colunas das tabelas `subjects` e `academic_tasks`.
- Implementar telas ou lógica de frontend no Streamlit nesta mudança (escopo exclusivo de APIs de backend).
- Realizar deploy, push ou sincronização automática com o Xano remoto (conforme diretrizes em `AGENTES.md`, o escopo se encerra na geração dos arquivos locais).

## Decisions

### Decisão 1: Organização dos Grupos de API (API Groups)
- **Decisão**: Criar dois grupos de API modulares no XanoScript:
  - `api/subjects/` para endpoints de disciplinas: `subjects.xs`, `subjects_POST.xs`, `subjects_GET.xs`, e sob `subjects/`: `subjects_id_GET.xs`, `subjects_id_PATCH.xs`, `subjects_id_DELETE.xs`.
  - `api/academic_tasks/` para endpoints de tarefas: `academic_tasks.xs`, `academic_tasks_POST.xs`, `academic_tasks_GET.xs`, e sob `academic_tasks/`: `academic_tasks_id_GET.xs`, `academic_tasks_id_PATCH.xs`, `academic_tasks_id_DELETE.xs`.
- **Racional**: Segue a convenção do XanoScript observada em `api/auth/` e `api/api_browser/`, mantendo a separação clara de responsabilidades por recurso.
- **Alternativas consideradas**:
  - Misturar os endpoints em `api_browser`: Descartado pois `api_browser` continha endpoints de teste sem autenticação e modelo antigo.

### Decisão 2: Modelo de Isolamento de Dados para `subjects`
- **Decisão**:
  - `POST /subjects`: Atribuir `user_id = $auth.id` diretamente a partir do token de autenticação JWT, ignorando qualquer valor informado no body da requisição.
  - `GET /subjects`: Filtrar os registros com `where = $db.subjects.user_id == $auth.id`.
  - `GET /subjects/{id}`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`: Buscar ou modificar o registro condicionado a `id == $input.subjects_id` E `user_id == $auth.id`. Caso o registro não pertença ao usuário, retornar erro 404 (Not Found) ou 403 (Forbidden).
- **Racional**: Previne vulnerabilidades de Broken Object Level Authorization (BOLA/IDOR), impedindo que um usuário acesse ou sobrescreva disciplinas de outro estudante.
- **Alternativas consideradas**:
  - Confiar em `user_id` enviado no payload: Descartado veementemente por violar princípios básicos de segurança.

### Decisão 3: Modelo de Isolamento e Validação para `academic_tasks`
- **Decisão**:
  - `POST /academic_tasks`: Antes de inserir a tarefa, verificar se a disciplina informada (`subject_id`) existe e tem `user_id == $auth.id`. Se não pertencer, abortar a operação com erro.
  - `GET /academic_tasks`: Consultar as tarefas fazendo join ou filtrando `subject_id` pertencente à lista de disciplinas do usuário autenticado (`subjects.user_id == $auth.id`). Permitir filtro opcional por `subject_id` específico.
  - `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`: Obter a tarefa e validar a propriedade da disciplina associada antes de efetuar leitura, atualização ou remoção. Em caso de alteração de `subject_id` no `PATCH`, validar também a nova disciplina.
- **Racional**: Garante a consistência relacional e integridade de isolamento mesmo que a tabela `academic_tasks` não possua uma coluna direta `user_id`.
- **Alternativas consideradas**:
  - Adicionar coluna redundante `user_id` em `academic_tasks`: Descartado para não alterar a tabela existente já definida e aprovada em `table/academic_tasks.xs`.

### Decisão 4: Padronização dos Verbos e Respostas HTTP
- **Decisão**:
  - Operações de leitura e listagem utilizam `verb=GET`.
  - Criação utiliza `verb=POST` retornando o registro criado.
  - Atualização utiliza `verb=PATCH` aplicando modificações parciais.
  - Exclusão utiliza `verb=DELETE` retornando confirmação.
  - Todos os endpoints definem `auth = "User"` como requisito obrigatório de autenticação.
- **Racional**: Alinhamento com a arquitetura REST e convenções nativas do Xano.

## Risks / Trade-offs

- **[Risco] Associação de tarefa a disciplina de outro usuário** → *Mitigação*: Validação explícita no endpoint `POST` e `PATCH` de `academic_tasks` verificando `db.get subjects` com `user_id == $auth.id` antes da mutação.
- **[Risco] Tentativa de acesso direto por ID a recursos de terceiros** → *Mitigação*: Todas as operações por ID utilizam cláusulas estritas verificando ownership, retornando erro quando o registro não pertencer ao usuário logado.
- **[Risco] Tarefas sem disciplina correspondente caso uma disciplina seja excluída** → *Mitigação*: Integridade referencial configurada no Xano na foreign key `subject_id -> subjects`.

## Migration Plan

1. Criar as definições de API group `api/subjects/subjects.xs` e `api/academic_tasks/academic_tasks.xs`.
2. Implementar os arquivos de endpoints XanoScript para `subjects`:
   - `POST /subjects` (`subjects_POST.xs`)
   - `GET /subjects` (`subjects_GET.xs`)
   - `GET /subjects/{subjects_id}` (`subjects/subjects_id_GET.xs`)
   - `PATCH /subjects/{subjects_id}` (`subjects/subjects_id_PATCH.xs`)
   - `DELETE /subjects/{subjects_id}` (`subjects/subjects_id_DELETE.xs`)
3. Implementar os arquivos de endpoints XanoScript para `academic_tasks`:
   - `POST /academic_tasks` (`academic_tasks_POST.xs`)
   - `GET /academic_tasks` (`academic_tasks_GET.xs`)
   - `GET /academic_tasks/{academic_tasks_id}` (`academic_tasks/academic_tasks_id_GET.xs`)
   - `PATCH /academic_tasks/{academic_tasks_id}` (`academic_tasks/academic_tasks_id_PATCH.xs`)
   - `DELETE /academic_tasks/{academic_tasks_id}` (`academic_tasks/academic_tasks_id_DELETE.xs`)
4. Os arquivos serão mantidos no repositório local para revisão e posterior push manual pelo desenvolvedor.

