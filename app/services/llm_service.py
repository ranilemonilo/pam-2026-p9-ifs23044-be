import requests
from flask import current_app

def generate_recipes_with_ai(category: str, total: int) -> str:
    base_url  = current_app.config.get("LLM_BASE_URL", "https://delcom.org/api")
    llm_token = current_app.config.get("LLM_TOKEN", "")

    prompt = f"""Buatkan {total} resep masakan dengan kategori "{category}".
Jawab HANYA dalam format JSON array berikut, tanpa teks lain:
[
  {{
    "title": "Nama Resep",
    "ingredients": ["bahan 1", "bahan 2", "..."],
    "steps": ["Langkah 1...", "Langkah 2...", "..."],
    "category": "{category}",
    "difficulty": "Mudah/Sedang/Sulit",
    "duration_minutes": 30
  }}
]
Pastikan resep autentik, detail, dan dalam Bahasa Indonesia."""

    response = requests.post(
        f"{base_url}/llm/chat",
        json={
            "token": llm_token,
            "chat": prompt,
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.text[:300]}")

    data = response.json()

    # Cek format response dari delcom
    if isinstance(data, str):
        return data
    if "data" in data:
        return data["data"]
    if "response" in data:
        return data["response"]
    if "message" in data:
        return data["message"]
    if "content" in data:
        return data["content"]

    return str(data)