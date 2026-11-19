
import os

import requests
import streamlit as st


# --------------------------------------------------
# CONFIGURAÇÃO VISUAL
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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

    .section-heading {
        color: #14213D;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    div[data-testid="stForm"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 15px;
        padding: 22px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-color: #E2E8F0;
        border-radius: 15px;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        border-radius: 9px;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 9px;
        font-weight: 600;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.title("📚 Minhas Disciplinas")

st.markdown(
    '<p class="page-subtitle">'
    'Organize suas matérias, professores e cargas horárias.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# CONEXÃO COM O XANO
# --------------------------------------------------

def get_base_url():
    """Obtém a URL base do grupo subjects."""

    if "URL_base_SUBJECTS" in st.secrets:
        return (
            str(st.secrets["URL_base_SUBJECTS"])
            .strip()
            .strip('"')
            .strip("'")
            .rstrip("/")
        )

    return os.environ.get("URL_base_SUBJECTS", "").rstrip("/")


def get_headers():
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


base_url = get_base_url()
headers = get_headers()

if not base_url:
    st.error(
        "A URL base de Disciplinas (URL_base_SUBJECTS) "
        "não foi configurada em .streamlit/secrets.toml."
    )
    st.stop()

if not headers:
    st.warning(
        "Faça login na página Perfil para acessar suas disciplinas."
    )
    st.stop()


# --------------------------------------------------
# BUSCAR DISCIPLINAS
# --------------------------------------------------

def buscar_disciplinas():
    resposta = requests.get(
        f"{base_url}/subjects",
        headers=headers,
        timeout=15,
    )

    resposta.raise_for_status()

    dados = resposta.json()

    if isinstance(dados, list):
        return dados

    if isinstance(dados, dict):
        return dados.get("items", [])

    return []


# --------------------------------------------------
# ABAS
# --------------------------------------------------

aba_cadastro, aba_lista = st.tabs(
    ["➕ Cadastrar disciplina", "📚 Minhas disciplinas"]
)


# --------------------------------------------------
# CADASTRAR DISCIPLINA
# --------------------------------------------------

with aba_cadastro:

    st.subheader("Adicionar nova disciplina")

    st.write(
        "Preencha as informações abaixo para cadastrar uma matéria."
    )

    with st.form("form_cadastrar_disciplina"):

        nome = st.text_input(
            "Nome da disciplina",
            placeholder="Ex.: Engenharia de Software"
        )

        professor = st.text_input(
            "Professor",
            placeholder="Nome do professor"
        )

        horas = st.number_input(
            "Carga horária (horas)",
            min_value=1,
            step=1,
        )

        enviar = st.form_submit_button(
            "➕ Cadastrar disciplina",
            use_container_width=True
        )

    if enviar:

        if not nome.strip():
            st.warning("Informe o nome da disciplina.")

        else:
            payload = {
                "name": nome.strip(),
                "teacher": professor.strip() or None,
                "hours": int(horas),
            }

            try:
                resposta = requests.post(
                    f"{base_url}/subjects",
                    headers=headers,
                    json=payload,
                    timeout=15,
                )

                if resposta.status_code in (200, 201):
                    st.success("Disciplina cadastrada no Xano!")
                    st.rerun()

                else:
                    st.error(
                        f"Não foi possível cadastrar a disciplina "
                        f"(HTTP {resposta.status_code})."
                    )

            except requests.RequestException:
                st.error(
                    "Erro de conexão ao cadastrar a disciplina."
                )


# --------------------------------------------------
# LISTAR DISCIPLINAS
# --------------------------------------------------

with aba_lista:

    st.subheader("Suas disciplinas cadastradas")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(
            "Confira suas matérias e respectivas informações."
        )

    with col2:
        atualizar = st.button(
            "🔄 Atualizar lista",
            use_container_width=True
        )

    if atualizar:
        st.rerun()

    try:
        disciplinas = buscar_disciplinas()

        if not disciplinas:

            st.info(
                "Você ainda não possui disciplinas cadastradas. "
                "Acesse a aba de cadastro para adicionar sua primeira matéria."
            )

        else:

            st.caption(
                f"Total de disciplinas: {len(disciplinas)}"
            )

            for disciplina in disciplinas:

                nome_disciplina = disciplina.get(
                    "name", "Sem nome"
                )

                professor_disciplina = (
                    disciplina.get("teacher") or "Não informado"
                )

                carga_horaria = disciplina.get(
                    "hours", "Não informada"
                )

                with st.container(border=True):

                    st.markdown(
                        f"### 📘 {nome_disciplina}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**👨‍🏫 Professor**")
                        st.write(professor_disciplina)

                    with col2:
                        st.markdown("**⏱️ Carga horária**")
                        st.write(f"{carga_horaria} horas")

    except requests.RequestException:

        st.error(
            "Não foi possível carregar as disciplinas do Xano. "
            "Verifique a URL, a autenticação e o endpoint."
        )
