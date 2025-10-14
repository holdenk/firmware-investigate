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

if [ -d .venv/ ]; then
  echo "Reusing exisitng venv."
else
  # Create virtual environment with uv
  echo "Creating virtual environment..."
  uv venv
fi

# Activate virtual environment
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate  # On Linux/macOS"
echo "  .venv\\Scripts\\activate     # On Windows"

# Install package with dependencies
echo ""
echo "Installing package and dependencies..."
uv pip install -e ".[dev]"

if ! command -v mitmproxy &> /dev/null; then
  if command -v brew; then
    brew install mitmproxy
  else
    if [ ! -f mitmproxy-12.1.2-linux-x86_64.tar.gz ]; then
      wget https://downloads.mitmproxy.org/12.1.2/mitmproxy-12.1.2-linux-x86_64.tar.gz || echo "Error downloading mitm proxy?"
    fi
    if [ ! -d mitmproxy-12.1.2-linux-x86_64 ]; then
      tar -xvf mitmproxy-12.1.2-linux-x86_64.tar.gz || echo "Error extracting mitmproxy"
    fi
    export PATH="$PATH:""$(pwd)/"
  fi
fi

echo ""
echo "Setup complete! The project is ready to use."
echo ""
if ! command -v mitmproxy &> /dev/null; then
  echo "IMPORTANT: mitmproxy must be installed separately:"
  echo "  - macOS: brew install mitmproxy"
  echo "  - Linux: Download from https://mitmproxy.org/"
  echo "  - Windows: Download from https://mitmproxy.org/"
  echo ""
fi

if ! command -v virtualbox &> /dev/null; then
  if command -v apt-get &> /dev/null; then
    sudo apt-get install -y virtualbox
    echo "Make sure to setup virtualbox to run the updater."
  fi
fi

echo "Available commands:"
echo "  firmware-investigate      # Download firmware updaters"
echo "  firmware-investigate-e2e  # Run end-to-end workflow"
echo ""
echo "Run tests with: pytest tests/"
