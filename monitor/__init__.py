"""Server Monitor Flask application factory."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect

from monitor.config import Config
from monitor.db import init_db

csrf = CSRFProtect()


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask app (localhost demo, no login)."""
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent.parent / "static"),
    )
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Ensure instance folder exists for SQLite
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    if not app.config.get("DATABASE"):
        app.config["DATABASE"] = str(Path(app.instance_path) / "monitor.db")

    csrf.init_app(app)
    init_db(app)

    from monitor.routes import bp

    app.register_blueprint(bp)

    @app.context_processor
    def inject_globals():
        return {"max_servers": app.config["MAX_SERVERS"]}

    return app
