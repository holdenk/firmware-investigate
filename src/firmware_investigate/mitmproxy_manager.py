"""Module for managing mitmproxy configuration and execution."""

import signal
import subprocess
from pathlib import Path
from typing import Optional
import os


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
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        addon_script = current_dir + "/firmware_addon.py"

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
        mitm_env = os.environ.copy()
        mitm_env["OUTDIR"] = str(self.output_dir)

        if background:
            # Start in background
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=mitm_env,
            )

            try:
                # Give it a short moment to fail fast; if it returns, it exited
                out, err = self.process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                # Still running after timeout -> started successfully in background
                print(f"mitmproxy started in background (PID: {self.process.pid})")
                return self.process
            # Process exited before the 2 seconds.
            msg = "mitmproxy failed to start."
            if out:
                out_decoded = out.decode()
                msg += f"\nstdout:\n{out_decoded}"
            if err:
                err_decoded = err.decode()
                msg += f"\nstderr:\n{err_decoded}"
            raise RuntimeError(msg)
        else:
            # Run in foreground (blocking)
            subprocess.run(cmd, env=mitm_env)
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
