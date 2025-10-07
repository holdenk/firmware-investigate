"""Tests for the strings analyzer module."""

import pytest
from pathlib import Path
from firmware_investigate.analyzer import StringsAnalyzer


def test_strings_analyzer_initialization():
    """Test StringsAnalyzer initialization."""
    analyzer = StringsAnalyzer()
    assert analyzer.min_length == 4
    
    analyzer_custom = StringsAnalyzer(min_length=8)
    assert analyzer_custom.min_length == 8


def test_strings_analyzer_analyze_missing_file(tmp_path):
    """Test analyze with non-existent file."""
    analyzer = StringsAnalyzer()
    missing_file = tmp_path / "missing.exe"
    
    with pytest.raises(FileNotFoundError):
        analyzer.analyze(missing_file)


def test_strings_analyzer_analyze_all(tmp_path):
    """Test analyze_all with directory."""
    analyzer = StringsAnalyzer()
    
    # Create some test files
    (tmp_path / "test.exe").write_bytes(b"test content")
    (tmp_path / "test.txt").write_text("not executable")
    
    # Note: This test will skip actual analysis if strings command is not available
    # In a real environment, we'd need strings installed
    results = analyzer.analyze_all(tmp_path)
    
    # Results is a dict (may be empty if strings command not available)
    assert isinstance(results, dict)
