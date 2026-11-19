
import os

import requests
import streamlit as st


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Perfil - EduTrack AI",
    page_icon="👤",
    layout="wide"
)


# --------------------------------------------------
# ESTILO VISUAL
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    h1, h2, h3 {
        color: #14213D;
    }

    .page-subtitle {
        color: #64748B;
        font-size: 16px;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .profile-card {
        background: linear-gradient(120deg, #14213D, #2563EB);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .profile-card h2 {
        color: white;
        margin-bottom: 8px;
    }

    .profile-card p {
        color: #E2E8F0;
        margin-bottom: 0;
    }

    .account-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 15px;
        padding: 22px;
        margin-bottom: 15px;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 9px;
    }

    div[data-testid="stButton"] button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# GERENCIAMENTO DA SESSÃO
# --------------------------------------------------

def limpar_sessao():
    """Remove os dados associados à conta anterior."""

    chaves = [
        "auth_token",
        "user_data",
        "pdf_report_path",
        "pdf_report_bytes",
        "subjects",
        "academic_tasks",
    ]

    for chave in chaves:
        st.session_state.pop(chave, None)


# --------------------------------------------------
# CONFIGURAÇÃO DA API
# --------------------------------------------------

def get_auth_base_url():
    """Obtém a URL base da API de autenticação."""

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
    """Realiza o cadastro de um novo usuário."""

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
    """Realiza a autenticação do usuário."""

    return requests.post(
        f"{base_url.rstrip('/')}/auth/login",
        json={
            "email": email,
            "password": password
        },
        timeout=30
    )


def auth_me(base_url, token):
    """Consulta os dados do usuário autenticado."""

    return requests.get(
        f"{base_url.rstrip('/')}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=30
    )


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.title("👤 Meu Perfil")

st.markdown(
    '<p class="page-subtitle">'
    'Gerencie suas informações e acesse sua conta do EduTrack AI.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# VERIFICAÇÃO DA API
# --------------------------------------------------

base_url = get_auth_base_url()

if not base_url:
    st.error(
        "URL da API de autenticação não encontrada. "
        "Verifique a configuração URL_base_AUTH."
    )
    st.stop()


# --------------------------------------------------
# USUÁRIO AUTENTICADO
# --------------------------------------------------

auth_token = st.session_state.get("auth_token")

if auth_token:

    try:
        resposta = auth_me(base_url, auth_token)

        if resposta.status_code == 200:

            user_data = resposta.json()
            st.session_state["user_data"] = user_data

            nome_usuario = user_data.get("name", "Estudante")
            email_usuario = user_data.get("email", "Não informado")
            id_usuario = user_data.get("id", "Não informado")

            st.success("Você está conectado!")

            st.markdown(f"""
                <div class="profile-card">
                    <h2>Olá, {nome_usuario}! 👋</h2>
                    <p>Que bom ter você no EduTrack AI.</p>
                </div>
            """, unsafe_allow_html=True)

            st.subheader("Informações da conta")

            with st.container(border=True):

                st.markdown("### 👤 Dados pessoais")

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("NOME COMPLETO")
                    st.markdown(f"**{nome_usuario}**")

                with col2:
                    st.caption("E-MAIL")
                    st.markdown(f"**{email_usuario}**")

                st.divider()

                st.caption("IDENTIFICAÇÃO DA CONTA")
                st.code(str(id_usuario), language=None)

            st.write("")

            st.subheader("Segurança")

            st.write(
                "Encerre sua sessão quando terminar de utilizar "
                "o EduTrack AI."
            )

            if st.button(
                "🚪 Sair da conta",
                use_container_width=True
            ):

                limpar_sessao()

                st.success("Você saiu da sua conta.")
                st.rerun()

            st.stop()

        else:

            limpar_sessao()

            st.warning(
                "Sua sessão expirou. Faça login novamente."
            )

            st.rerun()

    except requests.RequestException as erro:

        st.error(f"Erro ao consultar perfil: {erro}")
        st.stop()


# --------------------------------------------------
# LOGIN E CADASTRO
# --------------------------------------------------

st.markdown("""
    <div style="margin-bottom: 20px;">
        <h3 style="color:#14213D;">Acesse sua conta</h3>
        <p style="color:#64748B;">
            Entre ou crie uma conta para organizar sua vida acadêmica.
        </p>
    </div>
""", unsafe_allow_html=True)

aba_login, aba_cadastro = st.tabs(
    ["🔐 Entrar", "✨ Criar conta"]
)


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

with aba_login:

    st.subheader("Bem-vindo de volta!")

    st.write("Informe seus dados para acessar sua conta.")

    with st.container(border=True):

        login_email = st.text_input(
            "E-mail",
            placeholder="seuemail@exemplo.com",
            key="login_email"
        ).strip().lower()

        login_password = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha",
            key="login_password"
        )

        if st.button(
            "Entrar na conta",
            key="btn_login",
            use_container_width=True
        ):

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

                            limpar_sessao()

                            st.session_state["auth_token"] = token

                            st.success("Login realizado com sucesso!")
                            st.rerun()

                        else:

                            limpar_sessao()

                            st.error(
                                "A API não retornou o token "
                                "de autenticação."
                            )

                    else:

                        st.error(
                            f"Erro no login: {resposta.text}"
                        )

                except requests.RequestException as erro:

                    st.error(
                        f"Erro ao conectar com a API: {erro}"
                    )


# --------------------------------------------------
# CADASTRO
# --------------------------------------------------

with aba_cadastro:

    st.subheader("Crie sua conta")

    st.write(
        "Preencha seus dados para começar a organizar seus estudos."
    )

    with st.container(border=True):

        signup_name = st.text_input(
            "Nome completo",
            placeholder="Digite seu nome",
            key="signup_name"
        ).strip()

        signup_email = st.text_input(
            "E-mail",
            placeholder="seuemail@exemplo.com",
            key="signup_email"
        ).strip().lower()

        signup_password = st.text_input(
            "Senha",
            type="password",
            placeholder="Crie uma senha",
            key="signup_password"
        )

        signup_password_confirm = st.text_input(
            "Confirmar senha",
            type="password",
            placeholder="Digite novamente sua senha",
            key="signup_password_confirm"
        )

        if st.button(
            "✨ Criar minha conta",
            key="btn_cadastro",
            use_container_width=True
        ):

            if not signup_name or not signup_email or not signup_password:

                st.warning("Preencha todos os campos.")

            elif (
                "@" not in signup_email
                or "." not in signup_email.split("@")[-1]
            ):

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

                        limpar_sessao()

                        if token:

                            st.session_state["auth_token"] = token

                            st.success(
                                "Cadastro realizado com sucesso!"
                            )

                            st.rerun()

                        else:

                            st.success(
                                "Conta criada com sucesso! "
                                "Agora entre com seu novo usuário."
                            )

                    else:

                        st.error(
                            f"Erro no cadastro: {resposta.text}"
                        )

                except requests.RequestException as erro:

                    st.error(
                        f"Erro ao conectar com a API: {erro}"
                    )
