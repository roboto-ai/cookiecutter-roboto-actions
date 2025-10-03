"""
Use as the entrypoint script when running in a Docker container.

Requires a number of Roboto-specific environment variables to be set,
which is done automatically when run on hosted compute.
"""

import logging

import roboto

from .. import Args, main

action_runtime = roboto.ActionRuntime.from_env()

args = Args(
    input_dir=action_runtime.input_dir,
    log_level=logging.INFO,
    output_dir=action_runtime.output_dir,
)

main(args)
