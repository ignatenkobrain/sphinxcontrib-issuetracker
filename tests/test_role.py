# -*- coding: utf-8 -*-
# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@gmail.com>
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
    test_role
    =========

    Test the ``issue`` role.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from sphinx_autoissues import Issue


@pytest.fixture
def issue(request: pytest.FixtureRequest):
    """
    A dummy issue, just to trigger issue resolval so that transformations can
    be seen in the output.
    """
    return Issue(id="10", title="Eggs", closed=False, url="eggs")


@pytest.mark.with_content(":issue:`10`")
def test_simple(doctree, issue):
    """
    Test simple usage of the role.
    """
    pytest.assert_issue_pending_xref(doctree, "10", "10")


@pytest.mark.with_content(":issue:`foo <10>`")
def test_with_title(doctree, issue):
    """
    Test role with an explicit title.
    """
    pytest.assert_issue_pending_xref(doctree, "10", "foo")


@pytest.mark.confoverrides(issuetracker_plaintext_issues=False)
@pytest.mark.with_content(":issue:`10` #10")
def test_without_plaintext_issues(doctree, issue):
    """
    Test that the role still works even if plaintext issues are disabled.
    """
    pytest.assert_issue_pending_xref(doctree, "10", "10")
