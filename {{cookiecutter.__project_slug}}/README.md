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
$ roboto actions invoke-local --file-query "dataset_id=ds_abc123 AND path LIKE 'logs/%.log'"
```
{% else %}
Example invocation:
```bash
# Process topics matching a RoboQL query
$ roboto actions invoke-local --topic-query "msgpaths[cpuload.load].max > 0.9"
```
{% endif %}

Full usage:
```bash
$ roboto actions invoke-local --help
usage: roboto actions invoke-local [-h] [--org ORG] [--file-query FILE_QUERY] [--topic-query TOPIC_QUERY] [--dataset DATASET_ID] [--file-path FILE_PATHS]
                                   [-p <PARAMETER_NAME>=<PARAMETER_VALUE>] [--workspace-dir WORKSPACE_DIR] [--dry-run] [--preserve-workspace]
                                   [action_or_path]

positional arguments:
  action_or_path        Action to invoke locally. Can be:
                          - A path to local action directory (e.g., '.', './my-action', '/abs/path')
                          - An action reference (e.g., 'my-action', 'org/my-action', 'action@digest')
                          - Omitted to use current directory
                        
                        Examples:
                          roboto actions invoke-local                    # Use current directory (implied)
                          roboto actions invoke-local .                  # Use current directory (explicit)
                          roboto actions invoke-local ./my-action        # Use local action
                          roboto actions invoke-local my-action          # Fetch from platform
                          roboto actions invoke-local org/my-action      # Fetch from specific org

options:
  --dry-run             Run in dry-run mode. Actions should use this flag to gate side effects such as uploading files, modifying metadata, or making non-idempotent API calls.
  --org ORG             The calling organization ID. Gets set implicitly if in a single org. The `ROBOTO_ORG_ID` environment variable can be set to control the default value.
  --preserve-workspace  Preserve existing workspace contents before execution. By default, the workspace is cleared to ensure a clean state. Use this flag to keep existing workspace contents, which can be useful when iterating on action development with the same file-based input data to avoid re-downloading data on each invocation.
  --workspace-dir WORKSPACE_DIR
                        Workspace directory for local execution. Only applicable when invoking a platform action (not an action defined in a local directory). If not specified, a temporary directory is created.
  -h, --help            show this help message and exit
  -p <PARAMETER_NAME>=<PARAMETER_VALUE>, --parameter <PARAMETER_NAME>=<PARAMETER_VALUE>
                        Parameter in ``<parameter_name>=<parameter_value>`` format. ``parameter_value`` is parsed as a string. Can be specified multiple times for multiple parameters.

Query-Based Input:
  Specify input data with a RoboQL query. Mutually exclusive with 'dataset file path'-based input.

  --file-query FILE_QUERY
                        RoboQL query to select input files.
  --topic-query TOPIC_QUERY
                        RoboQL query to select input topics.

Dataset and File Path-Based Input:
  Specify input data with a dataset id and one or more file paths. Mutually exclusive with query-based input.

  --dataset DATASET_ID  Unique identifier for dataset to use as data source for this invocation. Required if --file-path is provided.
  --file-path FILE_PATHS
                        Specific file path from the dataset. Can be specified multiple times for multiple file paths. Requires --dataset to be specified.

```

## Development

See [DEVELOPING.md](DEVELOPING.md) for detailed information about developing this action, including:
- Project structure and key files
- Local invocation
- Adding dependencies (runtime, system, and development)
- Working with action parameters (including secrets)
- Handling input and output data
- Building and deploying to Roboto
