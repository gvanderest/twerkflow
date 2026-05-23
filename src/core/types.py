"""Shared type definitions."""

from typing import TypedDict, List
from src.drivers.base import TaskService
from src.services.command_runner import CommandRunner


class WorkflowConfig(TypedDict):
    """Configuration for workflow nodes."""

    task_service: TaskService
    command_runner: CommandRunner
    ticket_id: str
    tags: List[str]
