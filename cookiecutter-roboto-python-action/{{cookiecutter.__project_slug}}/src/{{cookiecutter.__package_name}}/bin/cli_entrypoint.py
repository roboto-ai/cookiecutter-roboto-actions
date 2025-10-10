"""
Use as the entrypoint script when running locally.
"""

import dataclasses
import pathlib

import roboto
from roboto.domain.actions import ActionConfig
from roboto.action_runtime import prepare_invocation_environment
from roboto.domain.orgs import Org

from .. import main

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


def setup_workspace(workspare_dir: pathlib.Path) -> Workspace:
    input_dir = workspare_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    output_dir = workspare_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    config_dir = workspare_dir / ".roboto" / "action-runtime"
    config_dir.mkdir(parents=True, exist_ok=True)

    metadata_dir = output_dir / ".metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    parameters_file = config_dir / "action_parameters.json"
    secrets_file = config_dir / "secrets.json"
    input_data_manifest_file = input_dir / "action_inputs_manifest.json"
    dataset_metadata_changeset_file = metadata_dir / "dataset_metadata_changeset.json"

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


if __name__ == "__main__":
    args = Args()

    if not ACTION_JSON_FILE.exists():
        raise FileNotFoundError(
            "Could not find 'action.json' file providing configuration for this action."
        )

    action_config = ActionConfig.model_validate_json(ACTION_JSON_FILE.read_text())

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

    context = roboto.InvocationContext(
        dataset_id=dataset_id,
        input_dir=workspace.input_dir,
        invocation_id="inv_LOCAL_INVOCATION",
        output_dir=workspace.output_dir,
        input_data_manifest_file=workspace.input_data_manifest_file,
        parameters_file=workspace.parameters_file,
        secrets_file=workspace.secrets_file,
        org_id=org_id,
        roboto_client=roboto_client,
    )

    main(context, log_level=args.log_level, dry_run=args.dry_run)
