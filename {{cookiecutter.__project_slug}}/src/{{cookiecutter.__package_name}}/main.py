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

    action_input = context.get_input()
{% if cookiecutter.__action_type == "file-based" %}
    if action_input.files:
        log.info("Processing %d input file(s):", len(action_input.files))
        for file_record, local_path in action_input.files:
            log.info(
                "  File: %s (ID: %s)",
                file_record.relative_path,
                file_record.file_id,
            )

            if local_path:
                # File is downloaded and available at local_path
                log.info("    Local path: %s", local_path)
                log.info("    File size: %d bytes", local_path.stat().st_size)
            else:
                log.warning(" File not downloaded (requires_downloaded_inputs may be false)")
    else:
        log.info("No input files provided")
{% else %}
    if action_input.topics:
        log.info("Processing %d input topic(s):", len(action_input.topics))
        for topic in action_input.topics:
            log.info(
                "  Topic: %s (ID: %s, extracted from: %s)",
                topic.topic_name,
                topic.topic_id,
                topic.association.association_id,
            )

            # Example: Fetch and process topic data efficiently
            # Topic data is fetched on-demand as a pandas DataFrame
            df = topic.get_data_as_df()
            log.info("Topic has %d messages", len(df))
    else:
        log.info("No input topics provided")
{% endif %}
