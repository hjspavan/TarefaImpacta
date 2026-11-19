
import os

import requests
import streamlit as st


# ==================================================
# IDENTIDADE VISUAL
# ==================================================

st.title("📝 Minhas Tarefas")
st.caption("Organize suas atividades, acompanhe prazos e avance nos estudos.")

st.markdown(
    """
    <style>
    .task-hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, #4338CA, #6366F1, #818CF8);
        color: white;
        margin: 12px 0 24px 0;
    }

    .task-hero h2 {
        color: white;
        margin: 0 0 8px 0;
        font-size: 25px;
    }

    .task-hero p {
        color: #EEF2FF;
        margin: 0;
        font-size: 14px;
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
    <div class="task-hero">
        <h2>Seu planejamento acadêmico 🎯</h2>
        <p>
            Cadastre atividades, acompanhe entregas e mantenha
            seus estudos em dia.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CONFIGURAÇÃO DA API
# ==================================================

def get_config_url(nome_variavel):
    try:
        if nome_variavel in st.secrets:
            return (
                str(st.secrets[nome_variavel])
                .strip()
                .strip('"')
                .strip("'")
                .rstrip("/")
            )
    except Exception:
        pass

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


# ==================================================
# BUSCAR DISCIPLINAS
# ==================================================

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


# ==================================================
# VALIDAR ID DA DISCIPLINA
# ==================================================

def validar_subject_id(valor):
    if valor is None:
        return None

    try:
        identificador = int(valor)
    except (ValueError, TypeError):
        return None

    if identificador < 1:
        return None

    return identificador


# ==================================================
# BUSCAR TAREFAS
# ==================================================

def buscar_tarefas(subject_id=None):
    if subject_id is not None:
        id_validado = validar_subject_id(subject_id)

        if id_validado is None:
            raise ValueError(
                f"ID de disciplina inválido: {subject_id}"
            )

        ids_disciplinas = [id_validado]

    else:
        ids_disciplinas = []

        for disciplina in disciplinas:
            id_validado = validar_subject_id(
                disciplina.get("id")
            )

            if id_validado is not None:
                ids_disciplinas.append(id_validado)

    ids_disciplinas = list(dict.fromkeys(ids_disciplinas))

    if not ids_disciplinas:
        return []

    todas_tarefas = []

    for id_disciplina in ids_disciplinas:
        try:
            resposta = requests.get(
                f"{base_tasks}/academic_tasks",
                headers=headers,
                params={"subject_id": id_disciplina},
                timeout=15,
            )

            resposta.raise_for_status()
            dados = resposta.json()

            if isinstance(dados, list):
                tarefas = dados

            elif isinstance(dados, dict):
                tarefas = dados.get("items", [])

            else:
                tarefas = []

            if isinstance(tarefas, list):
                todas_tarefas.extend(tarefas)

        except requests.HTTPError as erro:
            detalhe = erro.response.text[:2000]

            raise RuntimeError(
                f"Erro ao consultar a disciplina ID {id_disciplina}. "
                f"HTTP {erro.response.status_code}. "
                f"Resposta do Xano: {detalhe}"
            ) from erro

    return todas_tarefas


# ==================================================
# CADASTRAR TAREFA
# ==================================================

def cadastrar_tarefa(payload):
    resposta = requests.post(
        f"{base_tasks}/academic_tasks",
        headers=headers,
        json=payload,
        timeout=15,
    )

    resposta.raise_for_status()
    return resposta


# ==================================================
# CARREGAR DISCIPLINAS
# ==================================================

try:
    disciplinas = buscar_disciplinas()

except requests.HTTPError as erro:
    st.error(
        f"Não foi possível carregar as disciplinas "
        f"(HTTP {erro.response.status_code})."
    )
    st.code(erro.response.text[:2000])
    st.stop()

except requests.RequestException as erro:
    st.error(f"Erro de conexão ao carregar disciplinas: {erro}")
    st.stop()


# ==================================================
# PREPARAR DISCIPLINAS VÁLIDAS
# ==================================================

nomes_disciplinas = {}

for disciplina in disciplinas:
    id_disciplina = validar_subject_id(disciplina.get("id"))

    if id_disciplina is not None:
        nomes_disciplinas[id_disciplina] = disciplina.get(
            "name", "Sem nome"
        )


# ==================================================
# ABAS
# ==================================================

aba_cadastro, aba_lista = st.tabs(
    ["➕ Cadastrar tarefa", "📋 Minhas tarefas"]
)


# ==================================================
# ABA DE CADASTRO
# ==================================================

with aba_cadastro:
    st.subheader("Adicionar nova tarefa")

    st.write(
        "Preencha os dados da atividade para adicioná-la ao seu planejamento."
    )

    if not nomes_disciplinas:
        st.info(
            "Nenhuma disciplina com ID válido foi encontrada. "
            "Verifique seu cadastro de disciplinas."
        )

    else:
        opcoes_disciplinas = {
            f"{nome} (ID {id_disciplina})": id_disciplina
            for id_disciplina, nome in nomes_disciplinas.items()
        }

        with st.form("form_cadastrar_tarefa"):
            titulo = st.text_input(
                "Título da tarefa",
                placeholder="Ex.: Trabalho de Engenharia de Software",
            )

            descricao = st.text_area(
                "Descrição",
                placeholder="Descreva os detalhes da atividade...",
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
                use_container_width=True,
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
                    st.error(
                        f"Não foi possível cadastrar a tarefa "
                        f"(HTTP {erro.response.status_code})."
                    )
                    st.code(erro.response.text[:2000])

                except requests.RequestException as erro:
                    st.error(f"Erro de conexão: {erro}")


# ==================================================
# ABA DE LISTAGEM
# ==================================================

with aba_lista:
    st.subheader("Suas tarefas cadastradas")

    col_info, col_button = st.columns([3, 1])

    with col_info:
        st.caption(
            "Consulte e filtre suas atividades acadêmicas."
        )

    with col_button:
        atualizar = st.button(
            "🔄 Atualizar lista",
            use_container_width=True,
        )

    if atualizar:
        st.rerun()

    opcoes_filtro = ["Todas as disciplinas"] + [
        nome for nome in nomes_disciplinas.values()
    ]

    filtro = st.selectbox(
        "Filtrar por disciplina",
        opcoes_filtro,
    )

    if filtro == "Todas as disciplinas":
        subject_id = None

    else:
        subject_id = next(
            (
                identificador
                for identificador, nome in nomes_disciplinas.items()
                if nome == filtro
            ),
            None,
        )

    try:
        tarefas = buscar_tarefas(subject_id)

        if not nomes_disciplinas:
            st.info("Cadastre uma disciplina para consultar tarefas.")

        elif not tarefas:
            st.info("Você ainda não possui tarefas cadastradas.")

        else:
            total = len(tarefas)

            concluidas = sum(
                1 for tarefa in tarefas
                if tarefa.get("status") == "Concluída"
            )

            pendentes = sum(
                1 for tarefa in tarefas
                if tarefa.get("status") == "Pendente"
            )

            andamento = sum(
                1 for tarefa in tarefas
                if tarefa.get("status") == "Em andamento"
            )

            taxa = concluidas / total * 100 if total else 0

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total de tarefas", total)

            with col2:
                st.metric("Concluídas", concluidas)

            with col3:
                st.metric("Pendentes", pendentes)

            st.progress(
                taxa / 100,
                text=f"Progresso de conclusão: {taxa:.1f}%",
            )

            st.caption(f"Em andamento: {andamento} tarefa(s)")

            st.divider()

            for tarefa in tarefas:
                titulo_tarefa = tarefa.get("title", "Sem título")
                descricao_tarefa = (
                    tarefa.get("description") or "Sem descrição"
                )

                id_tarefa = validar_subject_id(
                    tarefa.get("subject_id")
                )

                disciplina_tarefa = nomes_disciplinas.get(
                    id_tarefa,
                    "Disciplina não encontrada",
                )

                status_tarefa = tarefa.get(
                    "status", "Não informado"
                )

                prazo_tarefa = tarefa.get("due_date")

                if status_tarefa == "Concluída":
                    icone_status = "✅"
                elif status_tarefa == "Em andamento":
                    icone_status = "🔄"
                else:
                    icone_status = "⏳"

                with st.container(border=True):
                    st.markdown(f"### 📝 {titulo_tarefa}")
                    st.write(descricao_tarefa)

                    col_disciplina, col_status = st.columns(2)

                    with col_disciplina:
                        st.caption("DISCIPLINA")
                        st.write(f"📚 {disciplina_tarefa}")

                    with col_status:
                        st.caption("STATUS")
                        st.write(f"{icone_status} {status_tarefa}")

                    if prazo_tarefa:
                        st.caption("DATA DE ENTREGA")
                        st.write(f"📅 {prazo_tarefa}")

    except (RuntimeError, ValueError) as erro:
        st.error("Não foi possível carregar as tarefas.")
        st.code(str(erro))

    except requests.RequestException as erro:
        st.error(f"Erro de conexão ao carregar as tarefas: {erro}")


# ==================================================
# RODAPÉ
# ==================================================

st.divider()
st.caption("EduTrack AI • Gerenciamento de tarefas")
