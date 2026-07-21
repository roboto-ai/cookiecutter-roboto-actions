# {{cookiecutter.project_name}}

{% if cookiecutter.description -%}
{{ cookiecutter.description }}
{% endif %}

> **Note**: This README was generated from a template. Please customize it to describe what this specific action does: its inputs, outputs, parameters, and usage instructions.

## Table of Contents

- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running](#running)
    - [Local Invocation](#local-invocation)
    - [Hosted Invocation](#hosted-invocation)
- [Development](#development)
- [Deployment](#deployment)

## Quick Start

### Prerequisites

- **Docker** (Engine 19.03+): Local invocation always runs in Docker for production parity
- **Python 3**: A supported version (see [.python-version](.python-version))
- **Roboto CLI**: See the [installation instructions](https://github.com/roboto-ai/roboto-python-sdk/blob/main/README.md#cli)

```bash
$ docker --version
$ python3 --version
$ roboto --version
```

### Installation

Set up a virtual environment and install dependencies with the following command:

```bash
$ ./scripts/setup.sh
```

You must also be set up to [access Roboto programmatically](https://docs.roboto.ai/getting-started/programmatic-access.html). Verify with the following command:
```bash
$ roboto users whoami
```

### Running

#### Local Invocation

> **Note:** For complete local invocation documentation and examples, see [DEVELOPING.md](DEVELOPING.md#invoking-locally).

{% if cookiecutter.input_data_type == "files" -%}
Example invocation:
```bash
$ roboto --log-level=info actions invoke-local \
    --file-query="dataset_id='<ID>' AND path LIKE '%.mcap'" \
    --dry-run
```
{% else %}
Example invocation:
```bash
$ roboto --log-level=info actions invoke-local \
    --topic-query="msgpaths[cpuload.load].max > 0.9" \
    --dry-run
```
{% endif %}

Running without `--dry-run` may have side effects, depending on how this action is implemented. See [DEVELOPING.md](DEVELOPING.md#code-organization-best-practices).

Full usage:
```bash
$ roboto actions invoke-local --help
```

#### Hosted Invocation

> **Note:** To run this action on Roboto's hosted compute, you must first build and deploy it. See [DEVELOPING.md](DEVELOPING.md#build-and-deployment).

{% if cookiecutter.input_data_type == "files" -%}
Example invocation:
```bash
$ roboto actions invoke \
    --file-query="dataset_id='<ID>' AND path LIKE '%.mcap'" \
    {{ cookiecutter.__project_slug }}  # Action name is required for hosted invocation
```
{% else %}
Example invocation:
```bash
$ roboto actions invoke \
    --topic-query="msgpaths[cpuload.load].max > 0.9" \
    {{ cookiecutter.__project_slug }}  # Action name is required for hosted invocation
```
{% endif %}

Full usage:
```bash
$ roboto actions invoke --help
```

## Development

See [DEVELOPING.md](DEVELOPING.md) for detailed information about developing this action, including:
- Project structure and key files
- Local invocation
- Adding dependencies (runtime, system, and development)
- Working with action parameters (including secrets)
- Handling input and output data
- Building and deploying to Roboto

## Deployment

Build and deploy to the Roboto Platform with the following commands:

```bash
$ ./scripts/build.sh
$ ./scripts/deploy.sh [ROBOTO_ORG_ID]
```
