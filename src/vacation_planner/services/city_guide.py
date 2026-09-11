"""Gemini-backed City Guide service.

This module is deliberately server-side so API keys never reach browser code.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_MODEL = "gemini-3.8-flash"
APP_ROOT = Path(__file__).resolve().parents[3]
PRIVATE_KEY_FOLDERS = (APP_ROOT / "Transportation", APP_ROOT / "Hotel")


class CityGuideError(Exception):
    """A user-safe City Guide error with an HTTP status code."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def load_api_key(location: str) -> str:
    """Read an API key from an environment variable or approved private key file."""
    if location.startswith("env:"):
        variable = location.removeprefix("env:").strip()
        if not variable or not variable.replace("_", "").isalnum():
            raise CityGuideError("Use an environment variable such as env:GEMINI_API_KEY.")
        key = os.environ.get(variable, "").strip()
        if not key:
            raise CityGuideError(f"The environment variable {variable} is not set.")
        return key

    if not location:
        raise CityGuideError("Provide a key location, preferably env:GEMINI_API_KEY.")

    key_path = Path(location).expanduser().resolve()
    if not any(key_path.is_relative_to(folder.resolve()) for folder in PRIVATE_KEY_FOLDERS):
        raise CityGuideError("For safety, key files must be inside Transportation/ or Hotel/.")
    try:
        return key_path.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise CityGuideError("The key file could not be read.") from error


def city_guide_prompt(city: str, places: str, style: str) -> str:
    return f"""You are City Guide, a careful local-first trip planner. Plan a compact
walking/transit-friendly day in {city}. User's travel style: {style or 'balanced sightseeing and good food'}.
Places the user already wants: {places or 'none; propose suitable places'}.

Return ONLY valid JSON with a \"route\" array and a \"food\" array. Each item must have
name, area, why, and source_note. Route items must also have an order field. Favor independent
businesses and places recommended by local newspapers, resident-written guides, neighborhood
organizations, chefs, or long-running community forums. Explicitly avoid TikTok/YouTube influencer
lists, generic SEO lists, viral queues, tourist-only experiences, and businesses with no credible
local signal. Do not invent sources or claim you verified a recommendation; say \"needs local
verification\" in source_note when unsure. Include 3–5 route stops and 3–5 food options."""


def ask_city_guide(*, city: str, places: str, style: str, model: str, key_location: str) -> dict:
    """Ask Gemini for structured local-first sightseeing and food suggestions."""
    if not city:
        raise CityGuideError("Choose a city before asking City Guide.")

    key = load_api_key(key_location)
    payload = {
        "contents": [{"parts": [{"text": city_guide_prompt(city, places, style)}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/"
    endpoint += f"{quote(model, safe='')}:generateContent"
    api_request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urlopen(api_request, timeout=45) as response:
            body = json.load(response)
        text = "".join(part.get("text", "") for part in body["candidates"][0]["content"]["parts"])
        return json.loads(text)
    except HTTPError as error:
        raise CityGuideError(f"Gemini rejected the request (HTTP {error.code}). Check the model and key.", 502) from error
    except (URLError, TimeoutError) as error:
        raise CityGuideError("Could not reach Gemini. Check your internet connection.", 502) from error
    except (KeyError, IndexError, json.JSONDecodeError) as error:
        raise CityGuideError("Gemini returned an unexpected response. Try again.", 502) from error
