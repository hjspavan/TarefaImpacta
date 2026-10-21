# Proposal

## Why

Para permitir o acesso personalizado e seguro à plataforma EduTrack AI, é necessário implementar os fluxos de cadastro e autenticação de usuários na interface Streamlit em `pages/3_👤_Perfil.py`, integrando com os endpoints oficiais de autenticação do Xano (`auth/login`, `auth/signup`, `auth/me`) e utilizando as variáveis de ambiente armazenadas em `.env`.

## What Changes

- Configuração e leitura da URL base da API de autenticação a partir do arquivo `.env` na raiz do projeto.
- Implementação de interface interativa em `pages/3_👤_Perfil.py` com suporte aos fluxos:
  - **Cadastro (`auth/signup`)**: Permite que novos usuários informem nome, e-mail e senha para criar conta na tabela `user` do Xano.
  - **Login (`auth/login`)**: Autentica o usuário com e-mail e senha, recebendo o token de autenticação (JWT).
  - **Consulta de Perfil (`auth/me`)**: Recupera e exibe as informações do usuário autenticado utilizando o token no cabeçalho `Authorization`.
  - **Logout**: Limpa a sessão ativa no Streamlit (`st.session_state`).
- Gerenciamento de sessão de usuário via `st.session_state` no Streamlit para persistir o token e estado do usuário logado durante a navegação.

## Capabilities

### New Capabilities
- `user-auth`: Especifica os fluxos de cadastro, autenticação e recuperação de perfil do usuário integrado aos endpoints do Xano e gerenciamento de sessão no Streamlit.

### Modified Capabilities

## Impact

- **Frontend (`pages/3_👤_Perfil.py`)**: O script atual de mockup será substituído pelo fluxo real de cadastro, login e exibição de perfil.
- **Configuração (`.env`)**: Armazenamento e consumo da URL base da API de autenticação.
- **Dependências**: Utilização da biblioteca `requests` para chamadas HTTP aos endpoints do Xano e leitura de variáveis do `.env`.

