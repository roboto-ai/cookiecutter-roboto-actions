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

# Early exit if virtual environment does not exist
if [ ! -f "$PACKAGE_ROOT/.venv/bin/python" ]; then
    echo "Virtual environment does not exist. Please run ./scripts/setup.sh first."
    exit 1
fi

$PACKAGE_ROOT/.venv/bin/python -m src.{{ cookiecutter.__package_name }}.bin.cli_entrypoint "$@"
