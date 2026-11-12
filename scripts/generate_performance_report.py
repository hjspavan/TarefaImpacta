"""
generate_performance_report.py

Gera um relatório de desempenho acadêmico do aluno em formato PDF,
consolidando dados de usuário, disciplinas e tarefas acadêmicas
a partir dos endpoints do Xano.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests


def get_env_url(variable_name):
    """Lê uma variável de URL a partir de secrets.toml, .env ou os.environ."""
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


def escape_pdf_text(text):
    """Escapa caracteres reservados em strings de texto PDF."""
    if text is None:
        return ""
    text_str = str(text)
    # Remove ou substitui caracteres fora do padrão ASCII para compatibilidade PDF básica
    cleaned = (
        text_str.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("õ", "o")
        .replace("ô", "o")
        .replace("ú", "u")
        .replace("ç", "c")
        .replace("Ã", "A")
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace("Ç", "C")
    )
    return cleaned


class SimplePdfBuilder:
    """Construtor nativo de arquivos PDF 1.4 sem dependências externas."""

    def __init__(self):
        self.lines = []

    def add_line(self, x, y, text, font_size=12, font_name="F1"):
        safe_text = escape_pdf_text(text)
        stream_cmd = (
            f"BT\n/{font_name} {font_size} Tf\n{x} {y} Td\n({safe_text}) Tj\nET"
        )
        self.lines.append(stream_cmd)

    def build(self):
        content_stream = "\n".join(self.lines).encode("latin-1", errors="replace")
        stream_length = len(content_stream)

        objects = []
        objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")
        objects.append(
            b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj"
        )
        objects.append(
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R "
            b"/Resources << /Font << "
            b"/F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
            b"/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> "
            b">> >> /MediaBox [0 0 595 842] /Contents 4 0 R >>\nendobj"
        )
        objects.append(
            f"4 0 obj\n<< /Length {stream_length} >>\nstream\n".encode(
                "latin-1"
            )
            + content_stream
            + b"\nendstream\nendobj"
        )

        pdf_bytes = bytearray(b"%PDF-1.4\n")
        offsets = []

        for obj in objects:
            offsets.append(len(pdf_bytes))
            pdf_bytes.extend(obj + b"\n")

        xref_pos = len(pdf_bytes)
        pdf_bytes.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
        pdf_bytes.extend(b"0000000000 65535 f \n")

        for offset in offsets:
            pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

        trailer = (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("latin-1")
        pdf_bytes.extend(trailer)

        return bytes(pdf_bytes)


def fetch_student_data(auth_token):
    """Busca perfil, disciplinas e tarefas do usuário a partir dos endpoints Xano."""
    base_auth = get_env_url("URL_base_AUTH")
    base_subjects = get_env_url("URL_base_SUBJECTS")
    base_tasks = get_env_url("URL_base_ACADEMIC_TASKS")

    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Obter dados do usuário
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

    # 2. Obter disciplinas
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

    # 3. Obter tarefas
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


def generate_performance_pdf(user_info, subjects, tasks, output_path):
    """Compila os dados e grava o arquivo PDF de desempenho."""
    pdf = SimplePdfBuilder()

    # Cabeçalho
    pdf.add_line(50, 790, "EduTrack AI - Relatorio de Desempenho Academico", font_size=16, font_name="F2")
    data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.add_line(50, 770, f"Data de Emissao: {data_emissao}", font_size=10, font_name="F1")
    pdf.add_line(50, 755, "-------------------------------------------------------------------------------------------------", font_size=10, font_name="F1")

    # Identificação do Aluno
    nome_aluno = user_info.get("name") or user_info.get("nome") or "Aluno Nao Identificado"
    email_aluno = user_info.get("email") or "Nao informado"
    user_id = user_info.get("id") or "N/A"

    pdf.add_line(50, 735, "1. DADOS DO ESTUDANTE", font_size=12, font_name="F2")
    pdf.add_line(50, 718, f"Nome: {nome_aluno}", font_size=11, font_name="F1")
    pdf.add_line(50, 703, f"E-mail: {email_aluno}    |    ID Estudante: {user_id}", font_size=11, font_name="F1")
    pdf.add_line(50, 688, "-------------------------------------------------------------------------------------------------", font_size=10, font_name="F1")

    # Resumo Geral de Desempenho
    total_disciplinas = len(subjects)
    total_tarefas = len(tasks)
    tarefas_concluidas = sum(
        1
        for t in tasks
        if isinstance(t, dict)
        and str(t.get("status", "")).strip().lower()
        in ("concluida", "concluída", "completed")
    )
    tarefas_pendentes = total_tarefas - tarefas_concluidas
    progresso_geral = (
        (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0.0
    )

    pdf.add_line(50, 668, "2. RESUMO GERAL DE DESEMPENHO", font_size=12, font_name="F2")
    pdf.add_line(50, 650, f"Total de Disciplinas Cursadas: {total_disciplinas}", font_size=11, font_name="F1")
    pdf.add_line(50, 635, f"Total de Tarefas Registradas: {total_tarefas}", font_size=11, font_name="F1")
    pdf.add_line(50, 620, f"Tarefas Concluidas: {tarefas_concluidas}    |    Tarefas Pendentes: {tarefas_pendentes}", font_size=11, font_name="F1")
    pdf.add_line(50, 605, f"Taxa de Conclusao Geral: {progresso_geral:.1f}%", font_size=11, font_name="F2")
    pdf.add_line(50, 590, "-------------------------------------------------------------------------------------------------", font_size=10, font_name="F1")

    # Detalhamento por Disciplina
    pdf.add_line(50, 570, "3. DETALHAMENTO DAS DISCIPLINAS E TAREFAS", font_size=12, font_name="F2")

    current_y = 550
    if not subjects:
        pdf.add_line(50, current_y, "Nenhuma disciplina cadastrada ate o momento.", font_size=10, font_name="F1")
    else:
        for idx, subj in enumerate(subjects, start=1):
            if current_y < 80:
                break
            nome_disc = subj.get("name") or "Sem Nome"
            prof_disc = subj.get("teacher") or "Nao informado"
            horas_disc = subj.get("hours") or 0
            subj_id = subj.get("id")

            tarefas_disc = [t for t in tasks if isinstance(t, dict) and t.get("subject_id") == subj_id]
            total_td = len(tarefas_disc)
            concl_td = sum(
                1
                for t in tarefas_disc
                if str(t.get("status", "")).strip().lower()
                in ("concluida", "concluída", "completed")
            )
            prog_disc = (concl_td / total_td * 100) if total_td > 0 else 0.0

            pdf.add_line(50, current_y, f"{idx}. {nome_disc} ({horas_disc}h) - Docente: {prof_disc}", font_size=11, font_name="F2")
            current_y -= 16
            pdf.add_line(65, current_y, f"Progresso: {prog_disc:.1f}% ({concl_td}/{total_td} tarefas concluidas)", font_size=10, font_name="F1")
            current_y -= 22

    # Rodapé
    pdf.add_line(50, 40, "Documento gerado automaticamente pelo EduTrack AI - Sistema de Gestao Academica", font_size=8, font_name="F1")

    pdf_bytes = pdf.build()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        f.write(pdf_bytes)

    return str(out)


def generate_report(auth_token, output_path=None):
    """Função principal para consumo externo: compila dados e gera PDF."""
    if output_path is None:
        output_dir = Path(__file__).resolve().parent.parent / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"relatorio_desempenho_{timestamp}.pdf"

    user_info, subjects, tasks = fetch_student_data(auth_token)
    return generate_performance_pdf(user_info, subjects, tasks, output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python generate_performance_report.py <auth_token> [output_path]"}))
        sys.exit(1)

    token = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    caminho_gerado = generate_report(token, out_file)
    print(json.dumps({"success": True, "file_path": str(caminho_gerado)}))
