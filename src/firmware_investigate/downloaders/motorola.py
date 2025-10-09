"""Motorola Defy firmware downloader."""

from typing import Optional

from .base import BaseDownloader


class MotorolaDownloader(BaseDownloader):
    """Downloader for Motorola Defy Satellite firmware update tools."""

    # APK sources for Motorola Defy Satellite Link updater
    # The Motorola Defy Satellite Link uses the Bullitt Satellite Messenger app
    # for firmware updates, which runs on Android phones

    # Note: Direct APK downloads from third-party sources are unreliable.
    # Users should download from official sources or trusted APK repositories.
    MOTOROLA_APK_URL = "https://apkcombo.com/downloader/#package=com.bullitt.satellitemessenger"

    # Upstream sources to check if download fails
    MOTOROLA_PLAYSTORE_URL = (
        "https://play.google.com/store/apps/details?id=com.bullitt.satellitemessenger"
    )
    MOTOROLA_APKMIRROR_URL = (
        "https://www.apkmirror.com/apk/bullitt-group-limited/bullitt-satellite-messenger/"
    )

    def __init__(self, working_dir: str = "working", platform_override: Optional[str] = None):
        """Initialize Motorola downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (not used for APK downloads).
        """
        super().__init__(working_dir, platform_override)

    def get_url(self) -> str:
        """Get the download URL for Motorola firmware tools.

        Returns:
            The URL to download the Bullitt Satellite Messenger APK from.
        """
        # APKs are platform-agnostic, so we return the same URL regardless of platform
        return self.MOTOROLA_APK_URL

    def get_filename(self) -> str:
        """Get the filename for the Motorola download.

        Returns:
            The filename to save as (APK file).
        """
        # APKs are platform-agnostic
        return "bullitt_satellite_messenger.apk"
