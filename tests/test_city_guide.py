import os
from pathlib import Path

import pytest

from vacation_planner.services.city_guide import CityGuideError, load_api_key


def test_loads_key_from_environment(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    assert load_api_key("env:GEMINI_API_KEY") == "test-key"


def test_rejects_key_file_outside_private_folders(tmp_path):
    key_file = tmp_path / "key.txt"
    key_file.write_text("test-key")
    with pytest.raises(CityGuideError, match="Transportation"):
        load_api_key(str(key_file))
