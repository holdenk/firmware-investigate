# firmware-investigate

A toolkit for investigating and reverse-engineering firmware and update tooling for Sena and Cardo motorcycle headsets.

## Overview

This repository provides a reproducible scaffold to support reverse engineering of firmware update programs and installers for motorcycle communication headset manufacturers, starting with Sena and Cardo. The toolkit is designed to be expandable for additional vendors.

## Features

- **Automated firmware downloader**: Downloads vendor firmware update programs/installers only if not already present
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

Download all vendor firmware tools:

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
from firmware_investigate.downloaders import SenaDownloader, CardoDownloader

# Download Sena firmware
sena = SenaDownloader(working_dir="working")
sena.download()

# Download Cardo firmware
cardo = CardoDownloader(working_dir="working")
cardo.download()
```

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
