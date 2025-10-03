"""
Use as the entrypoint script when running locally.
"""

import argparse
import logging
import pathlib

from .. import Args, main


class VerbosityAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        kwargs.setdefault("default", logging.ERROR)
        kwargs.setdefault("nargs", 0)
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        current_level = getattr(namespace, self.dest, logging.ERROR)
        new_level = max(current_level - 10, logging.DEBUG)
        setattr(namespace, self.dest, new_level)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-dir",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent.parent / "input",
        help="Local filesystem path to input directory.",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent.parent / "output",
        help="Local filesystem path to output directory.",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Use dry_run to gate side effects like modifying Roboto resources while testing locally.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action=VerbosityAction,
        dest="log_level",
        help=(
            "Set increasing levels of verbosity. "
            "Only error logs are printed by default. "
            "Use -v (warn), -vv (info), -vvv (debug)."
        ),
    )

    parsed = parser.parse_args()

    args = Args(**vars(parsed))

    main(args)
