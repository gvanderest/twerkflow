# Twerkflow

Twerkflow is a LangGraph-based framework for end-to-end software development lifecycles that prioritizes human-in-the-loop (HILO) control, explicit guardrails, and agentic productivity.

## Tenets

*   **Agents in the Middle**: Agents (using Claude Code) execute the dynamic "middle" of workflows (thinking, design, coding). Deterministic, programmatic gates handle guardrails and requirements.
*   **Human in the Loop (HILO)**: All critical workflow stages require human approval via explicit sentinel commands. The system pauses at predefined checkpoints to await human intervention.
*   **Humans Always Take Over**: Everything the agent does is something a human can do (design, write code, make PRs, merge, deploy). The system is a collaborator, not a black-box autocrat; humans can always intervene or take over.
*   **Opt-in Only**: Automations are triggered only by explicit opt-in (e.g., an `twerkflow` Asana tag). The system will never act on untagged tasks or PRs.
*   **Watermark Comments**: Every interaction (comment, commit, PR update) authored by Twerkflow is watermarked (e.g., *--- Authored by Twerkflow*).
*   **Credential Security**: No secrets are stored in the codebase. All credentials are managed via `.env` files and environment variables, which are strictly gitignored.
*   **Ticket as Database**: The Asana/GitHub ticket description is the primary source of truth for durable state and audit history, utilizing a JSON structure `<twerkflow-state>...</twerkflow-state>` for persistence.

## Architecture

Twerkflow is built entirely using LangGraph. The lifecycle is represented as a directed graph where nodes are either:
1.  **Agentic Nodes**: Execute tasks using `claude-code` (via a non-interactive Python subprocess wrapper).
2.  **Programmatic Gate Nodes**: Perform deterministic checks (e.g., verifying CI status, parsing requirements).

### State Management
*   **Local Active Store**: An SQLite/JSON store manages active graph execution state.
*   **Durable Checkpoint**: State is synced to the ticket description at every major HILO checkpoint.
*   **Recovery**: If the system reboots, it rehydrates its local state from the ticket description.

### Interaction & HILO
*   **Sentinels**: Transitions (e.g., moving from Design to Code) are triggered only by explicit sentinel values in comments (e.g., `[TWERKFLOW_CMD: <ID> APPROVED_FOR_CODE]`).
*   **Self-Ignorance**: The system parses its own comments by a unique watermark/ID to ensure it does not trigger its own logic.

### Execution
*   The system acts as a collaborator using your credentials.
*   It utilizes headless `claude-code` with managed I/O, timeouts, and live observability tailing.

## Getting Started

1.  **Configure**: Set up your `.env` with the necessary API tokens (Asana, GitHub, etc.).
2.  **Tag**: Apply the `twerkflow` tag to an Asana task to opt-in to automation.
3.  **Monitor**: Interact via ticket comments using the required sentinel values when the system pauses for HILO approval.
