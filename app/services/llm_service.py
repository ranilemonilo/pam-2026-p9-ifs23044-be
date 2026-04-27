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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {llm_token}",
    }

    payload = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        f"{base_url}/v1/messages",
        json=payload,
        headers=headers,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.text[:300]}")

    data = response.json()

    # Format Anthropic: data["content"][0]["text"]
    if "content" in data:
        return data["content"][0]["text"]
    # Format OpenAI: data["choices"][0]["message"]["content"]
    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    raise Exception(f"Format response tidak dikenali: {str(data)[:200]}")