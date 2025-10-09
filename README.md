# firmware-investigate

A toolkit for investigating and reverse-engineering firmware and update tooling for Sena, Cardo, and Motorola Defy Satellite motorcycle headsets.

## Overview

This repository provides a reproducible scaffold to support reverse engineering of firmware update programs and installers for motorcycle communication headset manufacturers, starting with Sena, Cardo, and Motorola Defy Satellite. The toolkit is designed to be expandable for additional vendors.

## Features

- **Automated firmware downloader**: Downloads vendor firmware update programs/installers only if not already present
- **Multi-platform support**: Supports Windows and macOS updater downloads, plus Android APKs
- **Multi-vendor support**: Currently supports Sena, Cardo, and Motorola Defy Satellite, with architecture to easily add more
- **Python toolchain**: Clean Python package structure with `tox` for testing and linting
- **CI/CD**: Automated GitHub Actions workflows for continuous integration
- **Reproducible**: All downloads go to a `working/` directory that's git-ignored

## Installation

### From source

```bash
git clone https://github.com/holdenk/firmware-investigate.git
cd firmware-investigate
pip install -e .
```

### Development installation

For development with testing tools:

```bash
pip install -e ".[dev]"
# or
pip install -r requirements-dev.txt
```

## Usage

### Command-line interface

Download all vendor firmware tools (auto-detects platform):

```bash
firmware-investigate
```

Download only Sena firmware:

```bash
firmware-investigate --vendor sena
```

Download only Cardo firmware:

```bash
firmware-investigate --vendor cardo
```

Download only Motorola Defy Satellite firmware:

```bash
firmware-investigate --vendor motorola
```

Download Windows version on any platform:

```bash
firmware-investigate --platform windows
```

Download macOS version on any platform:

```bash
firmware-investigate --platform darwin
```

Specify a custom working directory:

```bash
firmware-investigate --working-dir /path/to/downloads
```

Force re-download even if files exist:

```bash
firmware-investigate --force
```

### Python API

```python
from firmware_investigate.downloaders import SenaDownloader, CardoDownloader, MotorolaDownloader

# Download Sena firmware for current platform
sena = SenaDownloader(working_dir="working")
sena.download()

# Download Sena firmware for Windows specifically
sena_win = SenaDownloader(working_dir="working", platform_override="windows")
sena_win.download()

# Download Cardo firmware for macOS specifically
cardo_mac = CardoDownloader(working_dir="working", platform_override="darwin")
cardo_mac.download()

# Download Motorola Defy Satellite firmware for Windows
motorola_win = MotorolaDownloader(working_dir="working", platform_override="windows")
motorola_win.download()
```

## Download Sources

The toolkit downloads firmware updater applications from the following sources:

### Sena
- **Windows**: https://firmware.sena.com/senabluetoothmanager/SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe
- **macOS**: https://firmware.sena.com/senabluetoothmanager/SENADeviceManagerForMAC-v4.4.16.pkg
- **Upstream source**: https://www.sena.com/en-us/support/device-manager/

### Cardo
- **Windows**: https://update.cardosystems.com/cardo-app/cardo_updater_win_latest.exe
- **macOS**: https://update.cardosystems.com/cardo-app/CardoUpdateLite_OTA_darwin_arm64_latest.dmg
- **Upstream source**: https://cardo.htskys.com/en/support/upadate-firmware/

### Motorola Defy Satellite
- **Android APK (via APKCombo)**: https://apkcombo.com/downloader/#package=com.bullitt.satellitemessenger (Bullitt Satellite Messenger app)
- **Play Store**: https://play.google.com/store/apps/details?id=com.bullitt.satellitemessenger
- **APKMirror**: https://www.apkmirror.com/apk/bullitt-group-limited/bullitt-satellite-messenger/
- **Note**: The Motorola Defy Satellite Link uses a phone app (Bullitt Satellite Messenger) for firmware updates, not a desktop application. Direct APK downloads may require manual intervention due to third-party APK repository restrictions.

## Development

### Running tests

Using tox (recommended):

```bash
tox
```

Using pytest directly:

```bash
pytest tests/
```

### Linting and formatting

Check code style:

```bash
tox -e lint
```

Format code:

```bash
tox -e format
```

Type checking:

```bash
tox -e type
```

### Project structure

```
firmware-investigate/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI configuration
├── src/
│   └── firmware_investigate/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       └── downloaders/
│           ├── __init__.py
│           ├── base.py     # Base downloader class
│           ├── sena.py     # Sena firmware downloader
│           ├── cardo.py    # Cardo firmware downloader
│           └── motorola.py # Motorola Defy Satellite firmware downloader
├── tests/                  # Test suite
├── working/                # Downloaded firmware files (git-ignored)
├── setup.py                # Package configuration
├── tox.ini                 # Tox configuration
└── README.md
```

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `tox`
2. Code is formatted: `tox -e format`
3. Type checking passes: `tox -e type`

## License

Apache License 2.0 - See LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Always respect intellectual property rights and terms of service when downloading and analyzing firmware.
