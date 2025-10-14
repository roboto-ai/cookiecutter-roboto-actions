"""
Use as the entrypoint script when running in a Docker container.

Requires Roboto-specific environment variables to be set,
which is done automatically when run on hosted compute or by run.sh for local Docker execution.
"""

import os
import logging

import roboto

from .. import main

context = roboto.InvocationContext.from_env()

# Support additional parameters for local development
log_level = int(os.environ.get("ROBOTO_LOG_LEVEL", str(logging.INFO)))
dry_run = os.environ.get("ROBOTO_DRY_RUN", "false").lower() == "true"

main(context, log_level=log_level, dry_run=dry_run)
