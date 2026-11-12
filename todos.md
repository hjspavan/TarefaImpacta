# TODOs

- [x] Definição do esquema da tabela `subjects` no formato XanoScript (`table/subjects.xs`) com os campos `id`, `name`, `teacher`, `hours` e `user_id` (FK para `user`/`users`).
- [x] Definição do esquema da tabela `academic_tasks` no formato XanoScript (`tables/academic_tasks.xs`) com os campos `id`, `title`, `description`, `due_date`, `status` e `subject_id` (FK para `subjects`).
- [x] Implementação de cadastro e login em `pages/3_👤_Perfil.py` consumindo os endpoints `auth/login`, `auth/signup` e `auth/me` do Xano com URL base no `.env`.
- [x] Criação dos endpoints CRUD autenticados (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `subjects` em `api/subjects/` com isolamento por usuário (`user_id == $auth.id`).
- [x] Criação dos endpoints CRUD autenticados (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `academic_tasks` em `api/academic_tasks/` com validação de propriedade via disciplina associada (`subjects.user_id == $auth.id`).
- [x] Migração da leitura de variáveis de ambiente do `.env` para `st.secrets` com fallback seguro em `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py`.
- [x] Implementação de script Python em `scripts/generate_performance_report.py` para geração de relatório de desempenho em PDF e criação do endpoint no Xano em `api/reports/performance_GET.xs` para download do relatório com `auth = "User"`.
