import json
from src.core.settings import Settings

def load_settings(path: str = "settings.json") -> Settings:
    with open(path, "r") as f:
        data = json.load(f)
    return Settings(**data)
