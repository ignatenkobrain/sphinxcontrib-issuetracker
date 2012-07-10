##########################
sphinxcontrib-issuetracker
##########################

.. image:: https://secure.travis-ci.org/lunaryorn/sphinxcontrib-issuetracker.png
   :target: http://travis-ci.org/lunaryorn/sphinxcontrib-issuetracker

http://sphinxcontrib-issuetracker.readthedocs.org/

A Sphinx_ extension to reference issues in issue trackers, either explicitly
with an "issue" role or optionally implicitly by issue ids like ``#10`` in
plaintext.

Currently the following issue trackers are supported:

- `GitHub <http://github.com>`_
- `BitBucket <http://bitbucket.org>`_
- `Launchpad <https://launchpad.net>`_
- `Google Code <http://code.google.com>`_
- `Debian BTS <http://bugs.debian.org>`_
- `Jira <http://www.atlassian.com/software/jira/>`_

A simple API is provided to add support for other issue trackers.  If you added
support for a new tracker, please consider sending a patch to make your work
available to other users of this extension.


Installation
------------

This extension can be installed from the `Python Package Index`_::

   pip install sphinxcontrib-issuetracker

This extension requires Sphinx 1.1 and Pythonn 2.6 or Python 3.1.


Usage
-----

Just add this extension to ``extensions`` and configure your issue tracker::

   extensions = ['sphinxcontrib.issuetracker']

   issuetracker = 'github'
   issuetracker_project = 'lunaryorn/sphinxcontrib-issuetracker'

Now issue references like ``#10`` are replaced with links to the issue tracker
of this extension, unless the reference occurs in literal text like inline
literals or code blocks.

You can disable this magic behaviour by setting issuetracker_plaintext_issues
to ``False``::

   issuetracker_plaintext_issues = False

Now textual references are no longer replaced. However, you can still explicitly
reference issues with the ``issue`` role.

For more details refer to the documentation_.


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


.. _Sphinx: http://sphinx.pocoo.org/latest
.. _documentation: http://sphinxcontrib-issuetracker.readthedocs.org
.. _Python package index: http://pypi.python.org/pypi/sphinxcontrib-issuetracker
.. _issue tracker: https://github.com/lunaryorn/sphinxcontrib-issuetracker/issues/
.. _pep8: http://pypi.python.org/pypi/pep8/
