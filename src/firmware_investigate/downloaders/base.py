"""Base downloader class for firmware downloads."""

import platform
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseDownloader(ABC):
    """Base class for firmware downloaders."""

    def __init__(self, working_dir: str = "working", platform_override: Optional[str] = None):
        """Initialize the downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (windows, darwin, linux).
        """
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform_override or platform.system().lower()

    @abstractmethod
    def get_url(self) -> str:
        """Get the download URL for the firmware.

        Returns:
            The URL to download the firmware from.
        """
        pass

    @abstractmethod
    def get_filename(self) -> str:
        """Get the filename to save the downloaded firmware as.

        Returns:
            The filename for the downloaded file.
        """
        pass

    def get_filepath(self) -> Path:
        """Get the full path where the file will be saved.

        Returns:
            Path object pointing to the download location.
        """
        return self.working_dir / self.get_filename()

    def file_exists(self) -> bool:
        """Check if the firmware file already exists.

        Returns:
            True if the file exists, False otherwise.
        """
        return self.get_filepath().exists()

    def download(self, force: bool = False) -> Optional[Path]:
        """Download the firmware if not already present.

        Args:
            force: If True, download even if file already exists.

        Returns:
            Path to the downloaded file, or None if download was skipped.
        """
        filepath = self.get_filepath()

        if self.file_exists() and not force:
            print(f"File already exists: {filepath}")
            return None

        print(f"Downloading {self.get_filename()} from {self.get_url()}...")

        try:
            import urllib.request

            urllib.request.urlretrieve(self.get_url(), filepath)
            print(f"Downloaded to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error downloading file: {e}")
            raise
