# user-auth Specification

## Purpose
Define os requisitos e cenários para cadastro, autenticação e gerenciamento de perfil de usuários na interface Streamlit integrando com os endpoints do Xano e variáveis de ambiente em `.env`.

## Requirements

### Requirement: Configuration of authentication base URL from environment
O sistema SHALL carregar a URL base dos endpoints de autenticação a partir do arquivo `.env` localizado na raiz do projeto.

#### Scenario: Base URL successfully loaded
- **WHEN** a página `pages/3_👤_Perfil.py` é carregada
- **THEN** o sistema lê a URL base de autenticação configurada no arquivo `.env` (ex.: `URL_base_AUTH`).

#### Scenario: Missing base URL configuration
- **WHEN** a variável com a URL base não estiver presente ou o arquivo `.env` não for encontrado
- **THEN** o sistema exibe uma mensagem de alerta orientando a configuração da variável de ambiente.

### Requirement: User registration via auth/signup
O sistema SHALL permitir que novos usuários realizem cadastro através de requisição POST ao endpoint `auth/signup` do Xano, persistindo os dados na tabela `user`.

#### Scenario: Successful user signup
- **WHEN** o usuário preenche nome, e-mail e senha válidos e submete o formulário de cadastro
- **THEN** o sistema envia os dados ao endpoint `auth/signup`, recebe o token de autenticação retornado pelo Xano e armazena na sessão do Streamlit.

#### Scenario: Registration failure
- **WHEN** a criação de conta falha devido a e-mail duplicado ou dados inválidos retornados pelo backend
- **THEN** o sistema SHALL exibir mensagem de erro amigável na interface mantendo o usuário no formulário de cadastro.

### Requirement: User authentication via auth/login
O sistema SHALL permitir que usuários existentes realizem login fornecendo e-mail e senha através de requisição POST ao endpoint `auth/login` do Xano.

#### Scenario: Successful login
- **WHEN** o usuário submete credenciais válidas (e-mail e senha)
- **THEN** o sistema envia a requisição para `auth/login`, recebe o token de autenticação (`authToken`) e salva o estado de autenticação em `st.session_state`.

#### Scenario: Failed login with invalid credentials
- **WHEN** o usuário submete e-mail ou senha incorretos
- **THEN** o sistema exibe mensagem de erro de autenticação e mantém o estado deslogado.

### Requirement: Fetch and display user profile via auth/me
O sistema SHALL consultar os dados do usuário autenticado no endpoint `auth/me` enviando o token no cabeçalho `Authorization: Bearer <token>`, permitindo a visualização dos dados e ação de logout.

#### Scenario: Display profile information for authenticated user
- **WHEN** um usuário com sessão ativa acessa `pages/3_👤_Perfil.py`
- **THEN** o sistema consulta o endpoint `auth/me` e exibe as informações do usuário (nome, e-mail, id) e o botão para encerrar a sessão.

#### Scenario: User logout
- **WHEN** o usuário autenticado aciona o botão de logout
- **THEN** o token e os dados de perfil são removidos de `st.session_state` e a interface volta a exibir as opções de login e cadastro.
