#!/usr/bin/env bash

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

# Set input_dir to one of: the first argument passed to this script, $ROBOTO_INPUT_DIR, or the package root
input_dir=${ROBOTO_INPUT_DIR:-$PACKAGE_ROOT}
if [ $# -gt 0 ]; then
    input_dir=$1  
fi

# Set output_dir variable to $ROBOTO_OUTPUT_DIR if defined, else set it to "output/" in the package root (creating if necessary)
output_dir=${ROBOTO_OUTPUT_DIR:-$PACKAGE_ROOT/output}
mkdir -p $output_dir

# Assert both directories are absolute paths
if [[ ! "$input_dir" = /* ]]; then
    echo "Input directory '$input_dir' must be specified as an absolute path"
    exit 1
fi

if [[ ! "$output_dir" = /* ]]; then
    echo "Output directory '$output_dir' must be specified as an absolute path"
    exit 1
fi

docker run --rm -it \
    -u $(id -u):$(id -g) \
    -v ~/.roboto/config.json:/roboto.config.json \
    -v $input_dir:/input \
    -v $output_dir:/output \
    -e ROBOTO_CONFIG_FILE=/roboto.config.json \
    -e ROBOTO_INPUT_DIR=/input \
    -e ROBOTO_OUTPUT_DIR=/output \
    -e ROBOTO_DATASET_ID=NOT_SET \
    -e ROBOTO_INVOCATION_ID=NOT_SET \
    -e ROBOTO_ORG_ID=NOT_SET \
    {{ cookiecutter.__package_name }}:latest
