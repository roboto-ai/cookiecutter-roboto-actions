#!/bin/bash

set -e

# Set input_dir variable to $ROBOTO_INPUT_DIR if it is defined, else set it to the current directory
input_dir=${ROBOTO_INPUT_DIR:-.}

# Set output_dir variable to $ROBOTO_OUTPUT_DIR if it is defined, else set it to a new directory in the current directory with the prefix "output-" and some random characters
output_dir=${ROBOTO_OUTPUT_DIR:-$(mktemp -p . -d -t output-XXXXXXXXXX)}

docker run --rm -it \
    -v $input_dir:/input \
    -v $output_dir:/output \
    -e ROBOTO_INPUT_DIR=/input \
    -e ROBOTO_OUTPUT_DIR=/output \
    {{ cookiecutter.__package_name }}:latest --input-dir /input --output-dir /output 
