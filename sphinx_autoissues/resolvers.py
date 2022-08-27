# Copyright (c) 2010, 2011, 2012, 2013 Sebastian Wiesner <lunaryorn@gmail.com>
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
    sphinx_autoissues.resolvers
    ===========================

    Builtin resolvers for :mod:`sphinx_autoissues`.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""


import time
import typing as t

import requests
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_autoissues import __version__
from sphinx_autoissues.types import Issue, TrackerConfig
from sphinx_autoissues.utils import is_issuetracker_env

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/repos/{0.project}/issues/{1}"


def check_project_with_username(tracker_config: TrackerConfig) -> None:
    if "/" not in tracker_config.project:
        raise ValueError(
            "username missing in project name: {0.project}".format(tracker_config)
        )


HEADERS = {"User-Agent": f"sphinx_autoissues v{__version__}"}


def get(app: Sphinx, url: str) -> t.Optional[requests.Response]:
    """
    Get a response from the given ``url``.
    ``url`` is a string containing the URL to request via GET. ``app`` is the
    Sphinx application object.
    Return the :class:`~requests.Response` object on status code 200, or
    ``None`` otherwise. If the status code is not 200 or 404, a warning is
    emitted via ``app``.
    """
    response = requests.get(url, headers=HEADERS)
    if response.status_code == requests.codes.ok:
        return response
    elif response.status_code != requests.codes.not_found:
        msg = "GET {0.url} failed with code {0.status_code}"
        logger.warning(msg.format(response))

    return None


def lookup_github_issue(
    app: Sphinx, tracker_config: TrackerConfig, issue_id: str
) -> t.Optional[Issue]:
    check_project_with_username(tracker_config)

    env = app.env
    if is_issuetracker_env(env):
        # Get rate limit information from the environment
        timestamp, limit_hit = getattr(env, "github_rate_limit", (0, False))

        if limit_hit and time.time() - timestamp > 3600:
            # Github limits applications hourly
            limit_hit = False

        if not limit_hit:
            url = GITHUB_API_URL.format(tracker_config, issue_id)
            response = get(app, url)
            if response:
                rate_remaining = response.headers.get("X-RateLimit-Remaining")
                assert rate_remaining is not None
                if rate_remaining.isdigit() and int(rate_remaining) == 0:
                    logger.warning("Github rate limit hit")
                    env.github_rate_limit = (time.time(), True)
                issue = response.json()
                closed = issue["state"] == "closed"
                return Issue(
                    id=issue_id,
                    title=issue["title"],
                    closed=closed,
                    url=issue["html_url"],
                )
        else:
            logger.warning(
                "Github rate limit exceeded, not resolving issue {0}".format(issue_id)
            )
    return None


BUILTIN_ISSUE_TRACKERS = {
    "github": lookup_github_issue,
}
