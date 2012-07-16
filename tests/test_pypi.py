# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012 Sebastian Wiesner <lunaryorn@gmail.com>
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

"""
    test_pypi
    =========

    Test that this package is handled correctly on the cheeseshop.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import os
import sys
from subprocess import Popen, PIPE, CalledProcessError

import pytest


@pytest.mark.skipif(str('sys.version_info[0] > 2'))
def test_description_rendering():
    """
    If this test raises any exception ReST rendering on PyPI will fail.

    It calls out to the renderer via subprocess to get a clean docutils import.
    Sphinx heavily monkey-patches some docutils internals, which causes
    different rendering and sometimes even exceptions.
    """
    test_directory = os.path.abspath(os.path.dirname(__file__))
    source_directory = os.path.abspath(os.path.join(test_directory, os.pardir))
    pypi = os.path.join(test_directory, 'pypi.py')
    readme = os.path.join(source_directory, 'README.rst')

    cmd = [sys.executable, pypi, readme]
    proc = Popen(cmd, stdout=PIPE)
    stdout = proc.communicate()[0]
    if proc.returncode != 0:
        raise CalledProcessError(proc.returncode, cmd)
    assert stdout
