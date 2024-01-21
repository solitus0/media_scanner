FROM python:3.10-slim

ENV APP_MEDIA_SCAN_DIRS=/media
ENV ENCODES_TEMP_DIR=/encodes
ENV ORIGINALS_DIR=/originals
ENV PRESETS_DIR=/presets

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip setuptools supervisor && \
    pip3 install --ignore-installed distlib pipenv

RUN apt-get update && apt-get install -y \
    software-properties-common \
    ffmpeg \
    handbrake-cli \
    zsh \
    make \
    procps \
    inotify-tools \
    jq

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /var/cli

COPY . /var/cli

RUN --mount=type=cache,target=/root/.cache/pip \
    pipenv install .

COPY supervisord.conf /etc/supervisord.conf
COPY bin/cli.sh /usr/local/bin/scanner
COPY bin/process_scanner_output.zsh /usr/local/bin/process_scanner_output

RUN chmod +x /usr/local/bin/scanner
RUN chmod +x /usr/local/bin/process_scanner_output

VOLUME [ "/media" ]
VOLUME [ "/originals" ]
VOLUME [ "/encodes" ]
VOLUME [ "/presets" ]

ENTRYPOINT ["/bin/zsh", "-c"]

CMD ["supervisord", ,"-n", "-c", "/etc/supervisord.conf"]
