# Twerkflow Implementation Roadmap

This roadmap defines the work required to enable Twerkflow to be implemented and operated end-to-end using GitHub Issues and Wikis as the primary interface and source of truth, aligning with the tenets established in `README.md`.

## Goal
Enable Twerkflow to manage the software development lifecycle by reading/writing to GitHub Issues for task management/state, and utilizing GitHub Wikis for project-wide documentation and state tracking.

---

## Phase 1: Ticket-as-Database Integration (GitHub Focus)

The primary goal is to shift from the current (conceptual) Asana/SQLite implementation to a robust GitHub-native model.

- [ ] **State Persistence Module**: Refactor state management to read/write the `<twerkflow-state>...</twerkflow-state>` JSON block directly into GitHub Issue descriptions.
    - *Note*: Initially, we will implement basic read/write persistence for speed, prioritizing execution over complex concurrency handling.
    - *Note*: The JSON state block will be versioned from the start to allow for the future addition of optimistic locking (e.g., version/hash checking) without breaking existing state blobs.
- [ ] **GitHub Issue Watcher**: Implement a mechanism to listen for activity (comments/edits) on tagged GitHub Issues.
- [ ] **Rehydration Logic**: Ensure that the LangGraph state can be perfectly reconstructed from the serialized state block in a GitHub Issue description upon startup or recovery.

## Phase 2: HILO Mechanisms & Sentinels

Enable human control over agentic workflows.

- [ ] **Sentinel Parsing Engine**: Implement a robust parser to detect and validate Twerkflow sentinel commands (e.g., `[TWERKFLOW_CMD: <ID> APPROVED_FOR_CODE]`) within GitHub Issue comments.
- [ ] **Checkpoint/Pause Controller**: Integrate LangGraph breakpoints that halt execution and prompt for human approval via an Issue comment.
- [ ] **Human-in-the-Loop Feedback Loop**: Create an interface (comment-based) for the agent to report progress and request specific approvals from the human.

## Phase 3: Agentic Execution Framework

Integrating with `claude-code`.

- [ ] **Subprocess Wrapper for Claude Code**: Ensure the non-interactive Python subprocess wrapper correctly handles I/O, timeouts, and error reporting back to the GitHub Issue.
- [ ] **Context Injection**: Ensure the agent receives the relevant context from the GitHub Issue (e.g., task requirements, current state, previous feedback).

## Phase 4: Observability, Security & Audit

- [ ] **Watermarking Service**: Ensure every action taken by Twerkflow on GitHub (comment, commit, PR update) is automatically appended with the required *--- Authored by Twerkflow* signature.
- [ ] **Credential Security Audit**: Validate that the GitHub Action environment provides a secure way to manage necessary tokens (GitHub PAT, API keys) without embedding them in the repo.
- [ ] **Wiki Documentation Sync**: Implement functionality to automatically update the project Wiki to reflect state changes, milestones, or finalized technical specs for documentation persistence.

---

## Technical Notes
- **Source of Truth**: The GitHub Issue comment stream is the primary audit log.
- **State Storage**: The `<twerkflow-state>` block in the Issue description is the primary durable checkpoint.
- **Communication**: All agent<->human interaction happens via comments on the tracked Issue.
