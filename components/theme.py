"""
theme.py

Shared theme system for EduTrack AI.
Provides CSS injection and reusable styled components for all pages.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------

COLORS = {
    "primary": "#2563EB",
    "primary_dark": "#14213D",
    "primary_light": "#DBEAFE",
    "background": "#F8FAFC",
    "white": "#FFFFFF",
    "text": "#1E293B",
    "text_secondary": "#64748B",
    "success": "#16A34A",
    "success_light": "#DCFCE7",
    "danger": "#DC2626",
    "danger_light": "#FEE2E2",
    "warning": "#F59E0B",
    "warning_light": "#FEF3C7",
    "info": "#2563EB",
    "info_light": "#DBEAFE",
    "border": "#E2E8F0",
    "shadow": "rgba(0,0,0,0.04)",
}

STATUS_COLORS = {
    "concluída": COLORS["success"],
    "concluida": COLORS["success"],
    "completed": COLORS["success"],
    "pendente": COLORS["warning"],
    "pending": COLORS["warning"],
    "em andamento": COLORS["primary"],
    "in_progress": COLORS["primary"],
}


# ---------------------------------------------------------------------------
# CSS Injection
# ---------------------------------------------------------------------------

def apply_theme():
    """Inject the full EduTrack AI CSS theme into the current page."""
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)


_GLOBAL_CSS = """
<style>
/* ============================== GLOBAL ============================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Root variables */
:root {
    --primary: #2563EB;
    --primary-dark: #14213D;
    --primary-light: #DBEAFE;
    --bg: #F8FAFC;
    --white: #FFFFFF;
    --text: #1E293B;
    --text-secondary: #64748B;
    --success: #16A34A;
    --success-light: #DCFCE7;
    --danger: #DC2626;
    --danger-light: #FEE2E2;
    --warning: #F59E0B;
    --warning-light: #FEF3C7;
    --border: #E2E8F0;
    --shadow: rgba(0,0,0,0.04);
    --radius: 12px;
    --radius-sm: 8px;
}

/* Base font */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* ============================== SIDEBAR ============================== */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14213D 0%, #1a2f52 100%) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

[data-testid="stSidebar"] .stRadio > label {
    color: #94A3B8 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stSidebar"] .stRadio > div > label {
    color: #CBD5E1 !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div [aria-checked="true"] + label {
    background: rgba(37,99,235,0.2) !important;
    color: #FFFFFF !important;
}

/* ============================== HEADINGS ============================== */

h1 {
    color: var(--primary-dark) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
    letter-spacing: -0.02em !important;
}

h2 {
    color: var(--primary-dark) !important;
    font-weight: 600 !important;
    font-size: 1.35rem !important;
}

h3 {
    color: var(--text) !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

/* ============================== BUTTONS ============================== */

.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.25rem !important;
    border: 1px solid var(--border) !important;
    transition: all 0.2s ease !important;
    font-size: 0.875rem !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.15) !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stFormSubmitButton"] {
    background: linear-gradient(135deg, #2563EB 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
}

/* ============================== INPUTS ============================== */

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid var(--border) !important;
    padding: 0.6rem 0.85rem !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* ============================== TABS ============================== */

.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: var(--bg);
    padding: 4px;
    border-radius: var(--radius);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 1.25rem !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    box-shadow: 0 1px 3px var(--shadow) !important;
    color: var(--primary) !important;
}

/* ============================== METRICS ============================== */

[data-testid="stMetric"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 1px 3px var(--shadow) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
}

[data-testid="stMetricValue"] {
    color: var(--primary-dark) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
}

/* ============================== ALERTS ============================== */

.stAlert {
    border-radius: var(--radius-sm) !important;
    border: none !important;
}

/* ============================== DOWNLOAD BUTTON ============================== */

.stDownloadButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    background: linear-gradient(135deg, #16A34A 0%, #15803d 100%) !important;
    color: white !important;
    border: none !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #15803d 0%, #166534 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(22,163,74,0.2) !important;
}

/* ============================== CHAT ============================== */

[data-testid="stChatMessage"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    padding: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.stChatInputContainer {
    border-radius: var(--radius) !important;
}

/* ============================== PROGRESS BAR ============================== */

.stProgress > div > div > div {
    border-radius: 999px !important;
    background: linear-gradient(90deg, #2563EB 0%, #16A34A 100%) !important;
}

.stProgress > div > div {
    border-radius: 999px !important;
    background: var(--border) !important;
}

/* ============================== CONTAINERS ============================== */

[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
}

/* ============================== FORM ============================== */

[data-testid="stForm"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.5rem !important;
    background: var(--white) !important;
}

/* ============================== DIVIDER ============================== */

hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ============================== CUSTOM COMPONENTS ============================== */

.edu-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
    margin-bottom: 0.75rem;
}

.edu-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

.edu-metric-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
}

.edu-metric-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

.edu-metric-icon {
    font-size: 1.75rem;
    margin-bottom: 0.25rem;
}

.edu-metric-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #14213D;
    line-height: 1.2;
}

.edu-metric-label {
    font-size: 0.75rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
    margin-top: 0.25rem;
}

