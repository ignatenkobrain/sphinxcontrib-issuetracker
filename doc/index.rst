sphinxcontrib.issuetracker -- Reference issues in issue trackers
================================================================

A Sphinx_ extension to reference issues in an issue tracker.

The extension is available under the terms of the BSD license, see
:doc:`license` for more information.


Installation
------------

Use ``pip`` to install this extension straight from the `Python Package
Index`_::

   pip install sphinxcontrib-issuetracker

This extension requires Sphinx 1.1 and Python 2.6 or Python 3.1.

.. note::

   Some builtin issue trackers do *not* support Python 3 currently. Refer to
   :confval:`issuetracker` for more information.


Usage
-----

Add this extension to :confval:`extensions` and configure the issue tracker to
use and the project in your :file:`conf.py`::

   extensions = ['sphinxcontrib.issuetracker']

   issuetracker = 'github'
   issuetracker_project = 'lunaryorn/sphinxcontrib-issuetracker'

Now issue references like ``#10`` are replaced with links to the `issue
tracker`_ of this extension, unless the reference occurs in literal text like
inline literals or code blocks.

You can disable this magic behaviour by setting
:confval:`issuetracker_plaintext_issues` to ``False``::

   issuetracker_plaintext_issues = False

Now textual references are no longer replaced. However, you can still explicitly
reference issues with the :rst:role:`issue` role.

For more details refer to the :doc:`usage` and :doc:`configuration` chapters. If
this extension does not yet support the issue tracker you're using, read the
:doc:`customization` chapter and implement support for your tracker.


Support
-------

Please report issues to the `issue tracker`_ if you have trouble, found a bug in
this extension or lack support for a specific issue tracker, but respect the
following rules:

- Check that the issue has not already been reported.
- Check that the issue is not already fixed in the ``master`` branch.
- Open issues with clear title and a detailed description in grammatically
  correct, complete sentences.


Development
-----------

The source code is hosted on Github_:

   git clone https://github.com/lunaryorn/sphinxcontrib-issuetracker

Please fork the repository and send pull requests with your fixes or cool new
features, but respect the following rules:

- Read `how to properly contribute to open source projects on GitHub
  <http://gun.io/blog/how-to-github-fork-branch-and-pull-request/>`_.
- Use a topic branch to easily amend a pull request later, if necessary.
- Write `good commit messages
  <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
- Squash commits on the topic branch before opening a pull request.
- Respect :pep:`8` (use `pep8`_ to check your coding style compliance)
- Add unit tests
- Open a `pull request <https://help.github.com/articles/using-pull-requests>`_
  that relates to but one subject with a clear title and description in
  grammatically correct, complete sentences.


.. include:: ../CREDITS


Contents
--------

.. toctree::

   usage
   configuration
   customization
   changes
   license

.. _Github: https://github.com/lunaryorn/sphinxcontrib-issuetracker
.. _Sphinx: http://sphinx.pocoo.org/
.. _issue tracker: https://github.com/lunaryorn/sphinxcontrib-issuetracker/issues/
.. _pep8: http://pypi.python.org/pypi/pep8/
.. _python package index: http://pypi.python.org/pypi/sphinxcontrib-issuetracker
