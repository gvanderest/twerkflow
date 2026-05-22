"""Defines application settings and configuration models."""

import os
from typing import Any, Dict, Union
from pydantic import BaseModel, Field, field_validator


class DriverConfig(BaseModel):
    """Configuration for a specific driver."""

    type: str
    params: Dict[str, Any] = Field(default_factory=dict)


class Settings(BaseModel):
    """Main application settings model."""

    context: str
    drivers: Dict[str, Union[str, DriverConfig]]
    poll_interval_seconds: int = 30  # Default value

    @field_validator("drivers")
    @classmethod
    def validate_drivers(cls, v: Dict[str, Union[str, DriverConfig]]) -> Dict[str, Union[str, DriverConfig]]:
        """Validates that all required drivers are present in the settings."""
        # Basic check: Ensure we have required drivers
        required = ["task_service", "doc_service", "pr_service"]
        for r in required:
            if r not in v:
                raise ValueError(f"Missing required driver: {r}")
        return v

    def get_driver_config(self, driver_key: str) -> DriverConfig:
        """Retrieves configuration for a specific driver by key."""
        config = self.drivers.get(driver_key)
        if config is None:
            raise ValueError(f"Driver {driver_key} not configured")
        if isinstance(config, str):
            return DriverConfig(type=config)
        return config


def validate_environment():
    """Validates that all required environment variables are present."""
    required_vars = ["GITHUB_TOKEN"]  # Expand as we add drivers
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
