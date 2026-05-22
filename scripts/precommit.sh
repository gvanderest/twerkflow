# Pre-commit script: Lint, Typecheck, and Test
# Uses the virtual environment python

VENV_PYTHON="./.venv/bin/python"

echo "--- Running Pre-commit Checks ---"

# 0. Check for forbidden patterns
echo "Checking for forbidden patterns..."
if grep -r -E "@patch" src tests; then
    echo "Error: @patch usage is forbidden. Please refactor to use Dependency Injection."
    exit 1
fi
if grep -r -E "monkeypatch" src tests --exclude-dir=__pycache__ | grep -v "conftest.py"; then
    echo "Error: monkeypatch usage is forbidden in tests (except conftest.py). Please refactor to use Dependency Injection."
    exit 1
fi

# 0.5. Check constructor complexity
echo "Checking constructor complexity..."
$VENV_PYTHON scripts/linters/constructor_checker.py || exit 1

# 1. Linting & Docstrings
echo "Running ruff (linting & docstrings)..."
$VENV_PYTHON -m ruff check src tests || { echo "Linting failed. Run 'make format' to fix style issues."; exit 1; }

# 2. Typechecking
echo "Running mypy (typechecking)..."
$VENV_PYTHON -m mypy src || exit 1

# 3. Unit Tests
echo "Running pytest (tests)..."
$VENV_PYTHON -m pytest --cov=src --cov-fail-under=90 tests || exit 1

echo "--- Pre-commit Checks Complete ---"
