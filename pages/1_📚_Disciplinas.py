
import os

import requests
import streamlit as st


# ==================================================
# CONFIGURAÇÃO E IDENTIDADE VISUAL
# ==================================================

st.title("📚 Disciplinas")
st.caption("Gerencie suas matérias e acompanhe sua jornada acadêmica.")

st.markdown(
    """
    <style>
    .subject-hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, #4338CA, #6366F1, #818CF8);
        color: white;
        margin: 12px 0 24px 0;
    }

    .subject-hero h2 {
        color: white;
        margin: 0 0 8px 0;
        font-size: 25px;
    }

    .subject-hero p {
        color: #EEF2FF;
        margin: 0;
        font-size: 14px;
    }

    .subject-card {
        padding: 20px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 16px;
        margin-bottom: 12px;
        background: var(--secondary-background-color);
    }

    .subject-card h3 {
        margin: 0 0 14px 0;
        font-size: 19px;
    }

    .subject-detail {
        font-size: 14px;
        margin: 6px 0;
        opacity: 0.85;
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 22px;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subject-hero">
        <h2>Organize suas disciplinas 🎓</h2>
        <p>
            Cadastre suas matérias, acompanhe os professores
            e mantenha sua vida acadêmica organizada.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CONFIGURAÇÃO DA API
# ==================================================

def get_base_url():
    """Obtém a URL base do grupo subjects."""

    try:
        if "URL_base_SUBJECTS" in st.secrets:
            return (
                str(st.secrets["URL_base_SUBJECTS"])
                .strip()
                .strip('"')
                .strip("'")
                .rstrip("/")
            )
    except Exception:
        pass

    return os.environ.get("URL_base_SUBJECTS", "").rstrip("/")


def get_headers():
    """Obtém o token de autenticação da sessão."""

    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


base_url = get_base_url()
headers = get_headers()

if not base_url:
    st.error(
        "A URL base de Disciplinas (`URL_base_SUBJECTS`) "
        "não foi configurada em `.streamlit/secrets.toml`."
    )
    st.stop()

if not headers:
    st.warning("Faça login na página Perfil para acessar suas disciplinas.")
    st.stop()


# ==================================================
# BUSCAR DISCIPLINAS
# ==================================================

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


# ==================================================
# NAVEGAÇÃO DAS ABAS
# ==================================================

aba_cadastro, aba_lista = st.tabs(
    ["➕ Cadastrar disciplina", "📚 Minhas disciplinas"]
)


# ==================================================
# ABA DE CADASTRO
# ==================================================

with aba_cadastro:
    st.subheader("Adicionar nova disciplina")

    st.write(
        "Preencha as informações abaixo para cadastrar uma matéria."
    )

    with st.form("form_cadastrar_disciplina"):
        nome = st.text_input(
            "Nome da disciplina",
            placeholder="Ex.: Engenharia de Software",
        )

        professor = st.text_input(
            "Professor",
            placeholder="Nome do professor",
        )

        horas = st.number_input(
            "Carga horária",
            min_value=1,
            step=1,
        )

        enviar = st.form_submit_button(
            "➕ Cadastrar disciplina",
            use_container_width=True,
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


# ==================================================
# ABA DE LISTAGEM
# ==================================================

with aba_lista:
    st.subheader("Suas disciplinas")

    col_info, col_button = st.columns([3, 1])

    with col_info:
        st.caption(
            "Consulte as matérias cadastradas na sua conta."
        )

    with col_button:
        atualizar = st.button(
            "🔄 Atualizar",
            use_container_width=True,
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
            # Indicadores
            total_disciplinas = len(disciplinas)

            total_horas = sum(
                int(d.get("hours") or 0)
                for d in disciplinas
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total de disciplinas",
                    total_disciplinas,
                    help="Quantidade de disciplinas cadastradas.",
                )

            with col2:
                st.metric(
                    "Carga horária total",
                    f"{total_horas} h",
                    help="Soma das cargas horárias cadastradas.",
                )

            st.divider()

            # Cartões das disciplinas
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

                    col_professor, col_horas = st.columns(2)

                    with col_professor:
                        st.caption("PROFESSOR")
                        st.write(professor_disciplina)

                    with col_horas:
                        st.caption("CARGA HORÁRIA")
                        st.write(f"{carga_horaria} horas")

    except requests.RequestException:
        st.error(
            "Não foi possível carregar as disciplinas do Xano. "
            "Verifique a URL, a autenticação e o endpoint."
        )


# ==================================================
# RODAPÉ
# ==================================================

st.divider()
st.caption("EduTrack AI • Gerenciamento de disciplinas")
