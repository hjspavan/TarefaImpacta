# Proposal

## Why

Atualmente, as páginas do frontend Streamlit (`1_📚_Disciplinas.py`, `2_📝_Tarefas.py` e `3_👤_Perfil.py`) realizam a leitura manual de arquivos `.env` na raiz do projeto para obter as URLs base das APIs do Xano. O Streamlit disponibiliza um mecanismo nativo, seguro e padronizado para gerenciamento de credenciais e configurações (`st.secrets`), facilitando tanto o desenvolvimento local (via `.streamlit/secrets.toml`) quanto o deploy em nuvem (Streamlit Community Cloud). A migração para `st.secrets` padroniza o acesso a configurações e elimina código redundante de parsing manual de arquivos de ambiente.

## What Changes

- Migração da leitura das variáveis de URL (`URL_base_AUTH`, `URL_base_SUBJECTS`, `URL_base_ACADEMIC_TASKS`) nas páginas Streamlit para utilizar prioritariamente `st.secrets`.
- Manutenção de fallback opcional para variáveis de ambiente (`os.environ`) para preservar compatibilidade em scripts que rodam fora do servidor Streamlit.
- Ajuste e validação do arquivo `.streamlit/secrets.toml` com a sintaxe TOML correta.
- Garantia de que `.streamlit/` ou `.streamlit/secrets.toml` permaneça ignorado no `.gitignore` para proteção das credenciais.

## Capabilities

### New Capabilities
- `streamlit-secrets`: Gerenciamento e leitura de URLs base de APIs e parâmetros de configuração do EduTrack AI através do mecanismo nativo `st.secrets` do Streamlit.

### Modified Capabilities

## Impact

- **Frontend (Streamlit)**: Atualização das funções de leitura de URLs nas páginas `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py`.
- **Configuração**: Padronização do `.streamlit/secrets.toml`.
- **Segurança**: Prevenção de commit acidental de secrets via `.gitignore`.

