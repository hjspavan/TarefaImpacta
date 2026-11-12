
import os
import requests
import streamlit as st


st.set_page_config(
    page_title="Perfil - EduTrack AI",
    page_icon="👤"
)


# ==============================
# CONFIGURAÇÃO DA API
# ==============================

def get_auth_base_url():
    try:
        return (
            st.secrets.get("URL_base_AUTH")
            or st.secrets.get("AUTH_BASE_URL")
            or os.getenv("URL_base_AUTH")
            or os.getenv("AUTH_BASE_URL")
        )
    except Exception:
        return (
            os.getenv("URL_base_AUTH")
            or os.getenv("AUTH_BASE_URL")
        )


def auth_signup(base_url, name, email, password):
    return requests.post(
        f"{base_url.rstrip('/')}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password
        },
        timeout=30
    )


def auth_login(base_url, email, password):
    return requests.post(
        f"{base_url.rstrip('/')}/auth/login",
        json={
            "email": email,
            "password": password
        },
        timeout=30
    )


def auth_me(base_url, token):
    return requests.get(
        f"{base_url.rstrip('/')}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=30
    )


# ==============================
# INFORMAÇÕES DA PÁGINA
# ==============================

st.title("👤 Meu Perfil")

base_url = get_auth_base_url()

if not base_url:
    st.error(
        "URL da API de autenticação não encontrada. "
        "Verifique a configuração URL_base_AUTH."
    )
    st.stop()


# ==============================
# USUÁRIO AUTENTICADO
# ==============================

auth_token = st.session_state.get("auth_token")

if auth_token:

    try:
        resposta = auth_me(base_url, auth_token)

        if resposta.status_code == 200:
            user_data = resposta.json()
            st.session_state["user_data"] = user_data

            st.success("Você está conectado!")

            st.subheader("Informações da conta")

            st.write(
                "**Nome:**",
                user_data.get("name", "Não informado")
            )

            st.write(
                "**E-mail:**",
                user_data.get("email", "Não informado")
            )

            st.write(
                "**ID:**",
                user_data.get("id", "Não informado")
            )

            st.divider()

            if st.button("🚪 Sair da conta"):
                st.session_state.pop("auth_token", None)
                st.session_state.pop("user_data", None)
                st.session_state.pop("pdf_report_path", None)
                st.session_state.pop("pdf_report_bytes", None)
                st.rerun()

            st.stop()

        else:
            st.warning(
                "Sua sessão expirou. Faça login novamente."
            )
            st.session_state.pop("auth_token", None)
            st.session_state.pop("user_data", None)

    except requests.RequestException as erro:
        st.error(f"Erro ao consultar perfil: {erro}")
        st.stop()


# ==============================
# LOGIN E CADASTRO
# ==============================

aba_login, aba_cadastro = st.tabs(
    ["Entrar", "Criar conta"]
)


# ==============================
# LOGIN
# ==============================

with aba_login:

    st.subheader("Entrar na conta")

    login_email = st.text_input(
        "E-mail",
        key="login_email"
    ).strip().lower()

    login_password = st.text_input(
        "Senha",
        type="password",
        key="login_password"
    )

    if st.button("Entrar", key="btn_login"):

        if not login_email or not login_password:
            st.warning("Preencha o e-mail e a senha.")

        else:
            try:
                resposta = auth_login(
                    base_url,
                    login_email,
                    login_password
                )

                if resposta.status_code == 200:
                    dados = resposta.json()
                    token = dados.get("authToken")

                    if token:
                        st.session_state["auth_token"] = token
                        st.success("Login realizado com sucesso!")
                        st.rerun()

                    else:
                        st.error(
                            "A API não retornou o token de autenticação."
                        )

                else:
                    st.error(
                        f"Erro no login: {resposta.text}"
                    )

            except requests.RequestException as erro:
                st.error(f"Erro ao conectar com a API: {erro}")


# ==============================
# CADASTRO
# ==============================

with aba_cadastro:

    st.subheader("Criar uma conta")

    signup_name = st.text_input(
        "Nome completo",
        key="signup_name"
    ).strip()

    signup_email = st.text_input(
        "E-mail",
        key="signup_email"
    ).strip().lower()

    signup_password = st.text_input(
        "Senha",
        type="password",
        key="signup_password"
    )

    signup_password_confirm = st.text_input(
        "Confirmar senha",
        type="password",
        key="signup_password_confirm"
    )

    if st.button("Cadastrar", key="btn_cadastro"):

        if not signup_name or not signup_email or not signup_password:
            st.warning("Preencha todos os campos.")

        elif "@" not in signup_email or "." not in signup_email.split("@")[-1]:
            st.warning("Digite um endereço de e-mail válido.")

        elif signup_password != signup_password_confirm:
            st.warning("As senhas não coincidem.")

        else:
            try:
                resposta = auth_signup(
                    base_url,
                    signup_name,
                    signup_email,
                    signup_password
                )

                if resposta.status_code in (200, 201):

                    dados = resposta.json()
                    token = dados.get("authToken")

                    if token:
                        st.session_state["auth_token"] = token
                        st.success("Cadastro realizado com sucesso!")
                        st.rerun()

                    else:
                        st.success(
                            "Conta criada com sucesso! "
                            "Agora você pode entrar na sua conta."
                        )

                else:
                    st.error(
                        f"Erro no cadastro: {resposta.text}"
                    )

            except requests.RequestException as erro:
                st.error(
                    f"Erro ao conectar com a API: {erro}"
                )
