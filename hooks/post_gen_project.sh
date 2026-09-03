#!/usr/bin/env bash

set -euo pipefail

{#- When answered interactively this is a bool, but an override passed on the command line
    (e.g. `cookiecutter --no-input . initialize_git_repo=false`) arrives as a string, and any
    non-empty string is truthy. Normalize to a lowercase string and accept the same spellings
    as cookiecutter's own yes/no prompt. -#}
{% if (cookiecutter.initialize_git_repo | string | lower) in ["1", "true", "t", "yes", "y", "on"] %}
git init --quiet --initial-branch=main
git add .
git commit -m "Initialize from project template"
{% endif %}
