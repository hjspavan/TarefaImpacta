
import os
from datetime import date, datetime

import requests
import streamlit as st


# ---------------------------------------------------------------------------
# Configuração e identidade visual
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Assistente Acadêmico",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    /* Fundo principal */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Área principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #14213D !important;
        font-weight: 750 !important;
        letter-spacing: -0.5px;
    }

    /* Textos */
    p, label {
        color: #475569;
    }

    /* Cabeçalho do assistente */
    .assistant-header {
        background: linear-gradient(135deg, #14213D 0%, #2563EB 100%);
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 8px 24px rgba(20, 33, 61, 0.12);
    }

    .assistant-header h2 {
        color: white !important;
        margin: 0 0 8px 0;
        font-size: 27px;
    }

    .assistant-header p {
        color: #DBEAFE;
        margin: 0;
        font-size: 15px;
    }

    /* Mensagens */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.035);
    }

    /* Avatares */
    [data-testid="stChatMessageAvatar"] {
        background-color: #EFF6FF;
        border-radius: 12px;
    }

    /* Campo de mensagem */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 16px;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #2563EB;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12);
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #14213D !important;
    }

    /* Cartões de métricas */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    [data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-weight: 800;
    }

    /* Barra de progresso */
    [data-testid="stProgressBar"] > div > div {
        background-color: #2563EB;
    }

    /* Botões */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
        border: none;
    }

    /* Alertas */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Separadores */
    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def get_config_url(var_name):
    """Read a URL (or key) from st.secrets or environment variables."""
    try:
        if var_name in st.secrets:
            return str(st.secrets[var_name]).strip().strip('"').strip("'").rstrip("/")
    except Exception:
        pass

    return os.environ.get(var_name, "").rstrip("/")


def get_headers():
    """Return authorization headers using the session token."""
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Auth check
# ---------------------------------------------------------------------------

auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning("Faça login na página Perfil para usar o assistente.")
    st.stop()

headers = get_headers()

base_subjects = get_config_url("URL_base_SUBJECTS")
base_tasks = get_config_url("URL_base_ACADEMIC_TASKS")

