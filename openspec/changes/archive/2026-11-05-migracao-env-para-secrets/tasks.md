# Tasks

## 1. Configuração de Secrets

- [x] 1.1 Corrigir e padronizar o arquivo `.streamlit/secrets.toml` com a sintaxe TOML válida para as URLs base (`URL_base_AUTH`, `URL_base_SUBJECTS`, `URL_base_ACADEMIC_TASKS`).

## 2. Migração nas Páginas Streamlit

- [x] 2.1 Atualizar `pages/1_📚_Disciplinas.py` substituindo a leitura manual do `.env` pela leitura de `URL_base_SUBJECTS` via `st.secrets`.
- [x] 2.2 Atualizar `pages/2_📝_Tarefas.py` substituindo a leitura manual do `.env` pela leitura de `URL_base_SUBJECTS` e `URL_base_ACADEMIC_TASKS` via `st.secrets`.
- [x] 2.3 Atualizar `pages/3_👤_Perfil.py` substituindo a leitura manual do `.env` pela leitura de `URL_base_AUTH` via `st.secrets`.

