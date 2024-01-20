#!/usr/bin/env python3

import click
from media_scanner.scanner.file_system import DirectoryScanner, FileManager
from media_scanner.scanner.ffmpeg_wrapper import FfmpegWrapper
from media_scanner.scanner import repository
from media_scanner.database import get_db
from media_scanner.scanner.schemas import MediaQuery
from click.termui import progressbar
import logging


@click.command()
@click.option("--soft", default=False, help="Soft scan, adds only new files.")
def scan(soft: bool):
    db = get_db()
    scanner = DirectoryScanner()
    click.echo(f"Scanning for media files in {scanner.get_scan_paths()}")
    media_files = scanner.scan_for_media_files()
    click.echo(f"Found {len(media_files)} media files.")

    with progressbar(media_files, label="Scanning Media Files:") as bar:
        for media_file in bar:
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

    all_media = repository.all(db)
    for media in all_media:
        if FileManager().file_exist(media.file_path):
            continue

        repository.delete(db, media)

    db.close()


@click.command()
@click.option("--video_codec", type=str)
@click.option("--not_video_codec", type=str)
@click.option("--audio_codec", type=str)
@click.option("--not_audio_codec", type=str)
@click.option("--subtitle_codec", type=str)
@click.option("--not_subtitle_codec", type=str)
@click.option("--batch_size", type=int, default=10, help="Batch size")
@click.option("--page", type=int, default=1, help="Page")
@click.option("--min_size", type=int, default=None, help="Min size in MB")
@click.option("--query", type=str, default=None, help="Query")
def get(
    video_codec: str,
    not_video_codec: str,
    audio_codec: str,
    not_audio_codec: str,
    subtitle_codec: str,
    not_subtitle_codec: str,
    batch_size: int,
    page: int,
    min_size: int,
    query: str,
):
    query = MediaQuery.model_construct(
        video_codec=video_codec,
        not_video_codec=not_video_codec,
        audio_codec=audio_codec,
        not_audio_codec=not_audio_codec,
        subtitle_codec=subtitle_codec,
        not_subtitle_codec=not_subtitle_codec,
        batch_size=batch_size,
        page=page,
        min_size=min_size,
        query=query,
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
