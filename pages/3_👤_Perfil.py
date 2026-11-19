
import os

import requests
import streamlit as st


# ==================================================
# ESTILO VISUAL
# ==================================================

st.title("👤 Meu Perfil")
st.caption("Gerencie suas informações e acesse sua conta do EduTrack AI.")

st.markdown(
    """
    <style>
    .profile-hero {
        padding: 26px;
        border-radius: 18px;
        background: linear-gradient(120deg, #4338CA, #6366F1, #818CF8);
        color: white;
        margin: 12px 0 24px 0;
    }

    .profile-hero h2 {
        color: white;
        margin: 0 0 8px 0;
    }

    .profile-hero p {
        color: #EEF2FF;
        margin: 0;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }

    div[data-testid="stButton"] button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="profile-hero">
        <h2>Sua conta acadêmica 🎓</h2>
        <p>Seus dados e sua jornada de estudos em um só lugar.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# GERENCIAMENTO DA SESSÃO
# ==================================================

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


# ==================================================
# CONFIGURAÇÃO DA API
# ==================================================

def get_auth_base_url():
    """Obtém a URL base da API de autenticação."""

    try:
        return (
            st.secrets.get("URL_base_AUTH")
            or st.secrets.get("AUTH_BASE_URL")
            or os.getenv("URL_base_AUTH")
            or os.getenv("AUTH_BASE_URL")
            or ""
        )
    except Exception:
        return (
            os.getenv("URL_base_AUTH")
            or os.getenv("AUTH_BASE_URL")
            or ""
        )


def auth_signup(base_url, name, email, password):
    """Realiza o cadastro de um novo usuário."""

    return requests.post(
        f"{base_url.rstrip('/')}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
        timeout=30,
    )


def auth_login(base_url, email, password):
    """Realiza a autenticação do usuário."""

    return requests.post(
        f"{base_url.rstrip('/')}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=30,
    )


def auth_me(base_url, token):
    """Consulta os dados do usuário autenticado."""

    return requests.get(
        f"{base_url.rstrip('/')}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=30,
    )


# ==================================================
# VERIFICAÇÃO DA API
# ==================================================

base_url = get_auth_base_url()

if not base_url:
    st.error(
        "URL da API de autenticação não encontrada. "
        "Verifique a configuração URL_base_AUTH."
    )
    st.stop()


# ==================================================
# USUÁRIO AUTENTICADO
# ==================================================

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

            st.subheader(f"Olá, {nome_usuario}! 👋")

            st.write(
                "Que bom ter você no EduTrack AI. "
                "Confira as informações da sua conta."
            )

            # Informações pessoais
            with st.container(border=True):

                st.markdown("### 👤 Dados pessoais")

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("NOME COMPLETO")
                    st.write(nome_usuario)

                with col2:
                    st.caption("E-MAIL")
                    st.write(email_usuario)

                st.divider()

                st.caption("IDENTIFICAÇÃO DA CONTA")
                st.code(str(id_usuario), language=None)

            # Segurança
            st.subheader("🔐 Segurança")

            st.write(
                "Encerre sua sessão quando terminar de utilizar "
                "o EduTrack AI."
            )

            if st.button(
                "🚪 Sair da conta",
                use_container_width=True,
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


# ==================================================
# LOGIN E CADASTRO
# ==================================================

st.subheader("Acesse sua conta")

st.write(
    "Entre ou crie uma conta para organizar sua vida acadêmica."
)

aba_login, aba_cadastro = st.tabs(
    ["🔐 Entrar", "✨ Criar conta"]
)


# ==================================================
# LOGIN
# ==================================================

with aba_login:

    st.subheader("Bem-vindo de volta!")

    st.write("Informe seus dados para acessar sua conta.")

    with st.container(border=True):

        login_email = st.text_input(
            "E-mail",
            placeholder="seuemail@exemplo.com",
            key="login_email",
        ).strip().lower()

        login_password = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha",
            key="login_password",
        )

        if st.button(
            "Entrar na conta",
            key="btn_login",
            use_container_width=True,
        ):

            if not login_email or not login_password:

                st.warning("Preencha o e-mail e a senha.")

            else:

                try:
                    resposta = auth_login(
                        base_url,
                        login_email,
                        login_password,
                    )

                    if resposta.status_code == 200:

                        dados = resposta.json()
                        token = dados.get("authToken")

                        if token:

                            limpar_sessao()

                            st.session_state["auth_token"] = token

                            st.success(
                                "Login realizado com sucesso!"
                            )

                            st.rerun()

                        else:
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


# ==================================================
# CADASTRO
# ==================================================

with aba_cadastro:

    st.subheader("Crie sua conta")

    st.write(
        "Preencha seus dados para começar a organizar seus estudos."
    )

    with st.container(border=True):

        signup_name = st.text_input(
            "Nome completo",
            placeholder="Digite seu nome",
            key="signup_name",
        ).strip()

        signup_email = st.text_input(
            "E-mail",
            placeholder="seuemail@exemplo.com",
            key="signup_email",
        ).strip().lower()

        signup_password = st.text_input(
            "Senha",
            type="password",
            placeholder="Crie uma senha",
            key="signup_password",
        )

        signup_password_confirm = st.text_input(
            "Confirmar senha",
            type="password",
            placeholder="Digite novamente sua senha",
            key="signup_password_confirm",
        )

        if st.button(
            "✨ Criar minha conta",
            key="btn_cadastro",
            use_container_width=True,
        ):

            if (
                not signup_name
                or not signup_email
                or not signup_password
            ):

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
                        signup_password,
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


# ==================================================
# RODAPÉ
# ==================================================

st.divider()
st.caption("EduTrack AI • Gerenciamento de conta")
