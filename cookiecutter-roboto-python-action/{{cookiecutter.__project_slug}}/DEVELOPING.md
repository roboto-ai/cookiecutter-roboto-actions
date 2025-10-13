# Development Guide

This guide provides detailed information for developing Roboto Actions using this template.

## Table of Contents

- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Action Parameters](#action-parameters)
- [Input Data](#input-data)
- [Invoking Locally](#invoking-locally)

## Project Structure

### Key Files

#### `main.py`

The primary orchestrator of your action. This is where your action's core logic lives.

Simple actions may be defined in this single file, while complex actions benefit from being broken into separate modules, then imported and orchestrated here.

**Expected signature**:
```python
def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    # Your action logic here
    pass
```

The function receives three arguments:
1. `context: roboto.action_runtime.InvocationContext` - Provides access to parameters, input data, working directories, and organization/dataset information
2. `log_level: int` - Logging verbosity (e.g., `logging.INFO`, `logging.DEBUG`)
3. `dry_run: bool` - Whether to run in dry-run mode. Action developers should use this flag to gate side effects like modifying Roboto resources during local invocation.

#### `action.json`

Defines action metadata including:
- Action name and description
- Compute requirements (vCPU, memory, storage)
- Action parameters (see [Action Parameters](#action-parameters))
- Whether the action requires input data to be pre-downloaded into the working directory

See [ActionConfig](https://docs.roboto.ai/reference/python-sdk/roboto/domain/actions/index.html#roboto.domain.actions.ActionConfig) for details.

#### `Dockerfile`

Defines the Docker container image that runs your action. Modify this file to:
- Install system dependencies (see [System Dependencies](#system-dependencies))
- Customize the runtime environment

#### `.python-version`

Specifies the Python version for this action. This file is used by [pyenv](https://github.com/pyenv/pyenv) and similar tools to automatically set the correct Python version when working in this repository.

Update this file if you need a different Python version. Prefer a version compatible with or more recent than what's specified at repository initialization.

## Development Workflow

### Adding Dependencies

#### Runtime Dependencies

Add third-party Python libraries required at runtime by your action to `requirements.runtime.txt`.

Example:
```txt
numpy>=1.24.0
pandas>=2.0.0
```

After adding dependencies, rebuild your virtual environment:
```bash
$ ./scripts/setup.sh
```

#### System Dependencies

While this action is written in Python, it runs within a Docker container defined in the `Dockerfile`.

Some actions or third-party libraries require system dependencies that may be installed on your workstation but are not available in the container image.

To install additional system dependencies, add `RUN apt-get install` instructions in the `Dockerfile`. See the commented section beginning with `# -- INSTALL SYSTEM DEPENDENCIES --`.

Example:
```dockerfile
# -- INSTALL SYSTEM DEPENDENCIES --
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
```

**Important**: Always test the container's runtime environment before deploying to Roboto by building the image and invoking it locally (see [Invoking Locally](#invoking-locally)).

#### Development Dependencies

Add Python-based tools used only as part of development and QA (such as linting and testing) to `requirements.dev.txt`.

Example:
```txt
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
```

These dependencies are installed in your local virtual environment but are not included in the Docker image deployed to Roboto.

### Code Organization Best Practices

- **Single entry point**: Export a single `main()` function with the expected signature
- **Keep `main.py` focused**: It should orchestrate your action's workflow, not contain all implementation details
- **Use modules for complex logic**: Break complex actions into separate modules under `src/{{cookiecutter.__package_name}}/`
- **Type hints**: Use type hints for better code clarity and IDE support
- **Logging**: Use the provided `log_level` parameter to control verbosity
- **Dry-run support**: Use the `dry_run` flag to enable local invocation without side effects

## Action Parameters

### Overview

A Roboto Action can be thought of as a function. Like functions, actions can define required or optional arguments. Actions refer to these arguments as **parameters**. Parameters can be set when the action is invoked, either manually or by a Roboto Trigger.

### Defining Parameters

Parameters are defined in the `parameters` array within `action.json`. Each parameter follows the [ActionParameter](https://docs.roboto.ai/reference/python-sdk/roboto/domain/actions/action_record/index.html#roboto.domain.actions.action_record.ActionParameter) model schema.

Properties:
- `name`: Unique identifier for the parameter
- `description`: Human-readable description of the parameter's purpose
- `required`: Whether the parameter must be provided (defaults to `false`)
- `default`: Default value if not provided (only for optional parameters)

Example:
```json
{
    "name": "my-action",
    "description": "My action description",
    "parameters": [
        {
            "name": "threshold",
            "description": "Detection threshold",
            "required": true
        },
        {
            "name": "labeling_service_api_key",
            "description": "API key for the labeling service",
            "required": true
        },
        {
            "name": "output_format",
            "description": "Output format (json or csv)",
            "default": "json"
        }
    ]
}
```

### Passing Secrets Through Parameters

Roboto supports passing secrets to actions that have been registered in Roboto's secrets store.

Parameters that receive secret values are defined in `action.json` like any other parameter. When invoking the action, format the value as `roboto-secret://<secret-name>`. At runtime, use [`InvocationContext.get_secret_parameter()`](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext.get_secret_parameter) to resolve the secret to its actual value.

Example:
```bash
$ roboto secrets write my-labeling-service-api-key API_KEY_VALUE
$ ./scripts/run.sh --parameter labeling_service_api_key="roboto-secret://my-labeling-service-api-key"
```

### Using Parameters in Your Action

Action parameters are passed as environment variables in both hosted compute and local Docker execution.

**Local invocation**: When you run `./scripts/run.sh --parameter threshold=60 --parameter labeling_service_api_key="roboto-secret://my-labeling-service-api-key"`, the orchestration script converts your CLI arguments into environment variables before launching the Docker container.

**Hosted compute**: When run by Roboto on its platform, the platform infrastructure sets the same environment variables.

The Roboto Python SDK's [`roboto.InvocationContext`](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext) provides convenient access to these parameters. See: 
    - [get_parameter()](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext.get_parameter)
    - [get_optional_parameter()](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext.get_optional_parameter)
    - [get_secret_parameter()](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext.get_secret_parameter)

Example usage in `main.py`:
```python
def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    threshold = context.get_parameter("threshold")
    output_format = context.get_optional_parameter("output_format", "json")
    labeling_service_api_key = context.get_secret_parameter("labeling_service_api_key")
    ...
```

## Input Data

### Overview

Most actions operate on data uploaded to Roboto, and many upload results back to Roboto. Managing input data to seamlessly enable both local development and production usage is critical.

Roboto provides two approaches for working with input data:

### Approach A: Input Data Specified at Invocation Time

In this approach, input data is specified when the action is invoked using a RoboQL query or glob pattern that matches one or more files from a specified dataset.

When an action is automatically triggered by a Roboto event (such as file upload or ingestion), the trigger specifies the input data for the invocation.

**When to use**: This is the most common approach, and is suggested for use with actions invoked by both event-based triggers (e.g., `file_upload` or `file_ingested`) and scheduled triggers.

#### Using Input Data Specified at Invocation Time

When input data is specified at invocation, Roboto downloads it into the working directory where the action runs.

The data is available via the filesystem in a directory specified by the environment variable [`ROBOTO_INPUT_DIR`](https://docs.roboto.ai/reference/python-sdk/roboto/env/index.html#roboto.env.RobotoEnvKey.InputDir).

The Roboto Python SDK's [`roboto.InvocationContext`](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext) provides helpers for accessing this data. See [get_input()](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/invocation_context/index.html#roboto.action_runtime.invocation_context.InvocationContext.get_input) and [ActionInput](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_input/index.html#roboto.action_runtime.action_input.ActionInput) for more.

**Example using `get_input()`**:
```python
import roboto

def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    action_input = context.get_input()

    # Access input files
    for file_record, local_path in action_input.files:
        print(file_record.file_id, local_path)

    # Access input topics
    for topic in action_input.topics:
        df = topic.get_data_as_df()
```

**Example local invocation**:
```bash
$ ./scripts/run.sh --topic-query "msgpaths[cpuload.load].max > 0.9"
```

### Approach B: Query for Data at Runtime

In this approach, the action code queries Roboto for data at runtime, enabling it to operate on any data queryable from the Roboto API.

**Example**:
```python
import roboto

def main(
    context: roboto.InvocationContext,
    log_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    roboto_search = roboto.RobotoSearch.for_roboto_client(context.roboto_client)
    for topic in roboto_search.find_topics("msgpaths[cpuload.load].max > 0.9"):
        # Process topic
        df = topic.get_data_as_df()
        ...
```

**When to use**: This approach is most common for actions performing batch processing that will be invoked manually, with no changes expected in the query used to gather data. Prefer using [Approach A](#approach-a-input-data-specified-at-invocation-time) in general, as it allows you to more flexibly define how input data is selected, including the use of `LIMIT` when testing.

## Invoking Locally

### Overview

Local invocation always runs in a Docker container to ensure production parity. The Docker image is rebuilt on each invocation (Docker's layer caching makes this fast when nothing has changed).

### Basic Usage

```bash
# See all available options
$ ./scripts/run.sh --help

# Specify topics to use as input (accessible via `InvocationContext::get_input().topics`) and parameters
$ ./scripts/run.sh --topic-query="msgpaths[cpuload.load].max > 0.9" --parameter threshold=60 -vv
```

### How It Works

When you run `./scripts/run.sh`:

1. **Build**: The Docker image is built (or rebuilt if source or dependencies changed)
2. **Prepare**: Workspace directories are created on your host machine
3. **Download**: Input data is downloaded if specified (`requires_downloaded_inputs` in `action.json`)
4. **Launch**: A Docker container is launched with:
   - Your workspace mounted at `/workspace`
   - Your Roboto config mounted at `/roboto.config.json`
   - All necessary environment variables set
   - Your user/group ID to ensure proper file permissions
5. **Execute**: The action executes inside the container

### Workspace Structure

When invoking locally, the following directories are used:

- `workspace/`: Working directory for temporary files (Git-ignored)
- `workspace/input/`: Input data downloaded as part of setup, if applicable
- `workspace/output/`: Output data written by your action, if any

### Build and Deployment

#### Building the Docker Image

```bash
$ ./scripts/build.sh
```

Builds the Docker image locally. The image is tagged with your action name.

#### Deploying to Roboto Platform

```bash
$ ./scripts/deploy.sh
```

This script:
1. Builds the Docker image
2. Pushes it to Roboto's container registry
3. Creates or updates the action definition on the Roboto platform using configuration from `action.json`

**Prerequisites**: You must have a personal access token accessible in your environment. See [Programmatic Access](https://docs.roboto.ai/getting-started/programmatic-access.html#personal-access-token) for more.

