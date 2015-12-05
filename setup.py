#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from annex import __version__

class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--recreate']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

tests_require = open(os.path.join(os.path.dirname(__file__), 'requirements_test.txt')).read().split()

setup(
    name = "python-annex",
    version = __version__,
    packages = find_packages(exclude=["__pycache__"]),
    cmdclass={
        'test': Tox,
     },
    install_requires=[
        'six>=1.7.3',
	'schematics>=1.1.1',
	'gitpython>=1.0.1',
    ],
    tests_require=tests_require, 
)
