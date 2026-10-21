# Tasks

## 1. Configuração de Ambiente

- [x] 1.1 Configurar o arquivo `.env` na raiz do projeto com a URL base dos endpoints de autenticação do Xano (`URL_base_AUTH`) e validar sua leitura

## 2. Implementação da Autenticação em pages/3_👤_Perfil.py

- [x] 2.1 Implementar as funções de chamada HTTP aos endpoints `auth/signup`, `auth/login` e `auth/me` utilizando `requests` e a URL base do `.env`
- [x] 2.2 Desenvolver a interface de cadastro de novos usuários salvando os dados na tabela `user` via endpoint `auth/signup`
- [x] 2.3 Desenvolver a interface de login via endpoint `auth/login` persistindo o token de autenticação em `st.session_state`
- [x] 2.4 Desenvolver a visualização das informações do perfil do usuário obtidas via endpoint `auth/me` com opção de logout
