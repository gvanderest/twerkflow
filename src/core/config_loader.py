import json
from src.core.settings import Settings, validate_environment


def load_settings(path: str = "settings.json") -> Settings:
    # 1. Validate Env Vars
    validate_environment()

    # 2. Load and Validate JSON
    with open(path, "r") as f:
        data = json.load(f)

    return Settings(**data)
