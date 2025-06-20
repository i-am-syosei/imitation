"""Sphinx documentation configuration."""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import io
import os
import urllib.request
import zipfile
from importlib import metadata

project = "imitation"
copyright = "2019-2022, Center for Human-Compatible AI"  # noqa: A001
author = "Center for Human-Compatible AI"

# The full version, including alpha/beta/rc tags
try:
    version = metadata.version("imitation")
except metadata.PackageNotFoundError:  # pragma: no cover - package may not be installed
    version = "0.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    # optional extensions; skip if not installed
    "sphinx.ext.doctest",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
autosummary_generate = True

nb_execution_mode = os.getenv("NB_EXECUTION_MODE", "cache")
nb_execution_timeout = 200
nb_merge_streams = True
nb_output_stderr = "remove"
nb_execution_raise_on_error = True
nb_execution_show_tb = True

# The default engine ran into memory issues on some notebooks
# so we use lualatex instead
latex_engine = "lualatex"

# Enable LaTeX macros in markdown cells
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]

# skip_doctests is checked in our :skipif: directives in doctest examples
doctest_global_setup = """
import os

skip_doctests = os.getenv("SKIP_DOCTEST")
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "special-members": "__init__",
    "show-inheritance": True,
}

# Some optional dependencies are not installed in the documentation build
# environment. Mock them to prevent import errors during `autosummary`.
autodoc_mock_imports = [
    "shimmy",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
try:
    import furo  # type: ignore  # noqa: F401

    html_theme = "furo"
except Exception:  # pragma: no cover - optional theme may be missing  # noqa: B902
    html_theme = "alabaster"
html_title = "imitation"
html_theme_options = {
    "source_repository": "https://github.com/HumanCompatibleAI/imitation",
    "source_branch": "master",
    "source_directory": "docs",
    "light_css_variables": {
        "sidebar-item-font-size": "85%",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = ["css/custom.css"]

# -- Customization -----------------------------------------------------------


def no_namedtuple_attrib_docstring(app, what, name, obj, options, lines):
    """Remove redundant documentation in named tuples.

    Worksaround https://github.com/sphinx-doc/sphinx/issues/7353 -- adapted from
    https://chrisdown.name/2015/09/20/removing-namedtuple-docstrings-from-sphinx.html
    """  # noqa: DAR101
    is_namedtuple_docstring = 1 <= len(lines) <= 2 and lines[0].startswith(
        "Alias for field number",
    )
    if is_namedtuple_docstring:
        # We don't return, so we need to purge in-place
        del lines[:]


def setup(app):
    app.connect(
        "autodoc-process-docstring",
        no_namedtuple_attrib_docstring,
    )


# -- Download the latest benchmark summary -------------------------------------
download_url = (
    "https://github.com/HumanCompatibleAI/imitation/releases/latest/"
    "download/benchmark_runs.zip"
)

# Download the benchmark data, extract the summary and place it in the documentation.
# We skip the download when the environment variable ``SKIP_BENCHMARK_DOWNLOAD`` is
# set. This avoids network errors during offline builds (e.g. in CI).
if os.getenv("SKIP_BENCHMARK_DOWNLOAD") is None:
    try:
        with urllib.request.urlopen(download_url) as url:
            with zipfile.ZipFile(io.BytesIO(url.read())) as z:
                with z.open("benchmark_runs/summary.md") as f:
                    with open("main-concepts/benchmark_summary.md", "wb") as out:
                        out.write(f.read())
    except Exception as exc:  # pragma: no cover - download is optional  # noqa: B902
        print(f"Skipping benchmark summary download: {exc}")
