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
    test_tracker_config
    ===================

    Test the TrackerConfig class.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from sphinx_autoissues import TrackerConfig


@pytest.fixture
def content(request: pytest.FixtureRequest):
    """
    Dummy content for this test module, overrides the global ``content``
    funcarg.

    This test module doesn't need issue references, but just configured sphinx
    application to check creating tracker configs from sphinx config.
    """
    return "dummy content"


def test_tracker_config_only_project():
    """
    Test TrackerConfig constructor with a project only.
    """
    tracker_config = TrackerConfig("eggs")
    assert tracker_config.project == "eggs"


def test_tracker_config_project_and_url():
    """
    Test TrackerConfig constructor with a project and url.
    """
    tracker_config = TrackerConfig("eggs", "http://example.com")
    assert tracker_config.project == "eggs"
    assert tracker_config.url == "http://example.com"


def test_tracker_config_trailing_slash():
    """
    Test that the constructor removes trailing slashes from the url.
    """
    tracker_config = TrackerConfig("eggs", "http://example.com//")
    assert tracker_config.url == "http://example.com"


def test_tracker_config_equality():
    """
    Test equality and inequality of TrackerConfig objects.
    """
    c = TrackerConfig
    assert c("eggs") == c("eggs")
    assert c("eggs") != c("spam")
    assert c("eggs") != c("eggs", "spam")
    assert c("eggs", "spam") == c("eggs", "spam")
    assert c("eggs", "spam") != c("eggs", "foo")
    assert c("eggs", "spam") != c("spam", "spam")


@pytest.mark.confoverrides(project="eggs", issuetracker_url="http://example.com")
def test_tracker_config_from_sphinx_config_implicit_project(app):
    """
    Test that TrackerConfig uses the Sphinx project name, if the issuetracker
    project was not explicitly set.
    """
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == "eggs"
    assert tracker_config.url == "http://example.com"


@pytest.mark.confoverrides(
    project="eggs", issuetracker_project="spam", issuetracker_url="http://example.com"
)
def test_tracker_config_from_sphinx_config_explicit_project(app):
    """
    Test that TrackerConfig uses the issuetracker project, if it was explicitly
    set.
    """
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == "spam"
    assert tracker_config.url == "http://example.com"


@pytest.mark.confoverrides(project="eggs", issuetracker_url="http://example.com//")
def test_tracker_config_from_sphinx_config_trailing_slash(app):
    """
    Test that TrackerConfig strips trailing slashes when creating from sphinx
    config, too.
    """
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == "eggs"
    assert tracker_config.url == "http://example.com"
