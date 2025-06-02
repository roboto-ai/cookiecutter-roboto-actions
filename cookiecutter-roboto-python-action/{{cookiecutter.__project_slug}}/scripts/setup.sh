#!/usr/bin/env bash

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

venv_dir="$PACKAGE_ROOT/.venv"

# Create a virtual environment
python3 -m venv --clear --upgrade-deps $venv_dir

# Install dev deps
pip_exe="$venv_dir/bin/pip"
$pip_exe install --upgrade -r $PACKAGE_ROOT/requirements.dev.txt
