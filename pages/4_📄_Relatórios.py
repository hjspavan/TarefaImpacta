
import os
from pathlib import Path

import streamlit as st

from scripts.generate_performance_report import generate_report


# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.title("📄 Relatórios")
st.caption(
    "Acompanhe seu desempenho acadêmico e gere relatórios em PDF."
)


# ==================================================
# ESTILO VISUAL
# ==================================================

st.markdown(
    """
    <style>
    .report-hero {
        background: linear-gradient(120deg, #4338CA, #6366F1);
        color: white;
        padding: 28px;
        border-radius: 18px;
        margin: 12px 0 24px 0;
    }

    .report-hero h2 {
        color: white;
        margin-bottom: 8px;
    }

    .report-hero p {
        color: #EEF2FF;
        margin-bottom: 0;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
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
    <div class="report-hero">
        <h2>Seu desempenho em um só lugar 📊</h2>
        <p>
            Gere um documento com suas informações acadêmicas,
            disciplinas e progresso nas tarefas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# AUTENTICAÇÃO
# ==================================================

auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning(
        "Faça login na página Perfil para gerar seu relatório."
    )
    st.stop()


# ==================================================
# INFORMAÇÕES DO RELATÓRIO
# ==================================================

st.subheader("Relatório de desempenho")

st.write(
    "O documento reúne informações do estudante, "
    "resumo das tarefas e detalhamento por disciplina."
)

with st.container(border=True):

    st.markdown("### 📑 Relatório acadêmico")

    st.write(
        "O arquivo PDF é gerado com os dados consultados "
        "nos serviços do Xano."
    )

    st.write(
        "- Informações do estudante"
    )

    st.write(
        "- Resumo geral de desempenho"
    )

    st.write(
        "- Tarefas concluídas e pendentes"
    )

    st.write(
        "- Detalhamento por disciplina"
    )

    st.divider()

    if st.button(
        "📄 Gerar relatório PDF",
        use_container_width=True,
        type="primary",
    ):

        try:
            with st.spinner("Gerando seu relatório..."):

                caminho_pdf = generate_report(auth_token)

                caminho_pdf = Path(caminho_pdf)

                if not caminho_pdf.exists():
                    st.error(
                        "O relatório não foi encontrado após a geração."
                    )
                    st.stop()

                pdf_bytes = caminho_pdf.read_bytes()

                st.session_state["pdf_report_path"] = str(caminho_pdf)
                st.session_state["pdf_report_bytes"] = pdf_bytes

            st.success("Relatório gerado com sucesso!")

        except Exception as erro:
            st.error(
                f"Não foi possível gerar o relatório: {erro}"
            )


# ==================================================
# DOWNLOAD DO PDF
# ==================================================

pdf_bytes = st.session_state.get("pdf_report_bytes")

if pdf_bytes:

    st.divider()

    st.subheader("⬇️ Baixar relatório")

    st.write(
        "Seu relatório está pronto para download."
    )

    st.download_button(
        label="📥 Baixar relatório PDF",
        data=pdf_bytes,
        file_name="relatorio_desempenho_edutrack.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


# ==================================================
# RODAPÉ
# ==================================================

st.divider()

st.caption(
    "EduTrack AI • Relatórios de desempenho acadêmico"
)
