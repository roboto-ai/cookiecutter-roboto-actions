"""
Use as the entrypoint script when orchestrating local Docker execution.

This script prepares the workspace on the host, then launches a Docker container
with the appropriate environment variables to match hosted compute execution.
"""

import dataclasses
import os
import pathlib
import shutil
import signal
import socket
import subprocess
import sys

import roboto
from roboto.cli.validation import pydantic_validation_handler
from roboto.env import RobotoEnvKey
from roboto.domain.actions import ActionConfig
from roboto.action_runtime import prepare_invocation_environment
from roboto.domain.orgs import Org

from .cli import find_root_dir, Args

ACTION_JSON_FILE = find_root_dir() / "action.json"


@dataclasses.dataclass
class Workspace:
    input_dir: pathlib.Path
    output_dir: pathlib.Path
    config_dir: pathlib.Path
    metadata_dir: pathlib.Path
    parameters_file: pathlib.Path
    secrets_file: pathlib.Path
    input_data_manifest_file: pathlib.Path
    dataset_metadata_changeset_file: pathlib.Path


def empty_workspace(workspace_root: pathlib.Path):
    print("✔ Emptying workspace")
    if workspace_root.exists():
        for item in workspace_root.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def setup_workspace(workspace_root: pathlib.Path) -> Workspace:
    print("✔ Setting up workspace")

    input_dir = workspace_root / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    output_dir = workspace_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    config_dir = workspace_root / ".roboto"
    config_dir.mkdir(parents=True, exist_ok=True)

    metadata_dir = output_dir / ".metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    parameters_file = config_dir / "action_parameters.json"
    parameters_file.touch(exist_ok=True)

    secrets_file = config_dir / "secrets.json"
    secrets_file.touch(exist_ok=True)

    input_data_manifest_file = input_dir / "action_inputs_manifest.json"
    input_data_manifest_file.touch(exist_ok=True)

    dataset_metadata_changeset_file = metadata_dir / "dataset_metadata_changeset.json"
    dataset_metadata_changeset_file.touch(exist_ok=True)

    return Workspace(
        input_dir=input_dir,
        output_dir=output_dir,
        config_dir=config_dir,
        metadata_dir=metadata_dir,
        parameters_file=parameters_file,
        secrets_file=secrets_file,
        input_data_manifest_file=input_data_manifest_file,
        dataset_metadata_changeset_file=dataset_metadata_changeset_file,
    )


def raise_if_provided_parameter_not_specified_in_action_config(
    action_config: ActionConfig, provided: set[str]
):
    known = set(param.name for param in action_config.parameters)
    unknown = provided - known
    if unknown:
        raise ValueError(
            f"The following parameter(s) are not defined in action.json: {', '.join(sorted(unknown))}"
        )


if __name__ == "__main__":
    args = Args()

    if not ACTION_JSON_FILE.exists():
        raise FileNotFoundError(
            "Could not find 'action.json' file providing configuration for this action."
        )

    with pydantic_validation_handler("action.json"):
        action_config = ActionConfig.model_validate_json(ACTION_JSON_FILE.read_text())

    raise_if_provided_parameter_not_specified_in_action_config(
        action_config, set(args.params.keys())
    )

    roboto_client = (
        roboto.RobotoClient.for_profile(args.profile)
        if args.profile
        else roboto.RobotoClient.from_env()
    )
    roboto_search = roboto.RobotoSearch.for_roboto_client(roboto_client)

    org_id = args.org_id
    if org_id is None:
        member_orgs = Org.for_self(roboto_client=roboto_client)
        if not member_orgs:
            raise Exception(
                "It appears you are not a member of a Roboto organization. "
                "Please create an organization by logging into the web application (https://app.roboto.ai/) "
                "or try specifying the --org-id argument."
            )
        org_id = member_orgs[0].org_id

    dataset_id = (
        args.dataset_id
        if args.dataset_id
        else roboto.InvocationDataSource.unspecified().data_source_id
    )

    empty_workspace(args.workspace_dir)
    workspace = setup_workspace(args.workspace_dir)

    invocation_input = args.parse_input_spec()

    prepare_invocation_environment(
        action_parameters=action_config.parameters,
        provided_parameter_values=args.params,
        parameters_values_file=workspace.parameters_file,
        secrets_file=workspace.secrets_file,
        requires_downloaded_inputs=bool(action_config.requires_downloaded_inputs),
        input_data=invocation_input,
        input_download_dir=workspace.input_dir,
        inputs_data_manifest_file=workspace.input_data_manifest_file,
        dataset_metadata_changeset_path=workspace.dataset_metadata_changeset_file,
        org_id=args.org_id,
        roboto_client=roboto_client,
        roboto_search=roboto_search,
    )

    # Build environment variables dict
    # These match what Roboto's internal invocation scheduler does
    container_workspace_root = pathlib.Path(f"/{workspace.input_dir.parent.name}")

    def to_container_path(host_path: pathlib.Path) -> str:
        return str(container_workspace_root / host_path.relative_to(args.workspace_dir))

    env_vars = {
        RobotoEnvKey.DatasetId.value: dataset_id,
        RobotoEnvKey.InputDir.value: to_container_path(workspace.input_dir),
        RobotoEnvKey.OutputDir.value: to_container_path(workspace.output_dir),
        RobotoEnvKey.InvocationId.value: "inv_LOCAL_DOCKER_INVOCATION",
        RobotoEnvKey.OrgId.value: org_id,
        RobotoEnvKey.RobotoServiceEndpoint.value: roboto_client.endpoint,
        RobotoEnvKey.ActionRuntimeConfigDir.value: to_container_path(
            workspace.config_dir
        ),
        RobotoEnvKey.ActionInputsManifest.value: to_container_path(
            workspace.input_data_manifest_file
        ),
        RobotoEnvKey.ActionParametersFile.value: to_container_path(
            workspace.parameters_file
        ),
        RobotoEnvKey.DatasetMetadataChangesetFile.value: to_container_path(
            workspace.dataset_metadata_changeset_file
        ),
        RobotoEnvKey.RobotoEnv.value: f"LOCAL ({socket.getfqdn()})",
        # Additional parameters for local development
        "ROBOTO_LOG_LEVEL": str(args.log_level),
        "ROBOTO_DRY_RUN": "true" if args.dry_run else "false",
        "ROBOTO_CONFIG_FILE": "/roboto.config.json",
        "HOME": str(args.workspace_dir)
    }

    # Add all provided parameters as environment variables
    if args.params:
        for param_name, param_value in args.params.items():
            env_var_name = RobotoEnvKey.for_parameter(param_name)
            env_vars[env_var_name] = str(param_value)

    cmd = [
        "docker",
        "run",
        "--rm",
        "-it",
        "-u",
        f"{os.getuid()}:{os.getgid()}",
        "-v",
        f"{os.path.expanduser('~/.roboto/config.json')}:/roboto.config.json",
        "-v",
        f"{workspace.input_dir.parent}:/{workspace.input_dir.parent.name}",  # Mount workspace root
    ]

    for key, value in env_vars.items():
        cmd.extend(["-e", f"{key}={value}"])

    cmd.append("{{ cookiecutter.__package_name }}:latest")  # image name

    print("✔ Running action")
    with subprocess.Popen(
        cmd,
        text=True,
    ) as run_proc:
        try:
            run_proc.wait()
        except KeyboardInterrupt:
            run_proc.kill()
            print("")
            sys.exit(128 + signal.SIGINT.value)
        finally:
            # Always delete secrets file to avoid it sitting around on disk.
            # This is not a true security measure, just good housekeeping.
            workspace.secrets_file.unlink(missing_ok=True)
