#!/usr/bin/env bash
# call this in yer <repo root>/.git/hooks/pre-commit

echo "Doing pre-commit check..."

echo "Checking code smells..."
source ./scripts/check_code_smells.sh

echo "Checking code style..."
source ./scripts/check_git_style.sh

echo "Checking for conflicting migrations..."
source scripts/check_migrations.sh

echo "Passed pre-commit check"
