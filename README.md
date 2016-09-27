# click-man

[![Build Status](https://travis-ci.org/timofurrer/click-man.svg?branch=master)](https://travis-ci.org/timofurrer/click-man) [![PyPI Package version](https://badge.fury.io/py/click-man.svg)](https://pypi.python.org/pypi/click-man)

Create **man pages** for [click](https://github.com/pallets/click) application as easy as this:

```bash
python3 setup.py --command-packages=click_man.commands man_pages
```

![Demo](https://raw.githubusercontent.com/timofurrer/click-man/master/docs/asciicast.gif)

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
python setup.py --command-packages=click_man.commands man_pages
```

or specify the man pages target directory:

```bash
python setup.py --command-packages=click_man.commands man_pages --target path/to/man/pages
```

### Debian packages

*Coming soon ...*

### Standalone

*Coming soon ...*
