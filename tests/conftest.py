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

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docutils import nodes
from mock import Mock
from sphinx.addnodes import pending_xref
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.io import SphinxStandaloneReader

from sphinx_autoissues import Issue, IssueReferences

#: test configuration
CONF_PY = """\

extensions = ['sphinx_autoissues']

source_suffix = '.rst'

master_doc = 'index'

project = u'issuetracker-test'
copyright = u'2011, foo'

version = '1'
release = '1'

exclude_patterns = []

pygments_style = 'sphinx'
html_theme = 'default'
"""


def assert_issue_pending_xref(doctree, issue_id, title):
    """
    pytest helper which assert that the given ``doctree`` contains a single
    *pending* reference, which reference the given ``issue_id`` and has the
    given ``title``.
    """
    __tracebackhide__ = True
    assert len(doctree.traverse(pending_xref)) == 1
    xref = doctree.next_node(pending_xref)
    assert xref
    assert xref["reftarget"] == issue_id
    assert xref.astext() == title
    content = xref.next_node(nodes.inline)
    assert content
    classes = set(content["classes"])
    assert classes == set(["xref", "issue"])


def assert_issue_xref(doctree, issue, title):
    """
    pytest helper which asserts that the given ``doctree`` contains a single
    *resolved* reference, which references the given ``issue`` and has the
    given ``title``.

    Return the reference node.  Raise :exc:`~exceptions.AssertionError` if the
    ``doctree`` doesn't contain a reference to the given ``issue``.
    """
    __tracebackhide__ = True
    assert len(doctree.traverse(nodes.reference)) == 1
    reference = doctree.next_node(nodes.reference)
    assert reference
    assert reference["refuri"] == issue.url
    assert reference.get("reftitle") == issue.title
    assert reference.astext() == title
    content = reference.next_node(nodes.inline)
    assert content
    classes = set(content["classes"])
    expected_classes = set(["xref", "issue"])
    if issue.closed:
        expected_classes.add("closed")
    assert classes == expected_classes
    return reference


def pytest_addoption(parser):
    """
    Add --offline and --fast options to test runner.
    """
    parser.addoption(
        "--offline",
        action="store_true",
        help="Skip tests which require network connection",
    )
    parser.addoption(
        "--fast", action="store_true", help="Skip slow tests, implies --offline"
    )


def pytest_configure(config):
    """
    Configure issue tracker tests.

    Evaluates ``--fast`` and ``--offline``, and adds ``confpy`` attribute to
    ``config`` which provides the path to the test ``conf.py`` file.
    """
    config.run_fast = config.getvalue("fast")
    config.run_offline = config.run_fast or config.getvalue("offline")

    """
    Add the following functions to the pytest namespace:

    - :func:`get_index_doctree`
    - :func:`assert_issue_xref`
    """
    pytest.assert_issue_xref = assert_issue_xref
    pytest.assert_issue_pending_xref = assert_issue_pending_xref


def pytest_runtest_setup(item):
    """
    Evaluate ``needs_network`` and ``slow`` markers with respect to
    ``--offline`` and ``--fast``
    """
    if item.config.run_offline and "needs_network" in item.keywords:
        pytest.skip("network test in offline mode")
    if item.config.run_fast and "slow" in item.keywords:
        pytest.skip("skipping slow test in fast mode")


@pytest.fixture
def content(request: pytest.FixtureRequest):
    """
    The content for the test document as string.

    By default, the content is taken from the argument of the ``with_content``
    marker.  If no such marker exists, the content is build from the id
    returned by the ``issue_id`` funcargby prepending a dash before the id.
    The issue id ``'10'`` will thus produce the content ``'#10'``.  If the
    ``issue_id`` funcarg returns ``None``, a :exc:`~exceptions.ValueError` is
    raised eventually.

    Test modules may override this funcarg to add their own content.
    """
    content_mark = request.keywords.get("with_content")
    if content_mark:
        return content_mark.args[0]
    else:
        issue_id = request.getfixturevalue("issue_id")
        if issue_id:
            return "#{0}".format(issue_id)
    raise ValueError("no content provided")


@pytest.fixture
def srcdir(request: pytest.FixtureRequest):
    """
    The Sphinx source directory for the current test as path.

    This directory contains the standard test ``conf.py`` and a single document
    named ``index.rst``.  The content of this document is the return value of
    the ``content`` funcarg.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    srcdir = tmpdir.join("src")
    srcdir.ensure(dir=True)
    srcdir.join("conf.py").write(CONF_PY.encode("utf-8"), "wb")
    content = request.getfixturevalue("content")
    srcdir.join("index.rst").write(content.encode("utf-8"), "wb")
    return srcdir


@pytest.fixture
def outdir(request: pytest.FixtureRequest):
    """
    The Sphinx output directory for the current test as path.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    return tmpdir.join("html")


