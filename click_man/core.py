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


def generate_man_page(ctx, version=None):
    """
    Generate documentation for the given command.

    :param click.Context ctx: the click context for the
                              cli application.

    :rtype: str
    :returns: the generate man page from the given click Context.
    """
    # Create man page with the details from the given context
    man_page = ManPage(ctx.command_path)
    man_page.version = version
    man_page.short_help = ctx.command.short_help
    man_page.description = ctx.command.help
    man_page.synopsis = ' '.join(ctx.command.collect_usage_pieces(ctx))
    man_page.options = [x.get_help_record(None) for x in ctx.command.params if isinstance(x, click.Option)]
    commands = getattr(ctx.command, 'commands', None)
    if commands:
        man_page.commands = [(k, v.short_help) for k, v in commands.items()]

    return str(man_page)


def write_man_pages(name, cli, parent_ctx=None, version=None, target_dir=None):
    """
    Generate man page files recursively
    for the given click cli function.

    :param str name: the cli name
    :param cli: the cli instance
    :param click.Context parent_ctx: the parent click context
    :param str target_dir: the directory where the generated
                           man pages are stored.
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
        write_man_pages(name, command, parent_ctx=ctx, version=version, target_dir=target_dir)
