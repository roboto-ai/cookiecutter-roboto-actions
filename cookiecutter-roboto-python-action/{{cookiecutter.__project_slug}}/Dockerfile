ARG PYTHON_MAJOR=3
ARG PYTHON_MINOR=12
ARG OS_VARIANT=slim-bookworm
FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:${PYTHON_MAJOR}.${PYTHON_MINOR}-${OS_VARIANT}

COPY requirements.runtime.txt ./
RUN python -m pip install --upgrade pip setuptools && python -m pip install -r requirements.runtime.txt

COPY src/{{ cookiecutter.__package_name }}/ ./{{ cookiecutter.__package_name }}

# Force the stdout and stderr streams to be unbuffered to decrease latency when viewing real-time action logs
# and to maximum context captured in logs if this action fails.
ENV PYTHONUNBUFFERED=0

# Pass args to your script at runtime by setting the CMD.
# Those args can be parsed by argparse, for example.
ENTRYPOINT [ "python", "-m", "{{ cookiecutter.__package_name }}" ]
