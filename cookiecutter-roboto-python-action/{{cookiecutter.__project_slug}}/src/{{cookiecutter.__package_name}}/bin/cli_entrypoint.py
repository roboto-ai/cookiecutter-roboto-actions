"""
Use as the entrypoint script when running locally.
"""

import argparse
import logging
import pathlib

import roboto
import roboto.domain.orgs

from .. import main


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
        "--org-id",
        help=(
            "Roboto organization ID. "
            "Only necessary if you belong to multiple Roboto organizations."
        ),
    )

    parser.add_argument(
        "--profile",
        help="Roboto profile to use. Must match a section within the Roboto config.json.",
        required=False,
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

    roboto_client = roboto.RobotoClient.for_profile(parsed.profile) if parsed.profile is not None else roboto.RobotoClient.from_env()
    
    org_id = parsed.org_id
    if org_id is None:
        member_orgs = roboto.domain.orgs.Org.for_self(roboto_client=roboto_client)
        if not member_orgs:
            raise Exception(
                "No Roboto organizations found. "
                "Please create an organization or use the --org-id argument to specify one."
            )
        org_id = member_orgs[0].org_id

    context = roboto.InvocationContext(
        dataset_id="NOT_SET",
        input_dir=parsed.input_dir,
        invocation_id="inv_LOCAL_INVOCATION",
        output_dir=parsed.output_dir,
        org_id=org_id,
        roboto_env=roboto.RobotoEnv.default(),
        roboto_client=roboto_client,
    )

    main(context, log_level=parsed.log_level, dry_run=parsed.dry_run)
