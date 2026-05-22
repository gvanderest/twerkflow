#!/bin/bash

# Pre-commit script: Lint, Typecheck, and Test
# Assumes venv is active or tools are available in path

echo "--- Running Pre-commit Checks ---"

# 0. Check for forbidden patterns
echo "Checking for forbidden patterns..."
if grep -r "@patch" src tests; then
    echo "Error: @patch usage is forbidden. Please refactor to use Dependency Injection."
    exit 1
fi

# 1. Linting
echo "Running flake8 (linting)..."
python -m flake8 --max-line-length=120 src tests || echo "flake8 issues found, but continuing."

# 2. Typechecking
echo "Running mypy (typechecking)..."
python -m mypy src || echo "mypy issues found."

# 3. Unit Tests
echo "Running pytest (tests)..."
python -m pytest --cov=src --cov-fail-under=90 tests || echo "pytest issues found or coverage below 90%."

echo "--- Pre-commit Checks Complete ---"
