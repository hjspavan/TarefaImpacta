# Design

## Context

O EduTrack AI é uma aplicação construída com Streamlit no frontend e Xano no backend. Atualmente, o arquivo `pages/3_👤_Perfil.py` contém apenas campos estáticos simulados. Para viabilizar a experiência do aluno, implementaremos a comunicação real com a API de autenticação do Xano (`auth/login`, `auth/signup`, `auth/me`), consumindo a URL base definida no arquivo `.env`. Veja `proposal.md` para a motivação geral.

## Goals / Non-Goals

**Goals:**
- Implementar o fluxo completo de cadastro (`auth/signup`), login (`auth/login`) e visualização de perfil (`auth/me`) em `pages/3_👤_Perfil.py`.
- Carregar a URL base dos endpoints a partir do arquivo `.env` na raiz do projeto (`URL_base_AUTH`).
- Persistir o token de autenticação e os dados do usuário autenticado em `st.session_state`.
- Oferecer opção de logout que reinicia a sessão do usuário no Streamlit.

**Non-Goals:**
- Criação de novos endpoints ou modificação do esquema do Xano no servidor (os endpoints `auth/*` e a tabela `user` são padrão do Xano).
- Implementação de recuperação de senha por e-mail nesta etapa.
- Proteção de rota nas demais páginas (pode ser expandido em mudanças futuras).

## Decisions

### 1. Leitura de Configuração do `.env`
- **Decisão**: Implementar uma função utilitária para leitura do arquivo `.env` na raiz do projeto utilizando a biblioteca padrão do Python (`pathlib` / leitura de pares chave=valor) ou `os.environ`.
- **Racional**: Garante portabilidade imediata sem depender de bibliotecas externas adicionais além das já presentes no projeto (`requests`, `streamlit`).

### 2. Chamadas HTTP aos Endpoints Xano
- **Decisão**: Utilizar a biblioteca `requests` para executar as requisições:
  - `POST {URL_base_AUTH}/auth/signup` com payload JSON contendo `name`, `email`, `password`.
  - `POST {URL_base_AUTH}/auth/login` com payload JSON contendo `email`, `password`.
  - `GET {URL_base_AUTH}/auth/me` com cabeçalho `Authorization: Bearer <authToken>`.
- **Tratamento de Erros**: Tratar códigos de status diferentes de 200 (ex: 400 ou 403) exibindo a mensagem retornada pelo Xano ou aviso amigável via `st.error()`.

### 3. Estrutura da Interface em `pages/3_👤_Perfil.py`
- **Decisão**: Utilizar `st.session_state` para alternar entre os estados:
  - **Estado Deslogado**: Apresentar abas (`st.tabs(["Login", "Cadastro"])`) com formulários para cada ação. Ao obter sucesso, armazena `authToken` no `st.session_state` e chama `auth/me` para carregar o perfil.
  - **Estado Logado**: Exibir cartão com os dados do aluno (`name`, `email`, `id`), mensagem de boas-vindas e botão de "Sair da Conta" (Logout).

## Risks / Trade-offs

- **[Ausência da variável no .env]** → Mitigação: Validar a presença de `URL_base_AUTH` ao carregar a página e exibir mensagem explicativa caso o valor esteja ausente.
- **[Expiração do token JWT]** → Mitigação: Ao receber erro 401/403 na chamada para `auth/me`, limpar `st.session_state` e direcionar para nova autenticação.

## Migration Plan

1. Confirmar/definir a variável `URL_base_AUTH` no arquivo `.env` da raiz.
2. Substituir o conteúdo de `pages/3_👤_Perfil.py` pela implementação com funções de integração Xano e interface Streamlit.
3. Testar os fluxos de cadastro, login, exibição de perfil e logout.

