"""
click-man - Auto generate click documentations

This module provides a formatter for debian
man pages.
"""

from __future__ import unicode_literals


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

    def __init__(self, name, title):
        #: Holds the name for the man page
        self.name = name

        #: Holds the title for the man page
        self.title = title

        #: Holds the command path for the man page
        self.command_path = self.name

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

    def __str__(self):
        """
        Show the string representation for
        the man page.
        """
        lines = []

        # write title and footer
        lines.append('{0} {1} 1 "{2}" "{3} Manual"'.format(
            self.TITLE_KEYWORD, self.title, '21-Feb-1994', self.name))

        # write name section
        lines.append('{0} NAME'.format(self.SECTION_HEADING_KEYWORD))
        lines.append(r'{0} \- {1}'.format(self.title, self.short_help))

        # write synopsis
        lines.append('{0} SYNOPSIS'.format(self.SECTION_HEADING_KEYWORD))
        lines.append('{0} {1}'.format(self.BOLD_KEYWORD, self.command_path))
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

        return '\n'.join(lines)
