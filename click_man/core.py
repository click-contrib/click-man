"""
click-man - Auto generate click documentations
"""

import os

import click

from .man import ManPage


def generate_man_page(ctx):
    """
    Generate documentation for the given command.

    :param Command command: the command to generate the documentation for.
    """
    man_page = ManPage(ctx.command_path, ctx.command_path)
    man_page.command_path = ctx.command_path
    man_page.short_help = ctx.command.short_help
    man_page.description = ctx.command.help
    man_page.synopsis = ' '.join(ctx.command.collect_usage_pieces(ctx))
    man_page.options = [x.get_help_record(None) for x in ctx.command.params if isinstance(x, click.Option)]

    commands = getattr(ctx.command, 'commands', None)
    if commands:
        man_page.commands = [(k, v.short_help) for k, v in commands.items()]
    return str(man_page)


def write_man_pages(name, cli, parent_ctx=None, target_dir=None):
    """
    Generate man page files recursively
    for the given click cli function.

    :param str name: the cli name
    :param cli: the cli instance
    """
    ctx = click.Context(cli, info_name=name, parent=parent_ctx)

    man_page = generate_man_page(ctx)
    path = '{0}.man'.format(ctx.command_path.replace(' ', '-'))
    if target_dir:
        path = os.path.join(target_dir, path)

    with open(path, 'w+') as f:
        f.write(man_page)

    commands = getattr(cli, 'commands', {})
    print(commands)
    for name, command in commands.items():
        write_man_pages(name, command, parent_ctx=ctx, target_dir=target_dir)
