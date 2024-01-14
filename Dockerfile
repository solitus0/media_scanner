FROM python:3.10-slim

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip setuptools && \
    pip3 install --ignore-installed distlib pipenv

RUN apt-get update && apt-get install -y \
    software-properties-common \
    ffmpeg \
    handbrake-cli \
    zsh \
    make

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /var/cli

COPY . /var/cli

RUN --mount=type=cache,target=/root/.cache/pip \
    pipenv install .

COPY bin/docker_run.sh /usr/local/bin/scanner
RUN chmod +x /usr/local/bin/scanner


CMD ["python3"]
