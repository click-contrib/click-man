from setuptools import setup, find_packages

setup(
    name='click-man',
    version='0.2.1',
    license='MIT',
    description='Generate man pages for click based CLI applications',
    author='Timo Furrer',
    author_email='tuxtimo@gmail.com',
    install_requires=[
        'click'
    ],
    packages=find_packages()
)
