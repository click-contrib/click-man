"""
Module to test CLI functionality of click-man package.
"""

import os
from unittest import mock

import click
from click.testing import CliRunner as CLIRunner

from click_man import shell


@mock.patch.object(shell, 'iter_entry_points')
def test_missing_entry_point(mock_entry_points):
    mock_entry_points.return_value = iter([])

    runner = CLIRunner()
    result = runner.invoke(shell.cli, 'foo')

    assert result.exit_code == 1, result
    assert 'not an installed console script' in result.output.strip()

    mock_entry_points.assert_called_once_with('console_scripts', name='foo')


@mock.patch('os.makedirs', new=mock.Mock())
@mock.patch.object(shell, 'write_man_pages')
@mock.patch.object(click, 'echo')
@mock.patch.object(shell, 'iter_entry_points')
def test_is_click_command(mock_entry_points, mock_echo, mock_write):
    fake_target = os.path.join(os.getcwd(), 'man')
    fake_command = click.Command(name='foo')
    fake_version = '1.2.3'
    entry_point = mock.Mock()
    entry_point.resolve.return_value = fake_command
    entry_point.dist.version = fake_version

    mock_entry_points.return_value = iter([entry_point])

    runner = CLIRunner()
    result = runner.invoke(shell.cli, ['foo'])

    assert result.exit_code == 0, result.output

    mock_entry_points.assert_called_once_with('console_scripts', name='foo')
    mock_echo.assert_has_calls([
        mock.call('Load entry point foo'),
        mock.call('Generate man pages for foo in %s' % fake_target),
    ])
    mock_write.assert_called_once_with(
        'foo', fake_command, version=fake_version, target_dir=fake_target,
    )
