# `sphinx-autoissues` &middot; [![Python Package](https://img.shields.io/pypi/v/sphinx-autoissues.svg)](https://pypi.org/project/sphinx-autoissues/) [![License](https://img.shields.io/github/license/tony/sphinx-autoissues.svg)](https://github.com/tony/sphinx-autoissues/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/tony/sphinx-autoissues/branch/master/graph/badge.svg)](https://codecov.io/gh/tony/sphinx-autoissues)

<https://sphinx-autoissues.git-pull.com/>

This is a fork of Sebastian Wiesner <lunaryorn@gmail.com>'s excellent
[sphinxcontrib-issuetracker](https://github.com/lunaryorn/sphinxcontrib-issuetracker) plugin.

A [Sphinx](https://www.sphinx-doc.org/en/latest) extension to reference issues in issue trackers,
either explicitly with an "issue" role or optionally implicitly by issue ids like `#10` in
plaintext.

Currently the following issue trackers are supported: [GitHub](https://github.com)

A simple API is provided to add support for other issue trackers. If you added support for a new
tracker, please consider sending a patch to make your work available to other users of this
extension.

## What's changed from sphinx-issuetracker?

The old codebase has most of its commits from 2010-2012. For that time, the quality is impeccable,
but a lot has happened tooling wise.

We've incorporated the python toolset from git-pull projects like tmuxp / libvcs / cihai: mypy,
black, isort, pytest, markdown docs w/ doctests, github workflows, etc. In addition:

- Python 2.x support removed via `pyupgrade` and by hand
  - Compat import, `__future__` statements
- Poetry
- Minimum python version 3.7
- Updated to latest sphinx (from 1.1)
  - Import changes
  - See [sphinx deprecations](https://www.sphinx-doc.org/en/master/extdev/deprecated.html)
- Updated to latest pytest (from 2.2)
  - Remove `funcargs` and marker usage that wouldn't work in pytest 7+
  - See [pytest deprecations](https://docs.pytest.org/en/7.1.x/deprecations.html)

## Installation

This extension can be installed from the
[Python Package Index](http://pypi.python.org/pypi/sphinx-autoissues):

```console
$ pip install sphinx-autoissues
```

This extension requires Sphinx 1.1 and Python 2.6 or Python 3.1.

## Usage

Just add this extension to `extensions` and configure your issue tracker:

```python
extensions = ['sphinx_autoissues']
```

```python
issuetracker = 'github'
issuetracker_project = 'tony/sphinx-autoissues'
```

Now issue references like `#10` are replaced with links to the issue tracker of this extension,
unless the reference occurs in literal text like inline literals or code blocks.

You can disable this magic behaviour by setting `issuetracker_plaintext_issues` to `False`:

```python
issuetracker_plaintext_issues = False
```

Now textual references are no longer replaced. However, you can still explicitly reference issues
with the `issue` role.

For more details refer to the [documentation](https://sphinx-autoissues.git-pull.com).

## Support

Please report issues to the [issue tracker](https://github.com/tony/sphinx-autoissues/issues/) if
you have trouble, found a bug in this extension or lack support for a specific issue tracker, but
respect the following rules:

- Check that the issue has not already been reported.
- Check that the issue is not already fixed in the `master` branch.
- Open issues with clear title and a detailed description in grammatically correct, complete
  sentences.

## Development

The source code is hosted on [Github](https://github.com/):

```console
$ git clone https://github.com/tony/sphinx-autoissues
```

Please fork the repository and send pull requests with your fixes or cool new features, but respect
the following rules:

- Read
  [how to properly contribute to open source projects on GitHub](http://gun.io/blog/how-to-github-fork-branch-and-pull-request/).
- Use a topic branch to easily amend a pull request later, if necessary.
- Write
  [good commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
- Squash commits on the topic branch before opening a pull request.
- Respect `8` (use [pep8](https://pypi.python.org/pypi/pep8/) to check your coding style compliance)
- Add unit tests
- Open a [pull request](https://help.github.com/articles/using-pull-requests) that relates to but
  one subject with a clear title and description in grammatically correct, complete sentences.

[![Docs](https://github.com/tony/sphinx-autoissues/workflows/docs/badge.svg)](https://sphinx-autoissues.git-pull.com/)
[![Build Status](https://github.com/tony/sphinx-autoissues/workflows/tests/badge.svg)](https://github.com/tony/sphinx-autoissues/actions?query=workflow%3A%22tests%22)
