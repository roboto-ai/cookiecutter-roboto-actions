#!/usr/bin/env bash
#
# USAGE:
#   ./scripts/run.sh [OPTIONS]
#
# OPTIONS:
#   ./scripts/run.sh --help

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

# Always (re)build the container image
# Layer caching makes this fast when nothing but source code has changed
echo "### Building container image ###"
$SCRIPTS_ROOT/build.sh --quiet

# Workspace preparation requires the roboto SDK
if [ ! -f "$PACKAGE_ROOT/.venv/bin/python" ]; then
    echo "Virtual environment does not exist. Please run ./scripts/setup.sh first."
    exit 1
fi

echo "### Running ###"
# Run script which will exec docker run
$PACKAGE_ROOT/.venv/bin/python -m src.{{ cookiecutter.__package_name }}.bin.cli_entrypoint "$@"
