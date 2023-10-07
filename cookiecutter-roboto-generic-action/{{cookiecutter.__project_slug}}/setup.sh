#!/bin/bash

set -e

# Create a virtual environment
python -m venv --upgrade-deps .venv

# Install roboto
.venv/bin/pip install -r requirements.dev.txt
