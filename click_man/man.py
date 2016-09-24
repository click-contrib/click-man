"""
click-man - Auto generate click documentations

This module provides a formatter for debian
man pages.
"""

from datetime import datetime


class ManPage(object):
    """
    Represent a man page

    :param str name: the name of the man page
    :param str title: the title for the man page
    """
    TITLE_KEYWORD = '.TH'
    SECTION_HEADING_KEYWORD = '.SH'
    PARAGRAPH_KEYWORD = '.PP'
    BOLD_KEYWORD = '.B'
    INDENT_KEYWORDD = '.TP'

    def __init__(self, command):
        #: Holds the command for the man page
        self.command = command

        #: Holds the short help for the man page
        self.short_help = ''

        #: Holds the synopsis for the man page
        self.synopsis = ''

        #: Holds the description for the man page
        self.description = ''

        #: Holds a list of tuple options for the man page
        #  the first item in the tuple are the option switches
        #  and the second one is the option's description
        self.options = []

        #: Holds the commands for the man page
        self.commands = []

        #: Holds the date for the man page creation time.
        self.date = datetime.now().strftime("%d-%b-%Y")

    def __str__(self):
        """
        Show the string representation for
        the man page.
        """
        lines = []

        # write title and footer
        lines.append('{0} {1} 1 "{2}" "{3} Manual"'.format(
            self.TITLE_KEYWORD, self.command, self.date, self.command))

        # write name section
        lines.append('{0} NAME'.format(self.SECTION_HEADING_KEYWORD))
        lines.append(r'{0} \- {1}'.format(self.command, self.short_help))

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
                lines.append(option.replace('-', r'\-'))
                lines.append(description)

        # write commands
        if self.commands:
            lines.append('{0} COMMANDS'.format(self.SECTION_HEADING_KEYWORD))
            for name, description in self.commands:
                lines.append(self.INDENT_KEYWORDD)
                lines.append(name)
                lines.append(description)

        return '\n'.join(lines)
