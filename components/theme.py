import streamlit as st


THEMES = {
    "light": {
        "background": "#F5F7FC",
        "surface": "#FFFFFF",
        "surface_alt": "#F0F3FA",
        "text": "#172033",
        "muted": "#69758B",
        "primary": "#635BEB",
        "primary_hover": "#5148D8",
        "border": "#E3E8F2",
        "success": "#16A36A",
        "warning": "#D99018",
        "danger": "#DC4C64",
        "sidebar": "#FFFFFF",
    },
    "dark": {
        "background": "#101522",
        "surface": "#192235",
        "surface_alt": "#222E43",
        "text": "#EDF1FA",
        "muted": "#A0ADC2",
        "primary": "#8B83FF",
        "primary_hover": "#756CF0",
        "border": "#303D53",
        "success": "#42C995",
        "warning": "#F2B84B",
        "danger": "#FF7188",
        "sidebar": "#151E2E",
    },
}


def init_theme():
    """Inicializa o tema salvo na sessão."""
    if "edu_theme" not in st.session_state:
        st.session_state["edu_theme"] = "light"


def get_theme():
    """Retorna o tema atual."""
    init_theme()
    return st.session_state["edu_theme"]


def get_colors():
    """Retorna as cores do tema atual."""
    return THEMES[get_theme()]


def render_theme_toggle():
    """Exibe o seletor de tema na barra lateral."""
    init_theme()

    current = get_theme()

    st.sidebar.markdown("### Aparência")

    selected = st.sidebar.radio(
        "Tema do aplicativo",
        options=["light", "dark"],
        format_func=lambda value: (
            "☀️ Claro" if value == "light" else "🌙 Escuro"
        ),
        index=0 if current == "light" else 1,
        key="edu_theme_selector",
        horizontal=True,
        label_visibility="collapsed",
    )

    if selected != current:
        st.session_state["edu_theme"] = selected
        st.rerun()


