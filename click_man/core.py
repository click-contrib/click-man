"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the core functionality to
generate man pages for entire click applications.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

import os

import click

from .man import ManPage

CLICK_VERSION = tuple(int(x) for x in click.__version__.split('.')[:2])


def get_short_help_str(command, limit=45):
    """
    Gets short help for the command or makes it by shortening the long help string.
    """
    return (
        command.short_help
        or command.help
        and click.utils.make_default_short_help(command.help, limit)
        or ''
    )


def generate_man_page(ctx, version=None, date=None):
    """
    Generate documentation for the given command.

    :param click.Context ctx: the click context for the
        cli application.
    :param str version: The version information to include in the man page.
    :param str date: The date information to include in the man page.

    :returns: the generate man page from the given click Context.
    :rtype: str
    """
    # Create man page with the details from the given context
    man_page = ManPage(ctx.command_path)
    man_page.version = version
    man_page.short_help = get_short_help_str(ctx.command)
    man_page.description = ctx.command.help
    man_page.synopsis = ' '.join(ctx.command.collect_usage_pieces(ctx))
    man_page.options = [
        x.get_help_record(ctx)
        for x in ctx.command.params
        if isinstance(x, click.Option) and not getattr(x, 'hidden', False)
    ]

    if date:
        man_page.date = date

    commands = getattr(ctx.command, 'commands', None)
    if commands:
        man_page.commands = [
            (k, get_short_help_str(v)) for k, v in commands.items()
        ]

    return str(man_page)


def write_man_pages(
    name,
    cli,
    parent_ctx=None,
    version=None,
    target_dir=None,
    date=None,
):
    """
    Generate man page files recursively
    for the given click cli function.

    :param str name: the cli name
    :param cli: the cli instance
    :param click.Context parent_ctx: the parent click context
    :param str target_dir: the directory where the generated
                           man pages are stored.
    :param date: the date to include in the header
    """
    ctx = click.Context(cli, info_name=name, parent=parent_ctx)

    man_page = generate_man_page(ctx, version)
    path = '{0}.1'.format(ctx.command_path.replace(' ', '-'))
    if target_dir:
        path = os.path.join(target_dir, path)

    with open(path, 'w+') as f:
        f.write(man_page)

    commands = getattr(cli, 'commands', {})
    for name, command in commands.items():
        if CLICK_VERSION >= (7, 0):
            # Since Click 7.0, we have been able to mark commands as hidden
            if command.hidden:
                # Do not write a man page for a hidden command
                continue

        write_man_pages(
            name,
            command,
            parent_ctx=ctx,
            version=version,
            target_dir=target_dir,
            date=date,
        )
