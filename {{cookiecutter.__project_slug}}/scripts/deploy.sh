#!/usr/bin/env bash

set -euo pipefail

SCRIPTS_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PACKAGE_ROOT=$(dirname "${SCRIPTS_ROOT}")

# Early exit if the Roboto CLI is not installed
if ! command -v roboto &> /dev/null; then
    echo "The Roboto CLI is not installed or not on PATH."
    echo "See https://github.com/roboto-ai/roboto-python-sdk/blob/main/README.md#cli for installation instructions."
    exit 1
fi

echo "Building container image"
$SCRIPTS_ROOT/build.sh --quiet

# Set org_id to $ROBOTO_ORG_ID if defined, else the first argument passed to this script
org_id=${ROBOTO_ORG_ID:-}
if [ $# -gt 0 ]; then
    org_id=$1  
fi

echo "Pushing {{ cookiecutter.__package_name }}:latest to Roboto's private registry"
image_push_args=(
    --suppress-upgrade-check
    images push
    --quiet
)
if [[ -n $org_id ]]; then
    image_push_args+=(--org $org_id)
fi
image_push_args+=({{ cookiecutter.__package_name }}:latest)
image_push_ret_code=0
image_uri=$(roboto "${image_push_args[@]}")
image_push_ret_code=$?

if [ $image_push_ret_code -ne 0 ]; then
    echo "Failed to push {{ cookiecutter.__package_name }}:latest to Roboto's private registry"
    exit 1
fi

echo "Creating/updating {{ cookiecutter.__package_name }} action"
create_args=(
  --from-file $PACKAGE_ROOT/action.json
  --image $image_uri
  --yes
)
if [[ -n $org_id ]]; then
    create_args+=(--org $org_id)
fi
roboto actions create "${create_args[@]}"
