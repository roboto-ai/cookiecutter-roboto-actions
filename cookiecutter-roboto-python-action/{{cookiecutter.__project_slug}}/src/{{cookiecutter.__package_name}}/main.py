import dataclasses
import logging
import pathlib

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(name="{{cookiecutter.__package_name}}")


@dataclasses.dataclass
class Args:
    input_dir: pathlib.Path
    log_level: int  # logging.ERROR | logging.INFO | logging.DEBUG
    output_dir: pathlib.Path
    dry_run: bool = False
    """Use dry_run to gate side effects like modifying Roboto resources while testing locally."""


def main(args: Args) -> None:
    log.setLevel(args.log_level)

    log.info("Input directory is: %r", args.input_dir)
    if args.input_dir.exists():
        log.info("Contents of input directory %r:", args.input_dir)
        for file in args.input_dir.iterdir():
            log.info("  %s", file)

    log.info("Output directory is: %r", args.output_dir)

    if args.dry_run:
        log.warning("Dry run: skipping a step with a side-effect")
    else:
        log.info("Side effect!")
