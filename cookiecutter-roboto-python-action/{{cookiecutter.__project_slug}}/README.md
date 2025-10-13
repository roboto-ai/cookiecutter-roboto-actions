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

Set up a virtual environment and install dependencies:

```bash
$ ./scripts/setup.sh
```

### Invoking Locally

```bash
# See all available options
$ ./scripts/run.sh --help

# Run with parameters
$ ./scripts/run.sh --parameter foo=bar --parameter baz=qux -vv

# Run with dataset and file inputs
$ ./scripts/run.sh --dataset-id ds_123 --file-paths "**/*.log" -vv

# Run in dry-run mode (no side effects)
$ ./scripts/run.sh --parameter foo=bar --dry-run -vv
```

### Deployment

Build and deploy to the Roboto Platform:

```bash
$ ./scripts/build.sh
$ ./scripts/deploy.sh
```

## Development

See [DEVELOPING.md](DEVELOPING.md) for detailed information about developing this action, including:
- Adding dependencies
- Code organization and best practices
- Working with action parameters and input data
- Understanding the Docker-based development workflow
- Architecture and implementation details
