
import streamlit as st

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# ESTILIZAÇÃO
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

    .welcome-card {
        background: linear-gradient(120deg, #14213D, #2563EB);
        padding: 35px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .welcome-card h1 {
        color: white;
        font-size: 30px;
        margin-bottom: 10px;
    }

    .welcome-card p {
        color: #E2E8F0;
        font-size: 16px;
        margin-bottom: 0;
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

    h1, h2, h3 {
        color: #14213D;
    }

    div[role="radiogroup"] {
        gap: 8px;
    }

    div[role="radiogroup"] label {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 12px;
    }

    div[role="radiogroup"] label:hover {
        border-color: #2563EB;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.markdown("""
<h2 style="color:#14213D; margin-bottom:0;">
    🎓 EduTrack AI
</h2>
<p style="color:#64748B; margin-top:4px;">
    Seu assistente acadêmico
</p>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# NAVEGAÇÃO
# --------------------------------------------------

menu_option = st.radio(
    "Navegação",
    [
        "🏠 Dashboard",
        "📚 Disciplinas",
        "📝 Tarefas",
        "👤 Perfil",
        "📄 Relatórios",
        "🤖 Assistente IA"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")

# --------------------------------------------------
# REDIRECIONAMENTO DAS PÁGINAS
# --------------------------------------------------

if menu_option == "📚 Disciplinas":
    st.switch_page("pages/1_📚_Disciplinas.py")

elif menu_option == "📝 Tarefas":
    st.switch_page("pages/2_📝_Tarefas.py")

elif menu_option == "👤 Perfil":
    st.switch_page("pages/3_👤_Perfil.py")

elif menu_option == "📄 Relatórios":
    st.switch_page("pages/4_📄_Relatórios.py")

elif menu_option == "🤖 Assistente IA":
    st.switch_page("pages/5_🤖_Assistente.py")

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

else:

    st.markdown("""
        <div class="welcome-card">
            <h1>Olá! Seja bem-vindo ao EduTrack AI 👋</h1>
            <p>
                Organize seus estudos, acompanhe suas tarefas
                e alcance seus objetivos acadêmicos.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Visão geral")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📚 Disciplinas Ativas", "—")

    with col2:
        st.metric("📝 Tarefas Pendentes", "—")

    st.write("")
    st.divider()

    st.subheader("🚀 Organize sua rotina acadêmica")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📚 Minhas disciplinas")
        st.write(
            "Cadastre suas disciplinas, professores "
            "e informações acadêmicas."
        )
        st.info("Acesse Disciplinas para cadastrar suas matérias.")

    with col2:
        st.markdown("### 📝 Minhas tarefas")
        st.write(
            "Cadastre atividades, acompanhe prazos "
            "e controle seu progresso."
        )
        st.info("Acesse Tarefas para cadastrar suas atividades.")

    st.divider()

    st.subheader("🎯 Outras funcionalidades")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 👤 Perfil")
        st.write("Crie sua conta ou faça login.")

    with col2:
        st.markdown("### 📄 Relatórios")
        st.write("Gere relatórios acadêmicos em PDF.")

    with col3:
        st.markdown("### 🤖 Assistente IA")
        st.write("Receba ajuda para organizar seus estudos.")
