#!/usr/bin/env bash

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

# Early exit if virtual environment does not exist and/or roboto is not yet installed
if [ ! -f "$PACKAGE_ROOT/.venv/bin/roboto" ]; then
    echo "Virtual environment with roboto CLI does not exist. Please run ./scripts/setup.sh first."
    exit 1
fi

roboto_exe="$PACKAGE_ROOT/.venv/bin/roboto"
$roboto_exe actions create --from-file $PACKAGE_ROOT/action.json --yes
