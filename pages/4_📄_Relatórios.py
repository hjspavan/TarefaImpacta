import os
from pathlib import Path
from datetime import datetime, date

import requests
import streamlit as st


st.set_page_config(page_title="Relatórios - EduTrack AI", page_icon="📄")
st.title("📄 Relatórios de Desempenho")
st.write("Visualize seus indicadores acadêmicos e gere relatórios PDF completos.")

# Auth check
auth_token = st.session_state.get("auth_token")
if not auth_token:
    st.warning("Você precisa entrar na sua conta para gerar um relatório.")
    st.info("Acesse a página Perfil e faça login.")
    st.stop()

# Helper to get URLs from st.secrets or os.environ
def get_config_url(var_name):
    try:
        if var_name in st.secrets:
            return str(st.secrets[var_name]).strip().strip('"').strip("'").rstrip("/")
    except Exception:
        pass
    return os.environ.get(var_name, "").rstrip("/")

# Fetch data for indicators
def fetch_indicators():
    """Fetch subjects and tasks to show summary indicators."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    base_subjects = get_config_url("URL_base_SUBJECTS")
    base_tasks = get_config_url("URL_base_ACADEMIC_TASKS")

    subjects = []
    tasks = []

    if base_subjects:
        try:
            resp = requests.get(f"{base_subjects}/subjects", headers=headers, timeout=15)
            if resp.ok:
                data = resp.json()
                subjects = data if isinstance(data, list) else data.get("items", [])
        except requests.RequestException:
            pass

    if base_tasks:
        try:
            resp = requests.get(f"{base_tasks}/academic_tasks", headers=headers, timeout=15)
            if resp.ok:
                data = resp.json()
                tasks = data if isinstance(data, list) else data.get("items", [])
        except requests.RequestException:
            pass

    return subjects, tasks

# Count helpers
def is_completed(task):
    return str(task.get("status", "")).strip().lower() in ("concluida", "concluída", "completed")

def is_overdue(task):
    if is_completed(task):
        return False
    due = task.get("due_date")
    if not due:
        return False
    try:
        if isinstance(due, str):
            due_date = datetime.fromisoformat(due.replace("Z", "+00:00")).date()
        else:
            due_date = due
        return due_date < date.today()
    except (ValueError, TypeError):
        return False

st.divider()

# SECTION 1: Summary indicators
st.subheader("📊 Resumo Acadêmico")

with st.spinner("Carregando indicadores..."):
    subjects, tasks = fetch_indicators()

total_subjects = len(subjects)
total_tasks = len(tasks)
completed = sum(1 for t in tasks if is_completed(t))
pending = total_tasks - completed
overdue = sum(1 for t in tasks if is_overdue(t))
completion_pct = (completed / total_tasks * 100) if total_tasks > 0 else 0.0

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("📚 Disciplinas", total_subjects)
col2.metric("📝 Tarefas", total_tasks)
col3.metric("✅ Concluídas", completed)
col4.metric("⏰ Atrasadas", overdue)

# Progress bar
st.markdown(f"**Taxa de conclusão geral: {completion_pct:.1f}%**")
st.progress(min(completion_pct / 100.0, 1.0))

if overdue > 0:
    st.warning(f"⚠️ Você tem {overdue} tarefa(s) atrasada(s). Gere o relatório para ver detalhes.")

st.divider()

# SECTION 2: Generate PDF
st.subheader("📄 Gerar Relatório PDF")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    generate = st.button("📄 Gerar relatório PDF", type="primary")

with col_btn2:
    regenerate = st.button("🔄 Gerar novamente")

if generate or regenerate:
    try:
        from scripts.generate_performance_report import generate_report

        with st.spinner("Gerando seu relatório completo..."):
            pdf_path = generate_report(auth_token)
            pdf_path = Path(pdf_path)

            if not pdf_path.exists():
                raise FileNotFoundError("O arquivo PDF não foi encontrado após a geração.")

            if pdf_path.stat().st_size == 0:
                raise ValueError("O arquivo PDF foi gerado vazio.")

            with open(pdf_path, "rb") as arquivo:
                pdf_bytes = arquivo.read()

            if not pdf_bytes.startswith(b"%PDF-"):
                raise ValueError("O arquivo gerado não possui um formato PDF válido.")

            st.session_state["pdf_report_bytes"] = pdf_bytes
            st.session_state["pdf_report_generated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        st.success("✅ Relatório gerado com sucesso!")

    except ImportError:
        st.error("O módulo de geração de relatórios não foi encontrado.")
    except Exception as erro:
        st.error(f"❌ Não foi possível gerar o relatório: {erro}")

# SECTION 3: Download
pdf_bytes = st.session_state.get("pdf_report_bytes")
generated_at = st.session_state.get("pdf_report_generated_at")

if pdf_bytes:
    st.divider()
    st.success(f"✅ Seu relatório está pronto para download. (Gerado em: {generated_at or 'N/A'})")

    st.download_button(
        label="📥 Baixar relatório PDF",
        data=pdf_bytes,
        file_name=f"relatorio_desempenho_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        type="primary"
    )
else:
    st.info("Clique em 'Gerar relatório PDF' para criar seu relatório completo.")
