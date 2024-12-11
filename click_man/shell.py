"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a click CLI command to
generate man pages from a click application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

from datetime import datetime
import importlib.metadata
import os
import sys
from typing import Optional

import click

from click_man.core import write_man_pages


def _get_entry_point(name: str) -> Optional[importlib.metadata.EntryPoint]:
    entry_points = importlib.metadata.entry_points()
    if sys.version_info >= (3, 10):
        console_scripts = entry_points.select(
            group='console_scripts', name=name
        )
    else:
        console_scripts = [
            ep
            for ep in entry_points.get('console_scripts', [])
            if ep.name == name
        ]

    if len(console_scripts) < 1:
        return None

    # Only generate man pages for first console script
    return tuple(console_scripts)[0]


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option(
    '--target',
    '-t',
    default=os.path.join(os.getcwd(), 'man'),
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help='Target location for the man pages',
)
@click.option('--man-version', help='Version to use in generated man page(s)')
@click.option('--man-date', help='Date to use in generated man page(s)')
@click.version_option(
    importlib.metadata.version('click-man'), '-V', '--version'
)
@click.argument('name')
def cli(target, name, man_version, man_date):
    """
    Generate man pages for the scripts defined in the ``console_scripts`` entry
    point.

    The cli application is gathered from entry points of installed packages.

    The generated man pages are written to files in the directory given
    by ``--target``.
    """
    entry_point = _get_entry_point(name)
    if not entry_point:
        raise click.ClickException(
            '"{0}" is not an installed console script.'.format(name)
        )

    # create target directory if it does not exist yet
    try:
        os.makedirs(target)
    except OSError:
        pass

    if not man_version:
        man_version = entry_point.version

    if man_date:
        try:
            datetime.strptime(man_date, '%Y-%m-%d')
        except ValueError:
            raise click.ClickException(
                '"{0}" is not a valid date.'.format(man_date)
            )

    click.echo('Load entry point {0}'.format(name))
    cli = entry_point.load()

    # If the entry point isn't a click.Command object, try to find it in the
    # module
    if not isinstance(cli, click.Command):
        from importlib import import_module
        from inspect import getmembers

        if not entry_point.module:
            raise click.ClickException(
                'Could not find module name for "{0}".'.format(name)
            )

        ep_module = import_module(entry_point.module)
        ep_members = getmembers(
            ep_module,
            lambda x: isinstance(x, click.Command),
        )

        if len(ep_members) < 1:
            raise click.ClickException(
                'Could not find click.Command object for "{0}".'.format(name)
            )

        ep_name, cli = ep_members[0]
        click.echo(
            'Found alternate entry point {0} in {1}'.format(ep_name, name)
        )

    click.echo('Generate man pages for {0} in {1}'.format(name, target))
    write_man_pages(
        name,
        cli,
        version=man_version,
        target_dir=target,
        date=man_date,
    )
