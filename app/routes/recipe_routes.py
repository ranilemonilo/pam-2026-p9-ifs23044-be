from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from app.services.recipe_service import get_recipes, generate_and_save_recipes, delete_recipe

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")


# ─── Simple Token Auth ────────────────────────────────────────────────────────

def require_auth(f):
    """Decorator: periksa Authorization header (Basic atau Bearer token)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            # Basic auth
            if (
                auth.username == current_app.config["ADMIN_USERNAME"]
                and auth.password == current_app.config["ADMIN_PASSWORD"]
            ):
                return f(*args, **kwargs)
        # Bearer token (token = "username:password" base64 simple)
        token = request.headers.get("X-Admin-Token", "")
        expected = (
            current_app.config["ADMIN_USERNAME"]
            + ":"
            + current_app.config["ADMIN_PASSWORD"]
        )
        if token == expected:
            return f(*args, **kwargs)

        return jsonify({"error": "Unauthorized. Login required."}), 401

    return decorated


# ─── Login ────────────────────────────────────────────────────────────────────

@recipe_bp.route("/login", methods=["POST"])
def login():
    """
    POST /recipes/login
    Body: { "username": "admin", "password": "admin123" }
    Returns token jika berhasil.
    """
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if (
        username == current_app.config["ADMIN_USERNAME"]
        and password == current_app.config["ADMIN_PASSWORD"]
    ):
        token = f"{username}:{password}"
        return jsonify({"token": token, "message": "Login berhasil"}), 200

    return jsonify({"error": "Username atau password salah"}), 401


# ─── GET /recipes ─────────────────────────────────────────────────────────────

@recipe_bp.route("", methods=["GET"])
@require_auth
def list_recipes():
    """
    GET /recipes?page=1&per_page=10
    Daftar resep tersimpan (paginasi).
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    result = get_recipes(page, per_page)
    return jsonify(result), 200


# ─── POST /recipes/generate ───────────────────────────────────────────────────

@recipe_bp.route("/generate", methods=["POST"])
@require_auth
def generate():
    """
    POST /recipes/generate
    Body: { "category": "masakan Padang", "total": 3 }
    Generate resep baru dengan AI lalu simpan ke DB.
    """
    data = request.get_json()
    category = data.get("category", "")
    total = data.get("total", 3)

    if not category:
        return jsonify({"error": "Field 'category' wajib diisi"}), 400
    if total < 1 or total > 10:
        return jsonify({"error": "Total harus antara 1-10"}), 400

    try:
        result = generate_and_save_recipes(category, total)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": f"Gagal generate: {str(e)}"}), 500


# ─── DELETE /recipes/<id> ─────────────────────────────────────────────────────

@recipe_bp.route("/<int:recipe_id>", methods=["DELETE"])
@require_auth
def remove_recipe(recipe_id):
    """DELETE /recipes/<id> — hapus resep."""
    deleted = delete_recipe(recipe_id)
    if deleted:
        return jsonify({"message": f"Resep {recipe_id} berhasil dihapus"}), 200
    return jsonify({"error": "Resep tidak ditemukan"}), 404