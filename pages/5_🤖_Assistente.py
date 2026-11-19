
import os
from datetime import date, datetime

import requests
import streamlit as st


# ==================================================
# CONFIGURAÇÃO E IDENTIDADE VISUAL
# ==================================================

st.set_page_config(
    page_title="Assistente Acadêmico",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Assistente Acadêmico")
st.caption(
    "Seu assistente inteligente para acompanhar o desempenho acadêmico."
)

st.markdown(
    """
    <style>
    .assistant-hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, #4338CA, #6366F1, #818CF8);
        color: white;
        margin: 12px 0 24px 0;
    }

    .assistant-hero h2 {
        color: white;
        margin: 0 0 8px 0;
        font-size: 25px;
    }

    .assistant-hero p {
        color: #EEF2FF;
        margin: 0;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="assistant-hero">
        <h2>Seu desempenho em foco 🎯</h2>
        <p>
            Converse com seu assistente, acompanhe suas tarefas
            e receba recomendações para organizar seus estudos.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CONFIGURAÇÃO DA API
# ==================================================

def get_config_url(var_name):
    """Obtém uma configuração do Streamlit Secrets ou ambiente."""

    try:
        if var_name in st.secrets:
            return (
                str(st.secrets[var_name])
                .strip()
                .strip('"')
                .strip("'")
                .rstrip("/")
            )
    except Exception:
        pass

    return os.environ.get(var_name, "").rstrip("/")


def get_headers():
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


# ==================================================
# AUTENTICAÇÃO
# ==================================================

auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning("Faça login na página Perfil para usar o assistente.")
    st.stop()

headers = get_headers()

base_subjects = get_config_url("URL_base_SUBJECTS")
base_tasks = get_config_url("URL_base_ACADEMIC_TASKS")

if not base_subjects or not base_tasks:
    st.error(
        "Configure URL_base_SUBJECTS e URL_base_ACADEMIC_TASKS "
        "no arquivo .streamlit/secrets.toml."
    )
    st.stop()


# ==================================================
# EXTRAIR DADOS DA API
# ==================================================

def extract_items(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        items = data.get("items", [])
        return items if isinstance(items, list) else []

    return []


# ==================================================
# BUSCAR DISCIPLINAS
# ==================================================

def fetch_subjects():
    try:
        response = requests.get(
            f"{base_subjects}/subjects",
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()

        return extract_items(response.json())

    except requests.RequestException as error:
        st.warning(
            f"Não foi possível consultar as disciplinas: {error}"
        )
        return []


# ==================================================
# BUSCAR TAREFAS
# ==================================================

def fetch_tasks(subjects):
    """
    Consulta as tarefas individualmente por disciplina.
    O endpoint Xano exige subject_id >= 1.
    """

    todas_tarefas = []

    ids_disciplinas = []

    for subject in subjects:
        subject_id = subject.get("id")

        try:
            subject_id = int(subject_id)
        except (ValueError, TypeError):
            continue

        if subject_id >= 1 and subject_id not in ids_disciplinas:
            ids_disciplinas.append(subject_id)

    for subject_id in ids_disciplinas:
        try:
            response = requests.get(
                f"{base_tasks}/academic_tasks",
                headers=headers,
                params={"subject_id": subject_id},
                timeout=15,
            )

            response.raise_for_status()

            tarefas = extract_items(response.json())
            todas_tarefas.extend(tarefas)

        except requests.HTTPError as error:
            st.warning(
                f"Erro ao consultar tarefas da disciplina "
                f"{subject_id}: HTTP {error.response.status_code}. "
                f"{error.response.text[:500]}"
            )

        except requests.RequestException as error:
            st.warning(
                f"Erro de conexão ao consultar a disciplina "
                f"{subject_id}: {error}"
            )

    return todas_tarefas


# ==================================================
# BUSCAR DADOS DO ALUNO
# ==================================================

def fetch_student_data():
    """Busca disciplinas e tarefas do aluno."""

    subjects = fetch_subjects()

    # Reutiliza as disciplinas já carregadas.
    tasks = fetch_tasks(subjects)

    return subjects, tasks


# ==================================================
# AUXILIARES DE STATUS E PRAZO
# ==================================================

def is_completed(task):
    status = str(task.get("status", "")).lower()

    if status in (
        "completed",
        "concluída",
        "concluida",
        "done",
        "finalizada",
    ):
        return True

    return task.get("completed") is True


def parse_due_date(task):
    due = task.get("due_date")

    if not due:
        return None

    try:
        if isinstance(due, str):
            return datetime.fromisoformat(
                due.replace("Z", "+00:00")
            ).date()

        if isinstance(due, datetime):
            return due.date()

        if isinstance(due, date):
            return due

    except (ValueError, TypeError):
        return None

    return None


def is_overdue(task):
    if is_completed(task):
        return False

    due_date = parse_due_date(task)

    if not due_date:
        return False

    return due_date < date.today()


# ==================================================
# ANÁLISE ACADÊMICA
# ==================================================

def analyze_academic_data(subjects, tasks):
    total_tasks = len(tasks)

    completed_tasks = [
        task for task in tasks if is_completed(task)
    ]

    overdue_tasks = [
        task for task in tasks if is_overdue(task)
    ]

    pending_tasks = [
        task for task in tasks
        if not is_completed(task) and not is_overdue(task)
    ]

    completion_rate = (
        len(completed_tasks) / total_tasks * 100
        if total_tasks > 0 else 0.0
    )

    subject_map = {}

    for subject in subjects:
        subject_id = subject.get("id")

        try:
            subject_id = int(subject_id)
        except (ValueError, TypeError):
            continue

        subject_map[subject_id] = subject.get("name", "Sem nome")

    per_subject = {}

    for subject in subjects:
        subject_id = subject.get("id")

        try:
            subject_id = int(subject_id)
        except (ValueError, TypeError):
            continue

        subject_name = subject.get("name", "Sem nome")

        subject_tasks = [
            task for task in tasks
            if str(task.get("subject_id")) == str(subject_id)
        ]

        subject_completed = [
            task for task in subject_tasks if is_completed(task)
        ]

        subject_overdue = [
            task for task in subject_tasks if is_overdue(task)
        ]

        subject_pending = [
            task for task in subject_tasks
            if not is_completed(task) and not is_overdue(task)
        ]

        subject_rate = (
            len(subject_completed) / len(subject_tasks) * 100
            if subject_tasks else 0.0
        )

        per_subject[subject_id] = {
            "name": subject_name,
            "total": len(subject_tasks),
            "completed": len(subject_completed),
            "pending": len(subject_pending),
            "overdue": len(subject_overdue),
            "completion_rate": subject_rate,
        }

    at_risk = sorted(
        [
            info for info in per_subject.values()
            if info["total"] > 0
        ],
        key=lambda item: item["completion_rate"],
    )

    return {
        "total_subjects": len(subjects),
        "total_tasks": total_tasks,
        "completed": len(completed_tasks),
        "pending": len(pending_tasks),
        "overdue": len(overdue_tasks),
        "completion_rate": completion_rate,
        "per_subject": per_subject,
        "at_risk_subjects": at_risk,
        "subject_map": subject_map,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "pending_tasks": pending_tasks,
    }


# ==================================================
# CONTEXTO PARA GEMINI
# ==================================================

def build_context_string(analysis, subjects, tasks):
    lines = [
        f"Total de disciplinas: {analysis['total_subjects']}",
        f"Total de tarefas: {analysis['total_tasks']}",
        f"Concluídas: {analysis['completed']}",
        f"Pendentes: {analysis['pending']}",
        f"Atrasadas: {analysis['overdue']}",
        f"Taxa de conclusão: {analysis['completion_rate']:.1f}%",
        "",
        "--- Disciplinas ---",
    ]

    for info in analysis["per_subject"].values():
        lines.append(
            f"- {info['name']}: "
            f"{info['completed']}/{info['total']} concluídas, "
            f"{info['overdue']} atrasadas."
        )

    if analysis["overdue_tasks"]:
        lines.append("")
        lines.append("--- Tarefas atrasadas ---")

        for task in analysis["overdue_tasks"]:
            subject_name = analysis["subject_map"].get(
                int(task.get("subject_id", 0) or 0),
                "Sem disciplina",
            )

            lines.append(
                f"- {task.get('title', 'Sem título')} "
                f"({subject_name}) - "
                f"Prazo: {task.get('due_date', 'Sem data')}"
            )

    if analysis["pending_tasks"]:
        lines.append("")
        lines.append("--- Tarefas pendentes ---")

        sorted_pending = sorted(
            analysis["pending_tasks"],
            key=lambda task: parse_due_date(task) or date.max,
        )

        for task in sorted_pending[:10]:
            subject_name = analysis["subject_map"].get(
                int(task.get("subject_id", 0) or 0),
                "Sem disciplina",
            )

            lines.append(
                f"- {task.get('title', 'Sem título')} "
                f"({subject_name}) - "
                f"Prazo: {task.get('due_date', 'Sem data')}"
            )

    return "\n".join(lines)


# ==================================================
# RESPOSTAS LOCAIS
# ==================================================

def generate_local_response(user_message, analysis):
    msg = user_message.lower()

    if (
        analysis["total_tasks"] == 0
        and analysis["total_subjects"] == 0
    ):
        return (
            "Não há dados suficientes para análise. "
            "Cadastre disciplinas e tarefas primeiro."
        )

    if any(word in msg for word in ["atrasad", "atraso", "vencid"]):
        if not analysis["overdue_tasks"]:
            return (
                "🎉 **Parabéns!** Você não possui tarefas "
                "atrasadas no momento. Continue assim!"
            )

        lines = [
            f"⚠️ **Você possui {analysis['overdue']} tarefa(s) atrasada(s):**"
        ]

        for task in analysis["overdue_tasks"]:
            subject_name = analysis["subject_map"].get(
                int(task.get("subject_id", 0) or 0),
                "?",
            )

            lines.append(
                f"- 🔴 **{task.get('title', 'Sem título')}** "
                f"({subject_name}) — "
                f"vencimento: {task.get('due_date', 'sem data')}"
            )

        lines.append(
            "\n💡 Priorize as tarefas mais antigas primeiro."
        )

        return "\n".join(lines)

    if any(
        word in msg
        for word in [
            "como estou",
            "desempenho",
            "progresso",
            "resumo",
            "geral",
            "visão",
        ]
    ):
        lines = [
            "📊 **Visão Geral do seu Desempenho:**",
            f"- 📚 Disciplinas: {analysis['total_subjects']}",
            f"- 📝 Total de tarefas: {analysis['total_tasks']}",
            f"- ✅ Concluídas: {analysis['completed']}",
            f"- ⏳ Pendentes: {analysis['pending']}",
            f"- 🔴 Atrasadas: {analysis['overdue']}",
            f"- 📈 Taxa de conclusão: "
            f"{analysis['completion_rate']:.1f}%",
        ]

        if analysis["completion_rate"] >= 80:
            lines.append(
                "\n🌟 **Excelente!** Você está com ótimo aproveitamento!"
            )
        elif analysis["completion_rate"] >= 50:
            lines.append(
                "\n👍 **Bom progresso!** Continue focando nas tarefas pendentes."
            )
        else:
            lines.append(
                "\n⚡ **Atenção!** Considere montar um cronograma de estudos."
            )

        if analysis["at_risk_subjects"]:
            worst = analysis["at_risk_subjects"][0]

            lines.append(
                f"\n🔎 Disciplina que precisa de atenção: "
                f"**{worst['name']}** "
                f"({worst['completion_rate']:.0f}% concluído)"
            )

        return "\n".join(lines)

    if any(
        word in msg
        for word in [
            "priorid", "foco", "estud", "dica",
            "sugest", "recomend", "ajuda",
        ]
    ):
        lines = ["📝 **Recomendações de Estudo:**"]

        if analysis["overdue_tasks"]:
            lines.append(
                f"- 🔴 Resolver primeiro as "
                f"{analysis['overdue']} tarefa(s) atrasada(s)."
            )

        if analysis["at_risk_subjects"]:
            worst = analysis["at_risk_subjects"][0]

            lines.append(
                f"- 📚 Dar atenção especial à disciplina "
                f"**{worst['name']}**."
            )

        sorted_pending = sorted(
            analysis["pending_tasks"],
            key=lambda task: parse_due_date(task) or date.max,
        )

        if sorted_pending:
            lines.append("- 📅 Próximas entregas:")

            for task in sorted_pending[:3]:
                lines.append(
                    f"  - {task.get('title', 'Sem título')} "
                    f"({task.get('due_date', 'Sem data')})"
                )

        lines.append(
            "\n💡 Divida tarefas grandes em etapas menores "
            "e experimente a técnica Pomodoro."
        )

        return "\n".join(lines)

    if any(
        word in msg
        for word in ["disciplin", "matéria", "materia", "subject"]
    ):
        if not analysis["per_subject"]:
            return "Você ainda não possui disciplinas cadastradas."

        lines = ["📚 **Desempenho por Disciplina:**"]

        for info in sorted(
            analysis["per_subject"].values(),
            key=lambda item: item["completion_rate"],
        ):
            filled = int(info["completion_rate"] / 10)
            bar = "🟩" * filled + "⬜" * (10 - filled)

            lines.append(
                f"- **{info['name']}**: {bar} "
                f"{info['completion_rate']:.0f}% "
                f"({info['completed']}/{info['total']} tarefas)"
            )

        return "\n".join(lines)

    if any(
        word in msg
        for word in [
            "concluí", "concluida", "complet",
            "feita", "feito", "terminad",
        ]
    ):
        if not analysis["completed_tasks"]:
            return (
                "Você ainda não concluiu nenhuma tarefa. "
                "Comece pelas mais urgentes!"
            )

        lines = [
            f"✅ **Tarefas Concluídas ({analysis['completed']}):**"
        ]

        for task in analysis["completed_tasks"][:15]:
            subject_name = analysis["subject_map"].get(
                int(task.get("subject_id", 0) or 0),
                "?",
            )

            lines.append(
                f"- ✅ **{task.get('title', 'Sem título')}** "
                f"({subject_name})"
            )

        return "\n".join(lines)

    return (
        "🤖 **Assistente Acadêmico EduTrack AI**\n\n"
        f"Você possui {analysis['total_subjects']} disciplina(s) "
        f"e {analysis['total_tasks']} tarefa(s).\n\n"
        "**Experimente perguntar:**\n"
        "- Como estou indo?\n"
        "- Quais tarefas estão atrasadas?\n"
        "- Qual disciplina precisa de mais atenção?\n"
        "- Me dê dicas de estudo."
    )


# ==================================================
# INTEGRAÇÃO GEMINI
# ==================================================

def try_gemini_response(user_message, analysis, subjects, tasks):
    try:
        import google.generativeai as genai
    except ImportError:
        return None

    api_key = get_config_url("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.0-flash")

        context = build_context_string(analysis, subjects, tasks)

        system_prompt = (
            "Você é um assistente acadêmico inteligente do EduTrack AI. "
            "Analise os dados do aluno e forneça recomendações "
            "personalizadas, motivacionais e práticas. "
            "Responda sempre em português brasileiro. "
            "Use emojis e Markdown. "
            "Não invente dados que não estejam no contexto."
        )

        prompt = (
            f"{system_prompt}\n\n"
            f"Dados do aluno:\n{context}\n\n"
            f"Pergunta do aluno: {user_message}"
        )

        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return None


# ==================================================
# CARREGAR DADOS
# ==================================================

@st.cache_data(ttl=120, show_spinner=False)
def cached_fetch_student_data(_token):
    return fetch_student_data()


with st.spinner("Carregando seus dados acadêmicos..."):
    subjects, tasks = cached_fetch_student_data(auth_token)

analysis = analyze_academic_data(subjects, tasks)


# ==================================================
# PAINEL LATERAL
# ==================================================

with st.sidebar:
    st.subheader("📊 Resumo Rápido")

    col1, col2 = st.columns(2)

    col1.metric("Disciplinas", analysis["total_subjects"])
    col2.metric("Tarefas", analysis["total_tasks"])

    col3, col4 = st.columns(2)

    col3.metric("Concluídas", analysis["completed"])
    col4.metric("Atrasadas", analysis["overdue"])

    st.progress(
        min(analysis["completion_rate"] / 100, 1.0),
        text=f"Conclusão: {analysis['completion_rate']:.0f}%",
    )

    if get_config_url("GEMINI_API_KEY"):
        st.caption("✨ Modo: Gemini AI ativado")
    else:
        st.caption("🧠 Modo: Análise local")


# ==================================================
# HISTÓRICO DO CHAT
# ==================================================

if "assistant_messages" not in st.session_state:
    st.session_state["assistant_messages"] = [
        {
            "role": "assistant",
            "content": (
                "👋 Olá! Sou o **Assistente Acadêmico** "
                "do EduTrack AI.\n\n"
                "Posso analisar suas disciplinas e tarefas "
                "para ajudar você a organizar seus estudos.\n\n"
                "Experimente perguntar:\n"
                "- Como estou indo?\n"
                "- Quais tarefas estão atrasadas?\n"
                "- Me dê dicas de estudo.\n"
                "- Qual disciplina precisa de mais atenção?"
            ),
        }
    ]


# ==================================================
# EXIBIR HISTÓRICO
# ==================================================

for msg in st.session_state["assistant_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ==================================================
# INTERFACE DO CHAT
# ==================================================

user_input = st.chat_input("Digite sua pergunta...")

if user_input:
    st.session_state["assistant_messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analisando seus dados..."):

            # Atualiza os dados para cada pergunta.
            subjects, tasks = fetch_student_data()
            analysis = analyze_academic_data(subjects, tasks)

            # Tenta utilizar Gemini primeiro.
            response_text = try_gemini_response(
                user_input,
                analysis,
                subjects,
                tasks,
            )

            # Utiliza análise local se Gemini não estiver disponível.
            if response_text is None:
                response_text = generate_local_response(
                    user_input,
                    analysis,
                )

        st.markdown(response_text)

    st.session_state["assistant_messages"].append(
        {
            "role": "assistant",
            "content": response_text,
        }
    )
