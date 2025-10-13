# firmware-investigate

A toolkit for investigating and reverse-engineering firmware and update tooling for Sena and Cardo motorcycle headsets.

## Overview

This repository provides a reproducible scaffold to support reverse engineering of firmware update programs and installers for motorcycle communication headset manufacturers, starting with Sena and Cardo. The toolkit is designed to be expandable for additional vendors.

## Features

- **Automated firmware downloader**: Downloads vendor firmware update programs/installers only if not already present
- **USB Gadget Device Faker**: Creates fake USB devices for Sena and Cardo to test firmware updaters (Linux only, requires root)
- **Multi-platform support**: Supports both Windows and macOS updater downloads
- **Multi-vendor support**: Currently supports Sena and Cardo, with architecture to easily add more
- **Strings analysis**: Extracts strings from binary files for reverse engineering
- **Network traffic interception**: Uses mitmproxy to capture and analyze firmware update traffic
- **Wine integration**: Runs Windows updaters on Linux/macOS with proxy configuration
- **USB device passthrough**: Configures USB device support for Sena and Cardo headsets
- **End-to-end workflow**: Single command to orchestrate the complete investigation process
- **Python toolchain**: Clean Python package structure with `tox` for testing and linting
- **CI/CD**: Automated GitHub Actions workflows for continuous integration
- **Reproducible**: All downloads go to a `working/` directory that's git-ignored

## Installation

### Using uv (recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer:

```bash
git clone https://github.com/holdenk/firmware-investigate.git
cd firmware-investigate
./setup-uv.sh
```

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

### Additional dependencies

For the end-to-end workflow, you may need:

- **Wine** (for running Windows executables): `sudo apt-get install wine` (Ubuntu/Debian) or `brew install wine-stable` (macOS)
- **strings** (for binary analysis): Usually included with binutils
- **mitmproxy** (installed automatically with the package)

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

### End-to-end workflow

Run the complete investigation workflow with a single command:

```bash
# Run complete workflow for all vendors
firmware-investigate-e2e --vendor all

# Run only for Sena
firmware-investigate-e2e --vendor sena

# Skip Wine execution (useful if Wine is not installed)
firmware-investigate-e2e --vendor all --skip-wine

# Skip strings analysis
firmware-investigate-e2e --vendor cardo --skip-strings

# Use existing downloads
firmware-investigate-e2e --skip-download --vendor all
```

The E2E workflow performs the following steps:
1. **Downloads** firmware updaters for the specified vendor(s)
2. **Analyzes** binaries using the `strings` command to extract readable strings
3. **Starts** mitmproxy to intercept network traffic
4. **Runs** updaters in Wine with proxy configuration
5. **Captures** and logs all HTTP/HTTPS traffic for analysis

USB device passthrough configuration:
- **Sena**: Vendor ID `0x0003`, Product ID `0x092B`
- **Cardo**: Vendor ID `0x2685`, Product ID `0x0900`
Check for USB devices:

```bash
firmware-investigate --check-usb-devices
```

Create fake USB devices for testing (requires root and Linux with USB gadget support):

```bash
sudo firmware-investigate --setup-usb-gadgets
```

Alternatively, use the standalone USB gadget module:

```bash
# Check if devices are present
python -m firmware_investigate.usb_gadget --check-only

# Create fake devices if not present
sudo python -m firmware_investigate.usb_gadget

# Force create devices even if real ones are present
sudo python -m firmware_investigate.usb_gadget --force

# Clean up fake devices
sudo python -m firmware_investigate.usb_gadget --cleanup
```

### Python API

#### Firmware Downloaders

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

## Documentation

- **[E2E Workflow Guide](E2E_GUIDE.md)**: Comprehensive guide for the end-to-end firmware investigation workflow
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the project
#### USB Gadget Faker

```python
from firmware_investigate import USBGadgetFaker

# Create faker instance
faker = USBGadgetFaker()

# Check if devices are present
sena_present = faker.check_device_present("0x0003", "0x092b")
cardo_present = faker.check_device_present("0x2685", "0x0900")

# Create fake devices if not present (requires root on Linux)
results = faker.setup_fake_devices(check_existing=True)

# Clean up fake devices
faker.cleanup()
```

## USB Device Information

The USB gadget faker creates fake devices with the following identifiers:

### Sena Device
- **Vendor ID**: 0x0003
- **Product ID**: 0x092b
- **Manufacturer**: Sena Technologies
- **Product**: Sena Bluetooth Device

### Cardo Device
- **Vendor ID**: 0x2685
- **Product ID**: 0x0900
- **Manufacturer**: Cardo Systems
- **Product**: Cardo Bluetooth Device

### Requirements for USB Gadget Functionality

The USB gadget faker requires:
- Linux operating system with USB gadget support
- ConfigFS mounted at `/sys/kernel/config/usb_gadget`
- Available USB Device Controller (UDC)
- Root privileges to create gadget devices

For testing purposes, you can load the `dummy_hcd` kernel module:
```bash
sudo modprobe dummy_hcd
```

Note: This functionality is primarily for testing firmware updaters in environments where physical devices are not available.

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
