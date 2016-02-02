#!/usr/bin/env python

import sys

from setuptools import setup

setup(
    name='Signaller',
    version='1.1.0',
    description='Signals and slots implementation with asyncio support',
    author='Michal Krenek (Mikos)',
    author_email='m.krenek@gmail.com',
    url='https://github.com/xmikos/signaller',
    license='MIT',
    py_modules=['signaller'],
    install_requires=[],
    keywords='signal slot dispatch dispatcher observer event notify asyncio weakref',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
