#!/bin/bash

set -e

docker build -f Dockerfile -t {{ cookiecutter.__project_slug }}:latest src
