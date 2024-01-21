#!/bin/sh

PIPENV_DONT_LOAD_ENV=1 pipenv run python /var/cli/src/media_scanner/cli.py "$@"
