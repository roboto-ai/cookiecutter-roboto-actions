import argparse
import collections.abc
import pathlib
import sys

from .actions import VerbosityAction, KeyValuePairsAction


def find_root_dir(signal_file_name: str = "action.json"):
    """Walk fs upwards, looking for first directory that contains a file named `signal_file_name`."""
    current_dir = pathlib.Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        signal_file = current_dir / signal_file_name
        if signal_file.exists():
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError(
        f"Could not find {signal_file_name} in any parent directory"
    )


class Args(argparse.Namespace):
    params: dict[str, str]
    dry_run: bool
    log_level: int
    input_dir: pathlib.Path
    output_dir: pathlib.Path
    dataset_id: str | None
    file_paths: list[str] | None
    file_query: str | None
    topic_query: str | None
    org_id: str | None
    profile: str | None

    def __init__(self, args: collections.abc.Sequence[str] | None = None):
        super().__init__()
        self.__parse(args)

    def __parse(self, args: collections.abc.Sequence[str] | None):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-p",
            "--parameter",
            metavar="<PARAMETER_NAME>=<PARAMETER_VALUE>",
            dest="params",
            nargs="*",
            action=KeyValuePairsAction,
            help=(
                "Zero or more `<parameter_name>=<parameter_value>` pairs. "
                "`parameter_value` is parsed as JSON. "
            ),
        )

        query_group = parser.add_argument_group(
            "Query-Based Input",
            description=(
                "Specify input data with a RoboQL query. "
                "Mutually exclusive with 'dataset file path'-based input."
            ),
        )
        query_group.add_argument("--file-query")
        query_group.add_argument("--topic-query")

        dataset_group = parser.add_argument_group(
            "Dataset and File Path-Based Input",
            description=(
                "Specify input data with a dataset ID and one or more file paths. "
                "Mutually exclusive with query-based input."
            ),
        )
        dataset_group.add_argument("--dataset-id")
        dataset_group.add_argument(
            "--file-paths",
            type=str,
            nargs="+",
            action="extend",
        )

        fs_paths = parser.add_argument_group(
            "Local Data Directories",
            description=(
                "Optionally specify local filesystem paths to input and output directories."
            ),
        )
        root_dir = find_root_dir()
        fs_paths.add_argument(
            "-i",
            "--input-dir",
            type=pathlib.Path,
            default=root_dir / "input",
            help=(
                "Local filesystem path to input directory. "
                f"Default: {root_dir / 'input'}"
            ),
        )

        fs_paths.add_argument(
            "-o",
            "--output-dir",
            type=pathlib.Path,
            default=root_dir / "output",
            help=(
                "Local filesystem path to output directory. "
                f"Default: {root_dir / 'output'}"
            ),
        )

        global_options = parser.add_argument_group("Global Options")
        global_options.add_argument(
            "--org-id",
            help=(
                "Roboto organization ID. "
                "Only necessary if you belong to multiple Roboto organizations."
            ),
        )

        global_options.add_argument(
            "--profile",
            help="Roboto profile to use. Must match a section within the Roboto config.json.",
            required=False,
        )

        global_options.add_argument(
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

        global_options.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Use dry_run to gate side effects like modifying Roboto resources while testing locally.",
        )

        parser_args = args if args else sys.argv[1:]
        if not parser_args:
            parser.print_help()
            sys.exit(1)

        parser.parse_args(args=parser_args, namespace=self)
        self.__validate_input_constraints()

    def __validate_input_constraints(self):
        dataset_args = bool(self.dataset_id or getattr(self, "file_paths", None))
        query_args = bool(
            getattr(self, "file_query", None) or getattr(self, "topic_query", None)
        )

        if dataset_args and query_args:
            raise argparse.ArgumentError(
                None,
                "Cannot specify input data as both a query and as a dataset/file paths combination.",
            )
