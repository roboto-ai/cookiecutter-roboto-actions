# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

## Setup

1. Ensure `python3` is available on your workstation and is a recent, supported version.

```bash
$ python3 --version
```

Prefer authoring your action with a version of Python that is compatible or more recent than the version specified in [.python-version](.python-version) on repository initialization. Update [.python-version](.python-version) as necessary.

[.python-version](.python-version) is included as a directive to [pyenv](https://github.com/pyenv/pyenv) and similar tools to set a matching version of Python while working in this repository.


2. Setup a virtual environment and install dependencies:

```bash
$ ./scripts/setup.sh
```

The virtual environment will be created in the root of the repository, under `.venv/`.

## Development

### Adding dependencies

#### Runtime dependencies

Add third-party Python libraries required at runtime by your action to `requirements.runtime.txt`.

#### System dependencies

While this action is written in Python, it is run by Roboto within a Docker container, defined in the [Dockerfile](Dockerfile). 

Some actions or third-party libraries require system dependencies that may be installed on your workstation,
but may not be already available in the container image.

To install additional system dependencies into the container image, add `RUN apt-get install` instructions in the [Dockerfile](Dockerfile).
See the commented section of the [Dockerfile](Dockerfile) beginning with `# -- INSTALL SYSTEM DEPENDENCIES --`.

Test the container's runtime environment before deployment to Roboto by building the image and (optionally) running it locally.

#### Development dependencies

Add Python-based tools used only as part of development and QA (such as linting and testing) to `requirements.dev.txt`.

### Code organization and best practices

This action was initialized with a `main.py` and two entrypoints, `bin/cli_entrypoint.py` and `bin/docker_entrypoint.py`.

#### `main.py`

The primary orchestrator of your action.

Simple actions may be defined in this single file, while more complicated actions benefit from being broken up into separate modules, then imported and orchestrated in this file.

Prefer exporting a single `main` function that takes an `Args` parameter object as its only argument.

#### `bin/cli_entrypoint.py`

Used as the entrypoint when running locally.

#### `bin/docker_entrypoint.py`
  
Used as the entrypoint when this action is run within a Docker container, including when run by Roboto on its hosted compute platform.

This entrypoint calls [`roboto.ActionRuntime.from_env`](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_runtime/index.html#roboto.action_runtime.action_runtime.ActionRuntime.from_env), which assumes it is running within a particular execution environment with many environment variables set.

It is unlikely that running this script directly on your workstation will work as intended.

## Input data and action parameters

A Roboto Action can be thought of as a function. Like functions, actions can define required or optional arguments. Actions refer to arguments as parameters. Parameters can be set when the action is invoked, either manually or by a Roboto Trigger.

Most actions will also operate on data uploaded to Roboto, and many will upload results back to Roboto.

Managing input data and action parameters in a way that seamlessly enables local development and execution of the action as well as production usage of the action on Roboto is critical.

### Action parameters

#### Defining parameters

Parameters are defined in [action.json](action.json).

##### Using parameters in your action

When run by Roboto on its hosted compute platform, action parameters are set as environment variables. As a convenience, the Roboto Python SDK exposes the [roboto.ActionRuntime](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_runtime/index.html#roboto.action_runtime.action_runtime.ActionRuntime) utility for retrieving parameter values and other execution environment-related information.

When running an action locally, you'll need to set parameters yourself. We recommend the following workflow:

- Maintain the argument interface used by your action's primary export in `main.py`.
In the example code this repository was initialized with, that interface looks like:

```python
class Args(argparse.Namespace):
  ...


def main(args: Args) -> None:
  ...
```

- As you add arguments to `Args`, update the `argparse.Parser` in `bin/cli_entrypoint.py` to match.
- Additionally, as you add arguments, update `bin/docker_entrypoint.py` to instantiate an instance of `Args`, setting values by using `roboto.ActionRuntime`.
- Avoid importing or making use of `roboto.ActionRuntime` in `main.py`, or otherwise depending on looking up environment variables.

The effect will be to remove testing your action locally from dependence on properly setting environment variables.
  - When run by Roboto in a Docker container, those environment variables will be set automatically.
  - When run by you locally, set parameters using the commandline as you see fit.


### Input data

#### Defining input data

Action authors generally have a well-defined set of input data they intend a given action to work with. For example, an action may expect to be given an `MCAP` file, extract its image data, and perform segmentation on those images. If that same action is given a text file instead, the action is unlikely to work.

Roboto enables two ways of specifying input data.

##### a. Input data specified at invocation time

In this form, input data must be specified as a glob pattern that matches one or more files from the specified dataset. For example, via the Roboto CLI:

```bash
$ roboto actions invoke --dataset-id <DATASET_ID> --input-data "**/*.mcap" <ACTION_NAME>
```

When an action is automatically triggered by a Roboto event (such as file upload),
the trigger will specify the input data for the action invocation.

This form of providing input data is most common when writing actions that will be invoked by an event-based trigger (e.g., `file_upload` or `file_ingested`)

#####  b. Query for data at runtime

In this form, the action code itself queries Roboto for data at runtime, freeing it to operate on any type of data queryable from the Roboto API. For example:

```python
import roboto

roboto_search = roboto.RobotoSearch()
for topic in roboto_search.find_topics("msgpaths[cpuload.load].max > 0.9"):
  ...
```

This form of providing input data is most common when writing an action performing batch processing that will be invoked manually or by a scheduled trigger (e.g., once a day every day).

#### Using input data in your action

##### a. Input data specified at invocation time

When input data is specified at action invocation, Roboto readies the data for use by downloading it into the isolated, ephemeral compute environment the action runs within.

For example, an action that is written to operate against `journal.log` files can be invoked by a trigger whenever any `journal.log` is uploaded to Roboto. When invoked, the specific `journal.log` whose upload triggered the action will be available to the action invocation via the filesystem, in a directory specified by the environment variable [`ROBOTO_INPUT_DIR`](https://docs.roboto.ai/reference/python-sdk/roboto/env/index.html#roboto.env.RobotoEnvKey.InputDir).

The Roboto Python SDK's [roboto.ActionRuntime](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_runtime/index.html#roboto.action_runtime.action_runtime.ActionRuntime) utility provides helpers for looking up and iterating this data.

For example, [roboto.ActionRuntime.input_dir](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_runtime/index.html#roboto.action_runtime.action_runtime.ActionRuntime.input_dir):
```python
import roboto

from ..main import Args, main

action_runtime = roboto.ActionRuntime.from_env()

args = Args(input_dir=action_runtime.input_dir)
main(args)
```

For example, [roboto.ActionRuntime.get_input](https://docs.roboto.ai/reference/python-sdk/roboto/action_runtime/action_runtime/index.html#roboto.action_runtime.action_runtime.ActionRuntime.get_input):
```python
import roboto

from ..main import Args, main

action_runtime = roboto.ActionRuntime.from_env()

args = Args(files=action_runtime.get_input().files)
main(args)
```

When running the action locally, download input data to test your action. By default, `bin/cli_entrypoint.py` treats the Git-ignored [input/] directory as its input data root.

##### b. Query for data at runtime

When actions are authored such that they do not assume presence of already-downloaded input data, they often instead make a runtime query for data.

In this case, it is the responsibility of the action author to download data at runtime if that is required as part of the action's processing.

## Running locally

```bash
$ ./scripts/run.sh --help
```

## Deployment

1. Build as Docker image:

```bash
$ ./scripts/build.sh
```

2. Deploy to Roboto Platform:

```bash
$ ./scripts/deploy.sh
```
