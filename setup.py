import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='click-man',
    version='0.4.2',
    url='https://github.com/click-contrib/click-man',
    license='MIT',
    description='Generate man pages for click based CLI applications',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Timo Furrer',
    author_email='tuxtimo@gmail.com',
    install_requires=[
        'click',
        'setuptools',
    ],
    packages=find_packages(exclude=('tests', )),
    entry_points={
        'console_scripts': [
            'click-man = click_man.__main__:cli',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
    ],
)
