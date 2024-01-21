#!/bin/bash

PIPENV_DONT_LOAD_ENV=1 pipenv run python /Users/ernestas/Projects/media_scanner/src/media_scanner/cli.py "$@"
