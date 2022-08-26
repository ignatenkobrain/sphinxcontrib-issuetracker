import dataclasses
import typing as t

from docutils import nodes
from sphinx.addnodes import pending_xref
from sphinx.config import Config
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole


class IssueTrackerBuildEnvironment(BuildEnvironment):
    tracker_config: "TrackerConfig"
    issuetracker_cache: "IssueTrackerCache"
    github_rate_limit: t.Tuple[float, bool]


class Issue(t.NamedTuple):
    id: str
    title: str
    url: str
    closed: bool


IssueTrackerCache = t.Dict[str, Issue]


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

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: nodes.reference,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> t.Tuple[str, str]:
        # store the tracker config in the reference node
        refnode["trackerconfig"] = TrackerConfig.from_sphinx_config(env.config)
        return title, target


class PendingIssueXRef(pending_xref):
    tracker_config: TrackerConfig
