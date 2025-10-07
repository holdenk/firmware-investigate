# Working Directory

This directory is used to store downloaded firmware update programs and installers.

Files downloaded here are git-ignored and are only downloaded if they don't already exist.

## Downloaded Files

When you run the `firmware-investigate` tool, firmware update programs will be downloaded to this directory:

- `SenaDeviceManager_Setup.exe` - Sena firmware update tool
- `CardoUpdater_Setup.exe` - Cardo firmware update tool

## Purpose

This directory structure ensures:
1. Downloaded files are not accidentally committed to version control
2. Downloads are only performed once (unless forced with `--force` flag)
3. A clean separation between source code and downloaded artifacts
