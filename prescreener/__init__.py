from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("prescreener.config.Config")

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["TEMP_FOLDER"]).mkdir(parents=True, exist_ok=True)

    from prescreener.logging_config import setup_logging
    setup_logging(app)

    db.init_app(app)

    from prescreener.routes.dashboard import bp as dashboard_bp
    from prescreener.routes.analyze import bp as analyze_bp
    from prescreener.routes.results import bp as results_bp
    from prescreener.routes.api import bp as api_bp
    from prescreener.routes.costs import bp as costs_bp
    from prescreener.routes.logs import bp as logs_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(costs_bp)
    app.register_blueprint(logs_bp)

    with app.app_context():
        from prescreener import models  # noqa: F401
        db.create_all()

    return app
