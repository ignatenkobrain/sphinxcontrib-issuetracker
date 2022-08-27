# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import typing as t
from pathlib import Path

import sphinx_autoissues

# Get the project root dir, which is the parent dir of this
doc_path = Path(__file__).parent
project_root = doc_path.parent

extensions = [
    "sphinx.ext.napoleon",  # Should go first
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_inline_tabs",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
    "sphinx_toolbox.confval",
    "myst_parser",
]
myst_enable_extensions = ["colon_fence", "substitution", "replacements"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

master_doc = "index"

project = "sphinx_autoissues"
copyright = "2022- Tony Narlock (revived version), 2010, 2011, 2012 Sebastian Wiesner"
version = ".".join(sphinx_autoissues.__version__.split(".")[:2])
release = sphinx_autoissues.__version__

exclude_patterns = ["_build/*"]

pygments_style = "monokai"
pygments_dark_style = "monokai"

html_theme = "furo"
html_static_path: t.List[str] = []

# sphinx.ext.autodoc
autoclass_content = "both"
autodoc_member_order = "bysource"

# sphinx-autodoc-typehints
autodoc_typehints = "description"  # show type hints in doc body instead of signature
simplify_optional_unions = True

# sphinx.ext.napoleon
napoleon_google_docstring = True
napoleon_include_init_with_doc = True

# sphinx-copybutton
copybutton_prompt_text = (
    r">>> |\.\.\. |> |\$ |\# | In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True

# sphinxext-rediraffe
rediraffe_redirects = "redirects.txt"
rediraffe_branch = "master~1"

intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

issuetracker = "github"
issuetracker_project = "tony/sphinx_autoissues"
