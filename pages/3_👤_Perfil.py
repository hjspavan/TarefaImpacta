import streamlit as st

st.title("👤 Perfil")

st.subheader("Informações do aluno")

nome = st.text_input("Nome")
email = st.text_input("E-mail")

curso = st.selectbox(
    "Curso",
    ["Análise de Dados", "Programação", "Banco de Dados"]
)

if st.button("Salvar perfil"):
    st.success("Perfil salvo com sucesso!")

st.divider()

st.write("### Informações")
st.write(f"Nome: {nome}")
st.write(f"E-mail: {email}")
st.write(f"Curso: {curso}")