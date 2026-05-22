"""Core configuration loading utilities."""

import json
from src.core.settings import Settings, validate_environment


def load_settings(path: str = "settings.json") -> Settings:
    """Loads settings from a JSON file and returns a validated Settings object.

    Args:
        path: Path to the JSON settings file.

    Returns:
        A validated Settings object.
    """
    # 1. Validate Env Vars
    validate_environment()

    # 2. Load and Validate JSON
    with open(path, "r") as f:
        data = json.load(f)

    return Settings(**data)