@pytest.fixture
def doctreedir(request: pytest.FixtureRequest):
    """
    The Sphinx doctree directory for the current test as path.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    return tmpdir.join("doctrees")


@pytest.fixture
def doctree(request: pytest.FixtureRequest):
    """
    The transformed doctree of the ``content``.

    .. note::

       This funcarg builds the application before test execution.
    """
    app = request.getfixturevalue("app")
    app.build()
    return app.env.get_doctree("index")


@pytest.fixture
def resolved_doctree(request: pytest.FixtureRequest):
    """
    The resolved doctree of the ``content``.

    .. note::

       This funcarg builds the application before test execution.
    """
    app = request.getfixturevalue("app")
    app.build()
    return app.env.get_and_resolve_doctree("index", app.builder)


@pytest.fixture
def cache(request: pytest.FixtureRequest):
    """
    Return the issue tracker cache.

    .. note::

       This funcarg builds the application before test execution.
    """
    app = request.getfixturevalue("app")
    app.build()
    return app.env.issuetracker_cache


@pytest.fixture
def index_html_file(request: pytest.FixtureRequest):
    """
    Return the path of the ``index.html`` created by building.

    This file contains the ``content`` rendered as HTML.  The ``app`` is build
    by this funcarg to generate the ``index.html`` file.
    """
    app = request.getfixturevalue("app")
    app.build()
    outdir = request.getfixturevalue("outdir")
    return outdir.join("index.html")


def reset_global_state():
    """
    Remove global state setup by Sphinx.

    Makes sure that we got a fresh test application for each test.
    """
    try:
        SphinxStandaloneReader.transforms.remove(IssueReferences)
    except ValueError:
        pass
    StandaloneHTMLBuilder.css_files.remove("_static/issuetracker.css")


@pytest.fixture
def confoverrides(request: pytest.FixtureRequest):
    """
    Configuration value overrides for the current test as dictionary.

    By default this funcarg takes the configuration overrides from the keyword
    arguments of the ``confoverrides`` marker.  If the marker doesn't exist,
    an empty dictionary is returned.

    Test modules may override this funcarg to return custom ``confoverrides``.
    """
    confoverrides_marker = request.keywords.get("confoverrides")
    return confoverrides_marker.kwargs if confoverrides_marker else {}


@pytest.fixture
def app(request: pytest.FixtureRequest):
    """
    A Sphinx application for testing.

    The app uses the source directory from the ``srcdir`` funcarg, and writes
    to the directories given by the ``outdir`` and ``doctreedir`` funcargs.
    Additional configuration values can be inserted into this application
    through the ``confoverrides`` funcarg.

    If the marker ``mock_lookup`` is attached to the current test, the lookup
    callback returned by the ``mock_lookup`` funcarg is automatically connected
    to the ``issuetracker-lookup-issue`` event in the the created application.

    If the marker ``build_app`` is attached to the current test, the app is
    build before returning it.  Otherwise you need to build explicitly in order
    to get the output.
    """
    srcdir = request.getfixturevalue("srcdir")
    outdir = request.getfixturevalue("outdir")
    doctreedir = request.getfixturevalue("doctreedir")
    confoverrides = request.getfixturevalue("confoverrides")
    app = Sphinx(
        str(srcdir),
        str(srcdir),
        str(outdir),
        str(doctreedir),
        "html",
        confoverrides=confoverrides,
        status=None,
        warning=None,
        freshenv=True,
    )
    request.addfinalizer(reset_global_state)
    if "mock_lookup" in request.keywords:
        lookup_mock_issue = request.getfixturevalue("mock_lookup")
        app.connect(str("issuetracker-lookup-issue"), lookup_mock_issue)
    if "build_app" in request.keywords:
        app.build()
    return app


@pytest.fixture
def issue(request: pytest.FixtureRequest):
    """
    An :class:`~sphinx_autoissues.Issue` for the current test, or
    ``None``, if no issue is to be used.

    By default, this funcarg creates an issue from the arguments of the
    ``with_issue`` marker, or returns ``None``, if there is no such marker on
    the current test.

    Test modules may override this funcarg to provide their own issues for
    tests.
    """
    issue_marker = request.keywords.get("with_issue")
    if issue_marker:
        return Issue(*issue_marker.args, **issue_marker.kwargs)
    return None


@pytest.fixture
def issue_id(request: pytest.FixtureRequest):
    """
    The issue id for the current test, or ``None``, if no issue id is to be
    used.

    The issue id is taken from the ``id`` attribute of the issue returned by
    the ``issue`` funcarg.  If the ``issue`` funcarg returns ``None``, this
    funcarg also returns ``None``.
    """
    issue = request.getfixturevalue("issue")
    if issue:
        return issue.id
    else:
        return None


@pytest.fixture
def mock_lookup(request: pytest.FixtureRequest):
    """
    A mocked callback for the ``issuetracker-lookup-issue`` event as
    :class:`~mock.Mock` object.

    If the ``issue`` funcarg doesn't return ``None``, the callback will return
    this issue if the issue id given to the callback matches the id of this
    issue.  Otherwise it will always return ``None``.
    """
    lookup_mock_issue = Mock(name="lookup_mock_issue", return_value=None)
    issue = request.getfixturevalue("issue")
    if issue:

        def lookup(app, tracker_config, issue_id):
            return issue if issue_id == issue.id else None

        lookup_mock_issue.side_effect = lookup
    return lookup_mock_issue
