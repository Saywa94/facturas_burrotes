from flask import Flask
from .config import BaseConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app
