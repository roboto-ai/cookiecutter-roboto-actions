#!/usr/bin/env bash

set -euo pipefail

{% if cookiecutter.initialize_git_repo %}
git init --quiet --initial-branch=main
git add .
git commit -m "Initialize from project template"
{% endif %}
