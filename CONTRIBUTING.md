# Contributing to firmware-investigate

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/holdenk/firmware-investigate.git
cd firmware-investigate
```

2. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

Or install development dependencies separately:
```bash
pip install -r requirements-dev.txt
```

## Running Tests

We use `pytest` for testing. Run tests with:

```bash
pytest tests/
```

Or use `tox` to test across multiple Python versions:

```bash
tox
```

## Code Quality

### Formatting

We use `black` for code formatting:

```bash
# Check formatting
black --check src/ tests/

# Auto-format code
black src/ tests/
# or
tox -e format
```

### Linting

We use `flake8` for linting:

```bash
flake8 src/ tests/ --max-line-length=100
# or
tox -e lint
```

### Type Checking

We use `mypy` for static type checking:

```bash
mypy src/firmware_investigate
# or
tox -e type
```

## Adding a New Vendor Downloader

To add support for a new firmware vendor:

1. Create a new file in `src/firmware_investigate/downloaders/` (e.g., `vendor_name.py`)
2. Implement a class that extends `BaseDownloader`
3. Implement the required abstract methods: `get_url()` and `get_filename()`
4. Support multiple platforms (Windows, macOS) by checking `self.platform`
5. Add the new downloader to `src/firmware_investigate/downloaders/__init__.py`
6. Create corresponding tests in `tests/test_vendor_name_downloader.py`
7. Update the CLI to support the new vendor in `src/firmware_investigate/cli.py`

Example:

```python
from typing import Optional
from .base import BaseDownloader

class NewVendorDownloader(BaseDownloader):
    """Downloader for NewVendor firmware update tools."""

    # Platform-specific URLs
    NEW_VENDOR_WINDOWS_URL = "https://www.newvendor.com/downloads/updater-win.exe"
    NEW_VENDOR_MACOS_URL = "https://www.newvendor.com/downloads/updater-mac.dmg"
    NEW_VENDOR_UPSTREAM_URL = "https://www.newvendor.com/support/downloads/"

    def __init__(
        self, working_dir: str = "working", platform_override: Optional[str] = None
    ):
        """Initialize NewVendor downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (windows, darwin).
        """
        super().__init__(working_dir, platform_override)

    def get_url(self) -> str:
        """Get the download URL based on platform."""
        if self.platform == "windows":
            return self.NEW_VENDOR_WINDOWS_URL
        elif self.platform == "darwin":
            return self.NEW_VENDOR_MACOS_URL
        else:
            # Default to Windows if platform not recognized
            return self.NEW_VENDOR_WINDOWS_URL

    def get_filename(self) -> str:
        """Get the filename based on platform."""
        if self.platform == "windows":
            return "NewVendorUpdater_Setup.exe"
        elif self.platform == "darwin":
            return "NewVendorUpdater.dmg"
        else:
            return "NewVendorUpdater_Setup.exe"
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass (`tox`)
5. Format your code (`tox -e format`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code of Conduct

Please be respectful and constructive in all interactions. This is a research and educational project.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