if not base_subjects or not base_tasks:
    st.error(
        "Configure `URL_base_SUBJECTS` e `URL_base_ACADEMIC_TASKS` "
        "no arquivo `.streamlit/secrets.toml`."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_subjects():
    """Fetch subjects from the Xano API."""
    try:
        response = requests.get(
            f"{base_subjects}/subjects",
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("items", [])

        return []

    except requests.RequestException:
        return []


def fetch_tasks():
    """Fetch academic tasks from the Xano API."""
    try:
        response = requests.get(
            f"{base_tasks}/academic_tasks",
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("items", [])

        return []

    except requests.RequestException:
        return []


def fetch_student_data():
    """Fetch subjects and tasks from Xano and return both lists."""
    subjects = fetch_subjects()
    tasks = fetch_tasks()

    return subjects, tasks


# ---------------------------------------------------------------------------
# Task status helpers
# ---------------------------------------------------------------------------

def is_completed(task):
    """Check if a task is completed based on common status fields."""
    status = str(task.get("status", "")).lower()

    if status in ("completed", "concluída", "concluida", "done", "finalizada"):
        return True

    if task.get("completed") is True:
        return True

    return False


def parse_due_date(task):
    """Parse the due_date field into a date object, or return None."""
    due = task.get("due_date")

    if not due:
        return None

    try:
        if isinstance(due, str):
            return datetime.fromisoformat(
                due.replace("Z", "+00:00")
            ).date()

        if isinstance(due, (datetime, date)):
            return due if isinstance(due, date) else due.date()

    except (ValueError, TypeError):
        return None

    return None


def is_overdue(task):
    """Return True if the task is past its due date and not completed."""
    if is_completed(task):
        return False

    due_date = parse_due_date(task)

    if not due_date:
        return False

    return due_date < date.today()


# ---------------------------------------------------------------------------
# Academic analysis
# ---------------------------------------------------------------------------

def analyze_academic_data(subjects, tasks):
    """Analyze the student's academic data and return a structured dict."""

    total_tasks = len(tasks)

    completed_tasks = [t for t in tasks if is_completed(t)]
    overdue_tasks = [t for t in tasks if is_overdue(t)]
    pending_tasks = [
        t for t in tasks
        if not is_completed(t) and not is_overdue(t)
    ]

    completion_rate = (
        len(completed_tasks) / total_tasks * 100
        if total_tasks > 0 else 0.0
    )

    # Build a subject id → name map
    subject_map = {
        s.get("id"): s.get("name", "Sem nome")
        for s in subjects
    }

    # Per-subject breakdown
    per_subject = {}

    for subj in subjects:
        sid = subj.get("id")
        sname = subj.get("name", "Sem nome")

        subj_tasks = [
            t for t in tasks
            if t.get("subject_id") == sid
        ]

        subj_completed = [
            t for t in subj_tasks if is_completed(t)
        ]

        subj_overdue = [
            t for t in subj_tasks if is_overdue(t)
        ]

        subj_pending = [
            t for t in subj_tasks
            if not is_completed(t) and not is_overdue(t)
        ]

        subj_rate = (
            len(subj_completed) / len(subj_tasks) * 100
            if subj_tasks else 0.0
        )

        per_subject[sid] = {
            "name": sname,
            "total": len(subj_tasks),
            "completed": len(subj_completed),
            "pending": len(subj_pending),
            "overdue": len(subj_overdue),
            "completion_rate": subj_rate,
        }

    # Identify subjects needing attention
    at_risk = sorted(
        [v for v in per_subject.values() if v["total"] > 0],
        key=lambda x: x["completion_rate"],
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
        "pending_tasks": [
            t for t in tasks
            if not is_completed(t) and not is_overdue(t)
        ],
    }


# ---------------------------------------------------------------------------
# Context builder (for Gemini)
# ---------------------------------------------------------------------------

def build_context_string(analysis, subjects, tasks):
    """Build a plain-text context string with the student's data."""

    lines = []

    lines.append(f"Total de disciplinas: {analysis['total_subjects']}")
    lines.append(f"Total de tarefas: {analysis['total_tasks']}")
    lines.append(f"Concluídas: {analysis['completed']}")
    lines.append(f"Pendentes: {analysis['pending']}")
    lines.append(f"Atrasadas: {analysis['overdue']}")
    lines.append(
        f"Taxa de conclusão geral: {analysis['completion_rate']:.1f}%"
    )

    lines.append("")
    lines.append("--- Disciplinas ---")

    for info in analysis["per_subject"].values():
        lines.append(
            f"- {info['name']}: {info['completed']}/{info['total']} concluídas "
            f"({info['completion_rate']:.0f}%), {info['overdue']} atrasadas"
        )

    lines.append("")

    if analysis["overdue_tasks"]:
        lines.append("--- Tarefas Atrasadas ---")

        for t in analysis["overdue_tasks"]:
            subj_name = analysis["subject_map"].get(
                t.get("subject_id"), "?"
            )
            due = t.get("due_date", "sem data")

            lines.append(
                f"- [{subj_name}] {t.get('title', 'Sem título')} "
                f"(vencimento: {due})"
            )

        lines.append("")

    if analysis["pending_tasks"]:
        lines.append("--- Próximas Tarefas Pendentes ---")

        sorted_pending = sorted(
            analysis["pending_tasks"],
            key=lambda t: parse_due_date(t) or date.max,
        )

        for t in sorted_pending[:10]:
            subj_name = analysis["subject_map"].get(
                t.get("subject_id"), "?"
            )
            due = t.get("due_date", "sem data")

            lines.append(
                f"- [{subj_name}] {t.get('title', 'Sem título')} "
                f"(vencimento: {due})"
            )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Local (rule-based) response generator
# ---------------------------------------------------------------------------

def generate_local_response(user_message, analysis):
    """Generate a response without external AI, using keyword matching."""

    msg_lower = user_message.lower()

    # No data at all
    if analysis["total_tasks"] == 0 and analysis["total_subjects"] == 0:
        return (
            "Não há dados suficientes para análise. "
            "Cadastre disciplinas e tarefas primeiro."
        )

    # --- Overdue tasks ---
    if any(
        word in msg_lower
        for word in ["atrasad", "atraso", "vencid", "overdue"]
    ):

        if not analysis["overdue_tasks"]:
            return (
                "🎉 **Parabéns!** Você não possui tarefas atrasadas "
                "no momento. Continue assim!"
            )

        lines = [
            f"⚠️ **Você possui {analysis['overdue']} tarefa(s) atrasada(s):**\n"
        ]

        for t in analysis["overdue_tasks"]:
            subj_name = analysis["subject_map"].get(
                t.get("subject_id"), "?"
            )
            due = t.get("due_date", "sem data")
            title = t.get("title", "Sem título")

            lines.append(
                f"- 🔴 **{title}** ({subj_name}) — vencimento: `{due}`"
            )

        lines.append(
            "\n💡 **Dica:** Priorize as tarefas mais antigas primeiro "
            "e converse com seus professores caso precise de prazos extras."
        )

        return "\n".join(lines)

    # --- General overview ---
    if any(
        word in msg_lower
        for word in [
            "como estou", "desempenho", "progresso",
            "resumo", "geral", "visão"
        ]
    ):

        lines = ["📊 **Visão Geral do seu Desempenho:**\n"]

        lines.append(
            f"- 📚 **Disciplinas:** {analysis['total_subjects']}"
        )
        lines.append(
            f"- 📝 **Total de tarefas:** {analysis['total_tasks']}"
        )
        lines.append(
            f"- ✅ **Concluídas:** {analysis['completed']}"
        )
        lines.append(
            f"- ⏳ **Pendentes:** {analysis['pending']}"
        )
        lines.append(
            f"- 🔴 **Atrasadas:** {analysis['overdue']}"
        )
        lines.append(
            f"- 📈 **Taxa de conclusão:** {analysis['completion_rate']:.1f}%"
        )

        if analysis["completion_rate"] >= 80:
            lines.append(
                "\n🌟 **Excelente!** Você está com um ótimo aproveitamento!"
            )

        elif analysis["completion_rate"] >= 50:
            lines.append(
                "\n👍 **Bom progresso!** Continue focando nas tarefas "
                "pendentes para melhorar ainda mais."
            )

        else:
            lines.append(
                "\n⚡ **Atenção!** Sua taxa de conclusão está abaixo de 50%. "
                "Considere montar um cronograma de estudos."
            )

        if analysis["at_risk_subjects"]:
            worst = analysis["at_risk_subjects"][0]

            lines.append(
                f"\n🔎 **Disciplina que mais precisa de atenção:** "
                f"**{worst['name']}** "
                f"({worst['completion_rate']:.0f}% concluído)"
            )

        return "\n".join(lines)

    # --- Study tips / priorities ---
    if any(
        word in msg_lower
        for word in [
            "priorid", "foco", "estud", "dica",
            "sugest", "recomend", "ajuda"
        ]
    ):

        lines = ["📝 **Recomendações de Estudo:**\n"]

        # Overdue first
        if analysis["overdue_tasks"]:
            lines.append(
                f"1️⃣ **Resolver tarefas atrasadas** — Você tem "
                f"{analysis['overdue']} tarefa(s) vencida(s). "
                "Comece por elas!"
            )

        # At-risk subjects
        if analysis["at_risk_subjects"]:
            worst = analysis["at_risk_subjects"][0]

            lines.append(
                f"2️⃣ **Focar em {worst['name']}** — Esta disciplina "
                f"tem a menor taxa de conclusão "
                f"({worst['completion_rate']:.0f}%)."
            )

        # Upcoming deadlines
        sorted_pending = sorted(
            analysis["pending_tasks"],
            key=lambda t: parse_due_date(t) or date.max,
        )

        upcoming = sorted_pending[:3]

        if upcoming:
            lines.append("3️⃣ **Próximas entregas:**")

            for t in upcoming:
                subj_name = analysis["subject_map"].get(
                    t.get("subject_id"), "?"
                )
                due = t.get("due_date", "sem data")

                lines.append(
                    f"   - **{t.get('title', 'Sem título')}** "
                    f"({subj_name}) — `{due}`"
                )

        lines.append(
            "\n💡 **Dica geral:** Divida tarefas grandes em blocos menores, "
            "use a técnica Pomodoro (25 min de foco + 5 min de pausa) "
            "e revise o conteúdo antes das avaliações."
        )

        return "\n".join(lines)

    # --- Per-subject breakdown ---
    if any(
        word in msg_lower
        for word in ["disciplin", "matéria", "materia", "subject"]
    ):

        if not analysis["per_subject"]:
            return "Você ainda não possui disciplinas cadastradas."

        lines = ["📚 **Desempenho por Disciplina:**\n"]

        for info in sorted(
            analysis["per_subject"].values(),
            key=lambda x: x["completion_rate"]
        ):

            bar_filled = int(info["completion_rate"] / 10)
            bar_empty = 10 - bar_filled

            bar = "🟩" * bar_filled + "⬜" * bar_empty

            status_emoji = (
                "✅" if info["completion_rate"] >= 80
                else (
                    "⚠️" if info["completion_rate"] >= 50
                    else "🔴"
                )
            )

            lines.append(
                f"{status_emoji} **{info['name']}**: {bar} "
                f"{info['completion_rate']:.0f}% "
                f"({info['completed']}/{info['total']} tarefas)"
            )

            if info["overdue"] > 0:
                lines.append(
                    f"   ↳ 🔴 {info['overdue']} tarefa(s) atrasada(s)"
                )

        return "\n".join(lines)

    # --- Completed tasks ---
    if any(
        word in msg_lower
        for word in [
            "concluí", "concluida", "complet",
            "feita", "feito", "terminad"
        ]
    ):

        if not analysis["completed_tasks"]:
            return (
                "Você ainda não concluiu nenhuma tarefa. "
                "Comece pelas mais urgentes!"
            )

        lines = [
            f"✅ **Tarefas Concluídas ({analysis['completed']}):**\n"
        ]

        for t in analysis["completed_tasks"][:15]:
            subj_name = analysis["subject_map"].get(
                t.get("subject_id"), "?"
            )

            lines.append(
                f"- ✅ **{t.get('title', 'Sem título')}** ({subj_name})"
            )

        if analysis["completed"] > 15:
            lines.append(
                f"\n... e mais {analysis['completed'] - 15} tarefa(s)."
            )

        return "\n".join(lines)

    # --- Default / catch-all ---
    lines = ["🤖 **Assistente Acadêmico EduTrack AI**\n"]

    lines.append("Aqui está um resumo rápido:\n")
    lines.append(f"- 📚 {analysis['total_subjects']} disciplina(s)")
    lines.append(f"- 📝 {analysis['total_tasks']} tarefa(s) total")
    lines.append(f"- ✅ {analysis['completed']} concluída(s)")
    lines.append(f"- ⏳ {analysis['pending']} pendente(s)")
    lines.append(f"- 🔴 {analysis['overdue']} atrasada(s)")

    lines.append(
        f"\n📈 Taxa de conclusão: **{analysis['completion_rate']:.1f}%**"
    )

    lines.append("\n**Experimente perguntar:**")
    lines.append('- _"Como estou indo?"_')
    lines.append('- _"Quais tarefas estão atrasadas?"_')
    lines.append('- _"Qual disciplina precisa de mais atenção?"_')
    lines.append('- _"Me dê dicas de estudo"_')

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Gemini API response (optional)
# ---------------------------------------------------------------------------

def try_gemini_response(user_message, analysis, subjects, tasks):
    """Attempt to generate a response using the Gemini API."""

    try:
        import google.generativeai as genai
    except ImportError:
        return None

    api_key = (
        get_config_url("GEMINI_API_KEY")
        or os.environ.get("GEMINI_API_KEY", "")
    )

    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.0-flash")

        context = build_context_string(analysis, subjects, tasks)

        system_prompt = (
            "Você é um assistente acadêmico inteligente do EduTrack AI. "
            "Analise os dados do aluno e forneça recomendações personalizadas, "
            "motivacionais e práticas. Responda sempre em português brasileiro. "
            "Use emojis e formatação markdown para tornar a resposta clara e agradável. "
            "Seja conciso, mas completo. Não invente dados que não estejam no contexto fornecido."
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


# ---------------------------------------------------------------------------
# Sidebar — quick stats
# ---------------------------------------------------------------------------

@st.cache_data(ttl=120, show_spinner=False)
def cached_fetch_student_data(_token):
    """Cached wrapper so we don't re-fetch on every rerun."""
    return fetch_student_data()


subjects, tasks = cached_fetch_student_data(auth_token)
analysis = analyze_academic_data(subjects, tasks)


# ---------------------------------------------------------------------------
# Cabeçalho visual do assistente
# ---------------------------------------------------------------------------

st.markdown("""
<div class="assistant-header">
    <h2>🤖 Assistente Acadêmico</h2>
    <p>
        Seu parceiro inteligente para acompanhar seu desempenho,
        organizar seus estudos e planejar suas próximas tarefas.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 📊 Resumo Rápido")
    st.caption("Acompanhe seus indicadores acadêmicos.")

    if analysis["total_subjects"] == 0 and analysis["total_tasks"] == 0:
        st.info(
            "Cadastre disciplinas e tarefas para visualizar suas estatísticas."
        )

    else:
        col1, col2 = st.columns(2)

        col1.metric(
            "Disciplinas",
            analysis["total_subjects"]
        )

        col2.metric(
            "Tarefas",
            analysis["total_tasks"]
        )

        col3, col4 = st.columns(2)

        col3.metric(
            "Concluídas",
            analysis["completed"]
        )

        col4.metric(
            "Atrasadas",
            analysis["overdue"]
        )

        st.progress(
            min(analysis["completion_rate"] / 100, 1.0),
            text=f"Conclusão: {analysis['completion_rate']:.0f}%"
        )

        st.divider()

        api_key = (
            get_config_url("GEMINI_API_KEY")
            or os.environ.get("GEMINI_API_KEY", "")
        )

        if api_key:
            st.caption("✨ Modo: Gemini AI ativado")
        else:
            st.caption("🧠 Modo: Análise local")


# ---------------------------------------------------------------------------
# Chat interface
# ---------------------------------------------------------------------------

# Initialise message history
if "assistant_messages" not in st.session_state:
    st.session_state["assistant_messages"] = [
        {
            "role": "assistant",
            "content": (
                "👋 Olá! Sou o **Assistente Acadêmico** do EduTrack AI.\n\n"
                "Posso analisar suas disciplinas e tarefas para ajudar você a "
                "organizar seus estudos. Experimente perguntar:\n"
                '- _"Como estou indo?"_\n'
                '- _"Quais tarefas estão atrasadas?"_\n'
                '- _"Me dê dicas de estudo"_\n'
                '- _"Qual disciplina precisa de mais atenção?"_'
            ),
        }
    ]


# Display chat history
for msg in st.session_state["assistant_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
user_input = st.chat_input("Digite sua pergunta...")

if user_input:

    # Append user message
    st.session_state["assistant_messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analisando seus dados..."):

            # Refresh data for the current question
            subjects, tasks = fetch_student_data()

            analysis = analyze_academic_data(subjects, tasks)

            # Try Gemini first, fall back to local
            response_text = try_gemini_response(
                user_input,
                analysis,
                subjects,
                tasks
            )

            if response_text is None:
                response_text = generate_local_response(
                    user_input,
                    analysis
                )

        st.markdown(response_text)

    # Append assistant response to history
    st.session_state["assistant_messages"].append(
        {"role": "assistant", "content": response_text}
    )
