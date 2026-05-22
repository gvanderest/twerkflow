# Twerkflow Coding Standards

These standards ensure our LangGraph workflows remain maintainable, reusable, and inspectable.

## 1. Node Philosophy
- **Separation**: Agents (`src/agents/`) handle dynamic/complex tasks; Gates (`src/gates/`) handle deterministic checks.
- **Independence**: Nodes should be independently testable. Do not hardcode external API calls directly in node logic; inject them as tool instances.
- **Persistence**: All state transitions must be serialized. Do not rely on node-local memory for critical state.

## 2. Graph Definition
- **Declarative**: Use the `StateGraph` builder to clearly define edges and conditionals.
- **Explicit**: Avoid implicit "magic" transitions. If a transition is complex, use a named conditional edge.

## 3. Watermarking
- **Requirement**: All agent-generated output (comments, logs, PR descriptions) MUST include a watermark.
- **Format**: `--- *Authored by Twerkflow (vX.Y)*` (or equivalent identifier).
- **Self-Ignorance**: Nodes responsible for triggering actions based on comments must parse existing comments to ignore those containing the watermark.

## 4. State Management
- **Pydantic**: All `State` objects must be Pydantic models.
- **Serializability**: Ensure state can be fully serialized to JSON for storage in ticket descriptions.
