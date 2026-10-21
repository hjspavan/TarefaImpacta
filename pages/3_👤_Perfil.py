import os
from pathlib import Path
import requests
import streamlit as st

st.set_page_config(page_title="Perfil - EduTrack AI", page_icon="👤")

def get_auth_base_url() -> str:
    """Carrega a URL base dos endpoints de autenticação a partir do .env."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        if key.strip() in ("URL_base_AUTH", "AUTH_BASE_URL"):
                            return val.strip().strip('"').strip("'")
        except Exception:
            pass
    return os.environ.get("URL_base_AUTH") or os.environ.get("AUTH_BASE_URL", "")

def auth_signup(base_url: str, name: str, email: str, password: str):
    """Envia requisição para cadastro de novo usuário no endpoint auth/signup."""
    url = f"{base_url.rstrip('/')}/auth/signup"
    payload = {"name": name, "email": email, "password": password}
    return requests.post(url, json=payload, timeout=10)

def auth_login(base_url: str, email: str, password: str):
    """Envia requisição para autenticação de usuário no endpoint auth/login."""
    url = f"{base_url.rstrip('/')}/auth/login"
    payload = {"email": email, "password": password}
    return requests.post(url, json=payload, timeout=10)

def auth_me(base_url: str, token: str):
    """Consulta dados do perfil do usuário autenticado no endpoint auth/me."""
    url = f"{base_url.rstrip('/')}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=10)

# Inicialização da URL base
base_url = get_auth_base_url()

if not base_url:
    st.error("A URL base de autenticação (`URL_base_AUTH`) não foi encontrada no arquivo `.env` na raiz do projeto.")
    st.stop()

# Inicialização de estado da sessão
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_data" not in st.session_state:
    st.session_state["user_data"] = None

# Fluxo de Usuário Logado
if st.session_state["auth_token"]:
    st.title("👤 Meu Perfil")

    # Atualiza ou recupera os dados do usuário autenticado se necessário
    if not st.session_state["user_data"]:
        with st.spinner("Carregando perfil..."):
            try:
                res = auth_me(base_url, st.session_state["auth_token"])
                if res.status_code == 200:
                    st.session_state["user_data"] = res.json()
                elif res.status_code in (401, 403):
                    st.warning("Sessão expirada. Faça login novamente.")
                    st.session_state["auth_token"] = None
                    st.session_state["user_data"] = None
                    st.rerun()
                else:
                    st.error("Não foi possível carregar os dados do perfil.")
            except Exception as e:
                st.error(f"Erro ao conectar com o serviço de autenticação: {e}")

    user = st.session_state.get("user_data") or {}

    if user:
        st.subheader(f"Olá, {user.get('name', 'Estudante')}! 👋")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nome", value=str(user.get("name", "")), disabled=True)
            st.text_input("Identificador (ID)", value=str(user.get("id", "")), disabled=True)
        with col2:
            st.text_input("E-mail", value=str(user.get("email", "")), disabled=True)
            created_at = user.get("created_at")
            if created_at:
                st.text_input("Conta criada em", value=str(created_at), disabled=True)

    st.divider()

    if st.button("🚪 Sair da Conta (Logout)", type="secondary"):
        st.session_state["auth_token"] = None
        st.session_state["user_data"] = None
        st.success("Você saiu da sua conta.")
        st.rerun()

# Fluxo de Usuário Não Logado (Login / Cadastro)
else:
    st.title("👤 Acesso à Plataforma")
    st.write("Faça login com sua conta ou cadastre-se para acessar suas disciplinas e tarefas.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Cadastrar (Signup)"])

    # Aba de Login
    with tab_login:
        st.subheader("Login de Usuário")
        with st.form("form_login"):
            login_email = st.text_input("E-mail", key="login_email").strip()
            login_password = st.text_input("Senha", type="password", key="login_password").strip()
            submit_login = st.form_submit_button("Entrar")

            if submit_login:
                if not login_email or not login_password:
                    st.warning("Por favor, preencha o e-mail e a senha.")
                else:
                    with st.spinner("Autenticando..."):
                        try:
                            response = auth_login(base_url, login_email, login_password)
                            if response.status_code == 200:
                                data = response.json()
                                token = data.get("authToken")
                                if token:
                                    st.session_state["auth_token"] = token
                                    # Consulta os dados do perfil em auth/me
                                    me_res = auth_me(base_url, token)
                                    if me_res.status_code == 200:
                                        st.session_state["user_data"] = me_res.json()
                                    st.success("Login realizado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Token de autenticação não retornado pelo servidor.")
                            else:
                                err_msg = response.json().get("message", "Credenciais inválidas. Verifique seu e-mail e senha.")
                                st.error(f"Erro no login: {err_msg}")
                        except Exception as e:
                            st.error(f"Erro de conexão com o backend: {e}")

    # Aba de Cadastro
    with tab_signup:
        st.subheader("Criar Nova Conta")
        with st.form("form_signup"):
            signup_name = st.text_input("Nome Completo", key="signup_name").strip()
            signup_email = st.text_input("E-mail", key="signup_email").strip()
            signup_password = st.text_input("Senha", type="password", key="signup_password").strip()
            submit_signup = st.form_submit_button("Criar Conta")

            if submit_signup:
                if not signup_name or not signup_email or not signup_password:
                    st.warning("Por favor, preencha todos os campos obrigatórios.")
                else:
                    with st.spinner("Cadastrando..."):
                        try:
                            response = auth_signup(base_url, signup_name, signup_email, signup_password)
                            if response.status_code == 200:
                                data = response.json()
                                token = data.get("authToken")
                                if token:
                                    st.session_state["auth_token"] = token
                                    # Consulta os dados do perfil em auth/me
                                    me_res = auth_me(base_url, token)
                                    if me_res.status_code == 200:
                                        st.session_state["user_data"] = me_res.json()
                                    st.success("Cadastro realizado com sucesso!")
                                    st.rerun()
                                else:
                                    st.success("Conta criada com sucesso! Faça login na aba ao lado.")
                            else:
                                err_msg = response.json().get("message", "Não foi possível concluir o cadastro.")
                                st.error(f"Erro no cadastro: {err_msg}")
                        except Exception as e:
                            st.error(f"Erro de conexão com o backend: {e}")
