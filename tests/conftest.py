import pathlib
import sys
import typing as t

import pytest

from sphinx.testing.path import path as sphinx_path

pytest_plugins = "sphinx.testing.fixtures"

AppParams = t.Tuple[t.Any, t.Dict[str, t.Any]]

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


class MakeAppParams(Protocol):
    def __call__(
        self,
        tracker: t.Optional[str] = ...,
        #: test-specific tracker configuration
        tracker_config: t.Optional[t.Any] = ...,
        #: index content
        index: t.Optional[t.Union[t.IO[str], str]] = ...,
        *args: object,
        **kwargs: t.Any,
    ) -> AppParams:
        ...


@pytest.fixture(scope="function")
def make_app_params(
    request: pytest.FixtureRequest,
    app_params: AppParams,
    tmp_path: pathlib.Path,
) -> t.Generator[t.Callable[[t.Any], AppParams], None, None]:
    def fn(*args: object, **kwargs: t.Any) -> AppParams:
        args, kwargs = app_params
        kwargs.setdefault("confoverrides", {"extensions": "sphinx_autoissues"})
        kwargs.setdefault("buildername", "html")
        kwargs.setdefault("status", None)
        kwargs.setdefault("warning", None)
        kwargs.setdefault("freshenv", True)
        kwargs["srcdir"] = sphinx_path(tmp_path)
        return args, kwargs

    yield fn


@pytest.fixture(scope="function")
def make_autoissues_test_app_params(
    request: pytest.FixtureRequest,
    make_app_params: t.Callable[[t.Any, t.Any], AppParams],
) -> t.Generator[MakeAppParams, None, None]:
    """sphinx.testing.fixtures.app_params() with autoissues test fixtures"""

    def fn(
        #: The tracker name as string, or ``None``, if no tracker is known.
        tracker: t.Optional[str] = None,
        #: test-specific tracker configuration
        tracker_config: t.Optional[t.Any] = None,
        #: index content
        index: t.Optional[t.Union[t.IO[str], str]] = None,
        *args: object,
        **kwargs: t.Any,
    ) -> AppParams:
        args, kwargs = make_app_params(*args, **kwargs)
        kwargs.setdefault("confoverrides", {})
        if tracker is not None:
            kwargs["confoverrides"]["issuetracker"] = tracker
        if tracker_config is not None:
            # bring tracker configuration in
            kwargs["confoverrides"].update(
                issuetracker_project=tracker_config.project,
                issuetracker_url=tracker_config.url,
            )

        (kwargs["srcdir"] / "conf.py").write_text("", encoding="utf8")
        if index is not None:
            (kwargs["srcdir"] / "index.rst").write_text(index, encoding="utf8")

        return args, kwargs

    yield fn
