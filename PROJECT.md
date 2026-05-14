# Twerk Project Definition

## Preamble and Project Context

Welcome to the Twerk project. Twerk is an ambitious initiative to create an intelligent, automated system for project management and workflow orchestration. Its core purpose is to integrate with common development and project management tools such as Asana, Notion, and GitHub, enabling the automation of complex, multi-step processes.

This project is structured into two primary components:

1.  **`twerk-lib`**: The core library that will provide the foundational APIs, SDK, and the execution engine for defining and running workflows. This is where the universal logic resides.
2.  **User Configuration Repositories**: These will be separate repositories where users define their specific project workflows, triggers, event sources, and output configurations. This allows for a clean separation between the Twerk engine and its application to individual projects.

The ultimate goal is for Twerk to become so sophisticated that it can manage its own development lifecycle, eventually rendering this `PROJECT.md` file obsolete by using its own workflows to drive its evolution.

For the current stage, our immediate focus is on **researching and selecting a suitable framework** that will form the backbone of Twerk's workflow definition and execution capabilities. This will lay the groundwork for the first iteration of the `twerk-lib`.

## Project Goal: First Iteration

The primary objective for this initial phase is to establish the foundational research and architectural decisions necessary to build a working prototype of the Twerk engine. This includes:

### 1. Framework Research and Selection

*   **Objective**: Identify and evaluate existing workflow automation frameworks, libraries, or platforms that can facilitate the definition and execution of event-driven workflows.
*   **Key Considerations**:
    *   Ability to define triggers (e.g., webhooks, polling).
    *   Support for defining sequential and conditional workflows.
    *   Integration capabilities with external services (Asana, Notion, GitHub).
    *   Extensibility for custom logic and custom integrations.
    *   Ease of use and developer experience for defining workflows in code.
    *   Potential candidates include, but are not limited to, PydanticAI, Airflow, Prefect, Dagster, or custom solutions.
*   **Deliverable**: A documented decision on the primary framework to be leveraged, with clear justification.

### 2. Core `twerk-lib` Design

*   **Objective**: Outline the fundamental structure and APIs for the `twerk-lib`.
*   **Key Areas**:
    *   **Workflow Definition Schema**: How workflows, triggers, sources, and outputs will be programmatically defined.
    *   **Execution Engine**: The basic architecture for parsing definitions and orchestrating task execution.
    *   **Integration Layer**: High-level design for interfacing with external services (Asana, Notion, GitHub APIs).
    *   **Configuration Management**: How `twerk-lib` will load and manage workflow configurations.
*   **Deliverable**: Initial design documentation and potentially skeletal code structure for `twerk-lib`.

### 3. Basic Workflow Execution Mechanism

*   **Objective**: Develop a minimal, runnable engine capable of parsing a simple workflow definition and executing its steps.
*   **Requirements**:
    *   Ability to start a "twerk" server/process.
    *   Support for a basic trigger (e.g., a simple timer or manual invocation).
    *   Execution of a predefined sequence of actions.
*   **Deliverable**: A proof-of-concept engine demonstrating basic workflow execution.

### 4. Workflow Configuration Specification

*   **Objective**: Define the precise format and syntax for configuration files that users will use to define their workflows.
*   **Requirements**:
    *   Clear definition of how to specify triggers (e.g., Asana webhook, GitHub event).
    *   Specification for defining workflow steps, including actions, inputs, and outputs.
    *   A structured way to define data sources and destinations.
*   **Deliverable**: A specification document or example configuration file demonstrating the intended structure.

## Current State

This project is in its inception phase. The concept has been defined, and the immediate need is to establish a solid technical foundation through framework research.

## Next Steps for the Next Agent

Upon receiving this `PROJECT.md`, the next agent should:

1.  **Initiate Framework Research**: Begin a deep dive into potential frameworks, with a particular focus on PydanticAI as a starting point, but also exploring alternatives. Gather information on their capabilities, limitations, and suitability for the Twerk project's goals.
2.  **Propose Framework Selection**: Based on the research, recommend a primary framework and provide a well-reasoned justification for its adoption.
3.  **Begin `twerk-lib` Design**: Start outlining the core components and structure of the `twerk-lib` based on the proposed framework. This includes sketching out the workflow definition schema and the basic execution engine architecture.
4.  **Define Configuration Schema**: Draft the initial schema for workflow configuration files, considering how triggers, actions, and integrations will be represented.

This first iteration aims to de-risk the project by making critical architectural choices early on, setting a clear path for subsequent development.
