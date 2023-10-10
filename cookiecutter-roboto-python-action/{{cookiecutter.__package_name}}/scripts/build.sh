#!/usr/bin/env bash

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

docker build -f $PACKAGE_ROOT/Dockerfile -t {{ cookiecutter.__package_name }}:latest $PACKAGE_ROOT
