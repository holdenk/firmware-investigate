#!/usr/bin/env python3
"""End-to-end run script for firmware investigation workflow.

This script orchestrates the complete workflow:
1. Download firmware updaters
2. Run strings analysis on binaries
3. Start mitmproxy
4. Run updaters in Wine with proxy configured
5. Analyze captured traffic
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Tuple, Type

from firmware_investigate.analyzer import StringsAnalyzer
from firmware_investigate.downloaders import CardoDownloader, SenaDownloader
from firmware_investigate.downloaders.base import BaseDownloader
from firmware_investigate.mitmproxy_manager import MitmproxyManager
from firmware_investigate.virtualbox_runner import VirtualBoxRunner
from firmware_investigate.wine_runner import WineRunner


# USB device configurations
SENA_USB_DEVICES = [
    {"vendor_id": "0x0003", "product_id": "0x092B"},
]

CARDO_USB_DEVICES = [
    {"vendor_id": "0x2685", "product_id": "0x0900"},
]


def run_e2e(
    vendor: str,
    working_dir: Path,
    platform: str = "windows",
    skip_download: bool = False,
    skip_strings: bool = False,
    skip_wine: bool = False,
) -> int:
    """Run the end-to-end firmware investigation workflow.

    Args:
        vendor: Vendor to investigate ('sena', 'cardo', or 'all').
        working_dir: Working directory for downloads and analysis.
        platform: Platform to download for (default: 'windows').
        skip_download: Skip download step if files already exist.
        skip_strings: Skip strings analysis step.
        skip_wine: Skip Wine execution step.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    print("=" * 80)
    print("Firmware Investigation E2E Workflow")
    print("=" * 80)
    print(f"Vendor: {vendor}")
    print(f"Working directory: {working_dir}")
    print(f"Platform: {platform}")
    print()

    # Determine which vendors to process
    vendors_to_process: List[Tuple[str, Type[BaseDownloader], List[dict[str, str]]]] = []
    if vendor in ["sena", "all"]:
        vendors_to_process.append(("Sena", SenaDownloader, SENA_USB_DEVICES))
    if vendor in ["cardo", "all"]:
        vendors_to_process.append(("Cardo", CardoDownloader, CARDO_USB_DEVICES))

    # Step 1: Download firmware updaters
    if not skip_download:
        print("\n" + "=" * 80)
        print("STEP 1: Downloading Firmware Updaters")
        print("=" * 80)

        for vendor_name, downloader_class, _ in vendors_to_process:
            print(f"\n{vendor_name}:")
            downloader = downloader_class(
                working_dir=str(working_dir),
                platform_override=platform,
            )

            try:
                result = downloader.download(force=False)
                if result:
                    print(f"✓ Downloaded to: {result}")
                else:
                    print(f"✓ File already exists: {downloader.get_filepath()}")
            except Exception as e:
                print(f"✗ Error downloading: {e}")
                return 1
    else:
        print("\n[SKIPPED] Download step (--skip-download)")

    # Step 2: Run strings analysis
    if not skip_strings:
        print("\n" + "=" * 80)
        print("STEP 2: Strings Analysis")
        print("=" * 80)

        analyzer = StringsAnalyzer(min_length=4)
        strings_output_dir = working_dir / "strings_analysis"
        strings_output_dir.mkdir(parents=True, exist_ok=True)

        for vendor_name, downloader_class, _ in vendors_to_process:
            downloader = downloader_class(
                working_dir=str(working_dir),
                platform_override=platform,
            )
            filepath = downloader.get_filepath()

            if filepath.exists():
                print(f"\nAnalyzing {vendor_name}: {filepath.name}")
                output_file = strings_output_dir / f"{filepath.stem}_strings.txt"

                try:
                    strings_list = analyzer.analyze(filepath, output_file=output_file)
                    print(f"✓ Found {len(strings_list)} strings")
                    print(f"✓ Saved to: {output_file}")
                except Exception as e:
                    print(f"✗ Error analyzing: {e}")
            else:
                print(f"\n⚠ Skipping {vendor_name}: file not found at {filepath}")
    else:
        print("\n[SKIPPED] Strings analysis (--skip-strings)")

    # Step 3: Start mitmproxy
    print("\n" + "=" * 80)
    print("STEP 3: Starting mitmproxy")
    print("=" * 80)

    mitmproxy_dir = working_dir / "mitmproxy"
    mitm_manager = MitmproxyManager(port=8080, output_dir=mitmproxy_dir)

    try:
        mitm_process = mitm_manager.start(background=True)
        print("✓ mitmproxy started successfully")
        print("  Listening on: 127.0.0.1:8080")
        print(f"  Output directory: {mitmproxy_dir}")
    except Exception as e:
        print(f"✗ Failed to start mitmproxy: {e}")
        print("  Note: mitmproxy must be installed separately")
        print("  - macOS: brew install mitmproxy")
        print("  - Linux/Windows: Download from https://mitmproxy.org/")
        print("  Continuing without proxy...")
        mitm_process = None

    # Step 4: Run updaters in VirtualBox or Wine
    if not skip_wine:
        print("\n" + "=" * 80)
        print("STEP 4: Running Updaters")
        print("=" * 80)

        # Check for VirtualBox first (preferred for USB passthrough)
        vbox_runner = VirtualBoxRunner(
            vm_name="firmware-investigate-vm",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )

        wine_runner = WineRunner(
            wine_prefix=working_dir / "wine_prefix",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )

        # Prefer VirtualBox if available and VM exists
        if vbox_runner.check_virtualbox_installed() and vbox_runner.check_vm_exists():
            print("✓ Using VirtualBox runner (supports USB passthrough)")
            runner = vbox_runner
            runner_name = "VirtualBox"
        elif wine_runner.check_wine_installed():
            print("✓ Using Wine runner (USB passthrough not supported)")
            print(
                "  For USB support, install VirtualBox and create a VM named "
                "'firmware-investigate-vm'"
            )
            runner = wine_runner
            runner_name = "Wine"
        else:
            print("✗ No suitable runner found")
            print("  Install Wine or VirtualBox to run Windows executables")
            print(
                "  Wine: sudo apt-get install wine (Ubuntu/Debian) or "
                "brew install wine-stable (macOS)"
            )
            print("  VirtualBox: Download from https://www.virtualbox.org/")
            runner = None
            runner_name = None

        if runner:
            for vendor_name, downloader_class, usb_devices in vendors_to_process:
                downloader = downloader_class(
                    working_dir=str(working_dir),
                    platform_override=platform,
                )
                filepath = downloader.get_filepath()

                if filepath.exists() and filepath.suffix == ".exe":
                    print("\n{}: Running {}".format(vendor_name, filepath.name))
                    print(f"Using {runner_name} runner")
                    print("USB devices to pass through:")
                    for device in usb_devices:
                        print(
                            "  - Vendor: {}, Product: {}".format(
                                device["vendor_id"], device["product_id"]
                            )
                        )

                    try:
                        result = runner.run(
                            executable=filepath,
                            usb_devices=usb_devices,
                        )
                        print(f"✓ Execution completed (exit code: {result.returncode})")
                    except Exception as e:
                        print(f"✗ Error running {runner_name}: {e}")
                else:
                    if not filepath.exists():
                        print("\n⚠ Skipping {}: file not found".format(vendor_name))
                    else:
                        print(
                            "\n⚠ Skipping {}: {} files not supported".format(
                                vendor_name, filepath.suffix
                            )
                        )
    else:
        print("\n[SKIPPED] Wine execution (--skip-wine)")

    # Step 5: Stop mitmproxy and summarize
    print("\n" + "=" * 80)
    print("STEP 5: Cleanup and Summary")
    print("=" * 80)

    if mitm_process:
        print("\nStopping mitmproxy...")
        time.sleep(2)  # Give some time for final requests
        mitm_manager.stop()
        print("✓ mitmproxy stopped")

        print("\nCaptured traffic saved to:")
        print(f"  - Flow file: {mitmproxy_dir / 'traffic.mitm'}")
        print(f"  - Request log: {mitmproxy_dir / 'requests.jsonl'}")
        print(f"  - Response log: {mitmproxy_dir / 'responses.jsonl'}")

    print("\n" + "=" * 80)
    print("E2E Workflow Complete!")
    print("=" * 80)
    print(f"\nResults available in: {working_dir}")
    print("\nNext steps:")
    print("  1. Review strings analysis in: strings_analysis/")
    print("  2. Analyze captured traffic in: mitmproxy/")
    print("  3. Examine any downloaded firmware binaries")

    return 0


