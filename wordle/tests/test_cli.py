#!/usr/bin/env python3

# cSpell:words wordle

"""Test `wordle` package CLI tests"""
from click.testing import CliRunner

from wordle.__main__ import cli


def test_cli_click():
    """Test the Click CLI"""

    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0

    help_result = runner.invoke(cli, ["--help"])

    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    assert "Show this message and exit." in help_result.output
