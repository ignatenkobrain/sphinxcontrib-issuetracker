# -*- coding: utf-8 -*-
# Copyright (c) 2009 Python Software Foundation
# Copyright (c) 2013 Sebastian Wiesner <lunaryorn@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
# NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    pypi
    ~~~~

    This file contains code to render ReST description like PyPI does, in order
    to test whether our README is correct.

    This code is taken and adapted from
    https://bitbucket.org/loewis/pypi/src/tip/description_utils.py, hence the
    different license of this file.
"""

from __future__ import (print_function, unicode_literals, absolute_import,
                        division)

import sys
from urlparse import urlparse

# Work around docutils #3596884, see
# http://sourceforge.net/tracker/?func=detail&aid=3596884&group_id=38414&atid=422030
import docutils.utils
from docutils import io, readers
from docutils.core import publish_doctree, Publisher
from docutils.transforms import TransformError


def trim_docstring(text):
    """
    Trim indentation and blank lines from docstring text & return it.

    See PEP 257.
    """
    if not text:
        return text
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = text.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


ALLOWED_SCHEMES = '''file ftp gopher hdl http https imap mailto mms news nntp
prospero rsync rtsp rtspu sftp shttp sip sips snews svn svn+ssh telnet
wais'''.split()


def process_description(source, output_encoding='unicode'):
    """Given an source string, returns an HTML fragment as a string.

    The return value is the contents of the <body> tag.

    Parameters:

    - `source`: A multi-line text string; required.
    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    # Dedent all lines of `source`.
    source = trim_docstring(source)

    settings_overrides = {
        'raw_enabled': 0,  # no raw HTML code
        'file_insertion_enabled': 0,  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
    }

    parts = None

    # Convert reStructuredText to HTML using Docutils.
    document = publish_doctree(source=source,
                               settings_overrides=settings_overrides)

    for node in document.traverse():
        if node.tagname == '#text':
            continue
        if node.hasattr('refuri'):
            uri = node['refuri']
        elif node.hasattr('uri'):
            uri = node['uri']
        else:
            continue
        o = urlparse(uri)
        if o.scheme not in ALLOWED_SCHEMES:
            raise TransformError('link scheme not allowed: {0}'.format(uri))

    # now turn the transformed document into HTML
    reader = readers.doctree.Reader(parser_name='null')
    pub = Publisher(reader, source=io.DocTreeInput(document),
                    destination_class=io.StringOutput)
    pub.set_writer('html')
    pub.process_programmatic_settings(None, settings_overrides, None)
    pub.set_destination(None, None)
    pub.publish()
    parts = pub.writer.parts

    output = parts['body']

    if output_encoding != 'unicode':
        output = output.encode(output_encoding)

    return output


def main():
    filename = sys.argv[1]
    with open(filename) as source:
        output = process_description(source.read().decode('utf-8'))
    print(output)


if __name__ == '__main__':
    main()
