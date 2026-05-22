#!/bin/bash

# Pre-commit script: Lint, Typecheck, and Test
# Assumes venv is active or tools are available in path

echo "--- Running Pre-commit Checks ---"

# 1. Linting
echo "Running flake8 (linting)..."
python -m flake8 src tests || echo "flake8 issues found."

# 2. Typechecking
echo "Running mypy (typechecking)..."
python -m mypy src || echo "mypy issues found."

# 3. Unit Tests
echo "Running pytest (tests)..."
python -m pytest tests || echo "pytest issues found."

echo "--- Pre-commit Checks Complete ---"
