"""Sena firmware downloader."""

from .base import BaseDownloader


class SenaDownloader(BaseDownloader):
    """Downloader for Sena firmware update tools."""

    # URL for Sena Device Manager (common firmware update tool)
    # This is the Windows installer for the device manager
    SENA_URL = "https://www.sena.com/downloads/download/11301"
    SENA_FILENAME = "SenaDeviceManager_Setup.exe"

    def get_url(self) -> str:
        """Get the download URL for Sena firmware tools.

        Returns:
            The URL to download from.
        """
        return self.SENA_URL

    def get_filename(self) -> str:
        """Get the filename for the Sena download.

        Returns:
            The filename to save as.
        """
        return self.SENA_FILENAME
