Usage and operation
===================

After configuring the :confval:`tracker <issuetracker>` and the
:confval:`project <issuetracker_project>` (and possibly the :confval:`tracker
url <issuetracker_url>`), you can reference issues in the issue tracker with
the :rst:role:`issue` role:

.. rst:role:: issue

   Create a reference to the given issue.  This role understands the standard
   :ref:`cross-referencing syntax <xref-syntax>` used by Sphinx.

   An explicit title given to this role is interpreted as `format string`_,
   which is formatted with the :class:`Issue` object representing the
   referenced issue available by the key ``issue``.  You may use any attribute
   of the :class:`Issue` object in your format string.  Use this feature to
   include information about the referenced issue in the reference title.  For
   instance, you might use ``:issue:`{issue.title} (#{issue.id}) <10>``` to use
   the title and the id of the issue ``10`` as reference title.

   .. versionadded:: 0.9

Information about the issue (like the title) is retrieved from the configured
issue tracker.  Aside of providing it for reference titles, the extension also
uses this information to mark closed issues in HTML output by striking the
reference text through.  For this purpose, a stylesheet is added to the
generated HTML.

You can provide your own styles for issue references by adding them to the
``.xref.issue`` and ``.xref.issue.closed`` selectors (the latter are closed
issues).  For instance, the following stylesheet uses red color for open, and
green color for closed issues::

   .xref.issue {
       color: green;
   }

   .xref.issue.closed {
       color: red;
   }

Issue ids in plain text
-----------------------

If :confval:`issuetracker_plaintext_issues` is ``True``, this extension also
searches for issue ids like ``#10`` in plain text and turns them into issue
references.  Issue ids in literal text (e.g. inline literals or code blocks)
are ignored.  The pattern used to extract issue ids from plain text can be
configured using :confval:`issuetracker_issue_pattern`.

.. _format string: http://docs.python.org/library/string.html#format-string-syntax