def apply_theme():
    """Aplica o tema visual global do EduTrack AI."""
    init_theme()

    colors = get_colors()

    css = f"""
    <style>
    :root {{
        --edu-bg: {colors["background"]};
        --edu-surface: {colors["surface"]};
        --edu-surface-alt: {colors["surface_alt"]};
        --edu-text: {colors["text"]};
        --edu-muted: {colors["muted"]};
        --edu-primary: {colors["primary"]};
        --edu-primary-hover: {colors["primary_hover"]};
        --edu-border: {colors["border"]};
        --edu-success: {colors["success"]};
        --edu-warning: {colors["warning"]};
        --edu-danger: {colors["danger"]};
        --edu-sidebar: {colors["sidebar"]};
    }}

    .stApp {{
        background: var(--edu-bg);
        color: var(--edu-text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background: var(--edu-sidebar);
        border-right: 1px solid var(--edu-border);
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: var(--edu-sidebar);
    }}

    [data-testid="stMain"] {{
        background: var(--edu-bg);
    }}

    h1, h2, h3, h4, h5, h6,
    p, label, span, li {{
        color: var(--edu-text);
    }}

    .stCaption, [data-testid="stCaptionContainer"] {{
        color: var(--edu-muted);
    }}

    [data-testid="stMetric"] {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(20, 30, 60, 0.04);
    }}

    [data-testid="stMetricLabel"] {{
        color: var(--edu-muted);
    }}

    [data-testid="stMetricValue"] {{
        color: var(--edu-primary);
        font-weight: 750;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: var(--edu-primary);
        color: white;
        border: 1px solid var(--edu-primary);
        border-radius: 10px;
        padding: 9px 18px;
        font-weight: 650;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background: var(--edu-primary-hover);
        border-color: var(--edu-primary-hover);
        color: white;
        transform: translateY(-1px);
    }}

    [data-testid="stBaseButton-secondary"] {{
        background: var(--edu-surface);
        color: var(--edu-text);
        border: 1px solid var(--edu-border);
    }}

    input, textarea,
    [data-baseweb="select"] > div {{
        background: var(--edu-surface) !important;
        color: var(--edu-text) !important;
        border-color: var(--edu-border) !important;
        border-radius: 10px !important;
    }}

    [data-testid="stTabs"] button {{
        color: var(--edu-muted);
        font-weight: 650;
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: var(--edu-primary);
    }}

    [data-testid="stExpander"] {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 12px;
    }}

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {{
        border: 1px solid var(--edu-border);
        border-radius: 12px;
        overflow: hidden;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    [data-testid="stProgressBar"] > div {{
        background: var(--edu-surface-alt);
        border-radius: 20px;
    }}

    [data-testid="stProgressBar"] > div > div {{
        background: var(--edu-primary);
        border-radius: 20px;
    }}

    [data-testid="stChatMessage"] {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 14px;
        padding: 12px;
    }}

    .edu-card {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(20, 30, 60, 0.04);
    }}

    .edu-header {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 24px;
    }}

    .edu-muted {{
        color: var(--edu-muted);
    }}

    .edu-status-badge {{
        display: inline-block;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }}

    .edu-status-success {{
        background: rgba(22, 163, 106, 0.12);
        color: var(--edu-success);
    }}

    .edu-status-warning {{
        background: rgba(217, 144, 24, 0.12);
        color: var(--edu-warning);
    }}

    .edu-status-danger {{
        background: rgba(220, 76, 100, 0.12);
        color: var(--edu-danger);
    }}

    div[data-testid="stForm"] {{
        background: var(--edu-surface);
        border: 1px solid var(--edu-border);
        border-radius: 16px;
        padding: 20px;
    }}

    hr {{
        border-color: var(--edu-border);
    }}

    @media (max-width: 768px) {{
        .edu-card, .edu-header {{
            padding: 16px;
        }}
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def render_page_header(title, subtitle=None, icon="📘"):
    """Exibe um cabeçalho padronizado."""
    st.markdown(
        f"""
        <div class="edu-header">
            <h1>{icon} {title}</h1>
            {f'<p class="edu-muted">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, icon="📊"):
    """Exibe um cartão de métrica."""
    st.markdown(
        f"""
        <div class="edu-card">
            <div style="font-size: 25px">{icon}</div>
            <div class="edu-muted">{label}</div>
            <div style="font-size: 28px; font-weight: 750; color: var(--edu-primary)">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(status):
    """Exibe um indicador visual de status."""
    normalized = str(status).strip().lower()

    if normalized in ("concluída", "concluida", "completed", "done"):
        css_class = "edu-status-success"
    elif normalized in ("atrasada", "overdue"):
        css_class = "edu-status-danger"
    else:
        css_class = "edu-status-warning"

    st.markdown(
        f'<span class="edu-status-badge {css_class}">{status}</span>',
        unsafe_allow_html=True,
    )


def render_overdue_badge():
    """Exibe um indicador de tarefa atrasada."""
    render_status_badge("Atrasada")


def render_empty_state(message, icon="📭"):
    """Exibe uma mensagem quando não existem registros."""
    st.markdown(
        f"""
        <div class="edu-card" style="text-align: center; padding: 35px">
            <div style="font-size: 38px">{icon}</div>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title, icon=""):
    """Exibe o título de uma seção."""
    st.markdown(f"### {icon} {title}")


def render_progress_bar(value, label=None):
    """Exibe uma barra de progresso."""
    value = max(0, min(float(value), 100))

    if label:
        st.caption(label)

    st.progress(value / 100)


def render_sidebar_branding():
    """Exibe a identidade visual na barra lateral."""
    st.sidebar.markdown(
        """
        <div style="padding: 12px 4px 20px">
            <div style="font-size: 25px; font-weight: 800;
                        color: var(--edu-primary)">
                EduTrack AI
            </div>
            <div class="edu-muted" style="font-size: 12px">
                Seu espaço acadêmico inteligente
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def check_auth():
    """Verifica se existe usuário autenticado."""
    if not st.session_state.get("auth_token"):
        st.warning("Faça login na página Perfil para continuar.")
        st.stop()
