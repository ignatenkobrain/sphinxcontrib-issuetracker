Customization
=============

.. module:: sphinxcontrib.issuetracker
   :synopsis: Parse issue references and link to the corresponding issues

To use an issue tracker not supported by this extension, set
:confval:`issuetracker` to ``None`` or leave it unset, and connect your own
callback to the event :event:`issuetracker-lookup-issue`:

.. event:: issuetracker-lookup-issue(app, tracker_config, issue_id)

   Emitted if the issue with the given ``issue_id`` should be looked up in the
   issue tracker.  Issue tracker configured is provided by ``tracker_config``.

   ``app`` is the Sphinx application object.  ``tracker_config`` is the
   issuetracker configuration as :class:`TrackerConfig` object.  ``issue_id``
   is the issue id as string.

   A callback should return an :class:`Issue` object containing the looked up
   issue, or ``None`` if it could not find the issue.  In the latter case other
   callbacks connected to this event are be invoked by Sphinx.

   .. versionchanged:: 0.8
      Replaced ``project`` argument with ``tracker_config``, changed return
      value from dictionary to :class:`Issue`

   .. versionchanged:: 0.9
      Renamed from :event:`issuetracker-resolve-issue` to
      :event:`issuetracker-lookup-issue`

Refer to the `builtin trackers`_ for examples.


Supporting classes
------------------

.. autoclass:: TrackerConfig

   .. attribute:: project

      The project name as string.

   .. attribute:: url

      The url of the issue tracker as string *without* any trailing slash, or
      ``None``, if there is no url configured for this tracker.  See
      :confval:`issuetracker_url`.

   .. versionadded:: 0.8

.. class:: Issue

   A :func:`~collections.namedtuple` providing issue information.

   .. attribute:: id

      The issue id as string.

      If you are writing your own custom callback for
      :event:`issuetracker-lookup-issue`, set this attribute to the
      ``issue_id`` that was given as argument.

   .. attribute:: title

      The human readable title of this issue as string.

   .. attribute:: url

      A string containing an URL for this issue.

      This URL is used as hyperlink target in the generated documentation.
      Thus it should point to a webpage or something similar that provides
      human-readable information about an issue.

   .. attribute:: closed

      ``True``, if the issue is closed, ``False`` otherwise.

   .. versionadded:: 0.8

.. _builtin trackers: https://github.com/lunaryorn/sphinxcontrib-issuetracker/blob/master/sphinxcontrib/issuetracker/resolvers.py
