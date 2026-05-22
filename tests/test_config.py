import pytest
import os
from src.core.config_loader import load_settings


def test_load_settings_success(tmp_path):
    # Create temp settings.json
    d = tmp_path / "settings.json"
    d.write_text(
        '{"context": "test", "drivers": {"task_service": "asana", "doc_service": "notion", "pr_service": "github_pr"}}'
    )

    os.environ["GITHUB_TOKEN"] = "fake"
    settings = load_settings(str(d))
    assert settings.context == "test"
    assert settings.get_driver_config("task_service").type == "asana"


def test_settings_missing_driver():
    from src.core.settings import Settings

    with pytest.raises(ValueError, match="Missing required driver"):
        Settings(context="test", drivers={"task_service": "github_issues"})


def test_settings_invalid_config():
    from src.core.settings import Settings

    with pytest.raises(ValueError, match="Driver pr_service_missing not configured"):
        s = Settings(
            context="test",
            drivers={
                "task_service": "github_issues",
                "doc_service": "notion",
                "pr_service": "github_pr",
            },
        )
        s.get_driver_config("pr_service_missing")
