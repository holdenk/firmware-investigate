#!/usr/bin/env python3
"""
Standalone script to find FCC information for motorcycle headsets and devices.

This script provides easy access to FCC IDs and links to FCC reports for:
- Sena 50S
- Cardo Packtalk Bold
- Motorola Defy Satellite

Usage:
    python scripts/find_fcc_info.py --list
    python scripts/find_fcc_info.py --device sena_50s
    python scripts/find_fcc_info.py --device cardo_packtalk_bold
    python scripts/find_fcc_info.py --device motorola_defy_satellite
"""

import sys
from pathlib import Path

# Add src directory to path so we can import the module
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from firmware_investigate.fcc_lookup import main

if __name__ == "__main__":
    sys.exit(main())
