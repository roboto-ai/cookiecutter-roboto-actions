#!/usr/bin/env bash

set -euo pipefail

git init --quiet --initial-branch=main
git add .
git commit -m "Initialize from project template"
