"""Vacation Planner Flask application package."""

from flask import Flask


def create_app() -> Flask:
    """Create the local-only Vacation Planner web application."""
    app = Flask(__name__)

    from .routes import planner

    app.register_blueprint(planner)
    return app
