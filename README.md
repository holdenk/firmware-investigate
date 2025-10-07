# firmware-investigate

A toolkit for investigating and reverse-engineering firmware and update tooling for Sena and Cardo motorcycle headsets.

## Overview

This repository provides a reproducible scaffold to support reverse engineering of firmware update programs and installers for motorcycle communication headset manufacturers, starting with Sena and Cardo. The toolkit is designed to be expandable for additional vendors.

## Features

- **Automated firmware downloader**: Downloads vendor firmware update programs/installers only if not already present
- **FCC ID lookup**: Quickly access FCC information for known devices (Sena 50S, Cardo Packtalk Bold, Motorola Defy Satellite)
- **Multi-platform support**: Supports both Windows and macOS updater downloads
- **Multi-vendor support**: Currently supports Sena and Cardo, with architecture to easily add more
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

#### Firmware Downloads

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

#### FCC ID Lookup

List all known devices and their FCC information:

```bash
fcc-lookup --list
```

Look up a specific device:

```bash
fcc-lookup --device sena_50s
fcc-lookup --device cardo_packtalk_bold
fcc-lookup --device motorola_defy_satellite
```

Look up an arbitrary FCC ID:

```bash
fcc-lookup --fcc-id Q95ER19
```

You can also use the standalone script:

```bash
python scripts/find_fcc_info.py --list
```

### Python API

#### Firmware Downloads

```python
from firmware_investigate.downloaders import SenaDownloader, CardoDownloader

# Download Sena firmware for current platform
sena = SenaDownloader(working_dir="working")
sena.download()

# Download Sena firmware for Windows specifically
sena_win = SenaDownloader(working_dir="working", platform_override="windows")
sena_win.download()

# Download Cardo firmware for macOS specifically
cardo_mac = CardoDownloader(working_dir="working", platform_override="darwin")
cardo_mac.download()
```

#### FCC Lookup

```python
from firmware_investigate.fcc_lookup import get_device_info, list_all_devices

# Get info for a specific device
sena_info = get_device_info("sena_50s")
print(f"FCC ID: {sena_info.fcc_id}")
print(f"FCC Report: {sena_info.fcc_report_url}")

# List all known devices
all_devices = list_all_devices()
for device in all_devices:
    print(f"{device.name}: {device.fcc_id}")
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

## FCC Information

The toolkit includes FCC ID information for the following devices:

### Sena 50S
- **FCC ID**: Q95ER19
- **FCC Report**: https://fcc.report/FCC-ID/Q95ER19
- **Manufacturer**: Sena Technologies

### Cardo Packtalk Bold
- **FCC ID**: UDO-DMCJBL
- **FCC Report**: https://fcc.report/FCC-ID/UDO-DMCJBL
- **Manufacturer**: Cardo Systems

### Motorola Defy Satellite
- **FCC ID**: IHDT56WJ1
- **FCC Report**: https://fcc.report/FCC-ID/IHDT56WJ1
- **Manufacturer**: Motorola Mobility (Lenovo)

The FCC reports contain detailed information about the devices including:
- Internal photos
- External photos
- Test reports
- User manuals
- Technical specifications
- Chip/component information

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
├── scripts/
│   └── find_fcc_info.py    # Standalone FCC lookup script
├── src/
│   └── firmware_investigate/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── fcc_lookup.py   # FCC ID lookup functionality
│       └── downloaders/
│           ├── __init__.py
│           ├── base.py     # Base downloader class
│           ├── sena.py     # Sena firmware downloader
│           └── cardo.py    # Cardo firmware downloader
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
