"""
Module to test man page functionality of click-man package.
"""

from click_man.man import ManPage


def test_simple_man_page():
    """
    Test creating most simple man page
    """
    man = ManPage('my-command')
    man.short_help = 'Command to test man pages for click.'
    man.date = '21-Feb-1994'
    assert (
        str(man)
        == r""".TH "MY-COMMAND" "1" "21-Feb-1994" "1.0.0" "my-command Manual"
.SH NAME
my-command \- Command to test man pages for click.
.SH SYNOPSIS
.B my-command
"""
    )


def test_full_man_page():
    """
    Test creating man page with all options set
    """
    man = ManPage('my-command')
    man.short_help = 'Command to test man pages for click.'
    man.date = '21-Feb-1994'
    man.synopsis = '[--yolo] [--iambatman]'
    man.description = """This is my awesome

multi line description of a click-man test.

Boaa, richtig geili sach."""

    man.options = [
        ('--yolo', 'Do it in yolo style'),
        ('--iambatman', 'Make me think I am batman'),
    ]
    man.commands = [
        ('start', 'Start it'),
        ('stop', 'Stop it'),
        ('test', 'Pretend you are testing your code'),
    ]

    assert (
        str(man)
        == r""".TH "MY-COMMAND" "1" "21-Feb-1994" "1.0.0" "my-command Manual"
.SH NAME
my-command \- Command to test man pages for click.
.SH SYNOPSIS
.B my-command
[\-\-yolo] [\-\-iambatman]
.SH DESCRIPTION
This is my awesome
.PP
multi line description of a click-man test.
.PP
Boaa, richtig geili sach.
.SH OPTIONS
.TP
\fB\-\-yolo\fP
Do it in yolo style
.TP
\fB\-\-iambatman\fP
Make me think I am batman
.SH COMMANDS
.PP
\fBstart\fP
  Start it
  See \fBmy-command-start(1)\fP for full documentation on the \fBstart\fP command.
.PP
\fBstop\fP
  Stop it
  See \fBmy-command-stop(1)\fP for full documentation on the \fBstop\fP command.
.PP
\fBtest\fP
  Pretend you are testing your code
  See \fBmy-command-test(1)\fP for full documentation on the \fBtest\fP command.
"""
    )  # noqa: E501
