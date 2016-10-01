# click-man

[![Build Status](https://travis-ci.org/timofurrer/click-man.svg?branch=master)](https://travis-ci.org/timofurrer/click-man) [![PyPI Package version](https://badge.fury.io/py/click-man.svg)](https://pypi.python.org/pypi/click-man)

Create **man pages** for [click](https://github.com/pallets/click) application as easy as this:

```bash
python3 setup.py --command-packages=click_man.commands man_pages
```

→ Checkout the [debian packaging example](https://github.com/timofurrer/click-man#debian-packages)

## What it does

*click-man* will generate one man page per command from your click CLI application specified in `console_scripts` in your `setup.py`.

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

### Use with setuptools

**click-man** provides a sane setuptools command extension which can be used like the following:

```bash
python3 setup.py --command-packages=click_man.commands man_pages
```

or specify the man pages target directory:

```bash
python3 setup.py --command-packages=click_man.commands man_pages --target path/to/man/pages
```

### Automatic man page installed with setuptools and pip

This approach of installing man pages is problematic for various reasons:

#### (1) Man pages are a UNIX thing

Python in general and with that pip and setuptools are aimed to be platform independent.
Man pages are **not**: they are a UNIX thing which means setuptools does not provide a sane
solution to generate and install man pages.
We should consider using automatic man page installation only with vendor specific packaging, e.g. for `*.deb` or `*.rpm` packages.

#### (2) We want to generate man pages on the fly

First, we do not want to commit man pages to our source control.
We want to generate them on the fly. Either
during build or installation time.

With setuptools and pip we face two problems:

1. If we generate and install them during installation of the package pip does not know about the man pages and thus cannot uninstall it.
2. If we generate them in our build process and add them to your distribution we do not have a way to prevent installation to */usr/share/man* for non-UNIX-like Operating Systems.

### Debian packages

The `debhelper` packages provides a very convenient script called `dh_installman`.
It checks for the `debian/(pkg_name.)manpages` file and it contents which is basically a line by line list of man pages or globs:

```
debian/tmp/manpages/*
```

We override the rule provided by `dh_installman` to generate our man pages in advance, like this:

```Makefile
override_dh_installman:
	python3 setup.py --command-packages=click_man.commands man_pages --target debian/tmp/manpages
	dh_installman -O--buildsystem=pybuild
```

Checkout a working example here: [repo debian package](https://github.com/timofurrer/click-man/tree/master/examples/debian_pkg)
