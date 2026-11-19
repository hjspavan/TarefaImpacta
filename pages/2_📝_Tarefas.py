
import os

import requests
import streamlit as st


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

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stDateInput"] input {
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

    .task-label {
        color: #64748B;
        font-size: 13px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.title("📝 Minhas Tarefas")

st.markdown(
    '<p class="page-subtitle">'
    'Organize suas atividades, acompanhe os prazos e controle seu progresso.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# CONFIGURAÇÕES E AUTENTICAÇÃO
# --------------------------------------------------

def get_config_url(nome_variavel):
    """Obtém a URL base de um serviço."""

    if nome_variavel in st.secrets:
        return (
            str(st.secrets[nome_variavel])
            .strip()
            .strip('"')
            .strip("'")
            .rstrip("/")
        )

    return os.environ.get(nome_variavel, "").rstrip("/")


def get_headers():
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


base_subjects = get_config_url("URL_base_SUBJECTS")
base_tasks = get_config_url("URL_base_ACADEMIC_TASKS")
headers = get_headers()

if not base_subjects or not base_tasks:
    st.error(
        "Configure URL_base_SUBJECTS e URL_base_ACADEMIC_TASKS "
        "no arquivo .streamlit/secrets.toml."
    )
    st.stop()

if not headers:
    st.warning("Faça login na página Perfil para acessar suas tarefas.")
    st.stop()


# --------------------------------------------------
# BUSCAR DISCIPLINAS
# --------------------------------------------------

def buscar_disciplinas():
    resposta = requests.get(
        f"{base_subjects}/subjects",
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
# BUSCAR TAREFAS
# --------------------------------------------------

def buscar_tarefas(subject_id=None):
    params = {"subject_id": subject_id} if subject_id else {}

    resposta = requests.get(
        f"{base_tasks}/academic_tasks",
        headers=headers,
        params=params,
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
# CADASTRAR TAREFA
# --------------------------------------------------

def cadastrar_tarefa(payload):
    resposta = requests.post(
        f"{base_tasks}/academic_tasks",
        headers=headers,
        json=payload,
        timeout=15,
    )

    resposta.raise_for_status()
    return resposta


# --------------------------------------------------
# CARREGAR DISCIPLINAS
# --------------------------------------------------

try:
    disciplinas = buscar_disciplinas()

except requests.RequestException:
    st.error("Não foi possível carregar as disciplinas do Xano.")
    st.stop()


# --------------------------------------------------
# ABAS
# --------------------------------------------------

aba_cadastro, aba_lista = st.tabs(
    ["➕ Cadastrar tarefa", "📝 Minhas tarefas"]
)


# --------------------------------------------------
# ABA DE CADASTRO
# --------------------------------------------------

with aba_cadastro:

    st.subheader("Adicionar nova tarefa")

    st.write(
        "Preencha os dados abaixo para organizar uma nova atividade."
    )

    if not disciplinas:

        st.info("Cadastre uma disciplina antes de criar uma tarefa.")

    else:

        opcoes_disciplinas = {
            f"{disciplina.get('name', 'Sem nome')} (ID {disciplina.get('id')})":
            disciplina.get("id")
            for disciplina in disciplinas
        }

        with st.form("form_cadastrar_tarefa"):

            titulo = st.text_input(
                "Título da tarefa",
                placeholder="Ex.: Trabalho de Engenharia de Software"
            )

            descricao = st.text_area(
                "Descrição",
                placeholder="Descreva os detalhes da atividade..."
            )

            disciplina_escolhida = st.selectbox(
                "Disciplina",
                options=list(opcoes_disciplinas.keys()),
            )

            prazo = st.date_input("Data de entrega")

            status = st.selectbox(
                "Status",
                ["Pendente", "Em andamento", "Concluída"],
            )

            enviar = st.form_submit_button(
                "➕ Cadastrar tarefa",
                use_container_width=True
            )

        if enviar:

            if not titulo.strip():

                st.warning("Informe o título da tarefa.")

            else:

                payload = {
                    "title": titulo.strip(),
                    "description": descricao.strip() or None,
                    "due_date": f"{prazo.isoformat()}T12:00:00Z",
                    "status": status,
                    "subject_id": opcoes_disciplinas[disciplina_escolhida],
                }

                try:
                    cadastrar_tarefa(payload)

                    st.success("Tarefa cadastrada no Xano!")
                    st.rerun()

                except requests.HTTPError as erro:

                    codigo = erro.response.status_code

                    st.error(
                        f"Não foi possível cadastrar a tarefa (HTTP {codigo})."
                    )

                    st.caption(erro.response.text[:500])

                except requests.RequestException:

                    st.error("Erro de conexão ao cadastrar a tarefa.")


# --------------------------------------------------
# ABA DE LISTAGEM
# --------------------------------------------------

with aba_lista:

    st.subheader("Suas tarefas cadastradas")

    col1, col2 = st.columns([3, 1])

    with col1:

        st.write("Consulte e filtre suas atividades acadêmicas.")

    with col2:

        atualizar = st.button(
            "🔄 Atualizar lista",
            use_container_width=True
        )

    if atualizar:
        st.rerun()

    opcoes_filtro = ["Todas as disciplinas"] + [
        disciplina.get("name", "Sem nome")
        for disciplina in disciplinas
    ]

    filtro = st.selectbox(
        "🔎 Filtrar por disciplina",
        opcoes_filtro,
    )

    if filtro == "Todas as disciplinas":

        subject_id = None

    else:

        disciplina_filtro = next(
            disciplina
            for disciplina in disciplinas
            if disciplina.get("name", "Sem nome") == filtro
        )

        subject_id = disciplina_filtro.get("id")

    try:

        tarefas = buscar_tarefas(subject_id)

        nomes_disciplinas = {
            disciplina.get("id"): disciplina.get("name", "Sem nome")
            for disciplina in disciplinas
        }

        if not tarefas:

            st.info("Você ainda não possui tarefas cadastradas.")

        else:

            st.caption(f"Total de tarefas: {len(tarefas)}")

            for tarefa in tarefas:

                titulo_tarefa = tarefa.get("title", "Sem título")
                descricao_tarefa = (
                    tarefa.get("description") or "Sem descrição"
                )

                nome_disciplina = nomes_disciplinas.get(
                    tarefa.get("subject_id"),
                    "Disciplina não encontrada",
                )

                status_tarefa = tarefa.get(
                    "status",
                    "Não informado"
                )

                prazo_tarefa = tarefa.get("due_date")

                with st.container(border=True):

                    st.markdown(f"### 📝 {titulo_tarefa}")

                    st.write(descricao_tarefa)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**📚 Disciplina**")
                        st.write(nome_disciplina)

                    with col2:
                        st.markdown("**📌 Status**")
                        st.write(status_tarefa)

                    if prazo_tarefa:
                        st.markdown("**📅 Data de entrega**")
                        st.write(prazo_tarefa)

    except requests.HTTPError as erro:

        st.error(
            f"Não foi possível carregar as tarefas "
            f"(HTTP {erro.response.status_code})."
        )

    except requests.RequestException:

        st.error("Erro de conexão ao carregar as tarefas.")
