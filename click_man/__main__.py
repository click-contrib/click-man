"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a click CLI command to
generate man pages from a click application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

import importlib.metadata
import os

import click

from click_man.core import write_man_pages


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--target', '-t', default=os.path.join(os.getcwd(), 'man'),
              type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
              help='Target location for the man pages')
@click.version_option(importlib.metadata.version('click-man'), '-V', '--version')
@click.argument('name')
def cli(target, name):
    """
    Generate man pages for the scripts defined in the ``console_scripts`` entry point.

    The cli application is gathered from entry points of installed packages.

    The generated man pages are written to files in the directory given
    by ``--target``.
    """
    entry_points = importlib.metadata.entry_points()
    console_scripts = entry_points.select(group='console_scripts', name=name)
    if len(console_scripts) < 1:
        raise click.ClickException('"{0}" is not an installed console script.'.format(name))
    # Only generate man pages for first console script
    (entry_point,) = console_scripts

    # create target directory if it does not exist yet
    try:
        os.makedirs(target)
    except OSError:
        pass

    click.echo('Load entry point {0}'.format(name))
    cli = entry_point.load()

    # If the entry point isn't a click.Command object, try to find it in the module
    if not isinstance(cli, click.Command):
        from importlib import import_module
        from inspect import getmembers

        if not entry_point.module:
            raise click.ClickException('Could not find module name for "{0}".'.format(name))
        ep_module = import_module(entry_point.module)
        ep_members = getmembers(ep_module, lambda x: isinstance(x, click.Command))

        if len(ep_members) < 1:
            raise click.ClickException('Could not find click.Command object for "{0}".'.format(name))
        (ep_name, cli) = ep_members[0]
        click.echo('Found alternate entry point {0} in {1}'.format(ep_name, name))

    click.echo('Generate man pages for {0} in {1}'.format(name, target))
    write_man_pages(name, cli, version=entry_point.version, target_dir=target)


if __name__ == '__main__':
    cli()
