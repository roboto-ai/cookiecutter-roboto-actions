"""
Use as the entrypoint script when running in a Docker container.

Requires a number of Roboto-specific environment variables to be set,
which is done automatically when run on hosted compute.
"""
import roboto

from .. import main

context_from_env = roboto.InvocationContext.from_env()

main(context_from_env)
