"""
Module to test man page functionality of click-man package.
"""


from sure import expect

from click_man.man import ManPage


def test_simple_man_page():
    """
    Test creating most simple man page
    """
    man = ManPage('my-command')
    man.short_help = 'Command to test man pages for click.'
    man.date = '21-Feb-1994'
    expect(str(man)).to.be.equal(""".TH my-command 1 "21-Feb-1994" "my-command Manual"
.SH NAME
my-command \- Command to test man pages for click.
.SH SYNOPSIS
.B my-command

.SH DESCRIPTION
""")


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
        ('--yolo', 'Do it in yolo sytle'),
        ('--iambatman', 'Make me think I am batman')
    ]
    man.commands = [
        ('start', 'Start it'),
        ('stop', 'Stop it'),
        ('test', 'Pretend you are testing your code')
    ]

    expect(str(man)).to.be.equal(""".TH my-command 1 "21-Feb-1994" "my-command Manual"
.SH NAME
my-command \- Command to test man pages for click.
.SH SYNOPSIS
.B my-command
[\-\-yolo] [\-\-iambatman]
.SH DESCRIPTION
This is my awesome

multi line description of a click-man test.

Boaa, richtig geili sach.
.SH OPTIONS
.TP
\-\-yolo
Do it in yolo sytle
.TP
\-\-iambatman
Make me think I am batman
.SH COMMANDS
.TP
start
Start it
.TP
stop
Stop it
.TP
test
Pretend you are testing your code""")
