"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides functionality to
write a man page from some given information
about a CLI application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

from datetime import datetime


class ManPage(object):
    """
    Represent a man page

    :param str command: the name of the command
    """
    TITLE_KEYWORD = '.TH'
    SECTION_HEADING_KEYWORD = '.SH'
    PARAGRAPH_KEYWORD = '.PP'
    BOLD_KEYWORD = '.B'
    INDENT_KEYWORDD = '.TP'

    def __init__(self, command):
        #: Holds the command of the man page
        self.command = command

        #: Holds the short help of the man page
        self.short_help = ''

        #: Holds the synopsis of the man page
        self.synopsis = ''

        #: Holds the description of the man page
        self.description = ''

        #: Holds the version of the man page
        self.version = '1.0.0'

        #: Holds a list of tuple options of the man page
        #  the first item in the tuple are the option switches
        #  and the second one is the option's description
        self.options = []

        #: Holds the commands of the man page
        self.commands = []

        #: Holds the date of the man page creation time.
        self.date = datetime.now().strftime("%d-%b-%Y")

    def __str__(self):
        """
        Generate and return the string representation
        of this man page.
        """
        lines = []

        # write title and footer
        lines.append('{0} "{1}" "1" "{2}" "{3}" "{4} Manual"'.format(
            self.TITLE_KEYWORD, self.command.upper(), self.date, self.version, self.command))

        # write name section
        lines.append('{0} NAME'.format(self.SECTION_HEADING_KEYWORD))
        lines.append(r'{0} \- {1}'.format(self.command.replace(' ', r'\-'), self.short_help))

        # write synopsis
        lines.append('{0} SYNOPSIS'.format(self.SECTION_HEADING_KEYWORD))
        lines.append('{0} {1}'.format(self.BOLD_KEYWORD, self.command))
        lines.append(self.synopsis.replace('-', r'\-'))

        # write the description
        lines.append('{0} DESCRIPTION'.format(self.SECTION_HEADING_KEYWORD))
        lines.append(self.description)  # FIXME: replace empty lines with PARAGRAPH_KEYWORD

        # write the options
        if self.options:
            lines.append('{0} OPTIONS'.format(self.SECTION_HEADING_KEYWORD))
            for option, description in self.options:
                lines.append(self.INDENT_KEYWORDD)
                option_unpacked = option.replace('-', r'\-').split()
                lines.append(r'\fB{0}\fP{1}'.format(option_unpacked[0], (' ' + ' '.join(option_unpacked[1:])) if len(option_unpacked) > 1 else ''))
                lines.append(description)

        # write commands
        if self.commands:
            lines.append('{0} COMMANDS'.format(self.SECTION_HEADING_KEYWORD))
            for name, description in self.commands:
                lines.append(self.PARAGRAPH_KEYWORD)
                lines.append(r'\fB{0}\fP'.format(name))
                lines.append('  ' + description)
                lines.append(r'  See \fB{0}-{1}(1)\fP for full documentation on the \fB{1}\fP command.'.format(
                    self.command, name))
                lines.append('')

        return '\n'.join(lines)
