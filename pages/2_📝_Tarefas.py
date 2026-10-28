
import os
from pathlib import Path

import requests
import streamlit as st


st.title("📝 Tarefas")
st.write("Cadastro e consulta de tarefas acadêmicas")


def get_env_url(nome_variavel):
    """Lê uma variável de URL do arquivo .env."""
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)

                    if chave.strip() == nome_variavel:
                        return valor.strip().strip('"').strip("'").rstrip("/")

    return os.environ.get(nome_variavel, "").rstrip("/")


def get_headers():
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


base_subjects = get_env_url("URL_base_SUBJECTS")
base_tasks = get_env_url("URL_base_ACADEMIC_TASKS")
headers = get_headers()

if not base_subjects or not base_tasks:
    st.error(
        "Configure URL_base_SUBJECTS e URL_base_ACADEMIC_TASKS "
        "no arquivo .env."
    )
    st.stop()

if not headers:
    st.warning("Faça login na página Perfil para acessar suas tarefas.")
    st.stop()


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


def cadastrar_tarefa(payload):
    resposta = requests.post(
        f"{base_tasks}/academic_tasks",
        headers=headers,
        json=payload,
        timeout=15,
    )
    resposta.raise_for_status()
    return resposta


aba_cadastro, aba_lista = st.tabs(
    ["Cadastrar tarefa", "Minhas tarefas"]
)

try:
    disciplinas = buscar_disciplinas()
except requests.RequestException:
    st.error("Não foi possível carregar as disciplinas do Xano.")
    st.stop()

with aba_cadastro:
    st.subheader("Cadastrar tarefa")

    if not disciplinas:
        st.info("Cadastre uma disciplina antes de criar uma tarefa.")
    else:
        opcoes_disciplinas = {
            f"{disciplina.get('name', 'Sem nome')} (ID {disciplina.get('id')})":
            disciplina.get("id")
            for disciplina in disciplinas
        }

        with st.form("form_cadastrar_tarefa"):
            titulo = st.text_input("Título da tarefa")
            descricao = st.text_area("Descrição")
            disciplina_escolhida = st.selectbox(
                "Disciplina",
                options=list(opcoes_disciplinas.keys()),
            )
            prazo = st.date_input("Data de entrega")
            status = st.selectbox(
                "Status",
                ["Pendente", "Em andamento", "Concluída"],
            )

            enviar = st.form_submit_button("Cadastrar tarefa")

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
                    st.error(f"Não foi possível cadastrar a tarefa (HTTP {codigo}).")
                    st.caption(erro.response.text[:500])
                except requests.RequestException:
                    st.error("Erro de conexão ao cadastrar a tarefa.")

with aba_lista:
    st.subheader("Minhas tarefas")

    filtro = st.selectbox(
        "Filtrar por disciplina",
        ["Todas as disciplinas"] + [
            disciplina.get("name", "Sem nome")
            for disciplina in disciplinas
        ],
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
            for tarefa in tarefas:
                with st.container(border=True):
                    st.markdown(
                        f"### 📝 {tarefa.get('title', 'Sem título')}"
                    )
                    st.write(
                        tarefa.get("description") or "Sem descrição"
                    )
                    st.write(
                        "**Disciplina:** "
                        + nomes_disciplinas.get(
                            tarefa.get("subject_id"),
                            "Disciplina não encontrada",
                        )
                    )
                    st.write(f"**Status:** {tarefa.get('status', 'Não informado')}")
                    if tarefa.get("due_date"):
                        st.write(f"**Entrega:** {tarefa['due_date']}")

    except requests.HTTPError as erro:
        st.error(
            f"Não foi possível carregar as tarefas "
            f"(HTTP {erro.response.status_code})."
        )
    except requests.RequestException:
        st.error("Erro de conexão ao carregar as tarefas.")
