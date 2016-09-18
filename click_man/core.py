"""
click-man - Auto generate click documentations
"""

import click
from click.testing import CliRunner

from .man import ManPage


def generate_command_doc(command):
    """
    Generate documentation for the given command.

    :param Command command: the command to generate the documentation for.
    """
    # generate click command context.
    # It's used to properly generate the usage
    ctx = click.Context(command, info_name=command.name)

    man_page = ManPage(command.name, command.name)
    man_page.command_path = ctx.command_path
    man_page.short_help = command.short_help
    man_page.description = command.help
    man_page.synopsis = ' '.join(command.collect_usage_pieces(ctx))
    man_page.options = [x.get_help_record(None) for x in command.params if isinstance(x, click.Option)]

    return str(man_page)
