
import streamlit as st

from components.theme import (
    init_theme,
    apply_theme,
    render_theme_toggle,
)

# --------------------------------------------------
# CONFIGURAÇÃO
# --------------------------------------------------

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# TEMA
# --------------------------------------------------

init_theme()
apply_theme()

# --------------------------------------------------
# IDENTIDADE VISUAL
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 22px 0;">
            <div style="font-size: 28px; font-weight: 800;">
                🎓 EduTrack <span style="color: #6366F1;">AI</span>
            </div>
            <div style="font-size: 12px; opacity: 0.7;">
                Seu desempenho acadêmico em um só lugar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_theme_toggle()

    st.divider()

    st.caption("PLATAFORMA ACADÊMICA")
    st.caption("Organize. Acompanhe. Evolua.")

# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.markdown(
    """
    <div style="
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #4338CA, #6366F1, #818CF8);
        color: white;
        margin-bottom: 24px;
    ">
        <div style="font-size: 13px; opacity: 0.85;">
            BEM-VINDO AO SEU ESPAÇO ACADÊMICO
        </div>
        <div style="font-size: 32px; font-weight: 800; margin-top: 8px;">
            EduTrack AI
        </div>
        <div style="font-size: 15px; opacity: 0.9; margin-top: 8px;">
            Acompanhe suas disciplinas, organize suas tarefas
            e evolua nos seus estudos.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# NAVEGAÇÃO
# --------------------------------------------------

st.markdown("### Navegação")

paginas = {
    "🏠 Dashboard": None,
    "📚 Disciplinas": "pages/1_📚_Disciplinas.py",
    "📝 Tarefas": "pages/2_📝_Tarefas.py",
    "👤 Perfil": "pages/3_👤_Perfil.py",
    "📄 Relatórios": "pages/4_📄_Relatórios.py",
    "🤖 Assistente IA": "pages/5_🤖_Assistente.py",
}

pagina_atual = st.radio(
    "Escolha uma página",
    list(paginas.keys()),
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation",
)

destino = paginas[pagina_atual]

if destino is not None:
    st.switch_page(destino)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.markdown("## Visão geral")
st.markdown(
    "Tenha acesso rápido às principais áreas da sua vida acadêmica."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            padding: 22px;
            border-radius: 15px;
            border: 1px solid rgba(128,128,128,0.25);
            min-height: 150px;
        ">
            <div style="font-size: 28px;">📚</div>
            <div style="font-size: 18px; font-weight: 700;">
                Disciplinas
            </div>
            <div style="opacity: 0.7; font-size: 13px;">
                Gerencie suas matérias e acompanhe seus estudos.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Acessar disciplinas", use_container_width=True):
        st.switch_page(paginas["📚 Disciplinas"])

with col2:
    st.markdown(
        """
        <div style="
            padding: 22px;
            border-radius: 15px;
            border: 1px solid rgba(128,128,128,0.25);
            min-height: 150px;
        ">
            <div style="font-size: 28px;">📝</div>
            <div style="font-size: 18px; font-weight: 700;">
                Tarefas
            </div>
            <div style="opacity: 0.7; font-size: 13px;">
                Organize atividades e acompanhe os prazos.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Acessar tarefas", use_container_width=True):
        st.switch_page(paginas["📝 Tarefas"])

with col3:
    st.markdown(
        """
        <div style="
            padding: 22px;
            border-radius: 15px;
            border: 1px solid rgba(128,128,128,0.25);
            min-height: 150px;
        ">
            <div style="font-size: 28px;">📄</div>
            <div style="font-size: 18px; font-weight: 700;">
                Relatórios
            </div>
            <div style="opacity: 0.7; font-size: 13px;">
                Consulte seu desempenho e gere relatórios.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Acessar relatórios", use_container_width=True):
        st.switch_page(paginas["📄 Relatórios"])

st.divider()

st.markdown("### Inteligência artificial")

col_ai, col_profile = st.columns(2)

with col_ai:
    st.info(
        "🤖 **Assistente IA**\n\n"
        "Converse com seu assistente acadêmico e obtenha "
        "orientações sobre suas disciplinas e tarefas."
    )
    if st.button("Conversar com Assistente IA", use_container_width=True):
        st.switch_page(paginas["🤖 Assistente IA"])

with col_profile:
    st.info(
        "👤 **Seu perfil**\n\n"
        "Acesse sua conta, consulte seus dados e gerencie sua sessão."
    )
    if st.button("Acessar meu perfil", use_container_width=True):
        st.switch_page(paginas["👤 Perfil"])

st.divider()

st.caption("EduTrack AI • Organização acadêmica inteligente")
