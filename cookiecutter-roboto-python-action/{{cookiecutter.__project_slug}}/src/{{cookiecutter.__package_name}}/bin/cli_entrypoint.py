"""
Use as the entrypoint script when running locally.
"""

import roboto
import roboto.domain.orgs

from .. import main

from .cli import Args


if __name__ == "__main__":
    args = Args()

    roboto_client = (
        roboto.RobotoClient.for_profile(args.profile)
        if args.profile
        else roboto.RobotoClient.from_env()
    )

    org_id = args.org_id
    if org_id is None:
        member_orgs = roboto.domain.orgs.Org.for_self(roboto_client=roboto_client)
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

    context = roboto.InvocationContext(
        dataset_id=dataset_id,
        input_dir=args.input_dir,
        invocation_id="inv_LOCAL_INVOCATION",
        output_dir=args.output_dir,
        org_id=org_id,
        roboto_env=roboto.RobotoEnv.default(),
        roboto_client=roboto_client,
    )

    main(context, log_level=args.log_level, dry_run=args.dry_run)
