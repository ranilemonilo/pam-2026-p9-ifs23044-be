import json
from ..extensions import SessionLocal
from ..models.recipe import Recipe
from ..models.request_log import RequestLog
from .llm_service import generate_from_llm
from ..utils.parser import parse_llm_response

def create_recipes(category: str, total: int):
    session = SessionLocal()
    try:
        prompt = f"""
Dalam format JSON, buat {total} resep masakan dengan kategori "{category}".
Format:
{{
    "recipes": [
        {{
            "title": "Nama Resep",
            "ingredients": ["bahan 1", "bahan 2"],
            "steps": ["Langkah 1", "Langkah 2"],
            "difficulty": "Mudah/Sedang/Sulit",
            "duration_minutes": 30
        }}
    ]
}}
Jawab HANYA dengan JSON, tanpa teks lain. Gunakan Bahasa Indonesia.
"""
        result = generate_from_llm(prompt)
        recipes = parse_llm_response(result)

        req_log = RequestLog(category=category)
        session.add(req_log)
        session.commit()

        saved = []
        for item in recipes:
            r = Recipe(
                title=item.get("title", ""),
                ingredients=json.dumps(item.get("ingredients", []), ensure_ascii=False),
                steps=json.dumps(item.get("steps", []), ensure_ascii=False),
                category=category,
                difficulty=item.get("difficulty", "Sedang"),
                duration_minutes=item.get("duration_minutes", 30),
                request_id=req_log.id,
            )
            session.add(r)
            saved.append(item)

        session.commit()
        return saved
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_recipes(page: int = 1, per_page: int = 10):
    session = SessionLocal()
    try:
        query = session.query(Recipe)
        total = query.count()
        data = (
            query
            .order_by(Recipe.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        result = [
            {
                "id": r.id,
                "title": r.title,
                "ingredients": json.loads(r.ingredients or "[]"),
                "steps": json.loads(r.steps or "[]"),
                "category": r.category,
                "difficulty": r.difficulty,
                "duration_minutes": r.duration_minutes,
                "created_at": r.created_at.isoformat(),
            }
            for r in data
        ]
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result,
        }
    finally:
        session.close()

def remove_recipe(recipe_id: int):
    session = SessionLocal()
    try:
        r = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not r:
            return False
        session.delete(r)
        session.commit()
        return True
    finally:
        session.close()