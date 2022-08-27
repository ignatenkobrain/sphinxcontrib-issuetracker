import sys
import typing as t

from sphinx_autoissues.types import IssueTrackerBuildEnvironment

if t.TYPE_CHECKING:
    if sys.version_info >= (3, 10):
        from typing import TypeGuard
    else:
        from typing_extensions import TypeGuard


def is_issuetracker_env(
    env: t.Any,
) -> "TypeGuard['IssueTrackerBuildEnvironment']":
    return hasattr(env, "issuetracker_cache") and env.issuetracker_cache is not None
