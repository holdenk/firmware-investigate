# End-to-End Workflow Guide

This guide explains how to use the end-to-end (E2E) firmware investigation workflow.

## Overview

The E2E workflow automates the complete process of investigating firmware updaters:

1. **Download**: Fetch firmware updater applications from vendor websites
2. **Analyze**: Extract strings from binaries for reverse engineering
3. **Intercept**: Start mitmproxy to capture network traffic
4. **Execute**: Run updaters in Wine with proxy configuration
5. **Capture**: Log all HTTP/HTTPS requests and responses

## Prerequisites

### Required
- Python 3.8 or higher
- mitmproxy (installed automatically with the package)

### Optional
- **Wine**: For running Windows executables
  - Ubuntu/Debian: `sudo apt-get install wine`
  - macOS: `brew install wine-stable`
- **strings**: For binary analysis (usually included with binutils)
  - Ubuntu/Debian: `sudo apt-get install binutils`
  - macOS: Usually pre-installed

## Quick Start

### 1. Install the package

Using uv (recommended):
```bash
./setup-uv.sh
```

Or with pip:
```bash
pip install -e .
```

### 2. Run the E2E workflow

Basic usage (all vendors):
```bash
firmware-investigate-e2e --vendor all
```

For specific vendor:
```bash
firmware-investigate-e2e --vendor sena
```

Skip Wine execution (if Wine is not installed):
```bash
firmware-investigate-e2e --vendor all --skip-wine
```

## Workflow Steps Explained

### Step 1: Download Firmware Updaters

Downloads the latest firmware updater applications from:
- **Sena**: Windows Device Manager (v4.4.16)
- **Cardo**: Windows Update Manager

Files are saved to the `working/` directory by default.

### Step 2: Strings Analysis

Extracts all readable strings from the downloaded binaries using the `strings` command. This helps identify:
- URLs and endpoints
- API keys or tokens
- Debug messages
- Error messages
- File paths

Output is saved to `working/strings_analysis/`.

### Step 3: Start mitmproxy

Launches mitmproxy in the background to intercept network traffic:
- Listens on `127.0.0.1:8080` by default
- Captures all HTTP/HTTPS traffic
- Logs requests and responses to JSONL files
- Saves firmware binaries if detected

Configuration:
- SSL certificate validation is disabled for HTTPS interception
- Custom addon script logs detailed traffic information

### Step 4: Run Updaters in Wine

Executes Windows updaters using Wine with:
- Proxy environment variables set (`http_proxy`, `https_proxy`)
- Custom Wine prefix to isolate the environment
- USB device passthrough configuration:
  - **Sena**: Vendor ID `0x0003`, Product ID `0x092B`
  - **Cardo**: Vendor ID `0x2685`, Product ID `0x0900`

Note: USB passthrough requires additional Wine/QEMU configuration.

### Step 5: Cleanup and Summary

- Stops mitmproxy gracefully
- Displays summary of captured traffic
- Lists output file locations

## Output Files

After running the E2E workflow, you'll find:

```
working/
├── SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe
├── CardoUpdater_Setup.exe
├── strings_analysis/
│   ├── SenaDeviceManagerForWindows-v4.4.16-setup_x64_strings.txt
│   └── CardoUpdater_Setup_strings.txt
├── mitmproxy/
│   ├── traffic.mitm              # Binary flow file (open with mitmproxy)
│   ├── requests.jsonl            # HTTP/HTTPS requests
│   ├── responses.jsonl           # HTTP/HTTPS responses
│   ├── firmware_addon.py         # Mitmproxy addon script
│   └── firmware_*.bin            # Captured firmware binaries (if any)
└── wine_prefix/                  # Wine environment (isolated)
```

## Advanced Usage

### Custom Working Directory

```bash
firmware-investigate-e2e --working-dir /tmp/my-investigation --vendor cardo
```

### Skip Specific Steps

```bash
# Use existing downloads
firmware-investigate-e2e --skip-download

# Skip strings analysis
firmware-investigate-e2e --skip-strings

# Skip Wine execution
firmware-investigate-e2e --skip-wine

# Combine multiple skips
firmware-investigate-e2e --skip-strings --skip-wine
```

### Platform Selection

```bash
# Download macOS updaters instead of Windows
firmware-investigate-e2e --platform darwin
```

## Analyzing the Results

### View Captured Traffic in mitmproxy

```bash
mitmproxy -r working/mitmproxy/traffic.mitm
```

### Parse Request/Response Logs

```bash
# View all requests
cat working/mitmproxy/requests.jsonl | jq '.'

# Extract URLs
cat working/mitmproxy/requests.jsonl | jq -r '.url'

# View responses with status codes
cat working/mitmproxy/responses.jsonl | jq '{id, status_code, content_length}'
```

### Search Strings Output

```bash
# Find URLs in strings
grep -i "http" working/strings_analysis/*.txt

# Find potential API endpoints
grep -i "api" working/strings_analysis/*.txt

# Find version strings
grep -i "version" working/strings_analysis/*.txt
```

## Troubleshooting

### Wine Not Installed

If Wine is not installed, use `--skip-wine`:
```bash
firmware-investigate-e2e --vendor all --skip-wine
```

### strings Command Not Found

Install binutils:
```bash
# Ubuntu/Debian
sudo apt-get install binutils

# macOS
# Usually pre-installed
```

### mitmproxy Fails to Start

Check if another process is using port 8080:
```bash
lsof -i :8080
```

Kill the process or change the port in the source code.

### No Traffic Captured

Possible reasons:
- Updater doesn't make network requests without device connected
- Updater uses non-standard proxy configuration
- Updater requires administrator/root privileges

## USB Device Passthrough

The E2E workflow configures USB device passthrough for:

### Sena Devices
- Vendor ID: `0x0003`
- Product ID: `0x092B`

### Cardo Devices
- Vendor ID: `0x2685`
- Product ID: `0x0900`

Note: Actual USB passthrough requires additional configuration:
1. Wine with QEMU or VirtualBox backend
2. USB device rules in `/etc/udev/rules.d/`
3. User permissions for USB devices

## Python API

You can also use the workflow components programmatically:

```python
from pathlib import Path
from firmware_investigate.downloaders import SenaDownloader
from firmware_investigate.analyzer import StringsAnalyzer
from firmware_investigate.mitmproxy_manager import MitmproxyManager
from firmware_investigate.wine_runner import WineRunner

# Download
downloader = SenaDownloader(working_dir="working", platform_override="windows")
filepath = downloader.download()

# Analyze
analyzer = StringsAnalyzer(min_length=4)
strings = analyzer.analyze(filepath, output_file=Path("working/sena_strings.txt"))

# Start proxy
mitm = MitmproxyManager(port=8080, output_dir=Path("working/mitm"))
process = mitm.start(background=True)

# Run in Wine
wine = WineRunner(
    wine_prefix=Path("working/wine_prefix"),
    proxy_host="127.0.0.1",
    proxy_port=8080
)
result = wine.run(
    executable=filepath,
    usb_devices=[{"vendor_id": "0x0003", "product_id": "0x092B"}]
)

# Stop proxy
mitm.stop()
```

## Next Steps

1. Review captured traffic for interesting endpoints
2. Analyze strings output for hardcoded secrets or URLs
3. Examine firmware binaries with reverse engineering tools
4. Document findings and patterns
5. Contribute improvements back to the project

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request!
