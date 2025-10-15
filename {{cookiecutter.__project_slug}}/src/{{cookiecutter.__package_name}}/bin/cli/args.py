import argparse
import collections.abc
import logging
import pathlib
import sys

from roboto.domain.actions import InvocationInput, FileSelector, DataSelector

from .actions import LogLevelAction, KeyValuePairsAction


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
    """Prop bag for collected command-line arguments for local invocation.

    Warning:
        Do not customize this class for individual actions.
        CLI argument customizations only affect local invocation and will not apply on Roboto's compute platform.
    """

    params: dict[str, str]
    dry_run: bool
    log_level: int
    workspace_dir: pathlib.Path
    dataset_id: str | None
    file_paths: list[str] | None
    file_query: str | None
    topic_query: str | None
    org_id: str | None
    profile: str | None

    def parse_input_spec(self) -> InvocationInput | None:
        if self.file_query is not None or self.topic_query is not None:
            return InvocationInput(
                files=(
                    FileSelector(query=self.file_query)
                    if self.file_query is not None
                    else None
                ),
                topics=(
                    DataSelector(query=self.topic_query)
                    if self.topic_query is not None
                    else None
                ),
            )

        if self.dataset_id is not None and self.file_paths:
            return InvocationInput.from_dataset_file_paths(
                self.dataset_id, self.file_paths
            )

        return None

    def parse_from_sys_argv(
        self, args: collections.abc.Sequence[str] | None = None
    ) -> None:
        parser = argparse.ArgumentParser(
            prog="local_invoke", description="Invoke an action locally"
        )

        parser.add_argument(
            "-p",
            "--parameter",
            metavar="<PARAMETER_NAME>=<PARAMETER_VALUE>",
            dest="params",
            nargs="*",
            action=KeyValuePairsAction,
            default=dict(),
            help=(
                "Zero or more `<parameter_name>=<parameter_value>` pairs. "
                "`parameter_value` is parsed as a string."
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
            "Local Workspace Directory",
            description=(
                "Optionally specify local filesystem path to workspace directory."
            ),
        )
        root_dir = find_root_dir()
        default_workspace_path = root_dir / ".workspace"
        fs_paths.add_argument(
            "-w",
            "--workspace-dir",
            type=pathlib.Path,
            default=default_workspace_path,
            help=f"Local filesystem path to workspace directory. Default: {default_workspace_path}",
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
            "--log-level",
            action=LogLevelAction,
            dest="log_level",
            choices=["error", "warning", "info", "debug"],
            default=logging.INFO,
            help=(
                "Set the logging level. "
                "Choose from: error, warning, info, debug. "
                "Default: info."
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
