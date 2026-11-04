
"""
calculate_progress.py

Calcula a porcentagem de progresso de uma disciplina com base
nas tarefas acadêmicas concluídas, consumindo o endpoint
GET /academic_tasks do Xano.
"""

import json
import os
import sys
from pathlib import Path

import requests


def get_env_url(variable_name):
    """Lê uma variável de URL do arquivo .env na raiz do projeto."""

    env_path = Path(__file__).resolve().parent.parent / ".env"

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)

                    if key.strip() == variable_name:
                        return value.strip().strip('"').strip("'").rstrip("/")

    return os.environ.get(variable_name, "").rstrip("/")


def calculate_progress(subject_id, auth_token):
    """
    Calcula a porcentagem de progresso de uma disciplina.

    Consulta o endpoint GET /academic_tasks?subject_id=<id>
    e retorna um dicionário com a chave percentage.
    """

    base_url = get_env_url("URL_base_ACADEMIC_TASKS")

    if not base_url:
        return {"percentage": 0}

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    params = {
        "subject_id": subject_id
    }

    try:
        response = requests.get(
            f"{base_url}/academic_tasks",
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError):
        return {"percentage": 0}

    # Verifica o formato da resposta do Xano
    if isinstance(data, list):
        tasks = data

    elif isinstance(data, dict):
        tasks = data.get("items", [])

    else:
        tasks = []

    total = len(tasks)

    # Evita divisão por zero
    if total == 0:
        return {"percentage": 0}

    # Conta as tarefas concluídas
    completed = sum(
        1
        for task in tasks
        if isinstance(task, dict)
        and str(task.get("status", "")).strip().lower() in (
            "concluída",
            "concluida",
            "completed"
        )
    )

    # Calcula o percentual de progresso
    percentage = (completed / total) * 100

    return {
        "percentage": percentage
    }


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            json.dumps({
                "error": (
                    "Usage: python calculate_progress.py "
                    "<subject_id> <auth_token>"
                )
            })
        )
        sys.exit(1)

    subject_id = sys.argv[1]
    auth_token = sys.argv[2]

    result = calculate_progress(subject_id, auth_token)

    print(json.dumps(result))
