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

## 5. Dependency Injection (DI)
- **Constructor Injection**: All external services (APIs, clients, file systems) must be passed into class constructors.
- **No Hidden Dependencies**: Drivers and nodes should not initialize external clients (e.g., `Github()`, `asana.Client()`) within their `__init__` methods.
- **Testability**: By injecting dependencies, we enable seamless mocking during unit tests without requiring complex `unittest.mock.patch` calls.

## 6. Testing Philosophy: No Patching
- **Avoid `unittest.mock.patch`**: Patching makes tests fragile, relies on fragile string-based imports, and hides poor architectural boundaries.
- **Use Dependency Injection**: Test by injecting real objects or simple mocks into constructors, not by hijacking global names during test runtime.
- **Enforcement**: Our pre-commit hook automatically scans for `@patch` and will reject commits that introduce new patching usage.
