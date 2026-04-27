from flask import Flask
from .utils.config import Config
from .utils.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes.recipe_routes import recipe_bp
    app.register_blueprint(recipe_bp)

    # Auto-create tables
    with app.app_context():
        db.create_all()

    return app