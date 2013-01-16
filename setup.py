# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012, Sebastian Wiesner <lunaryorn@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import re

from setuptools import setup, find_packages


with open('README.rst') as stream:
    long_desc = stream.read()


VERSION_PATTERN = re.compile(r"__version__ = '([^']+)'")
VERSION_FILE = os.path.join('sphinxcontrib', 'issuetracker', '__init__.py')


def read_version_number():
    with open(VERSION_FILE) as stream:
        for line in stream:
            match = VERSION_PATTERN.search(line)
            if match:
                return match.group(1)
        else:
            raise ValueError('Could not extract version number')


setup(
    name='sphinxcontrib-issuetracker',
    version=read_version_number(),
    url='http://sphinxcontrib-issuetracker.readthedocs.org/',
    license='BSD',
    author='Sebastian Wiesner',
    author_email='lunaryorn@gmail.com',
    description='Sphinx integration with different issuetrackers',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Sphinx>=1.1', 'requests>=0.13,<1.0.3'],
    namespace_packages=['sphinxcontrib'],
)
