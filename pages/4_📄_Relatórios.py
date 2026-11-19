
import os
from pathlib import Path
from datetime import datetime, date

import requests
import streamlit as st


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Relatórios - EduTrack AI",
    page_icon="📄",
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

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 22px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #14213D;
        font-weight: bold;
    }

    div[data-testid="stProgress"] > div {
        background-color: #E2E8F0;
        border-radius: 10px;
    }

    div[data-testid="stProgress"] > div > div {
        background-color: #2563EB;
        border-radius: 10px;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-color: #E2E8F0;
        border-radius: 15px;
    }

    .report-card {
        background: linear-gradient(120deg, #14213D, #2563EB);
        padding: 28px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .report-card h2 {
        color: white;
        margin-bottom: 8px;
    }

    .report-card p {
        color: #E2E8F0;
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.title("📄 Relatórios de Desempenho")

st.markdown(
    '<p class="page-subtitle">'
    'Visualize seus indicadores acadêmicos e gere relatórios PDF completos.'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("""
    <div class="report-card">
        <h2>Seu desempenho acadêmico 📊</h2>
        <p>
            Acompanhe sua evolução, consulte suas atividades
            e tenha uma visão geral da sua rotina de estudos.
        </p>
    </div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# AUTENTICAÇÃO
# --------------------------------------------------

auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning(
        "Você precisa entrar na sua conta para gerar um relatório."
    )
    st.info("Acesse a página Perfil e faça login.")
    st.stop()


# --------------------------------------------------
# CONFIGURAÇÃO DAS APIs
# --------------------------------------------------

def get_config_url(var_name):
    """Obtém a URL de um serviço."""

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


# --------------------------------------------------
# BUSCAR INDICADORES
# --------------------------------------------------

def fetch_indicators():
    """Busca disciplinas e tarefas para os indicadores."""

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    base_subjects = get_config_url("URL_base_SUBJECTS")
    base_tasks = get_config_url("URL_base_ACADEMIC_TASKS")

    subjects = []
    tasks = []

    if base_subjects:
        try:
            resp = requests.get(
                f"{base_subjects}/subjects",
                headers=headers,
                timeout=15
            )

            if resp.ok:
                data = resp.json()
                subjects = (
                    data if isinstance(data, list)
                    else data.get("items", [])
                )

        except requests.RequestException:
            pass

    if base_tasks:
        try:
            resp = requests.get(
                f"{base_tasks}/academic_tasks",
                headers=headers,
                timeout=15
            )

            if resp.ok:
                data = resp.json()
                tasks = (
                    data if isinstance(data, list)
                    else data.get("items", [])
                )

        except requests.RequestException:
            pass

    return subjects, tasks


# --------------------------------------------------
# CONTAGEM DAS TAREFAS
# --------------------------------------------------

def is_completed(task):
    return str(
        task.get("status", "")
    ).strip().lower() in (
        "concluida",
        "concluída",
        "completed"
    )


def is_overdue(task):
    if is_completed(task):
        return False

    due = task.get("due_date")

    if not due:
        return False

    try:
        if isinstance(due, str):
            due_date = datetime.fromisoformat(
                due.replace("Z", "+00:00")
            ).date()
        else:
            due_date = due

        return due_date < date.today()

    except (ValueError, TypeError):
        return False


# --------------------------------------------------
# RESUMO ACADÊMICO
# --------------------------------------------------

st.divider()

st.subheader("📊 Resumo Acadêmico")

with st.spinner("Carregando seus indicadores..."):
    subjects, tasks = fetch_indicators()

total_subjects = len(subjects)
total_tasks = len(tasks)

completed = sum(
    1 for task in tasks if is_completed(task)
)

pending = total_tasks - completed

overdue = sum(
    1 for task in tasks if is_overdue(task)
)

completion_pct = (
    completed / total_tasks * 100
) if total_tasks > 0 else 0.0


# --------------------------------------------------
# CARTÕES DE INDICADORES
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Disciplinas",
        total_subjects
    )

with col2:
    st.metric(
        "📝 Total de tarefas",
        total_tasks
    )

with col3:
    st.metric(
        "✅ Concluídas",
        completed
    )

with col4:
    st.metric(
        "⏰ Atrasadas",
        overdue
    )


# --------------------------------------------------
# PROGRESSO ACADÊMICO
# --------------------------------------------------

st.write("")

with st.container(border=True):

    st.subheader("📈 Progresso das atividades")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("**Taxa de conclusão geral**")

    with col2:
        st.markdown(
            f"**{completion_pct:.1f}%**"
        )

    st.progress(
        min(completion_pct / 100.0, 1.0)
    )

    st.caption(
        f"{completed} de {total_tasks} tarefas concluídas."
    )


if overdue > 0:
    st.warning(
        f"⚠️ Você tem {overdue} tarefa(s) atrasada(s). "
        "Gere o relatório para ver os detalhes."
    )

st.divider()


# --------------------------------------------------
# GERAÇÃO DO RELATÓRIO PDF
# --------------------------------------------------

st.subheader("📄 Gerar Relatório PDF")

st.write(
    "Gere um documento completo com seus indicadores "
    "e informações acadêmicas."
)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    generate = st.button(
        "📄 Gerar relatório PDF",
        type="primary",
        use_container_width=True
    )

with col_btn2:
    regenerate = st.button(
        "🔄 Gerar novamente",
        use_container_width=True
    )


if generate or regenerate:

    try:
        from scripts.generate_performance_report import generate_report

        with st.spinner("Gerando seu relatório completo..."):

            pdf_path = generate_report(auth_token)
            pdf_path = Path(pdf_path)

            if not pdf_path.exists():
                raise FileNotFoundError(
                    "O arquivo PDF não foi encontrado após a geração."
                )

            if pdf_path.stat().st_size == 0:
                raise ValueError(
                    "O arquivo PDF foi gerado vazio."
                )

            with open(pdf_path, "rb") as arquivo:
                pdf_bytes = arquivo.read()

            if not pdf_bytes.startswith(b"%PDF-"):
                raise ValueError(
                    "O arquivo gerado não possui um formato PDF válido."
                )

            st.session_state["pdf_report_bytes"] = pdf_bytes

            st.session_state["pdf_report_generated_at"] = (
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )

        st.success("✅ Relatório gerado com sucesso!")

    except ImportError:
        st.error(
            "O módulo de geração de relatórios não foi encontrado."
        )

    except Exception as erro:
        st.error(
            f"❌ Não foi possível gerar o relatório: {erro}"
        )


# --------------------------------------------------
# DOWNLOAD DO PDF
# --------------------------------------------------

pdf_bytes = st.session_state.get("pdf_report_bytes")

generated_at = st.session_state.get(
    "pdf_report_generated_at"
)

st.divider()

st.subheader("📥 Download do relatório")

if pdf_bytes:

    with st.container(border=True):

        st.success(
            "Seu relatório está pronto para download!"
        )

        st.caption(
            f"Gerado em: {generated_at or 'N/A'}"
        )

        st.download_button(
            label="📥 Baixar relatório PDF",
            data=pdf_bytes,
            file_name=(
                f"relatorio_desempenho_"
                f"{datetime.now().strftime('%Y%m%d')}.pdf"
            ),
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

else:

    st.info(
        "Clique em 'Gerar relatório PDF' para criar "
        "seu relatório completo."
    )
