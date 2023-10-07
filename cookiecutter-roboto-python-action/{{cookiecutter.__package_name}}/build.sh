#!/bin/bash

set -e

docker build -f Dockerfile -t {{ cookiecutter.__package_name }}:latest .
