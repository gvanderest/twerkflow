import pytest
import os
from src.core.config_loader import load_settings

def test_load_settings_success(tmp_path):
    # Create temp settings.json
    d = tmp_path / "settings.json"
    d.write_text('{"context": "test", "drivers": {"task_service": "asana", "doc_service": "notion", "pr_service": "github_pr"}}')
    
    os.environ["GITHUB_TOKEN"] = "fake"
    settings = load_settings(str(d))
    assert settings.context == "test"
    assert settings.get_driver_config("task_service").type == "asana"

def test_load_settings_missing_env():
    if "GITHUB_TOKEN" in os.environ:
        del os.environ["GITHUB_TOKEN"]
    with pytest.raises(EnvironmentError):
        load_settings()
