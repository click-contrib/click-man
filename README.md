# click-man

[![Build Status](https://github.com/click-contrib/click-man/actions/workflows/ci.yaml/badge.svg)](https://github.com/click-contrib/click-man/actions/workflows/ci.yaml) [![PyPI Package version](https://badge.fury.io/py/click-man.svg)](https://pypi.python.org/pypi/click-man)

Create **man pages** for [click](https://github.com/pallets/click) application as easy as this:

```bash
python3 setup.py --command-packages=click_man.commands man_pages
```

→ Checkout the [debian packaging example](#debian-packages)

## What it does

*click-man* will generate one man page per command of your click CLI application specified in `console_scripts` in your `setup.py`.

## Installation

```bash
pip3 install click-man
```

**click-man** is also available for Python 2:

```bash
pip install click-man
```

## Usage Recipes

The following sections describe different usage example for *click-man*.

### Use with a previously installed package

**click-man** provides its own command line tool which can be passed the name of
an installed script:

```bash
click-man commandname
```

where `commandname` is the name of an installed `console_script` entry point.

To specify a target directory for the man pages, use the `--target` option:

```bash
click-man --target path/to/man/pages commandname
```

### Use with setuptools

**click-man** provides a sane setuptools command extension which can be used like the following:

```bash
python3 setup.py --command-packages=click_man.commands man_pages
```

or specify the man pages target directory:

```bash
python3 setup.py --command-packages=click_man.commands man_pages --target path/to/man/pages
```

### Automatic man page installation with setuptools and pip

This approach of installing man pages is problematic for various reasons:

#### (1) Man pages are a UNIX thing

Python in general and with that pip and setuptools are aimed to be platform independent.
Man pages are **not**: they are a UNIX thing which means setuptools does not provide a sane
solution to generate and install man pages. 
We should consider using automatic man page installation only with vendor specific packaging, e.g. for `*.deb` or `*.rpm` packages.

#### (2) Man pages are not compatible with Python virtualenvs

Even on systems that support man pages, Python packages can be installed in
virtualenvs via pip and setuptools, which do not make commands available
globally. In fact, one of the "features" of a virtualenv is the ability to
install a package without affecting the main system. As it is imposable to
ensure a man page is only generated when not installing into a virtualenv,
auto-generated man pages would pollute the main system and not stay contained in
the virtualenv. Additionally, as a user could install multiple different
versions of the same package into multiple different virtualenvs on the same
system, there is no guarantee that a globally installed man page will document
the version and behavior available in any given virtualenv.

#### (3) We want to generate man pages on the fly

First, we do not want to commit man pages to our source control.
We want to generate them on the fly. Either
during build or installation time.

With setuptools and pip we face two problems:

1. If we generate and install them during installation of the package pip does not know about the man pages and thus cannot uninstall it.
2. If we generate them in our build process and add them to your distribution we do not have a way to prevent installation to */usr/share/man* for non-UNIX-like Operating Systems or from within virtualenvs.

### Debian packages

The `debhelper` packages provides a very convenient script called `dh_installman`.
It checks for the `debian/(pkg_name.)manpages` file and it's content which is basically a line by line list of man pages or globs:

```
debian/tmp/manpages/*
```

We override the rule provided by `dh_installman` to generate our man pages in advance, like this:

```Makefile
override_dh_installman:
	python3 setup.py --command-packages=click_man.commands man_pages --target debian/tmp/manpages
	dh_installman -O--buildsystem=pybuild
```

Now we are able to build a debian package with the tool of our choice, e.g.:

```debuild -us -uc```

Checkout a working example here: [repo debian package](https://github.com/click-contrib/click-man/tree/master/examples/debian_pkg)
