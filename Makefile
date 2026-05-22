.PHONY: all setup test lint run clean

# Default target
all: setup

# Install dependencies and create venv if it doesn't exist
setup:
	@if [ ! -d ".venv" ]; then python -m venv .venv; fi
	@. .venv/bin/activate && pip install -r requirements-twerkflow.txt

# Run pre-commit checks
check:
	@. .venv/bin/activate && ./scripts/precommit.sh

# Run the application
run:
	@export PYTHONPATH=$PYTHONPATH:. && . .venv/bin/activate && python src/main.py

# Clean up build/venv artifacts
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
