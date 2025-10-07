"""Setup configuration for firmware-investigate package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="firmware-investigate",
    version="0.1.0",
    author="Holden Karau",
    description="Toolkit for investigating and reverse-engineering motorcycle headset firmware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/holdenk/firmware-investigate",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for basic downloader
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "firmware-investigate=firmware_investigate.cli:main",
            "fcc-lookup=firmware_investigate.fcc_lookup:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
