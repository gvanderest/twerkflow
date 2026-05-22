"""Configuration models for various drivers."""

import os
from typing import Optional

from pydantic import BaseModel, SecretStr, model_validator


class GitHubIssueConfig(BaseModel):
    """Configuration for GitHub issues."""

    repo_name: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        """Populates token from environment variable if missing."""
        if "token" not in data or data["token"] is None:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN environment variable not set")
            data["token"] = token
        return data


class AsanaConfig(BaseModel):
    """Configuration for Asana."""

    project_gid: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        """Populates token from environment variable if missing."""
        if "token" not in data or data["token"] is None:
            token = os.getenv("ASANA_PAT")
            if not token:
                raise ValueError("ASANA_PAT environment variable not set")
            data["token"] = token
        return data


class GitHubWikiConfig(BaseModel):
    """Configuration for GitHub wiki."""

    wiki_url: str = ""


class NotionConfig(BaseModel):
    """Configuration for Notion."""

    page_id: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        """Populates token from environment variable if missing."""
        if "token" not in data or data["token"] is None:
            token = os.getenv("NOTION_API_KEY")
            if not token:
                raise ValueError("NOTION_API_KEY environment variable not set")
            data["token"] = token
        return data


class GitHubPRConfig(BaseModel):
    """Configuration for GitHub Pull Requests."""

    repo_name: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        """Populates token from environment variable if missing."""
        if "token" not in data or data["token"] is None:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN environment variable not set")
            data["token"] = token
        return data
