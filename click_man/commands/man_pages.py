"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a setuptools command to
generate man pages from a click application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

import os
from distutils.core import Command
from distutils.errors import DistutilsSetupError
from pkg_resources import EntryPoint

from click_man.core import write_man_pages


__all__ = ['man_pages']



class man_pages(Command):
    description = 'distutils command to generate man pages'

    user_options = [
        ('target=', 't', 'Target location for the man pages'),
        ('version=', 'v', 'Version of the CLI application')
    ]
    boolean_options = []

    def initialize_options(self):
        self.target = os.path.join(os.getcwd(), 'man')
        self.version = ''

    def finalize_options(self):
        self.target = os.path.abspath(self.target)

        # create target directory if it does not exist yet
        try:
            os.makedirs(self.target)
        except OSError:
            pass

    def run(self):
        """
        Generate man pages for the scripts defined in distutils setup().

        The cli application is gathered from the setuptools setup()
        function in setup.py.

        The generated man pages are written to files in the directory given
        by ``--target``.
        """
        eps = EntryPoint.parse_map(self.distribution.entry_points or '')

        if 'console_scripts' not in eps or not eps['console_scripts']:
            raise DistutilsSetupError('No entry points defined in setup()')

        console_scripts = [(k, v) for k, v in eps['console_scripts'].items()]
        # FIXME: create own setup() attribute for CLI script configuration
        for name, entry_point in console_scripts:
            self.announce('Load entry point {0}'.format(name), level=2)
            cli = entry_point.resolve()
            self.announce('Generate man pages for {0}'.format(name), level=2)
            write_man_pages(name, cli, version=self.version, target_dir=self.target)
