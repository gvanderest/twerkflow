#!/bin/bash
# Check commit message format (Conventional Commits)

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(head -n 1 "$COMMIT_MSG_FILE")

# Pattern: <type>(<scope>): <subject>
# Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+$"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo "Error: Invalid commit message format."
    echo "Expected format: <type>(<scope>): <subject>"
    echo "Example: feat(core): add state persistence"
    echo "Actual message: $COMMIT_MSG"
    exit 1
fi
