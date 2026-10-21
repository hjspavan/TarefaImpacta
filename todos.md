# TODOs

- [x] Definição do esquema da tabela `subjects` no formato XanoScript (`table/subjects.xs`) com os campos `id`, `name`, `teacher`, `hours` e `user_id` (FK para `user`/`users`).
- [x] Definição do esquema da tabela `academic_tasks` no formato XanoScript (`tables/academic_tasks.xs`) com os campos `id`, `title`, `description`, `due_date`, `status` e `subject_id` (FK para `subjects`).
- [x] Implementação de cadastro e login em `pages/3_👤_Perfil.py` consumindo os endpoints `auth/login`, `auth/signup` e `auth/me` do Xano com URL base no `.env`.
- [x] Implementação de cadastro e login em `pages/3_👤_Perfil.py` consumindo os endpoints `auth/login`, `auth/signup` e `auth/me` do Xano com URL base no `.env`.

