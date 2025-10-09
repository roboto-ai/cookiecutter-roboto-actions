import os
import logging

import roboto

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(name="{{cookiecutter.__package_name}}")


def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False
) -> None:
    log.setLevel(log_level)

    log.debug(
        os.linesep.join([
            os.linesep,
            "#" * 88,
            "Invocation context:",
            "    invocation_id: %s",
            "    dataset_id: %s",
            "    input_dir: %s",
            "    output_dir: %s",
            "    org_id: %s",
            "#" * 88,
        ]),
        context.invocation_id,
        context.dataset_id,
        context.input_dir,
        context.output_dir,
        context.org_id,
    )

    if context.input_dir.exists():
        log.info("Contents of input directory %r:", context.input_dir)
        for file in context.input_dir.iterdir():
            log.info("  %s", file)

    if dry_run:
        log.warning("Dry run: skipping a step with a side-effect")
    else:
        log.info("Side effect!")
