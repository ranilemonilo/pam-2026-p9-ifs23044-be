import json
from app.utils.extensions import db
from app.models.recipe import Recipe
from app.services.llm_service import generate_recipes_with_ai
from app.utils.parser import parse_recipes_from_text


def get_recipes(page: int, per_page: int) -> dict:
    pagination = (
        Recipe.query.order_by(Recipe.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return {
        "data": [r.to_dict() for r in pagination.items],
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
    }


def generate_and_save_recipes(category: str, total: int) -> dict:
    raw_text = generate_recipes_with_ai(category, total)
    recipes_data = parse_recipes_from_text(raw_text)

    if not recipes_data:
        raise ValueError("AI tidak menghasilkan resep yang valid.")

    saved = []
    for item in recipes_data:
        recipe = Recipe(
            title=item.get("title", "Tanpa Judul"),
            ingredients=json.dumps(item.get("ingredients", []), ensure_ascii=False),
            steps=json.dumps(item.get("steps", []), ensure_ascii=False),
            category=item.get("category", category),
            difficulty=item.get("difficulty", "Sedang"),
            duration_minutes=item.get("duration_minutes", 30),
        )
        db.session.add(recipe)
        saved.append(recipe)

    db.session.commit()

    return {
        "data": [r.to_dict() for r in saved],
        "category": category,
        "total": len(saved),
    }


def delete_recipe(recipe_id: int) -> bool:
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return False
    db.session.delete(recipe)
    db.session.commit()
    return True