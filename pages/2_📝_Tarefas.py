import streamlit as st

st.title("📝 Tarefas")

st.subheader("Minhas tarefas")

col1, col2 = st.columns(2)

with col1:
    st.write("### Tarefa 1")
    st.write("Fazer exercício de Python")

    if st.button("Concluir", key="tarefa1"):
        st.success("Tarefa concluída!")

with col2:
    st.write("### Tarefa 2")
    st.write("Estudar Streamlit")

    if st.button("Concluir", key="tarefa2"):
        st.success("Tarefa concluída!")

st.divider()

with st.expander("Ver detalhes das tarefas"):
    st.write("Tarefa 1 - Exercício de Python")
    st.write("Tarefa 2 - Estudo de Streamlit")