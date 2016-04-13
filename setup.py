#!/usr/bin/env python

import os

from setuptools import setup


__dirname = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(__dirname, 'README.md')) as readme:
    README = readme.read()

setup(
    name='httpobs-cli',
    version=1.0,
    description='HTTP Observatory: command line to scan your website.',
    url='https://github.com/mozilla/http-observatory-cli',
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Topic :: Internet :: HTTP Servers',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
    ],
    author='April King',
    author_email='april@mozilla.com',
    packages=[],
    include_package_data=True,
    scripts=['httpobs-cli/scripts/httpobs'],
    zip_safe=False,
)