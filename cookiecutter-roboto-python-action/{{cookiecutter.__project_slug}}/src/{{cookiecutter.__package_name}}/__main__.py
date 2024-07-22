import logging

from roboto.action_runtime import ActionRuntime

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(name="{{cookiecutter.__package_name}}")
log.setLevel(logging.INFO)

action_runtime = ActionRuntime.from_env()


log.info(f"Contents of input directory {action_runtime.input_dir}:")
for file in action_runtime.input_dir.iterdir():
    log.info("  %s", file)

log.info("Output directory is: %s", action_runtime.output_dir)
