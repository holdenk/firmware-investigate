"""Module for managing mitmproxy configuration and execution."""

import signal
import subprocess
import time
from pathlib import Path
from typing import Optional


class MitmproxyManager:
    """Manager for mitmproxy execution and configuration."""

    def __init__(
        self,
        port: int = 8080,
        output_dir: Optional[Path] = None,
        mode: str = "regular",
    ):
        """Initialize the mitmproxy manager.

        Args:
            port: Port to listen on (default: 8080).
            output_dir: Directory to save captured traffic.
            mode: Proxy mode ('regular', 'transparent', 'socks5').
        """
        self.port = port
        self.output_dir = output_dir or Path("working/mitmproxy")
        self.mode = mode
        self.process: Optional[subprocess.Popen] = None

    def check_mitmproxy_installed(self) -> bool:
        """Check if mitmproxy is installed.

        Returns:
            True if mitmproxy is available, False otherwise.
        """
        try:
            subprocess.run(
                ["mitmdump", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def create_config_script(self) -> Path:
        """Create a mitmproxy addon script for logging and analysis.

        Returns:
            Path to the created addon script.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        addon_script = self.output_dir / "firmware_addon.py"

        addon_content = (
            '''"""Mitmproxy addon for firmware update traffic analysis."""

import json
from pathlib import Path
from mitmproxy import http


class FirmwareAddon:
    """Addon to log and analyze firmware update traffic."""

    def __init__(self):
        self.output_dir = Path("'''
            + str(self.output_dir)
            + '''")
        self.request_count = 0

    def request(self, flow: http.HTTPFlow) -> None:
        """Log HTTP/HTTPS requests."""
        self.request_count += 1

        log_entry = {
            "id": self.request_count,
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "headers": dict(flow.request.headers),
            "timestamp": flow.request.timestamp_start,
        }

        # Log to file
        log_file = self.output_dir / "requests.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\\n")

        print(f"[{self.request_count}] {flow.request.method} {flow.request.pretty_url}")

    def response(self, flow: http.HTTPFlow) -> None:
        """Log HTTP/HTTPS responses."""
        log_entry = {
            "id": self.request_count,
            "status_code": flow.response.status_code,
            "headers": dict(flow.response.headers),
            "content_length": len(flow.response.content) if flow.response.content else 0,
            "timestamp": flow.response.timestamp_end,
        }

        # Log to file
        log_file = self.output_dir / "responses.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\\n")

        print(f"[{self.request_count}] Response: {flow.response.status_code} "
              f"({log_entry['content_length']} bytes)")

        # Save firmware binaries if detected
        if flow.response.content:
            content_type = flow.response.headers.get("content-type", "")
            if any(ext in flow.request.url for ext in [".bin", ".hex", ".fw", ".firmware"]):
                filename = self.output_dir / f"firmware_{self.request_count}.bin"
                with open(filename, "wb") as f:
                    f.write(flow.response.content)
                print(f"[{self.request_count}] Saved firmware to {filename}")


addons = [FirmwareAddon()]
'''
        )

        with open(addon_script, "w") as f:
            f.write(addon_content)

        print(f"Created mitmproxy addon script: {addon_script}")
        return addon_script

    def start(self, background: bool = True) -> Optional[subprocess.Popen]:
        """Start mitmproxy in the background.

        Args:
            background: If True, run in background, else blocking.

        Returns:
            Popen process object if background=True, None otherwise.

        Raises:
            RuntimeError: If mitmproxy is not installed.
        """
        if not self.check_mitmproxy_installed():
            raise RuntimeError("mitmproxy is not installed. Install with: pip install mitmproxy")

        # Create addon script
        addon_script = self.create_config_script()

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Build mitmdump command
        flow_file = self.output_dir / "traffic.mitm"
        cmd = [
            "mitmdump",
            "-p",
            str(self.port),
            "-s",
            str(addon_script),
            "-w",
            str(flow_file),
            "--set",
            "block_global=false",
            "--ssl-insecure",  # Accept self-signed certificates
        ]

        print(f"Starting mitmproxy on port {self.port}")
        print(f"Traffic will be saved to: {flow_file}")
        print(f"Logs will be saved to: {self.output_dir}")

        if background:
            # Start in background
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Give it a moment to start
            time.sleep(2)

            # Check if it's still running
            if self.process.poll() is not None:
                raise RuntimeError("mitmproxy failed to start")

            print(f"mitmproxy started in background (PID: {self.process.pid})")
            return self.process
        else:
            # Run in foreground (blocking)
            subprocess.run(cmd)
            return None

    def stop(self) -> None:
        """Stop the running mitmproxy process."""
        if self.process:
            print(f"Stopping mitmproxy (PID: {self.process.pid})...")
            self.process.send_signal(signal.SIGTERM)

            # Wait for graceful shutdown
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing mitmproxy...")
                self.process.kill()

            self.process = None
            print("mitmproxy stopped")
