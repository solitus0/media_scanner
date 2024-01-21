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
	docker run -it -v /Users/ernestas/Downloads/media:/media:rw -v ./var:/var/cli/var:rw -v ./presets:/presets:ro -v ./encodes:/encodes:rw --name encoder encoder zsh -c "bin/media_scanner.sh"

test2:
	process_scanner_output $(scanner get --not_video_codec="hevc" --not_audio_codec="opus")

test3:
	bin/process_scanner_output.zsh $(bin/run.sh get --not_video_codec="hevc" --not_audio_codec="opus")

scan_local:
	bin/run.sh scan

scan:
	scanner scan

encode:
	process_scanner_output $(scanner get --not_video_codec="hevc")
