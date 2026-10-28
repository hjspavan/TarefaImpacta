
import os
from pathlib import Path

import requests
import streamlit as st


st.title("📚 Disciplinas")
st.write("Cadastro e consulta de disciplinas")


def get_base_url():
    """Obtém a URL base do grupo subjects no arquivo .env."""
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)

                    if chave.strip() == "URL_base_SUBJECTS":
                        return valor.strip().strip('"').strip("'").rstrip("/")

    return os.environ.get("URL_base_SUBJECTS", "").rstrip("/")


def get_headers():
    token = st.session_state.get("auth_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


base_url = get_base_url()
headers = get_headers()

if not base_url:
    st.error("A URL base de Disciplinas não foi encontrada no arquivo .env.")
    st.stop()

if not headers:
    st.warning("Faça login na página Perfil para acessar suas disciplinas.")
    st.stop()


def buscar_disciplinas():
    resposta = requests.get(
        f"{base_url}/subjects",
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


aba_cadastro, aba_lista = st.tabs(
    ["Cadastrar", "Minhas disciplinas"]
)

with aba_cadastro:
    st.subheader("Cadastrar disciplina")

    with st.form("form_cadastrar_disciplina"):
        nome = st.text_input("Nome da disciplina")
        professor = st.text_input("Professor")
        horas = st.number_input(
            "Carga horária",
            min_value=1,
            step=1,
        )

        enviar = st.form_submit_button("Cadastrar")

    if enviar:
        if not nome.strip():
            st.warning("Informe o nome da disciplina.")
        else:
            payload = {
                "name": nome.strip(),
                "teacher": professor.strip() or None,
                "hours": int(horas),
            }

            try:
                resposta = requests.post(
                    f"{base_url}/subjects",
                    headers=headers,
                    json=payload,
                    timeout=15,
                )

                if resposta.status_code in (200, 201):
                    st.success("Disciplina cadastrada no Xano!")
                    st.rerun()
                else:
                    st.error(
                        f"Não foi possível cadastrar a disciplina "
                        f"(HTTP {resposta.status_code})."
                    )

            except requests.RequestException:
                st.error("Erro de conexão ao cadastrar a disciplina.")

with aba_lista:
    st.subheader("Minhas disciplinas")

    if st.button("Atualizar lista"):
        st.rerun()

    try:
        disciplinas = buscar_disciplinas()

        if not disciplinas:
            st.info("Você ainda não possui disciplinas cadastradas.")
        else:
            for disciplina in disciplinas:
                nome_disciplina = disciplina.get("name", "Sem nome")
                professor_disciplina = (
                    disciplina.get("teacher") or "Não informado"
                )
                carga_horaria = disciplina.get("hours", "Não informada")

                with st.container(border=True):
                    st.markdown(f"### 📘 {nome_disciplina}")
                    st.write(f"**Professor:** {professor_disciplina}")
                    st.write(f"**Carga horária:** {carga_horaria} horas")

    except requests.RequestException:
        st.error(
            "Não foi possível carregar as disciplinas do Xano. "
            "Verifique a URL, a autenticação e o endpoint."
        )
