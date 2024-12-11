"""
Module to test CLI functionality of click-man package.
"""

import importlib.metadata
import os
from unittest import mock

import click
from click.testing import CliRunner as CLIRunner

from click_man import shell


@mock.patch.object(shell, '_get_entry_point')
def test_cli__missing_entry_point(mock_entry_point):
    mock_entry_point.return_value = None

    runner = CLIRunner()
    result = runner.invoke(shell.cli, 'foo')

    assert result.exit_code == 1, result
    assert 'not an installed console script' in result.output.strip()

    mock_entry_point.assert_called_once_with('foo')


@mock.patch('os.makedirs', new=mock.Mock())
@mock.patch.object(shell, 'write_man_pages')
@mock.patch.object(click, 'echo')
@mock.patch.object(shell, '_get_entry_point')
def test_cli__valid(mock_entry_point, mock_echo, mock_write):
    fake_target = os.path.join(os.getcwd(), 'man')
    fake_command = click.Command(name='foo')
    fake_version = '1.2.3'
    entry_point = mock.Mock(spec=importlib.metadata.EntryPoint)
    entry_point.load.return_value = fake_command
    entry_point.version = fake_version

    mock_entry_point.return_value = entry_point

    runner = CLIRunner()
    result = runner.invoke(shell.cli, ['foo'])

    assert result.exit_code == 0, result.output

    mock_entry_point.assert_called_once_with('foo')
    mock_echo.assert_has_calls(
        [
            mock.call('Load entry point foo'),
            mock.call('Generate man pages for foo in %s' % fake_target),
        ]
    )
    mock_write.assert_called_once_with(
        'foo',
        fake_command,
        version=fake_version,
        target_dir=fake_target,
        date=None,
    )


@mock.patch('os.makedirs', new=mock.Mock())
@mock.patch.object(shell, 'write_man_pages')
@mock.patch.object(click, 'echo')
@mock.patch.object(shell, '_get_entry_point')
def test_cli__with_man_date_version(mock_entry_point, mock_echo, mock_write):
    fake_target = os.path.join(os.getcwd(), 'man')
    fake_command = click.Command(name='foo')
    entry_point = mock.Mock(spec=importlib.metadata.EntryPoint)
    entry_point.load.return_value = fake_command

    mock_entry_point.return_value = entry_point

    runner = CLIRunner()
    result = runner.invoke(
        shell.cli,
        ['foo', '--man-version', '3.2.1', '--man-date', '2020-01-01'],
    )

    assert result.exit_code == 0, result.output

    mock_entry_point.assert_called_once_with('foo')
    mock_echo.assert_has_calls(
        [
            mock.call('Load entry point foo'),
            mock.call('Generate man pages for foo in %s' % fake_target),
        ]
    )
    mock_write.assert_called_once_with(
        'foo',
        fake_command,
        version='3.2.1',
        target_dir=fake_target,
        date='2020-01-01',
    )
