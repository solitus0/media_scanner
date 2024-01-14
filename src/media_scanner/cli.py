#!/usr/bin/env python3

import click
from media_scanner.scanner.file_system import DirectoryScanner
from media_scanner.scanner.ffmpeg_wrapper import FfmpegWrapper
from media_scanner.scanner import repository
from media_scanner.database import get_db
from media_scanner.scanner.schemas import MediaQuery
import logging


@click.command()
@click.option("--soft", default=False, help="Soft scan, adds only new files.")
def scan(soft: bool):
    db = get_db()
    scanner = DirectoryScanner()
    media_files = scanner.scan_for_media_files()

    for media_file in media_files:
        media_entity = repository.get_by_file_path(db, media_file)
        if media_entity and soft:
            continue

        try:
            ffmpeg_wrapper = FfmpegWrapper(media_file)
            data = ffmpeg_wrapper.data

            if media_entity:
                if repository.should_update(data, media_entity):
                    repository.update_media(db, media_entity, data)
            else:
                logging.info(f"Creating new media: {data.file_path}")
                repository.create_media(db, data)
        except Exception as e:
            logging.error(f"Error processing media file: {e}")

    db.close()


@click.command()
@click.option("--video_codec", type=str)
@click.option("--audio_codec", type=str)
@click.option("--sub_codec", type=str)
@click.option("--batch_size", type=int, default=10, help="Batch size")
@click.option("--page", type=int, default=1, help="Page")
@click.option("--min_size", type=int, default=None, help="Min size in MB")
def get(
    video_codec: str,
    audio_codec: str,
    sub_codec: str,
    batch_size: int,
    page: int,
    min_size: int,
):
    query = MediaQuery.model_construct(
        video_codec=video_codec,
        audio_codec=audio_codec,
        subtitle_codec=sub_codec,
        batch_size=batch_size,
        page=page,
        min_size=min_size,
    )

    db = get_db()
    result = repository.get_by_filter(db, query)

    for item in result:
        click.echo(item.file_path)

    db.close()


@click.group()
def cli():
    pass


cli.add_command(scan)
cli.add_command(get)


if __name__ == "__main__":
    cli()
