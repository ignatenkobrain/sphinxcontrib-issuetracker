0.11 (Jan 17, 2013)
===================

- Send proper user agent in API requests
- #4: Respect Github rate limits
- #5: Fix compatibility with requests 1.0


0.10.1 (Jun 19, 2012)
=====================

- Fix README rendering on PyPI
- #1: Fix test failure on Python 3


0.10 (Jun 18, 2012)
===================

- Extension now hosted at
  https://github.com/lunaryorn/sphinxcontrib-issuetracker
- Use requests library for HTTP requests
- Consider launchpad issues closed only if all referenced tasks are completed
- Support Python 3 (with exception of ``launchpad`` and ``debianbts`` trackers)


0.9 (Aug 31, 2011)
==================

Incompatible changes
--------------------

- Remove :confval:`issuetracker_expandtitle`, use
  ``issuetracker_title_template = '{issue.title}'`` instead
- Rename :event:`issuetracker-resolve-issue` to
  :event:`issuetracker-lookup-issue`

Other changes
-------------

* New features:

  - Add :rst:role:`issue` role for explicit issue references
  - Add :confval:`issuetracker_title_template`
  - Add :confval:`issuetracker_plaintext_issues`
  - Use issue title as link title

* Bug fixes and improvements:

  - Fix TypeError caused by ``launchpad`` issue tracker
  - Fix issue title in ``launchpad`` issue tracker
  - Fix detection of closed issues in ``launchpad`` issue tracker
  - Fix CSS classes for issue references to be more compatible with Sphinx
    themes


0.8 (Aug 24, 2011)
==================

Incompatible changes
--------------------

- Require Python 2.6 or newer now
- Remove ``issuetracker_user`` configuration value, GitHub and BitBucket
  projects must include the username now
- Custom resolvers must return :class:`~sphinxcontrib.issuetracker.Issue`
  objects instead of dictionaries now
- Change signature of :event:`issuetracker-resolve-issue`

Other changes
-------------

* General:

  - Builtin ``debian`` tracker is fully supported now

* New features:

  - Add Jira_ support
  - Add :confval:`issuetracker_url`
  - Add :confval:`issuetracker_expandtitle`

* Bugs fixes and improvements:

  - Use BitBucket API instead of scraping the BitBucket website
  - Cache failed issue lookups, too

.. _jira: http://www.atlassian.com/software/jira/


0.7.2 (Mar 10, 2011)
====================

- Fix source distribution to include tests again
- Fix extraction of issue state for open issues from bitbucket
- Ignore references in inline literals and literal blocks


0.7.1 (Jan 19, 2011)
====================

- Copy the stylesheet after build again to avoid exceptions on non-existing
  build directories


0.7 (Jan 08, 2011)
==================

- Issue information is now cached
- Custom issue trackers must now connect to the ``issuetracker-resolve-issue``
  event, the builtin ``missing-reference`` event is no longer used.


0.6 (Jan 04, 2011)
==================

- Add support for the debian bugtracker (thanks to Fladischer Michael)
- Fix NameError in launchpad issue tracker
- Use HTTPS for BitBucket


0.5.4 (Nov 15, 2010)
====================

- Use HTTPS for Github


0.5.3 (Nov 14, 2010)
====================

- Add license text to source tarball


0.5.2 (Sep 17, 2010)
====================

- Issue reference resolvers get the application object now as fourth
  argument.  The environment is availabe in the ``.env`` attribute of this
  object.
- Fix the URL of Google Code issues (thanks to Denis Bilenko)
- Fix detection of closed issues in Google Code (thanks to Denis Bilenko)
- Improve error message, if ``issuetracker_issue_pattern`` has too many groups
  (thanks to Denis Bilenko)
- Add warnings for unexpected HTTP status codes in BitBucket and Google Code
  issue trackers


0.5.1 (Jul 25, 2010)
====================

- Fix client string for launchpad access


0.5 (Jul 21, 2010)
==================

- Closed issues are automatically struck trough in HTML output
- Require Sphinx 1.0 now
- Fix installation on Windows


0.4 (May 21, 2010)
==================

- Misc spelling fixes


0.3 (May 02, 2010)
==================

- Add support for Google Code
- Add support for Launchpad
- Issue tracker callbacks get the build environment now


0.2 (Apr 13, 2010)
==================

- Use ``missing-reference`` event instead of custom event


0.1 (Apr 10, 2010)
==================

- Initial release
