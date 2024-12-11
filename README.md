# click-man

[![Build Status](https://github.com/click-contrib/click-man/actions/workflows/ci.yaml/badge.svg)](https://github.com/click-contrib/click-man/actions/workflows/ci.yaml) [![PyPI Package version](https://badge.fury.io/py/click-man.svg)](https://pypi.python.org/pypi/click-man)

Create **man pages** for [click](https://github.com/pallets/click) application as easy as this:

```bash
click-man foo
```

where `foo` is the name of your script, as defined in [`console_scripts`](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point).

→ Checkout the [debian packaging example](#debian-packages)

## What it does

*click-man* will generate one man page per command of your click CLI application specified in `console_scripts` in your `setup.py` / `setup.cfg` / `pyproject.toml`.

## Installation

```bash
pip install click-man
```

## Usage

The following sections describe different usage example for *click-man*.

### CLI

**click-man** provides its own command line tool which can be passed the name of an installed script:

```bash
click-man commandname
```

where `commandname` is the name of an installed `console_script` entry point.

To specify a target directory for the man pages, use the `--target` option:

```bash
click-man --target path/to/man/pages commandname
```

You can use the `manpath` command or `MANPATH` environment variable to identify where man pages can be placed.

### Automatic man page installation with setuptools and pip

While earlier version of click-man provided a distutils hook that could be used to automatically install man pages,
this approach had a number of caveats as outlined [below][issues-with-automatic-man-page-installation].
distutils was removed from Python stdlib in Python 3.12 and the distutils hook was removed from **click-man** in v0.5.0.

### Debian packages

The `debhelper` packages provides a very convenient script called `dh_installman`.
It checks for the `debian/(pkg_name.)manpages` file and it's content which is basically a line by line list of man pages or globs:

```
debian/tmp/manpages/*
```

We override the rule provided by `dh_installman` to generate our man pages in advance, like this:

```Makefile
override_dh_installman:
	click-man <executable> --target debian/tmp/manpages
	dh_installman -O--buildsystem=pybuild
```

Now we are able to build a Debian package with the tool of our choice, e.g.:

```bash
debuild -us -uc
```

Checkout a working example here: [repo debian package](https://github.com/click-contrib/click-man/tree/master/examples/debian_pkg)

### Other distro packages

To include man pages in packages for other package managers like `dnf`, `zypper`, or `pacman`, you will likely need to do one of the following:

* For upstream maintainers: generate man pages as part of a build release process and include them in version control or your generated sdists
* For packagers: generate man pages as part of the package build process and include these in the RPMs or tarballs, along with the relevant stanzas in the package definition

If you are packaging utilities, we would welcome PRs documenting best practices for those using **click-man** to document their utilities.

## Issues with automatic man page installation

### Man pages are a UNIX thing

Python in general and with that pip and setuptools are aimed to be platform independent.
Man pages are **not**: they are a UNIX thing which means setuptools does not provide a sane solution to generate and install man pages.
We should consider using automatic man page installation only with vendor specific packaging, e.g. for `*.deb` or `*.rpm` packages.

### Man pages are not compatible with Python virtualenvs

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

### We want to generate man pages on the fly

First, we do not want to commit man pages to our source control.
We want to generate them on the fly, either during build or installation time.

With setuptools and pip we face two problems:

1. If we generate and install them during installation of the package pip does not know about the man pages and thus cannot uninstall it.
2. If we generate them in our build process and add them to your distribution we do not have a way to prevent installation to */usr/share/man* for non-UNIX-like Operating Systems or from within virtualenvs.
