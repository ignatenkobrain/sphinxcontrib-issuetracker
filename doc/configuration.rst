Configuration
=============

General configuration
---------------------

Add ``sphinxcontrib.issuetracker`` to the configuration value
:confval:`extensions` to enable this extensions and configure the extension:

.. confval:: issuetracker

   The issuetracker to use.  As of now, the following trackers are
   supported:

   - ``github``: The issue tracker of https://github.com.
   - ``bitbucket``: The issue tracker of https://bitbucket.org.
   - ``launchpad``: The issue tracker of https://launchpad.net.  To use this
     issue tracker, launchpadlib_ must be installed. This tracker is not
     supported on Python 3, because launchpadlib_ is not yet available for
     Python 3.
   - ``google code``: The issue tracker of http://code.google.com.
   - ``debian``: The Debian issue tracker at http://bugs.debian.org.  To use
     this issue tracker, debianbts_ and SOAPpy_ must be installed. This issue
     tracker is not available on Python 3, because neither debianbts_ nor 
     SOAPpy_ are available for Python 3 yet.
   - ``jira``: A Jira_ instance.  With this issue tracker
     :confval:`issuetracker_url` must be set to the base url of the Jira
     instance to use.  Otherwise a :exc:`~exceptions.ValueError` is raised when
     resolving the first issue reference.

     .. versionadded:: 0.8

.. confval:: issuetracker_project

   The project inside the issue tracker or the project, to which the issue
   tracker belongs.  Defaults to the value of :confval:`project`.

   .. note::

      In case of BitBucket and GitHub, the project name must include the name
      of the user or organization, the project belongs to.  For instance, the
      project name of Sphinx_ itself is not just ``sphinx``, but
      ``birkenfeld/sphinx`` instead.  If the user name is missing, a
      :exc:`~exceptions.ValueError` will be raised when an issue is to be
      resolved the first time.

   .. versionchanged:: 0.8
      Project names must include the user name now.

.. confval:: issuetracker_url

   The base url of the issue tracker::

      issuetracker = 'jira'
      issuetracker_url = 'https://studio.atlassian.com'

   Required by all issue trackers which do not only have a single instance, but
   many different instances on many different sites.

   .. versionadded:: 0.8


Plaintext issues
----------------

.. confval:: issuetracker_plaintext_issues

   If ``True`` (the default) issue references are extracted from plain text by
   turning issue ids like ``#10`` into references to the corresponding issue.
   Issue ids in any kind of literal text (e.g. ``inline literals`` or code
   blocks) are ignored.  If ``False``, no issue references are created from
   plain text.

   Independently of this configuration value, you can always reference issues
   explicitly with the :rst:role:`issue` role.

   .. versionadded:: 0.9

By default the extension looks for issue references starting with a single
dash, like ``#10``.  You can however change the pattern, which is used to
find issue references:

.. confval:: issuetracker_issue_pattern

   A regular expression, which is used to find and parse issue references.
   Defaults to ``r'#(\d+)'``.  If changed to ``r'gh-(\d+)'`` for instance,
   this extension would not longer recognize references like ``#10``, but
   instead parse references like ``gh-10``.  The pattern must contain only a
   single group, which matches the issue id.

Normally the reference title will be the whole issue id.  However you can also
use a custom reference title:

.. confval:: issuetracker_title_template

   A `format string`_ template for the title of references created from
   plaintext issue ids.  The format string gets the :class:`Issue` object
   corresponding to the referenced issue in the ``issue`` key, you may use any
   attributes of this object in your format string.  You can for instance
   include the issue title and the issue id::

      issuetracker_title_template = '{issue.title} ({issue.id})'

   If unset, the whole text matched by :confval:`issuetracker_issue_pattern` is
   used as reference title.

   .. versionadded:: 0.9
      Replaces :confval:`issuetracker_expandtitle`


.. _Sphinx: http://sphinx.pocoo.org
.. _Sphinx issue tracker: https://bitbucket.org/birkenfeld/sphinx/issues/
.. _jira: http://www.atlassian.com/software/jira/
.. _launchpadlib: http://pypi.python.org/pypi/launchpadlib/
.. _debianbts: http://pypi.python.org/pypi/python-debianbts/
.. _SOAPpy: http://pypi.python.org/pypi/SOAPpy/
.. _sphinx-contrib: https://github.com/lunaryorn/sphinxcontrib-issuetracker
.. _format string: http://docs.python.org/library/string.html#format-string-syntax