def main():
    """Main entry point for E2E script."""
    parser = argparse.ArgumentParser(
        description="End-to-end firmware investigation workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete workflow for all vendors
  firmware-investigate-e2e --vendor all

  # Run only for Sena, skip Wine execution
  firmware-investigate-e2e --vendor sena --skip-wine

  # Use custom working directory
  firmware-investigate-e2e --working-dir /tmp/firmware --vendor cardo
        """,
    )

    parser.add_argument(
        "--vendor",
        choices=["sena", "cardo", "all"],
        default="all",
        help="Which vendor to investigate (default: all)",
    )

    parser.add_argument(
        "--working-dir",
        type=Path,
        default=Path("working"),
        help="Working directory for downloads and analysis (default: working)",
    )

    parser.add_argument(
        "--platform",
        choices=["windows", "darwin"],
        default="windows",
        help="Platform to download for (default: windows)",
    )

    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download step (use existing files)",
    )

    parser.add_argument(
        "--skip-strings",
        action="store_true",
        help="Skip strings analysis step",
    )

    parser.add_argument(
        "--skip-wine",
        action="store_true",
        help="Skip Wine execution step",
    )

    args = parser.parse_args()

    return run_e2e(
        vendor=args.vendor,
        working_dir=args.working_dir,
        platform=args.platform,
        skip_download=args.skip_download,
        skip_strings=args.skip_strings,
        skip_wine=args.skip_wine,
    )


if __name__ == "__main__":
    sys.exit(main())
