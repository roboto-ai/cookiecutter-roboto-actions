# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

> **Note**: This README was generated from a template. Please customize it to describe what this specific action does: its inputs, outputs, parameters, and/or usage instructions.

## Quick Start

### Prerequisites

- **Docker** (Engine 19.03+): Local invocation always runs in Docker for production parity
- **Python 3**: A supported version (see [.python-version](.python-version))

```bash
$ docker --version
$ python3 --version
```

### Installation

Set up a virtual environment and install dependencies with the following command:

```bash
$ ./scripts/setup.sh
```

You must be setup to [access Roboto programmatically](https://docs.roboto.ai/getting-started/programmatic-access.html). Verify with the following command:
```bash
$ .venv/bin/roboto users whoami
```

### Deployment

Build and deploy to the Roboto Platform with the following commands:

```bash
$ ./scripts/build.sh
$ ./scripts/deploy.sh [ROBOTO_ORG_ID]
```

### Local Action Invocation

{% if cookiecutter.__action_type == "file-based" %}
Example invocation:
```bash
# Process files matching a RoboQL query
$ ./scripts/run.sh --file-query "dataset_id=ds_abc123 AND path LIKE 'logs/%.log'"
```
{% else %}
Example invocation:
```bash
# Process topics matching a RoboQL query
$ ./scripts/run.sh --topic-query "msgpaths[cpuload.load].max > 0.9"
```
{% endif %}

Full usage:
```bash
$ ./scripts/run.sh --help
usage: local_invoke [-h] [-p [<PARAMETER_NAME>=<PARAMETER_VALUE> ...]]
                    [--file-query FILE_QUERY] [--topic-query TOPIC_QUERY]
                    [--dataset-id DATASET_ID]
                    [--file-paths FILE_PATHS [FILE_PATHS ...]]
                    [-w WORKSPACE_DIR] [--org-id ORG_ID] [--profile PROFILE]
                    [-v] [-d]

Invoke an action locally

options:
  -h, --help            show this help message and exit
  -p [<PARAMETER_NAME>=<PARAMETER_VALUE> ...], --parameter [<PARAMETER_NAME>=<PARAMETER_VALUE> ...]
                        Zero or more `<parameter_name>=<parameter_value>`
                        pairs. `parameter_value` is parsed as a string.

Query-Based Input:
  Specify input data with a RoboQL query. Mutually exclusive with 'dataset
  file path'-based input.

  --file-query FILE_QUERY
  --topic-query TOPIC_QUERY

Dataset and File Path-Based Input:
  Specify input data with a dataset ID and one or more file paths. Mutually
  exclusive with query-based input.

  --dataset-id DATASET_ID
  --file-paths FILE_PATHS [FILE_PATHS ...]

Local Workspace Directory:
  Optionally specify local filesystem path to workspace directory.

  -w WORKSPACE_DIR, --workspace-dir WORKSPACE_DIR
                        Local filesystem path to workspace directory. Default:
                        {{ cookiecutter.__project_slug }}/.workspace

Global Options:
  --org-id ORG_ID       Roboto organization ID. Only necessary if you belong
                        to multiple Roboto organizations.
  --profile PROFILE     Roboto profile to use. Must match a section within the
                        Roboto config.json.
  --log-level {error,warning,info,debug}
                        Set the logging level. Choose from: error, warning, info, debug.
                        Default: info.
  -d, --dry-run         Use dry_run to gate side effects like modifying Roboto
                        resources while testing locally.

```

## Development

See [DEVELOPING.md](DEVELOPING.md) for detailed information about developing this action, including:
- Project structure and key files
- Local invocation
- Adding dependencies (runtime, system, and development)
- Working with action parameters (including secrets)
- Handling input and output data
- Building and deploying to Roboto
