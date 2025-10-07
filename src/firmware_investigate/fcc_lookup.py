"""FCC ID lookup and chip identification for devices."""

import json
import urllib.request
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    """Information about a device and its FCC filings."""

    name: str
    fcc_id: str
    manufacturer: str
    fcc_report_url: str
    notes: Optional[str] = None


# Known devices and their FCC IDs
KNOWN_DEVICES = {
    "sena_50s": DeviceInfo(
        name="Sena 50S",
        fcc_id="Q95ER19",
        manufacturer="Sena Technologies",
        fcc_report_url="https://fcc.report/FCC-ID/Q95ER19",
        notes="Motorcycle communication headset",
    ),
    "cardo_packtalk_bold": DeviceInfo(
        name="Cardo Packtalk Bold",
        fcc_id="UDO-DMCJBL",
        manufacturer="Cardo Systems",
        fcc_report_url="https://fcc.report/FCC-ID/UDO-DMCJBL",
        notes="Motorcycle communication headset with JBL speakers",
    ),
    "motorola_defy_satellite": DeviceInfo(
        name="Motorola Defy Satellite",
        fcc_id="IHDT56WJ1",
        manufacturer="Motorola Mobility (Lenovo)",
        fcc_report_url="https://fcc.report/FCC-ID/IHDT56WJ1",
        notes="Satellite communication capable smartphone",
    ),
}


def get_device_info(device_key: str) -> Optional[DeviceInfo]:
    """Get FCC information for a known device.

    Args:
        device_key: Key for the device in KNOWN_DEVICES dict.

    Returns:
        DeviceInfo object if device is known, None otherwise.
    """
    return KNOWN_DEVICES.get(device_key)


def list_all_devices() -> List[DeviceInfo]:
    """Get a list of all known devices.

    Returns:
        List of DeviceInfo objects for all known devices.
    """
    return list(KNOWN_DEVICES.values())


def fetch_fcc_data(fcc_id: str) -> Dict:
    """Fetch FCC data from fcc.report API.

    Args:
        fcc_id: The FCC ID to look up (e.g., "Q95ER19").

    Returns:
        Dictionary containing FCC data from the API.

    Raises:
        urllib.error.HTTPError: If the API request fails.
    """
    # fcc.report provides a simple JSON API
    api_url = f"https://fcc.report/api/v1/fcc-id/{fcc_id}"

    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"FCC ID '{fcc_id}' not found") from e
        raise


def print_device_info(device: DeviceInfo) -> None:
    """Print formatted device information.

    Args:
        device: DeviceInfo object to print.
    """
    print(f"\nDevice: {device.name}")
    print(f"Manufacturer: {device.manufacturer}")
    print(f"FCC ID: {device.fcc_id}")
    print(f"FCC Report URL: {device.fcc_report_url}")
    if device.notes:
        print(f"Notes: {device.notes}")


def print_all_devices() -> None:
    """Print information about all known devices."""
    print("=" * 80)
    print("FCC Information for Known Devices")
    print("=" * 80)

    for device in list_all_devices():
        print_device_info(device)
        print("-" * 80)


def main() -> int:
    """Main entry point for FCC lookup tool.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="FCC ID lookup tool for motorcycle headsets and devices"
    )

    parser.add_argument(
        "--device",
        choices=list(KNOWN_DEVICES.keys()),
        help="Look up a specific device by key",
    )

    parser.add_argument(
        "--fcc-id",
        help="Look up an arbitrary FCC ID from the API",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all known devices",
    )

    args = parser.parse_args()

    if args.list or (not args.device and not args.fcc_id):
        print_all_devices()
        return 0

    if args.device:
        device = get_device_info(args.device)
        if device:
            print_device_info(device)

            # Try to fetch additional data from API
            print("\nFetching additional data from FCC API...")
            try:
                api_data = fetch_fcc_data(device.fcc_id)
                print(f"\nAPI Data available for: {device.fcc_id}")
                print(json.dumps(api_data, indent=2))
            except Exception as e:
                print(f"Could not fetch API data: {e}", file=sys.stderr)
        else:
            print(f"Unknown device: {args.device}", file=sys.stderr)
            return 1

    if args.fcc_id:
        try:
            print(f"Fetching FCC data for: {args.fcc_id}")
            data = fetch_fcc_data(args.fcc_id)
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error fetching FCC data: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
