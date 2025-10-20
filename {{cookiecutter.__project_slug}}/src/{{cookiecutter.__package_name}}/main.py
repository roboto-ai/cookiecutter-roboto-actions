import logging

import roboto

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
logger = logging.getLogger(name="{{cookiecutter.__package_name}}")


def main(context: roboto.InvocationContext) -> None:
    logger.setLevel(context.log_level)

    action_input = context.get_input()
{% if cookiecutter.__action_type == "file-based" %}
    if action_input.files:
        logger.info("Processing %d input file(s):", len(action_input.files))
        for file, local_path in action_input.files:
            logger.info(
                "  File: %s (ID: %s)",
                file.relative_path,
                file.file_id,
            )

            if local_path:
                # File is downloaded and available at local_path
                logger.info("    Local path: %s", local_path)
                logger.info("    File size: %d bytes", local_path.stat().st_size)
            else:
                logger.warning(" File not downloaded (requires_downloaded_inputs may be false)")
    else:
        logger.info("No input files provided")
{% else %}
    if action_input.topics:
        logger.info("Processing %d input topic(s):", len(action_input.topics))
        for topic in action_input.topics:
            logger.info(
                "  Topic: %s (ID: %s, extracted from: %s)",
                topic.topic_name,
                topic.topic_id,
                topic.association.association_id,
            )

            # Example: Fetch and process topic data efficiently
            # Topic data is fetched on-demand as a pandas DataFrame
            df = topic.get_data_as_df()
            logger.info("Topic has %d messages", len(df))
    else:
        logger.info("No input topics provided")
{% endif %}
