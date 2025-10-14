"""Module for analyzing binary files using strings command."""

import subprocess
from pathlib import Path
from typing import List, Optional


class StringsAnalyzer:
    """Analyzer for extracting strings from binary files."""

    def __init__(self, min_length: int = 4):
        """Initialize the strings analyzer.

        Args:
            min_length: Minimum length of strings to extract (default: 4).
        """
        self.min_length = min_length

    def analyze(self, filepath: Path, output_file: Optional[Path] = None) -> List[str]:
        """Run strings command on a binary file.

        Args:
            filepath: Path to the binary file to analyze.
            output_file: Optional path to save the strings output.

        Returns:
            List of strings extracted from the binary.

        Raises:
            FileNotFoundError: If the binary file doesn't exist.
            RuntimeError: If strings command fails.
        """
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            # Run strings command
            result = subprocess.run(
                ["strings", "-n", str(self.min_length), str(filepath)],
                capture_output=True,
                text=True,
                check=True,
            )

            strings_list = result.stdout.strip().split("\n")

            # Save to file if requested
            if output_file:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w") as f:
                    f.write(result.stdout)
                print(f"Strings output saved to: {output_file}")

            return strings_list

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"strings command failed: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("strings command not found. Please install binutils package.")

    def analyze_all(self, directory: Path) -> dict:
        """Analyze all executable files in a directory.

        Args:
            directory: Directory containing binary files.

        Returns:
            Dictionary mapping filenames to their extracted strings.
        """
        results = {}

        # Common executable extensions
        executable_patterns = ["*.exe", "*.dll", "*.pkg", "*.dmg", "*.app"]

        for pattern in executable_patterns:
            for filepath in directory.glob(pattern):
                try:
                    strings_list = self.analyze(filepath)
                    results[filepath.name] = strings_list
                    print(f"Analyzed {filepath.name}: {len(strings_list)} strings found")
                except Exception as e:
                    print(f"Error analyzing {filepath.name}: {e}")

        return results
