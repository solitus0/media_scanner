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
	docker run -it -v /Users/ernestas/Downloads/media:/media:rw -v ./var:/var/cli/var -v ./presets:/presets encoder zsh

test:
	HandBrakeCLI --input /media/sample_960x400_ocean_with_audio.mkv --output sample_960x400_ocean_with_audio_encoded.mkv --preset-import-file /var/cli/presets/anime_opus.json -Z "Anime opus"

not_hevc:
	scanner get --not_video_codec="hevc"| ./process_scanner_output.zsh

not_opus:
	scanner get --not_audio_codec="opus"| ./process_scanner_output.zsh

audio_info:
	ffprobe -v error -select_streams a -show_entries stream=index,codec_name,codec_long_name,channels,channel_layout,sample_rate,bit_rate -of default=noprint_wrappers=1:nokey=1 "originals/sample_960x400_ocean_with_audio 2.mkv"

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
