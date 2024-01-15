install:
	pipenv install .

install_dev:
	pipenv install --editable .

shell:
	pipenv shell

which:
	pipenv --venv

remove:
	pipenv --rm

pip_install:
	pip install -r requirements.txt

dump_requirements:
	pipenv requirements > requirements.txt

docker_build:
	docker build -t encoder .

run:
	docker run -it -e APP_MEDIA_SCAN_DIRS="/media" -v /Users/ernestas/Downloads/media:/media:rw encoder zsh

test:
	HandBrakeCLI --input /media/sample_960x400_ocean_with_audio.mkv --output sample_960x400_ocean_with_audio_encoded.mkv --preset-import-file /var/cli/presets/anime_opus.json -Z "Anime opus"
