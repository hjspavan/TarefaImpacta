"""
generate_performance_report.py

Generates a comprehensive, multi-page academic performance report in PDF format,
consolidating user data, subjects, and academic tasks from Xano endpoints.

Uses a custom native SimplePdfBuilder (raw PDF 1.4 bytes) with support for
multi-page documents, rectangles, lines, and color.
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

import requests


# ---------------------------------------------------------------------------
# Environment / config helpers
# ---------------------------------------------------------------------------

def get_env_url(variable_name):
    """Read a URL variable from secrets.toml, .env, or os.environ."""
    secrets_path = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() == variable_name:
                            return v.strip().strip('"').strip("'").rstrip("/")
        except Exception:
            pass

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip() == variable_name:
                            return value.strip().strip('"').strip("'").rstrip("/")
        except Exception:
            pass

    return os.environ.get(variable_name, "").rstrip("/")


# ---------------------------------------------------------------------------
# PDF text helper
# ---------------------------------------------------------------------------

def escape_pdf_text(text):
    """Escape reserved characters in PDF text strings and replace accented chars."""
    if text is None:
        return ""
    text_str = str(text)
    cleaned = (
        text_str.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("è", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("õ", "o")
        .replace("ô", "o")
        .replace("ú", "u")
        .replace("ü", "u")
        .replace("ç", "c")
        .replace("ñ", "n")
        .replace("Ã", "A")
        .replace("Á", "A")
        .replace("À", "A")
        .replace("Â", "A")
        .replace("É", "E")
        .replace("Ê", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Õ", "O")
        .replace("Ô", "O")
        .replace("Ú", "U")
        .replace("Ç", "C")
    )
    return cleaned


# ---------------------------------------------------------------------------
# Task analysis helpers
# ---------------------------------------------------------------------------

_COMPLETED_STATUSES = ("concluida", "concluída", "completed")


def _is_completed(task):
    """Return True if a task dict is marked as completed."""
    return str(task.get("status", "")).strip().lower() in _COMPLETED_STATUSES


def _parse_due_date(raw):
    """Flexibly parse a due_date value. Returns a date or None."""
    if raw is None:
        return None
    raw_str = str(raw).strip()
    if not raw_str:
        return None
    # Try several common formats
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ",
                "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw_str[:len(raw_str)], fmt).date()
        except (ValueError, TypeError):
            continue
    # Last resort: try parsing just the date portion before 'T'
    try:
        return datetime.strptime(raw_str[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _is_overdue(task):
    """A task is overdue when not completed AND due_date < today."""
    if _is_completed(task):
        return False
    due = _parse_due_date(task.get("due_date"))
    if due is None:
        return False
    return due < date.today()


def _get_task_subject_id(task):
    """Extract the subject_id from a task, handling int or dict values."""
    sid = task.get("subject_id")
    if isinstance(sid, dict):
        return sid.get("id")
    return sid


def _tasks_for_subject(tasks, subject):
    """Return tasks matching a subject's id."""
    subj_id = subject.get("id")
    return [t for t in tasks if isinstance(t, dict) and _get_task_subject_id(t) == subj_id]


def _count_completed(task_list):
    return sum(1 for t in task_list if _is_completed(t))


def _count_overdue(task_list):
    return sum(1 for t in task_list if _is_overdue(t))


# ---------------------------------------------------------------------------
# AI Recommendations (rule-based)
# ---------------------------------------------------------------------------

