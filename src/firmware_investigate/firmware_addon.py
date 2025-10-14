"""Mitmproxy addon for firmware update traffic analysis."""

import json
from pathlib import Path
from mitmproxy import http
import os


class FirmwareAddon:
    """Addon to log and analyze firmware update traffic."""

    def __init__(self):
        self.output_dir = Path(os.getenv("OUTDIR"))
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

        print(
            f"[{self.request_count}] Response: {flow.response.status_code} "
            f"({log_entry['content_length']} bytes)"
        )

        # Save firmware binaries if detected
        if flow.response.content:
            content_type = flow.response.headers.get("content-type", "")
            print(f"Flow content {content_type} for {flow.request.url}")
            if any(ext in flow.request.url for ext in [".bin", ".hex", ".fw", ".firmware"]) or "bin" in content_type:
                filename = self.output_dir / f"firmware_{self.request_count}.bin"
                with open(filename, "wb") as f:
                    f.write(flow.response.content)
                print(f"[{self.request_count}] Saved firmware to {filename}")


addons = [FirmwareAddon()]
