import streamlit as st

st.title("📚 Disciplinas")

st.write("Cadastro de disciplinas")

aba1, aba2 = st.tabs(["Cadastrar", "Disciplinas"])

with aba1:
    st.subheader("Cadastrar disciplina")

    nome = st.text_input("Nome da disciplina")
    professor = st.text_input("Professor")

    if st.button("Cadastrar"):
        if nome and professor:
            st.success("Disciplina cadastrada com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

with aba2:
    st.subheader("Minhas disciplinas")

    st.write("📘 Banco de Dados")
    st.write("💻 Programação")
    st.write("📊 Análise de Dados")