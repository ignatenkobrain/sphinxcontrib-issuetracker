# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011, 2012 Sebastian Wiesner <lunaryorn@gmail.com>
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
    sphinx_autoissues
    =================

    Integration with issue trackers.

    Provide explicit and (optionally) implicit (e.g. ``#10``) references to
    issues in issue trackers.

    .. moduleauthor::  Tony Narlock <tony@git-pull.com,
       Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "0.0.1a0"

import dataclasses
import re
import typing as t
from os import path

from docutils import nodes
from docutils.transforms import Transform
from sphinx.addnodes import pending_xref
from sphinx.config import Config
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.console import bold
from sphinx.util.osutil import copyfile

logger = logging.getLogger(__name__)


class Issue(t.NamedTuple):
    id: str
    title: str
    url: str
    closed: bool


@dataclasses.dataclass
class TrackerConfig:
    project: str
    url: t.Optional[str] = None

    """
    Issue tracker configuration.
    This class provides configuration for trackers, and is passed as
    ``tracker_config`` arguments to callbacks of
    :event:`issuetracker-lookup-issue`.
    """

    def __post_init__(self) -> None:
        if self.url is not None:
            self.url = self.url.rstrip("/")

    @classmethod
    def from_sphinx_config(cls, config: Config) -> "TrackerConfig":
        """
        Get tracker configuration from ``config``.
        """
        project = config.issuetracker_project or config.project
        url = config.issuetracker_url
        return cls(project=project, url=url)


class IssueRole(XRefRole):
    """
    Standard Sphinx cross-referencing role to reference issues.

    Supports standard Sphinx :ref:`cross-referencing syntax <xref-syntax>`.  An
    explicit title is interpreted as :xref:`format string <formatstrings>`,
    with the :class:`Issue` object of the referenced issue available by the
    ``issue`` key.
    """

    innernodeclass = nodes.inline

    def process_link(self, env, refnode, has_explicit_title, title, target):
        # store the tracker config in the reference node
        refnode["trackerconfig"] = TrackerConfig.from_sphinx_config(env.config)
        return title, target


class IssueReferences(Transform):
    """
    Parse and transform issue ids in a document.

    Issue ids are parsed in text nodes and transformed into
    :class:`~sphinx.addnodes.pending_xref` nodes for further processing in
    later stages of the build.
    """

    default_priority = 999

    def apply(self):
        config = self.document.settings.env.config
        tracker_config = TrackerConfig.from_sphinx_config(config)
        issue_pattern = config.issuetracker_issue_pattern
        title_template = config.issuetracker_title_template
        if isinstance(issue_pattern, str):
            issue_pattern = re.compile(issue_pattern)
        for node in self.document.traverse(nodes.Text):
            parent = node.parent
            if isinstance(parent, (nodes.literal, nodes.FixedTextElement)):
                # ignore inline and block literal text
                continue
            text = str(node)
            new_nodes = []
            last_issue_ref_end = 0
            for match in issue_pattern.finditer(text):
                # catch invalid pattern with too many groups
                if len(match.groups()) != 1:
                    raise ValueError(
                        "issuetracker_issue_pattern must have "
                        "exactly one group: {0!r}".format(match.groups())
                    )
                # extract the text between the last issue reference and the
                # current issue reference and put it into a new text node
                head = text[last_issue_ref_end : match.start()]
                if head:
                    new_nodes.append(nodes.Text(head))
                # adjust the position of the last issue reference in the
                # text
                last_issue_ref_end = match.end()
                # extract the issue text (including the leading dash)
                issuetext = match.group(0)
                # extract the issue number (excluding the leading dash)
                issue_id = match.group(1)
                # turn the issue reference into a reference node
                refnode = pending_xref()
                refnode["reftarget"] = issue_id
                refnode["reftype"] = "issue"
                refnode["trackerconfig"] = tracker_config
                reftitle = title_template or issuetext
                refnode.append(
                    nodes.inline(issuetext, reftitle, classes=["xref", "issue"])
                )
                new_nodes.append(refnode)
            if not new_nodes:
                # no issue references were found, move on to the next node
                continue
            # extract the remaining text after the last issue reference, and
            # put it into a text node
            tail = text[last_issue_ref_end:]
            if tail:
                new_nodes.append(nodes.Text(tail))
            # find and remove the original node, and insert all new nodes
            # instead
            parent.replace(node, new_nodes)


def make_issue_reference(issue, content_node):
    """
    Create a reference node for the given issue.

    ``content_node`` is a docutils node which is supposed to be added as
    content of the created reference.  ``issue`` is the :class:`Issue` which
    the reference shall point to.

    Return a :class:`docutils.nodes.reference` for the issue.
    """
    reference = nodes.reference()
    reference["refuri"] = issue.url
    if issue.title:
        reference["reftitle"] = issue.title
    if issue.closed:
        content_node["classes"].append("closed")
    reference.append(content_node)
    return reference


def lookup_issue(app, tracker_config, issue_id):
    """
    Lookup the given issue.

    The issue is first looked up in an internal cache.  If it is not found, the
    event ``issuetracker-lookup-issue`` is emitted.  The result of this
    invocation is then cached and returned.

    ``app`` is the sphinx application object.  ``tracker_config`` is the
    :class:`TrackerConfig` object representing the issue tracker configuration.
    ``issue_id`` is a string containing the issue id.

    Return a :class:`Issue` object for the issue with the given ``issue_id``,
    or ``None`` if the issue wasn't found.
    """
    cache = app.env.issuetracker_cache
    if issue_id not in cache:
        issue = app.emit_firstresult(
            "issuetracker-lookup-issue", tracker_config, issue_id
        )
        cache[issue_id] = issue
    return cache[issue_id]


def lookup_issues(app, doctree):
    """
    Lookup issues found in the given ``doctree``.

    Each issue reference in the given ``doctree`` is looked up.  Each lookup
    result is cached by mapping the referenced issue id to the looked up
    :class:`Issue` object (an existing issue) or ``None`` (a missing issue).

    The cache is available at ``app.env.issuetracker_cache`` and is pickled
    along with the environment.
    """
    for node in doctree.traverse(pending_xref):
        if node["reftype"] == "issue":
            lookup_issue(app, node["trackerconfig"], node["reftarget"])


def resolve_issue_reference(app, env, node, contnode):
    """
    Resolve an issue reference and turn it into a real reference to the
    corresponding issue.

    ``app`` and ``env`` are the Sphinx application and environment
    respectively.  ``node`` is a ``pending_xref`` node representing the missing
    reference.  It is expected to have the following attributes:

    - ``reftype``: The reference type
    - ``trackerconfig``: The :class:`TrackerConfig`` to use for this node
    - ``reftarget``: The issue id
    - ``classes``: The node classes

    References with a ``reftype`` other than ``'issue'`` are skipped by
    returning ``None``.  Otherwise the new node is returned.

    If the referenced issue was found, a real reference to this issue is
    returned.  The text of this reference is formatted with the :class:`Issue`
    object available in the ``issue`` key.  The reference title is set to the
    issue title.  If the issue is closed, the class ``closed`` is added to the
    new content node.

    Otherwise, if the issue was not found, the content node is returned.
    """
    if node["reftype"] != "issue":
        return None

    issue = lookup_issue(app, node["trackerconfig"], node["reftarget"])
    if not issue:
        return contnode
    else:
        classes = contnode["classes"]
        conttext = str(contnode[0])
        formatted_conttext = nodes.Text(conttext.format(issue=issue))
        formatted_contnode = nodes.inline(conttext, formatted_conttext, classes=classes)
        return make_issue_reference(issue, formatted_contnode)


def connect_builtin_tracker(app):
    from sphinx_autoissues.resolvers import BUILTIN_ISSUE_TRACKERS

    if app.config.issuetracker:
        tracker = BUILTIN_ISSUE_TRACKERS[app.config.issuetracker.lower()]
        app.connect(str("issuetracker-lookup-issue"), tracker)


def add_stylesheet(app):
    app.add_stylesheet("issuetracker.css")


def init_cache(app):
    if not hasattr(app.env, "issuetracker_cache"):
        app.env.issuetracker_cache = {}


def init_transformer(app):
    if app.config.issuetracker_plaintext_issues:
        app.add_transform(IssueReferences)


def copy_stylesheet(app, exception):
    if app.builder.name != "html" or exception:
        return
    logger.info(bold("Copying issuetracker stylesheet... "), nonl=True)
    dest = path.join(app.builder.outdir, "_static", "issuetracker.css")
    source = path.join(path.abspath(path.dirname(__file__)), "issuetracker.css")
    copyfile(source, dest)
    logger.info("done")


def setup(app):
    app.require_sphinx("1.0")
    app.add_role("issue", IssueRole())
    app.add_event(str("issuetracker-lookup-issue"))
    app.connect(str("builder-inited"), connect_builtin_tracker)
    # general configuration
    app.add_config_value("issuetracker", None, "env")
    app.add_config_value("issuetracker_project", None, "env")
    app.add_config_value("issuetracker_url", None, "env")
    app.add_config_value("issuetracker_redmine_key", None, "env")
    app.add_config_value("issuetracker_redmine_username", None, "env")
    app.add_config_value("issuetracker_redmine_password", None, "env")
    app.add_config_value("issuetracker_redmine_requests", {}, "env")
    # configuration specific to plaintext issue references
    app.add_config_value("issuetracker_plaintext_issues", True, "env")
    app.add_config_value("issuetracker_issue_pattern", re.compile(r"#(\d+)"), "env")
    app.add_config_value("issuetracker_title_template", None, "env")
    app.connect(str("builder-inited"), add_stylesheet)
    app.connect(str("builder-inited"), init_cache)
    app.connect(str("builder-inited"), init_transformer)
    app.connect(str("doctree-read"), lookup_issues)
    app.connect(str("missing-reference"), resolve_issue_reference)
    app.connect(str("build-finished"), copy_stylesheet)
