from flask import Flask
from flask_cors import CORS
from .config import BaseConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://burrotesbolivia.org",
                    "https://www.burrotesbolivia.org",
                ]
            }
        },
    )

    return app
