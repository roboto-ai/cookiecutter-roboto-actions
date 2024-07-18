import logging

from roboto.action_runtime import ActionRuntime

log = logging.getLogger()

action_runtime = ActionRuntime.from_env()


log.info(f"Contents of input directory {action_runtime.input_dir}:")
for file in action_runtime.input_dir.iterdir():
    log.info("  %s", file)

log.info("Output directory is: %s", action_runtime.output_dir)
