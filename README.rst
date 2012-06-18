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

- `GitHub <http//github.com>`_
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

This extension can be installed from the Python Package Index::

   pip install sphinxcontrib-issuetracker


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


.. _Sphinx: http://sphinx.pocoo.org/latest
.. _documentation: http://packages.python.org/sphinxcontrib-issuetracker
