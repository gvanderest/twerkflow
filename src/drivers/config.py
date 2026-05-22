import os
from typing import Optional
from pydantic import BaseModel, SecretStr, model_validator


class GitHubIssueConfig(BaseModel):
    repo_name: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        if "token" not in data or data["token"] is None:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN environment variable not set")
            data["token"] = token
        return data


class AsanaConfig(BaseModel):
    project_gid: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        if "token" not in data or data["token"] is None:
            token = os.getenv("ASANA_PAT")
            if not token:
                raise ValueError("ASANA_PAT environment variable not set")
            data["token"] = token
        return data


class GitHubWikiConfig(BaseModel):
    wiki_url: str = ""


class NotionConfig(BaseModel):
    page_id: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        if "token" not in data or data["token"] is None:
            token = os.getenv("NOTION_API_KEY")
            if not token:
                raise ValueError("NOTION_API_KEY environment variable not set")
            data["token"] = token
        return data


class GitHubPRConfig(BaseModel):
    repo_name: str
    token: Optional[SecretStr] = None

    @model_validator(mode="before")
    @classmethod
    def populate_token(cls, data: dict) -> dict:
        if "token" not in data or data["token"] is None:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN environment variable not set")
            data["token"] = token
        return data
