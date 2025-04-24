from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