def generate_recommendations(subjects, tasks, completion_rate, overdue_count):
    """Generate rule-based academic recommendations from student data."""
    recommendations = []

    # 1. General situation
    if completion_rate >= 80:
        recommendations.append(
            "Excelente desempenho academico! Voce esta no caminho certo. "
            "Continue mantendo essa disciplina e organizacao nos estudos."
        )
    elif completion_rate >= 50:
        recommendations.append(
            "Bom progresso nos estudos, mas ha espaco para melhoria. "
            "Tente estabelecer metas semanais para aumentar a taxa de conclusao."
        )
    elif completion_rate >= 25:
        recommendations.append(
            "Atencao: a taxa de conclusao esta abaixo de 50%. "
            "Recomenda-se revisar seu planejamento e priorizar as tarefas pendentes."
        )
    else:
        recommendations.append(
            "Situacao critica: a maioria das tarefas esta pendente. "
            "E fundamental criar um plano de recuperacao imediato e buscar apoio academico."
        )

    # 2. Overdue tasks
    if overdue_count > 0:
        recommendations.append(
            f"Existem {overdue_count} tarefa(s) atrasada(s) que precisam de atencao imediata. "
            "Priorize a entrega dessas atividades para evitar prejuizo na avaliacao."
        )
    elif len(tasks) > 0:
        recommendations.append(
            "Parabens! Nenhuma tarefa atrasada foi identificada. Continue assim!"
        )

    # 3. Per-subject analysis
    low_subjects = []
    for subject in subjects:
        subject_tasks = _tasks_for_subject(tasks, subject)
        if len(subject_tasks) == 0:
            continue
        completed = _count_completed(subject_tasks)
        rate = completed / len(subject_tasks)
        if rate < 0.3:
            name = subject.get("name") or "Sem Nome"
            low_subjects.append(name)
            recommendations.append(
                f"A disciplina '{escape_pdf_text(name)}' precisa de atencao urgente "
                f"(apenas {completed}/{len(subject_tasks)} tarefas concluidas, {rate*100:.0f}%)."
            )

    # 4. Priority suggestions – subjects with most overdue tasks first
    subject_overdue = []
    for subject in subjects:
        subject_tasks = _tasks_for_subject(tasks, subject)
        ov = _count_overdue(subject_tasks)
        if ov > 0:
            subject_overdue.append((subject.get("name", "Sem Nome"), ov))
    subject_overdue.sort(key=lambda x: x[1], reverse=True)

    if subject_overdue:
        priority_names = [f"{n} ({c} atraso(s))" for n, c in subject_overdue[:5]]
        recommendations.append(
            "Prioridade de estudo sugerida (por atrasos): " + ", ".join(priority_names) + "."
        )

    # 5. Organization tip
    if len(tasks) > 0:
        recommendations.append(
            "Dica de organizacao: utilize um calendario ou agenda para acompanhar "
            "os prazos de cada tarefa e evitar acumulo de atividades."
        )

    return recommendations


# ---------------------------------------------------------------------------
# Enhanced SimplePdfBuilder – raw PDF 1.4 with multi-page, rects, lines, color
# ---------------------------------------------------------------------------

