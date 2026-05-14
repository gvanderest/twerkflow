# Twerk

Twerk is an intelligent automation system designed to streamline project management by orchestrating workflows across various tools like Asana, Notion, and GitHub. It acts as a central hub, monitoring events, executing predefined workflows, and managing the continuous loop of project tasks.

## Core Concept: Event-Driven Orchestration

At its heart, Twerk operates on an event-driven model. It listens for specific triggers from integrated services (Asana, Notion, GitHub) and, upon detection, initiates pre-defined workflows. These workflows can involve taking inputs, processing data, running complex logic, and submitting outputs back to the integrated services or other destinations.

## Architecture

Twerk is designed with modularity in mind, separating core functionality from specific user configurations:

*   **`twerk-lib`**: This component will house the core library, APIs, SDK, and the fundamental structure for defining and executing workflows. It provides the engine and the building blocks.
*   **User Configuration Repositories**: Individual project repositories will contain the specific workflow definitions, triggers, sources, and outputs tailored to a particular project. This allows for easy customization and management of different project pipelines.

## Key Features & Goals

*   **Automated Event Monitoring**: Watch for critical events from Asana, Notion, and GitHub.
*   **Code-Defined Workflows**: Explicitly define complex workflows in code for clarity and maintainability.
*   **Continuous Loop Processing**: Seamlessly handle a sequence of tasks, from input to output, in an ongoing cycle.
*   **Flexible Configuration**: Define triggers, workflows, data sources, and outputs with a structured approach.
*   **Simple Execution**: Start the Twerk server with a single command to initiate configured workflows.

## Example Workflow Implementations

The power of Twerk lies in its ability to automate recurring project management tasks. Here are some examples of primary flows that Twerk can manage:

*   **Design Ticket**: Provide context to Twerk to research a ticket using multiple personas, compile findings, and generate a design document in Notion.
*   **Notion Feedback Integration**: Automatically re-review and update a Notion design doc when feedback is received on an associated Asana ticket.
*   **Execute Project**: Convert a design doc into an Asana task with subtasks, automate execution, and update task status.
*   **PR Babysitting**: Ensure the quality of a Pull Request by verifying unit test coverage, formatting, type checks, and CI/CD pipeline status.
*   **PR Feedback Loop**: Process comments and reviews on a PR, use the context to improve the code, re-run verifications, and return to PR Babysitting.
*   **PR Merge (Manual to Start)**: Once all verifications pass and quality checks are met, the PR can be manually merged.
*   **CI/CD Deployment**: Automate direct deployment through CI/CD pipelines, with verifications at DEV, STAGING, and PROD environments.
*   **Bugfix Ticket**: Handle bug fix workflows, potentially skipping some high-level steps but following a similar verification and execution path.

## Ultimate Goal: Self-Development

The long-term vision for Twerk is to achieve a state of self-development. By leveraging its own capabilities to manage its codebase, Twerk aims to eventually delete its `PROJECT.md` file, signifying a mature system capable of orchestrating its own evolution using external tools as its primary interface.

## Getting Started

The initial phase of Twerk development involves researching existing frameworks that can provide a robust foundation for defining and executing complex workflows. This research will guide the selection of technologies that best fit our needs for flexibility, extensibility, and ease of use.
