# click-man

It's never been easier to generate man pages for a python click CLI application.

![Demo](https://raw.githubusercontent.com/timofurrer/click-man/master/docs/asciicast.gif)

```bash
pip install click_man
python setup.py --command-packages=click_man.commands man_pages
```

This will create a `man` folder with all the man pages generated for this click application.
