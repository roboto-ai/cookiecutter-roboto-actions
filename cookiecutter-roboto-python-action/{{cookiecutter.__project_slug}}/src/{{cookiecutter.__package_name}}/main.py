import logging

import roboto

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(name="{{cookiecutter.__package_name}}")


def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    log.setLevel(log_level)

    if not dry_run:
        log.info("Invocation inputs:")
        action_input = context.get_input()
        if action_input.files:
            log.info("  Files:")
            for file, local_path in action_input.files:
                log.info(
                    "    (%s) %s (is downloaded into working directory: %s)",
                    file.file_id,
                    file.relative_path,
                    local_path is not None,
                )

        if action_input.topics:
            log.info("  Topics:")
            for topic in action_input.topics:
                log.info(
                    "    (%s) %s extracted from %s",
                    topic.topic_id,
                    topic.topic_name,
                    topic.association.association_id,
                )
