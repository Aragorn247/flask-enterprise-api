from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.routes import api_bp
from app.errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # Registra Flask-Migrate con la App y la BD

    app.register_blueprint(api_bp)
    register_error_handlers(app)

    return app