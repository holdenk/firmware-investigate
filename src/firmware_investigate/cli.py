"""Command-line interface for firmware investigation tools."""

import argparse
import sys

from .downloaders import CardoDownloader, SenaDownloader


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Firmware Investigation Toolkit - Download and analyze firmware"
    )

    parser.add_argument(
        "--vendor",
        choices=["sena", "cardo", "all"],
        default="all",
        help="Which vendor's firmware to download (default: all)",
    )

    parser.add_argument(
        "--working-dir",
        default="working",
        help="Directory to store downloaded files (default: working)",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download even if file already exists",
    )

    args = parser.parse_args()

    vendors = []
    if args.vendor in ["sena", "all"]:
        vendors.append(("Sena", SenaDownloader))
    if args.vendor in ["cardo", "all"]:
        vendors.append(("Cardo", CardoDownloader))

    print("Firmware Investigation Toolkit")
    print(f"Working directory: {args.working_dir}")
    print("-" * 60)

    for vendor_name, downloader_class in vendors:
        print(f"\n{vendor_name}:")
        downloader = downloader_class(working_dir=args.working_dir)

        try:
            result = downloader.download(force=args.force)
            if result:
                print(f"✓ Successfully downloaded to: {result}")
            else:
                print("✓ File already exists (use --force to re-download)")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            return 1

    print("\n" + "-" * 60)
    print("Download complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
