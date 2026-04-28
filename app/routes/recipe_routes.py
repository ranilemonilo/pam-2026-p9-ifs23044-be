from functools import wraps
from flask import Blueprint, request, jsonify
from ..config import Config
from ..services.recipe_service import create_recipes, get_all_recipes, remove_recipe

recipe_bp = Blueprint("recipe", __name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-Admin-Token", "")
        expected = f"{Config.ADMIN_USERNAME}:{Config.ADMIN_PASSWORD}"
        if token != expected:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@recipe_bp.route("/", methods=["GET"])
def index():
    return "API Resep Masakan dengan AI - PAM 2026"

@recipe_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        return jsonify({"token": f"{username}:{password}", "message": "Login berhasil"}), 200
    return jsonify({"error": "Username atau password salah"}), 401

@recipe_bp.route("/recipes/generate", methods=["POST"])
@require_auth
def generate():
    data = request.get_json()
    category = data.get("category", "")
    total = data.get("total")
    if not category:
        return jsonify({"error": "Category is required"}), 400
    if not total:
        return jsonify({"error": "Total is required"}), 400
    if total <= 0:
        return jsonify({"error": "Total harus lebih dari 0"}), 400
    if total > 10:
        return jsonify({"error": "Total maksimal 10"}), 400
    try:
        result = create_recipes(category, total)
        return jsonify({"category": category, "total": len(result), "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recipe_bp.route("/recipes", methods=["GET"])
@require_auth
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    return jsonify(get_all_recipes(page=page, per_page=per_page))

@recipe_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@require_auth
def delete(recipe_id):
    deleted = remove_recipe(recipe_id)
    if deleted:
        return jsonify({"message": f"Resep {recipe_id} berhasil dihapus"}), 200
    return jsonify({"error": "Resep tidak ditemukan"}), 404