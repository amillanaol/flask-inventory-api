import os
from flask import Flask
from app.config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.blueprints.auth.auth import auth
    from app.blueprints.dashboard.dashboard import dashboard
    from app.blueprints.products.products import products
    from app.blueprints.categories.categories import categories
    from app.blueprints.movements.movements import movements
    from app.blueprints.api.products import api_products
    from app.blueprints.api.categories import api_categories
    from app.blueprints.api.movements import api_movements

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(products)
    app.register_blueprint(categories)
    app.register_blueprint(movements)

    app.register_blueprint(api_products)
    app.register_blueprint(api_categories)
    app.register_blueprint(api_movements)

    csrf.exempt(api_products)
    csrf.exempt(api_categories)
    csrf.exempt(api_movements)

    from app.cli import register_commands

    register_commands(app)

    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Category, Product, Movement

        return {
            "db": db,
            "User": User,
            "Category": Category,
            "Product": Product,
            "Movement": Movement,
        }

    return app
