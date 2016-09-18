# click-man

*Under heavy development - feedback more than welcome!*

It's never been easier to generate man pages for a python click CLI application:

```bash
pip install click_man
python setup.py --command-packages=click_man.commands man_pages
```

![Demo](https://raw.githubusercontent.com/timofurrer/click-man/master/docs/asciicast.gif)


This will create a `man` folder with all the man pages generated for this click application.

## How does it find my click application

**click-man** finds the click application because you've defined it in the `entry_points` map in your `setup.py`.

## Installation

**click-man** is Python 2 and 3 compatible.

```bash
pip install click-man
pip3 install click-man
```

## Invoke

**click-man** provides a sane setuptools command extension which can be used like the following:

```bash
python setup.py --command-packages=click_man.commands man_pages
```

or specify the man pages target directory:

```bash
python setup.py --command-packages=click_man.commands man_pages --target path/to/man/pages
```
