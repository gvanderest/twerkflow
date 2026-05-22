# Twerkflow Configuration

Twerkflow uses a `settings.json` file for configuration.

## Table of Contents
- [Getting Started](#getting-started)
- [Configuration Structure](#configuration-structure)
- [Drivers](#drivers)

## Getting Started

1. Copy the example settings file:
   ```bash
   cp example-settings.json settings.json
   ```
2. Modify `settings.json` according to your needs. `settings.json` is ignored by git to protect your configuration.

## Configuration Structure

| Key | Type | Description |
| :--- | :--- | :--- |
| `context` | string | The environment context (e.g., `twerkflow_dev`). |
| `poll_interval_seconds` | integer | Interval in seconds for polling GitHub issues. |
| `drivers` | object | Configuration for various services. |

## Drivers

- `task_service` (object): Configures the task management service (e.g., GitHub Issues).
    - `type` (string): Driver type (e.g., `github_issues`).
    - `params` (object): Configuration parameters (e.g., `repo_name`).
- `doc_service` (string): Documentation service (e.g., `github_wiki`).
- `pr_service` (string): PR service (e.g., `github_pr`).
