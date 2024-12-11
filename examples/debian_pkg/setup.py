from setuptools import setup, find_packages


setup(
    name='repo',
    version='0.1.0',
    install_requires=['click'],
    packages=find_packages(),
    entry_points={'console_scripts': ['repo = repo.__main__:cli']},
)
