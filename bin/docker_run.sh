#!/bin/bash

export PIPENV_PIPFILE=/var/cli/Pipfile

pipenv run python /var/cli/src/media_scanner/cli.py "$@"
