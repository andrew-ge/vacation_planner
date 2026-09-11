"""HTTP routes for the planner interface and City Guide."""

from flask import Blueprint, jsonify, render_template, request

from .services.city_guide import DEFAULT_MODEL, CityGuideError, ask_city_guide

planner = Blueprint("planner", __name__)


@planner.get("/")
def index():
    return render_template("index.html", default_model=DEFAULT_MODEL)


@planner.post("/api/city-guide")
def city_guide():
    data = request.get_json(silent=True) or {}
    if data.get("provider") != "gemini":
        return jsonify(error="Only Google Gemini is available right now."), 400

    try:
        guide = ask_city_guide(
            city=str(data.get("city", "")).strip(),
            places=str(data.get("places", "")).strip(),
            style=str(data.get("style", "")).strip(),
            model=str(data.get("model", "")).strip() or DEFAULT_MODEL,
            key_location=str(data.get("key_location", "")).strip(),
        )
    except CityGuideError as error:
        return jsonify(error=str(error)), error.status_code

    return jsonify(guide=guide)
