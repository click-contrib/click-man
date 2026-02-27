"""
Module to test specific click-man issues.
"""

from click import Command, Context
from click_man.core import generate_man_page


def test_issue_59():
    """
    Test creating a man page with an indented docstring (issue #59)
    """
    command = 'my-command'
    version = '1.0.0'
    date = '21-Feb-1994'
    short_help = 'Command to test man pages for click.'
    docstring = """

    An imaginary description from an indented docstring, with newlines.

"""
    cmd = Command(command, short_help=short_help, help=docstring)
    ctx = Context(cmd, info_name=command)
    man = generate_man_page(ctx, version=version, date=date)

    assert (
        str(man)
        == r""".TH "MY-COMMAND" "1" "21-Feb-1994" "1.0.0" "my-command Manual"
.SH NAME
my-command \- Command to test man pages for click.
.SH SYNOPSIS
.B my-command
[OPTIONS]
.SH DESCRIPTION
An imaginary description from an indented docstring, with newlines.
"""
    )
