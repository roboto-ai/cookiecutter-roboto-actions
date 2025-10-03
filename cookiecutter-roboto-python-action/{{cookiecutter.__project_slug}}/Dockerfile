ARG PYTHON_MAJOR=3
ARG PYTHON_MINOR=12
ARG OS_VARIANT=slim-bookworm
FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:${PYTHON_MAJOR}.${PYTHON_MINOR}-${OS_VARIANT}

# -- INSTALL SYSTEM DEPENDENCIES --
# Uncomment the following RUN instruction and add the package name(s) to the apt-get install command.
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#       <PKG_NAME_1> \
#       <PKG_NAME_2> && \
#     rm -rf /var/lib/apt/lists/*

# -- INSTALL THIRD-PARTY PYTHON LIBRARIES --
COPY requirements.runtime.txt ./
RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install -r requirements.runtime.txt

COPY src/{{ cookiecutter.__package_name }}/ ./{{ cookiecutter.__package_name }}

# Force the stdout and stderr streams to be unbuffered to decrease latency when viewing real-time action logs
# and to maximize context captured in logs if this action fails.
ENV PYTHONUNBUFFERED=0

ENTRYPOINT [ "python", "-m", "{{ cookiecutter.__package_name }}.bin.docker_entrypoint" ]