.edu-status-badge {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.edu-status-completed {
    background: #DCFCE7;
    color: #16A34A;
}

.edu-status-pending {
    background: #FEF3C7;
    color: #D97706;
}

.edu-status-inprogress {
    background: #DBEAFE;
    color: #2563EB;
}

.edu-status-overdue {
    background: #FEE2E2;
    color: #DC2626;
}

.edu-header {
    background: linear-gradient(135deg, #14213D 0%, #1a2f52 100%);
    color: white;
    padding: 1.75rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.edu-header h2 {
    color: white !important;
    margin: 0 !important;
    font-size: 1.5rem !important;
}

.edu-header p {
    color: #94A3B8;
    margin: 0.25rem 0 0 0;
    font-size: 0.9rem;
}

.edu-header .greeting {
    color: #DBEAFE;
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}

.edu-section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #14213D;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #DBEAFE;
}

.edu-empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: #64748B;
}

.edu-empty-state .icon {
    font-size: 3rem;
    margin-bottom: 0.75rem;
    opacity: 0.5;
}

.edu-empty-state .message {
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.edu-empty-state .hint {
    font-size: 0.85rem;
    color: #94A3B8;
}

.edu-task-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1rem;
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.edu-task-row:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.edu-progress-bar {
    width: 100%;
    height: 8px;
    background: #E2E8F0;
    border-radius: 999px;
    overflow: hidden;
}

.edu-progress-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.5s ease;
}

.edu-chip {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 500;
    background: #F1F5F9;
    color: #64748B;
    margin-right: 0.25rem;
}

.edu-ai-header {
    background: linear-gradient(135deg, #2563EB 0%, #7c3aed 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    text-align: center;
}

.edu-ai-header h2 {
    color: white !important;
    margin: 0 !important;
}

.edu-suggestion-btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-radius: 999px;
    font-size: 0.8rem;
    color: #64748B;
    cursor: pointer;
    transition: all 0.15s ease;
    margin: 0.25rem;
}

.edu-suggestion-btn:hover {
    background: #DBEAFE;
    color: #2563EB;
    border-color: #93C5FD;
}

.edu-login-container {
    max-width: 420px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}

.edu-profile-card {
    background: linear-gradient(135deg, #14213D 0%, #1a2f52 100%);
    color: white;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 1.5rem;
}

.edu-profile-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(37,99,235,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 1rem;
    border: 3px solid rgba(255,255,255,0.2);
}

.edu-report-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

</style>
"""


# ---------------------------------------------------------------------------
# Reusable Component Functions
# ---------------------------------------------------------------------------

def render_page_header(icon, title, subtitle=None, greeting=None):
    """Render a styled page header with gradient background."""
    greeting_html = f'<p class="greeting">{greeting}</p>' if greeting else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="edu-header">
            {greeting_html}
            <h2>{icon} {title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(icon, value, label, color=None):
    """Render a styled metric card. Use inside st.columns()."""
    color_style = f"color: {color};" if color else ""
    st.markdown(
        f"""
        <div class="edu-metric-card">
            <div class="edu-metric-icon">{icon}</div>
            <div class="edu-metric-value" style="{color_style}">{value}</div>
            <div class="edu-metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(status):
    """Return HTML for a colored status badge."""
    status_lower = str(status).strip().lower()
    if status_lower in ("concluída", "concluida", "completed"):
        css_class = "edu-status-completed"
        label = "Concluída"
    elif status_lower in ("em andamento", "in_progress"):
        css_class = "edu-status-inprogress"
        label = "Em andamento"
    elif status_lower in ("pendente", "pending"):
        css_class = "edu-status-pending"
        label = "Pendente"
    else:
        css_class = "edu-status-pending"
        label = str(status)
    return f'<span class="edu-status-badge {css_class}">{label}</span>'


def render_overdue_badge():
    """Return HTML for an overdue badge."""
    return '<span class="edu-status-badge edu-status-overdue">Atrasada</span>'


def render_empty_state(icon, message, hint=None):
    """Render a friendly empty state."""
    hint_html = f'<p class="hint">{hint}</p>' if hint else ""
    st.markdown(
        f"""
        <div class="edu-empty-state">
            <div class="icon">{icon}</div>
            <p class="message">{message}</p>
            {hint_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(icon, title):
    """Render a section title with icon and bottom border."""
    st.markdown(
        f"""<div class="edu-section-title">{icon} {title}</div>""",
        unsafe_allow_html=True,
    )


def render_progress_bar(percentage, height=8):
    """Render a custom progress bar with dynamic color."""
    if percentage >= 70:
        color = COLORS["success"]
    elif percentage >= 40:
        color = COLORS["warning"]
    else:
        color = COLORS["danger"]
    pct = max(0, min(100, percentage))
    st.markdown(
        f"""
        <div class="edu-progress-bar" style="height:{height}px">
            <div class="edu-progress-fill" style="width:{pct}%;background:{color}"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_branding():
    """Render EduTrack AI branding in the sidebar."""
    st.sidebar.markdown(
        """
        <div style="text-align:center;padding:1rem 0 0.5rem;">
            <span style="font-size:2rem;">🎓</span>
            <h2 style="margin:0.25rem 0 0;font-size:1.25rem;color:white !important;">
                EduTrack AI
            </h2>
            <p style="margin:0;font-size:0.75rem;color:#94A3B8 !important;">
                Gestão Acadêmica Inteligente
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()


def check_auth():
    """Check if user is authenticated. Returns token or calls st.stop()."""
    auth_token = st.session_state.get("auth_token")
    if not auth_token:
        st.warning("🔒 Você precisa estar conectado para acessar esta página.")
        st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login.")
        st.stop()
    return auth_token
