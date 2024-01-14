import logging
import os
import unicodedata
from media_scanner.config import (
    MEDIA_EXTENSIONS,
    EXCLUDE_FOLDERS,
    TEMP_FOLDER,
    APP_MEDIA_SCAN_DIRS,
)
from typing import List


class DirectoryScanner:
    def __init__(self):
        self._scan_dirs = self.get_scan_paths()
        self._excluded_dirs = self.get_excluded_dirs()

    def get_scan_paths(self) -> List[str]:
        return APP_MEDIA_SCAN_DIRS

    def get_excluded_dirs(self) -> List[str]:
        excluded_dirs = []
        for scan_dir in self._scan_dirs:
            excluded_dirs.extend(
                os.path.join(scan_dir, folder) for folder in EXCLUDE_FOLDERS
            )
        return excluded_dirs

    def is_valid_media_file(self, file_path: str) -> bool:
        extension = os.path.splitext(file_path)[1]
        if extension not in MEDIA_EXTENSIONS:
            return False
        if any(
            file_path.startswith(excluded_dir) for excluded_dir in self._excluded_dirs
        ):
            return False
        return True

    def scan_for_media_files(self) -> List[str]:
        media_files = []

        for scan_dir in self._scan_dirs:
            if not os.path.isdir(scan_dir):
                logging.warning(f"Scan directory {scan_dir} does not exist")
                continue

            for dirpath, _, filenames in os.walk(scan_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if self.is_valid_media_file(file_path):
                        file_path = unicodedata.normalize("NFKD", file_path)
                        media_files.append(file_path)

        logging.info(f"Found {len(media_files)} media files")
        return media_files


class FileManager:
    def get_temp_dir(self) -> str:
        return TEMP_FOLDER

    def get_encode_temp_path(self, original_path: str) -> str:
        dest_dir = os.path.join(self.get_temp_dir(), "encodes")
        os.makedirs(dest_dir, exist_ok=True)
        return os.path.join(dest_dir, os.path.basename(original_path))

    def file_exist(self, path: str) -> bool:
        return os.path.isfile(path)

    def move_file(self, original_path: str, dest_path: str):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if original_path != dest_path:
            os.rename(original_path, dest_path)
            logging.info(f"Moved {original_path} to {dest_path}")

    def get_file_size_mb(self, file_path: str) -> float:
        return (
            float(f"{os.path.getsize(file_path) / 1024 / 1024:.2f}")
            if os.path.exists(file_path)
            else None
        )

    def move_original_to_temp(self, original_path: str):
        temp_path = os.path.join(
            self.get_temp_dir(), "originals", os.path.basename(original_path)
        )
        self.move_file(original_path, temp_path)
        logging.info(f"Moved {original_path} to {temp_path}")
