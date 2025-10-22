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

### Running

#### Local Invocation

> **Note:** For complete local invocation documentation and examples, see [DEVELOPING.md](DEVELOPING.md#invoking-locally).

{% if cookiecutter.input_data_type == "files" %}
Example invocation:
```bash
# Process files matching a RoboQL query
$ .venv/bin/roboto --log-level=info actions invoke-local --file-query="dataset_id=ds_abc123 AND path LIKE 'logs/%.log'"
```
{%- else %}
Example invocation:
```bash
# Process topics matching a RoboQL query
$ .venv/bin/roboto --log-level=info actions invoke-local --topic-query="msgpaths[cpuload.load].max > 0.9"
```
{%- endif %}

Full usage:
```bash
$ .venv/bin/roboto actions invoke-local --help
```

#### Hosted Invocation

{% if cookiecutter.input_data_type == "files" %}
Example invocation:
```bash
# Process files matching a RoboQL query
$ .venv/bin/roboto actions invoke --file-query="dataset_id=ds_abc123 AND path LIKE 'logs/%.log'"
```
{%- else %}
Example invocation:
```bash
# Process topics matching a RoboQL query
$ .venv/bin/roboto actions invoke --topic-query="msgpaths[cpuload.load].max > 0.9"
```
{%- endif %}

Full usage:
```bash
$ .venv/bin/roboto actions invoke --help
```

### Deployment

Build and deploy to the Roboto Platform with the following commands:

```bash
$ ./scripts/build.sh
$ ./scripts/deploy.sh [ROBOTO_ORG_ID]
```

## Development

See [DEVELOPING.md](DEVELOPING.md) for detailed information about developing this action, including:
- Project structure and key files
- Local invocation
- Adding dependencies (runtime, system, and development)
- Working with action parameters (including secrets)
- Handling input and output data
- Building and deploying to Roboto
