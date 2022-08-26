import typing as t

from sphinx.testing.util import SphinxTestApp

from sphinx_autoissues import Issue, TrackerConfig

if t.TYPE_CHECKING:
    from .conftest import MakeAppParams


def test_lookup(
    make_app: t.Callable[[t.Any], SphinxTestApp],
    make_autoissues_test_app_params: "MakeAppParams",
) -> None:
    """
    Test that this tracker correctly looks up an issue.
    """
    args, kwargs = make_autoissues_test_app_params(
        tracker="github",
        tracker_config=TrackerConfig("tmux-python/tmuxp"),
        index="#10",
    )
    app = make_app(*args, **kwargs)
    app.build()
    assert app.env.issuetracker_cache == {  # type: ignore
        "10": Issue(
            id="10",
            title="Release 0.1 (ignore, created by mistake)",
            url="https://github.com/tmux-python/tmuxp/issues/10",
            closed=True,
        )
    }
