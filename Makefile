#######################################
######### Make configuration ##########
#######################################
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --silent

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

#######################################
############### Venv ##################
#######################################
PYTHON_MAJOR = 3
PYTHON_MINOR = 10
PYTHON_VERSION = python$(PYTHON_MAJOR).$(PYTHON_MINOR)
VENV_NAME := .venv
VENV_BIN := $(VENV_NAME)/bin
PYTHON = $(VENV_BIN)/python3
SITE_PACKAGES := $(VENV_NAME)/lib/$(PYTHON_VERSION)/site-packages

.venv:
> $(PYTHON_VERSION) -m venv --copies --upgrade-deps $(VENV_NAME)
> $(PYTHON) -m pip install poetry~=1.6

poetry.lock: .venv pyproject.toml
> $(PYTHON) -m poetry lock

install: .venv
> $(PYTHON) -m poetry install --no-root --sync
.PHONY: install-dev

# Clear proj dir of all .gitignored files
clean:
> git clean -Xfd
.PHONY: clean

#######################################
########### Code quality ##############
#######################################
fmt:
> $(PYTHON) -m black .
> $(PYTHON) -m autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .
> $(PYTHON) -m isort .
.PHONY: fmt

lint:
> $(PYTHON) -m flake8 --count --show-source --statistics --exclude '.venv,build,.mypy_cache,.pytest_cache' .
.PHONY: lint
