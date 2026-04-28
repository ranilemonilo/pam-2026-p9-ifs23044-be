from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.recipe_routes import recipe_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Register blueprint
    app.register_blueprint(recipe_bp)

    return app