#!/bin/zsh

inotifywait -m /media -e create -e delete | while read path action file; do
    echo "The file '$file' appeared in directory '$path' via '$action'"
    PIPENV_DONT_LOAD_ENV=1 pipenv run python /var/cli/src/media_scanner/cli.py scan --soft
done
