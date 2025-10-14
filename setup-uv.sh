#!/bin/bash
# Setup script using uv for firmware-investigate
# uv is a fast Python package installer and resolver

set -e

echo "Setting up firmware-investigate using uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "Using uv version:"
uv --version

# Create virtual environment with uv
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate  # On Linux/macOS"
echo "  .venv\\Scripts\\activate     # On Windows"

# Install package with dependencies
echo ""
echo "Installing package and dependencies..."
uv pip install -e ".[dev]"

echo ""
echo "Setup complete! The project is ready to use."
echo ""
echo "IMPORTANT: mitmproxy must be installed separately:"
echo "  - macOS: brew install mitmproxy"
echo "  - Linux: Download from https://mitmproxy.org/"
echo "  - Windows: Download from https://mitmproxy.org/"
echo ""
echo "Available commands:"
echo "  firmware-investigate      # Download firmware updaters"
echo "  firmware-investigate-e2e  # Run end-to-end workflow"
echo ""
echo "Run tests with: pytest tests/"