class SimplePdfBuilder:
    """Native PDF 1.4 builder with multi-page support, graphics, and color."""

    PAGE_WIDTH = 595
    PAGE_HEIGHT = 842

    def __init__(self):
        # Each page is a list of stream commands (strings)
        self._pages = [[]]
        self._current_color = (0, 0, 0)  # default black

    # -- Page management ----------------------------------------------------

    def new_page(self):
        """Start a new page."""
        self._pages.append([])
        self._current_color = (0, 0, 0)

    @property
    def _current_page(self):
        return self._pages[-1]

    @property
    def page_count(self):
        return len(self._pages)

    # -- Color --------------------------------------------------------------

    def set_color(self, r, g, b):
        """Set text/stroke color (0-1 floats)."""
        self._current_color = (r, g, b)
        self._current_page.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        self._current_page.append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    # -- Text ---------------------------------------------------------------

    def add_line(self, x, y, text, font_size=12, font_name="F1"):
        """Add a line of text at (x, y)."""
        safe_text = escape_pdf_text(text)
        self._current_page.append(
            f"BT\n/{font_name} {font_size} Tf\n"
            f"{self._current_color[0]:.3f} {self._current_color[1]:.3f} {self._current_color[2]:.3f} rg\n"
            f"{x} {y} Td\n({safe_text}) Tj\nET"
        )

    # -- Graphics -----------------------------------------------------------

    def draw_rect(self, x, y, width, height, fill_r=0.0, fill_g=0.0, fill_b=0.0):
        """Draw a filled rectangle."""
        self._current_page.append(
            f"{fill_r:.3f} {fill_g:.3f} {fill_b:.3f} rg\n"
            f"{x} {y} {width} {height} re\nf"
        )

    def draw_line_segment(self, x1, y1, x2, y2, width=0.5):
        """Draw a line segment (stroke)."""
        self._current_page.append(
            f"{self._current_color[0]:.3f} {self._current_color[1]:.3f} {self._current_color[2]:.3f} RG\n"
            f"{width} w\n{x1} {y1} m\n{x2} {y2} l\nS"
        )

    def draw_rect_outline(self, x, y, width, height, line_width=0.5):
        """Draw a rectangle outline (stroke only)."""
        self._current_page.append(
            f"{self._current_color[0]:.3f} {self._current_color[1]:.3f} {self._current_color[2]:.3f} RG\n"
            f"{line_width} w\n{x} {y} {width} {height} re\nS"
        )

    # -- Build PDF bytes ----------------------------------------------------

    def build(self):
        """Build the complete multi-page PDF bytes."""
        num_pages = len(self._pages)
        # Object numbering:
        #   1 = Catalog
        #   2 = Pages
        #   3 = Font resource dictionary (shared)
        #   For each page i (0-based):
        #     4 + i*2     = Page object
        #     4 + i*2 + 1 = Content stream object
        total_objects = 3 + num_pages * 2

        objects = []  # list of bytes

        # -- Object 1: Catalog
        objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")

        # -- Object 2: Pages
        kids_refs = " ".join(f"{4 + i*2} 0 R" for i in range(num_pages))
        objects.append(
            f"2 0 obj\n<< /Type /Pages /Kids [{kids_refs}] /Count {num_pages} >>\nendobj"
            .encode("latin-1")
        )

        # -- Object 3: Font dictionary (shared via indirect reference)
        objects.append(
            b"3 0 obj\n<< /Font << "
            b"/F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
            b"/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> "
            b">> >>\nendobj"
        )

        # -- Page + content stream objects
        for i, page_cmds in enumerate(self._pages):
            page_obj_num = 4 + i * 2
            content_obj_num = page_obj_num + 1

            content_stream = "\n".join(page_cmds).encode("latin-1", errors="replace")
            stream_length = len(content_stream)

            # Page object
            objects.append(
                f"{page_obj_num} 0 obj\n"
                f"<< /Type /Page /Parent 2 0 R "
                f"/Resources 3 0 R "
                f"/MediaBox [0 0 {self.PAGE_WIDTH} {self.PAGE_HEIGHT}] "
                f"/Contents {content_obj_num} 0 R >>\n"
                f"endobj".encode("latin-1")
            )

            # Content stream object
            objects.append(
                f"{content_obj_num} 0 obj\n<< /Length {stream_length} >>\nstream\n"
                .encode("latin-1")
                + content_stream
                + b"\nendstream\nendobj"
            )

        # -- Assemble PDF
        pdf_bytes = bytearray(b"%PDF-1.4\n")
        offsets = []

        for obj in objects:
            offsets.append(len(pdf_bytes))
            pdf_bytes.extend(obj + b"\n")

        xref_pos = len(pdf_bytes)
        pdf_bytes.extend(f"xref\n0 {total_objects + 1}\n".encode("latin-1"))
        pdf_bytes.extend(b"0000000000 65535 f \n")

        for offset in offsets:
            pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

        trailer = (
            f"trailer\n<< /Size {total_objects + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("latin-1")
        pdf_bytes.extend(trailer)

        return bytes(pdf_bytes)


# ---------------------------------------------------------------------------
# PDF page drawing helpers
# ---------------------------------------------------------------------------

def _add_footer(pdf, page_number, total_pages):
    """Draw footer with page number and branding on the current page."""
    pdf.set_color(0.4, 0.4, 0.4)
    pdf.draw_line_segment(50, 55, 545, 55)
    pdf.add_line(250, 40, f"Pagina {page_number} de {total_pages}", font_size=8, font_name="F1")
    pdf.add_line(170, 28, "Gerado automaticamente pelo EduTrack AI - Sistema de Gestao Academica", font_size=7, font_name="F1")
    pdf.set_color(0, 0, 0)


def _draw_progress_bar(pdf, x, y, width, height, percentage, label=None):
    """Draw a progress bar: grey background + colored fill + optional label."""
    # Background (light grey)
    pdf.draw_rect(x, y, width, height, 0.85, 0.85, 0.85)
    # Filled portion
    fill_width = max(0, min(width, width * percentage / 100.0))
    if percentage >= 70:
        fill_r, fill_g, fill_b = 0.18, 0.69, 0.29  # green
    elif percentage >= 40:
        fill_r, fill_g, fill_b = 1.0, 0.76, 0.03  # yellow/amber
    else:
        fill_r, fill_g, fill_b = 0.90, 0.22, 0.21  # red
    if fill_width > 0:
        pdf.draw_rect(x, y, fill_width, height, fill_r, fill_g, fill_b)
    # Outline
    pdf.set_color(0.3, 0.3, 0.3)
    pdf.draw_rect_outline(x, y, width, height, 0.5)
    # Percentage text
    if label is None:
        label = f"{percentage:.1f}%"
    pdf.set_color(0, 0, 0)
    pdf.add_line(x + width + 8, y + 1, label, font_size=8, font_name="F2")


def _draw_header(pdf, title="EduTrack AI - Relatorio de Desempenho Academico"):
    """Draw the page header bar."""
    # Blue header bar
    pdf.draw_rect(0, 805, 595, 37, 0.13, 0.35, 0.67)
    pdf.set_color(1, 1, 1)
    pdf.add_line(50, 815, title, font_size=15, font_name="F2")
    generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.add_line(420, 817, f"Emitido: {generation_date}", font_size=8, font_name="F1")
    pdf.set_color(0, 0, 0)


def _draw_section_title(pdf, y, title):
    """Draw a section title with a coloured left bar."""
    pdf.draw_rect(50, y - 2, 4, 16, 0.13, 0.35, 0.67)
    pdf.set_color(0.10, 0.25, 0.50)
    pdf.add_line(60, y, title, font_size=13, font_name="F2")
    pdf.set_color(0, 0, 0)
    return y - 22


# ---------------------------------------------------------------------------
# Main PDF generation
# ---------------------------------------------------------------------------

def generate_performance_pdf(user_info, subjects, tasks, output_path):
    """Compile data and generate the multi-page performance PDF."""
    pdf = SimplePdfBuilder()

    # -- Compute global statistics -----------------------------------------
    total_subjects = len(subjects)
    total_tasks = len(tasks)
    completed_count = _count_completed(tasks)
    overdue_count = _count_overdue(tasks)
    pending_count = total_tasks - completed_count
    completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0.0

    student_name = user_info.get("name") or user_info.get("nome") or "Aluno Nao Identificado"
    student_email = user_info.get("email") or "Nao informado"
    generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Compute per-subject stats once
    subject_stats = []
    for subj in subjects:
        s_tasks = _tasks_for_subject(tasks, subj)
        s_completed = _count_completed(s_tasks)
        s_overdue = _count_overdue(s_tasks)
        s_total = len(s_tasks)
        s_pending = s_total - s_completed
        s_rate = (s_completed / s_total * 100) if s_total > 0 else 0.0
        subject_stats.append({
            "subject": subj,
            "tasks": s_tasks,
            "total": s_total,
            "completed": s_completed,
            "pending": s_pending,
            "overdue": s_overdue,
            "rate": s_rate,
        })

    # We need to know total_pages before writing footers.
    # Pre-calculate pages:
    #   Page 1: Cover / Summary (always)
    #   Page 2+: Per-discipline (we fit ~4 subjects per page)
    #   Next page: Productivity analysis
    #   Last page: AI Recommendations
    subjects_per_page = 4
    discipline_pages = max(1, -(-len(subjects) // subjects_per_page)) if subjects else 1
    total_pages = 1 + discipline_pages + 1 + 1  # cover + disciplines + productivity + recommendations

    # =====================================================================
    # PAGE 1: Cover + Identification + Summary
    # =====================================================================
    _draw_header(pdf)
    y = 785

    # Student identification
    y = _draw_section_title(pdf, y, "1. Identificacao do Estudante")
    pdf.add_line(65, y, f"Nome: {student_name}", font_size=11, font_name="F1")
    y -= 16
    pdf.add_line(65, y, f"E-mail: {student_email}", font_size=11, font_name="F1")
    y -= 16
    pdf.add_line(65, y, f"Data de Geracao: {generation_date}", font_size=10, font_name="F1")
    y -= 25

    # Separator
    pdf.set_color(0.7, 0.7, 0.7)
    pdf.draw_line_segment(50, y, 545, y)
    pdf.set_color(0, 0, 0)
    y -= 20

    # Academic summary
    y = _draw_section_title(pdf, y, "2. Resumo Academico")

    summary_items = [
        ("Total de Disciplinas:", str(total_subjects)),
        ("Total de Tarefas:", str(total_tasks)),
        ("Tarefas Concluidas:", str(completed_count)),
        ("Tarefas Pendentes:", str(pending_count)),
        ("Tarefas Atrasadas:", str(overdue_count)),
        ("Taxa de Conclusao:", f"{completion_rate:.1f}%"),
    ]
    for label, value in summary_items:
        pdf.add_line(65, y, label, font_size=10, font_name="F2")
        pdf.add_line(220, y, value, font_size=10, font_name="F1")
        y -= 16

    y -= 10

    # Visual progress bar
    pdf.add_line(65, y, "Progresso Geral:", font_size=10, font_name="F2")
    _draw_progress_bar(pdf, 180, y - 3, 300, 14, completion_rate)
    y -= 35

    # Separator
    pdf.set_color(0.7, 0.7, 0.7)
    pdf.draw_line_segment(50, y, 545, y)
    pdf.set_color(0, 0, 0)
    y -= 20

    # Quick subject overview table header
    y = _draw_section_title(pdf, y, "3. Visao Geral por Disciplina")
    pdf.set_color(0.13, 0.35, 0.67)
    pdf.add_line(65, y, "Disciplina", font_size=9, font_name="F2")
    pdf.add_line(280, y, "Concl.", font_size=9, font_name="F2")
    pdf.add_line(330, y, "Pend.", font_size=9, font_name="F2")
    pdf.add_line(375, y, "Atras.", font_size=9, font_name="F2")
    pdf.add_line(420, y, "Progresso", font_size=9, font_name="F2")
    pdf.set_color(0, 0, 0)
    y -= 4
    pdf.draw_line_segment(65, y, 540, y)
    y -= 14

    for ss in subject_stats:
        if y < 80:
            break
        s_name = (ss["subject"].get("name") or "Sem Nome")[:35]
        pdf.add_line(65, y, s_name, font_size=9, font_name="F1")
        pdf.add_line(290, y, str(ss["completed"]), font_size=9, font_name="F1")
        pdf.add_line(340, y, str(ss["pending"]), font_size=9, font_name="F1")
        pdf.add_line(385, y, str(ss["overdue"]), font_size=9, font_name="F1")
        _draw_progress_bar(pdf, 420, y - 2, 80, 10, ss["rate"], f"{ss['rate']:.0f}%")
        y -= 18

    _add_footer(pdf, 1, total_pages)

    # =====================================================================
    # PAGES 2+: Per-Discipline Breakdown
    # =====================================================================
    page_num = 2
    subjects_on_page = 0

    if not subjects:
        pdf.new_page()
        _draw_header(pdf, "EduTrack AI - Detalhamento por Disciplina")
        y = 785
        y = _draw_section_title(pdf, y, "Detalhamento por Disciplina")
        pdf.add_line(65, y, "Nenhuma disciplina cadastrada ate o momento.", font_size=10, font_name="F1")
        _add_footer(pdf, page_num, total_pages)
        page_num += 1
    else:
        y = 0  # force new page on first iteration
        for idx, ss in enumerate(subject_stats):
            # Start new page if needed
            if subjects_on_page >= subjects_per_page or y < 180:
                if idx > 0:
                    _add_footer(pdf, page_num, total_pages)
                    page_num += 1
                pdf.new_page()
                _draw_header(pdf, "EduTrack AI - Detalhamento por Disciplina")
                y = 785
                y = _draw_section_title(pdf, y, "Detalhamento por Disciplina")
                subjects_on_page = 0

            subj = ss["subject"]
            s_name = subj.get("name") or "Sem Nome"
            s_teacher = subj.get("teacher") or "Nao informado"

            # Subject header
            pdf.set_color(0.13, 0.35, 0.67)
            pdf.draw_rect(60, y - 2, 480, 18, 0.92, 0.95, 1.0)
            pdf.add_line(65, y, f"{idx + 1}. {s_name}", font_size=11, font_name="F2")
            pdf.set_color(0, 0, 0)
            y -= 20

            pdf.add_line(80, y, f"Professor(a): {s_teacher}", font_size=9, font_name="F1")
            y -= 16

            pdf.add_line(80, y, f"Total: {ss['total']}   |   Concluidas: {ss['completed']}   |   Pendentes: {ss['pending']}   |   Atrasadas: {ss['overdue']}", font_size=9, font_name="F1")
            y -= 16

            pdf.add_line(80, y, f"Conclusao: {ss['rate']:.1f}%", font_size=9, font_name="F2")
            _draw_progress_bar(pdf, 180, y - 2, 200, 10, ss["rate"])
            y -= 20

            # List overdue tasks for this subject
            overdue_tasks = [t for t in ss["tasks"] if _is_overdue(t)]
            if overdue_tasks:
                pdf.set_color(0.9, 0.22, 0.21)
                pdf.add_line(80, y, "Tarefas atrasadas:", font_size=8, font_name="F2")
                pdf.set_color(0, 0, 0)
                y -= 13
                for ot in overdue_tasks[:5]:
                    t_title = (ot.get("title") or ot.get("name") or "Sem titulo")[:60]
                    t_due = str(ot.get("due_date", ""))[:10]
                    pdf.add_line(95, y, f"- {t_title} (prazo: {t_due})", font_size=8, font_name="F1")
                    y -= 12
                if len(overdue_tasks) > 5:
                    pdf.add_line(95, y, f"  ... e mais {len(overdue_tasks) - 5} tarefa(s)", font_size=8, font_name="F1")
                    y -= 12

            y -= 15
            pdf.set_color(0.8, 0.8, 0.8)
            pdf.draw_line_segment(65, y + 8, 540, y + 8)
            pdf.set_color(0, 0, 0)

            subjects_on_page += 1

        _add_footer(pdf, page_num, total_pages)
        page_num += 1

    # =====================================================================
    # PRODUCTIVITY ANALYSIS PAGE
    # =====================================================================
    pdf.new_page()
    _draw_header(pdf, "EduTrack AI - Analise de Produtividade")
    y = 785

    y = _draw_section_title(pdf, y, "Analise de Produtividade")

    # Overall stats
    pdf.add_line(65, y, f"Taxa de Conclusao Geral: {completion_rate:.1f}%", font_size=11, font_name="F2")
    y -= 20
    pdf.add_line(65, y, f"Tarefas Concluidas: {completed_count}   |   Pendentes: {pending_count}   |   Atrasadas: {overdue_count}", font_size=10, font_name="F1")
    y -= 25

    # Comparison bar: completed vs pending
    pdf.add_line(65, y, "Comparativo:", font_size=10, font_name="F2")
    y -= 18
    bar_total_w = 400
    comp_w = int(bar_total_w * (completed_count / total_tasks)) if total_tasks > 0 else 0
    pend_w = bar_total_w - comp_w
    if comp_w > 0:
        pdf.draw_rect(65, y, comp_w, 16, 0.18, 0.69, 0.29)
    if pend_w > 0:
        pdf.draw_rect(65 + comp_w, y, pend_w, 16, 0.90, 0.22, 0.21)
    pdf.set_color(0.3, 0.3, 0.3)
    pdf.draw_rect_outline(65, y, bar_total_w, 16)
    pdf.set_color(0, 0, 0)
    y -= 16
    pdf.add_line(65, y, f"Concluidas ({completed_count})", font_size=7, font_name="F1")
    pdf.add_line(300, y, f"Pendentes/Atrasadas ({pending_count})", font_size=7, font_name="F1")
    y -= 30

    # Separator
    pdf.set_color(0.7, 0.7, 0.7)
    pdf.draw_line_segment(50, y, 545, y)
    pdf.set_color(0, 0, 0)
    y -= 20

    # Identification of delays
    y = _draw_section_title(pdf, y, "Identificacao de Atrasos")
    all_overdue = [t for t in tasks if isinstance(t, dict) and _is_overdue(t)]
    if not all_overdue:
        pdf.add_line(65, y, "Nenhuma tarefa atrasada identificada. Excelente!", font_size=10, font_name="F1")
        y -= 20
    else:
        shown = 0
        for ot in all_overdue[:10]:
            t_title = (ot.get("title") or ot.get("name") or "Sem titulo")[:50]
            t_due = str(ot.get("due_date", ""))[:10]
            # Try to find subject name
            sid = _get_task_subject_id(ot)
            s_name = "N/A"
            for s in subjects:
                if s.get("id") == sid:
                    s_name = (s.get("name") or "")[:25]
                    break
            pdf.set_color(0.9, 0.22, 0.21)
            pdf.add_line(65, y, f"- {t_title}", font_size=9, font_name="F1")
            pdf.set_color(0.4, 0.4, 0.4)
            pdf.add_line(350, y, f"Prazo: {t_due}  |  {s_name}", font_size=8, font_name="F1")
            pdf.set_color(0, 0, 0)
            y -= 14
            shown += 1
        if len(all_overdue) > 10:
            pdf.add_line(65, y, f"... e mais {len(all_overdue) - 10} tarefa(s) atrasada(s)", font_size=8, font_name="F1")
            y -= 14
    y -= 15

    # Separator
    pdf.set_color(0.7, 0.7, 0.7)
    pdf.draw_line_segment(50, y, 545, y)
    pdf.set_color(0, 0, 0)
    y -= 20

    # Horizontal bar chart – completion rate per subject
    y = _draw_section_title(pdf, y, "Grafico: Conclusao por Disciplina")
    if not subject_stats:
        pdf.add_line(65, y, "Sem dados para exibir.", font_size=10, font_name="F1")
    else:
        bar_max_w = 300
        for ss in subject_stats:
            if y < 80:
                break
            s_name = (ss["subject"].get("name") or "Sem Nome")[:25]
            pdf.add_line(65, y, s_name, font_size=8, font_name="F1")
            bar_w = int(bar_max_w * ss["rate"] / 100.0)
            # Background
            pdf.draw_rect(200, y - 2, bar_max_w, 12, 0.90, 0.90, 0.90)
            # Fill
            if bar_w > 0:
                if ss["rate"] >= 70:
                    pdf.draw_rect(200, y - 2, bar_w, 12, 0.18, 0.69, 0.29)
                elif ss["rate"] >= 40:
                    pdf.draw_rect(200, y - 2, bar_w, 12, 1.0, 0.76, 0.03)
                else:
                    pdf.draw_rect(200, y - 2, bar_w, 12, 0.90, 0.22, 0.21)
            pdf.set_color(0, 0, 0)
            pdf.add_line(200 + bar_max_w + 8, y, f"{ss['rate']:.0f}%", font_size=8, font_name="F2")
            y -= 20

    _add_footer(pdf, page_num, total_pages)
    page_num += 1

    # =====================================================================
    # AI RECOMMENDATIONS PAGE
    # =====================================================================
    pdf.new_page()
    _draw_header(pdf, "EduTrack AI - Recomendacoes Inteligentes")
    y = 785

    y = _draw_section_title(pdf, y, "Recomendacoes Inteligentes (IA)")

    recommendations = generate_recommendations(subjects, tasks, completion_rate, overdue_count)

    if not recommendations:
        pdf.add_line(65, y, "Nenhuma recomendacao disponivel no momento.", font_size=10, font_name="F1")
    else:
        for i, rec in enumerate(recommendations, 1):
            if y < 100:
                break
            # Recommendation number badge
            pdf.draw_rect(60, y - 2, 18, 14, 0.13, 0.35, 0.67)
            pdf.set_color(1, 1, 1)
            pdf.add_line(65, y, str(i), font_size=9, font_name="F2")
            pdf.set_color(0, 0, 0)

            # Recommendation text – split into lines of ~85 chars
            rec_escaped = escape_pdf_text(rec)
            words = rec_escaped.split()
            lines = []
            current_line = ""
            for word in words:
                test = (current_line + " " + word).strip()
                if len(test) > 85:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test
            if current_line:
                lines.append(current_line)

            for j, line in enumerate(lines):
                if y < 80:
                    break
                pdf.add_line(85, y, line, font_size=9, font_name="F1")
                y -= 13
            y -= 12

    # Additional tips section
    y -= 10
    if y > 160:
        pdf.set_color(0.7, 0.7, 0.7)
        pdf.draw_line_segment(50, y, 545, y)
        pdf.set_color(0, 0, 0)
        y -= 20
        y = _draw_section_title(pdf, y, "Dicas Gerais de Estudo")

        tips = [
            "Estabeleca horarios fixos de estudo e respeite-os diariamente.",
            "Divida tarefas grandes em subtarefas menores e mais gerenciaveis.",
            "Revise o conteudo das aulas no mesmo dia para melhor retencao.",
            "Utilize tecnicas como Pomodoro (25min estudo + 5min pausa) para manter o foco.",
            "Priorize as disciplinas com menor taxa de conclusao e mais atrasos.",
        ]
        for tip in tips:
            if y < 80:
                break
            pdf.add_line(70, y, f"  {escape_pdf_text(tip)}", font_size=9, font_name="F1")
            y -= 15

    _add_footer(pdf, page_num, total_pages)

    # =====================================================================
    # Write PDF to disk
    # =====================================================================
    pdf_bytes = pdf.build()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        f.write(pdf_bytes)

    return str(out)


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_student_data(auth_token):
    """Fetch user profile, subjects, and tasks from Xano endpoints."""
    base_auth = get_env_url("URL_base_AUTH")
    base_subjects = get_env_url("URL_base_SUBJECTS")
    base_tasks = get_env_url("URL_base_ACADEMIC_TASKS")

    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. User data
    user_info = {}
    if base_auth:
        try:
            resp_user = requests.get(
                f"{base_auth}/auth/me", headers=headers, timeout=15
            )
            if resp_user.ok:
                user_info = resp_user.json()
        except requests.RequestException:
            pass

    # 2. Subjects
    subjects = []
    if base_subjects:
        try:
            resp_sub = requests.get(
                f"{base_subjects}/subjects", headers=headers, timeout=15
            )
            if resp_sub.ok:
                data = resp_sub.json()
                subjects = data if isinstance(data, list) else data.get("items", [])
        except requests.RequestException:
            pass

    # 3. Tasks
    tasks = []
    if base_tasks:
        try:
            resp_tasks = requests.get(
                f"{base_tasks}/academic_tasks", headers=headers, timeout=15
            )
            if resp_tasks.ok:
                data = resp_tasks.json()
                tasks = data if isinstance(data, list) else data.get("items", [])
        except requests.RequestException:
            pass

    return user_info, subjects, tasks


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_report(auth_token, output_path=None):
    """Main entry point: fetch data and generate PDF report."""
    if output_path is None:
        output_dir = Path(__file__).resolve().parent.parent / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"relatorio_desempenho_{timestamp}.pdf"

    user_info, subjects, tasks = fetch_student_data(auth_token)
    return generate_performance_pdf(user_info, subjects, tasks, output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python generate_performance_report.py <auth_token> [output_path]"}))
        sys.exit(1)

    token = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    caminho_gerado = generate_report(token, out_file)
    print(json.dumps({"success": True, "file_path": str(caminho_gerado)}))
