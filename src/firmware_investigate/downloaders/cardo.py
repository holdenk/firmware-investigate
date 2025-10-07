"""Cardo firmware downloader."""

from .base import BaseDownloader


class CardoDownloader(BaseDownloader):
    """Downloader for Cardo firmware update tools."""

    # URL for Cardo Updater (common firmware update tool)
    # This is the Windows installer for the updater software
    CARDO_URL = "https://www.cardosystems.com/software-downloads/"
    CARDO_FILENAME = "CardoUpdater_Setup.exe"

    def get_url(self) -> str:
        """Get the download URL for Cardo firmware tools.

        Returns:
            The URL to download from.
        """
        return self.CARDO_URL

    def get_filename(self) -> str:
        """Get the filename for the Cardo download.

        Returns:
            The filename to save as.
        """
        return self.CARDO_FILENAME
