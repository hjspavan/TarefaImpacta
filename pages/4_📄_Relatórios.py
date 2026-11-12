
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Relatórios - EduTrack AI",
    page_icon="📄"
)

st.title("📄 Relatórios de Desempenho")

st.write(
    "Gere e baixe seu relatório acadêmico em PDF, "
    "com informações sobre suas disciplinas e tarefas."
)

# Verifica se o usuário está autenticado
auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning(
        "Você precisa entrar na sua conta para gerar um relatório."
    )
    st.info("Acesse a página Perfil e faça login.")
    st.stop()

st.divider()

st.subheader("Meu relatório acadêmico")


# Geração do relatório
if st.button("📄 Gerar relatório PDF", type="primary"):

    try:
        from scripts.generate_performance_report import generate_report

        with st.spinner("Gerando seu relatório..."):

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

            # Guarda o conteúdo do PDF na sessão
            st.session_state["pdf_report_bytes"] = pdf_bytes

        st.success("Relatório gerado com sucesso!")

    except Exception as erro:
        st.error(f"Não foi possível gerar o relatório: {erro}")


# Disponibiliza o PDF para download
pdf_bytes = st.session_state.get("pdf_report_bytes")

if pdf_bytes:

    st.divider()

    st.success("Seu relatório está pronto para download.")

    st.download_button(
        label="📥 Baixar relatório PDF",
        data=pdf_bytes,
        file_name="relatorio_desempenho.pdf",
        mime="application/pdf",
        type="primary"
    )

else:
    st.info(
        "Clique em 'Gerar relatório PDF' para criar seu relatório."
    )
