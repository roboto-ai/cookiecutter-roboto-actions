#!/bin/bash

set -e

# Early exit if virtual environment does not exist and/or roboto is not yet installed
if [ ! -f ".venv/bin/roboto" ]; then
    echo "Virtual environment with roboto CLI does not exist. Please run ./setup.sh first."
    exit 1
fi

.venv/bin/roboto actions create --from-file action.json
