# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'Wachtwoord Reset Tool'
copyright = '2021, Jeroen Brauns'
author = 'Jeroen Brauns'

# The full version, including alpha/beta/rc tags
release = '1.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_last_updated_by_git",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = []

# Hide show page source button
html_show_sourcelink = False

# Remove Sphinx footer
html_show_sphinx = False

# Make ASPX
# html_file_suffix = ".aspx"
# html_link_suffix = ".aspx"
# htmlhelp_file_suffix = ".aspx"
# htmlhelp_link_suffix = ".aspx"

# Change date time format
# %A = Weekday as locale’s full name.
# %d = Day of the month as a zero-padded decimal number.
# %B = Month as locale’s full name.
# %Y = Year with century as a decimal number.
# %H = Hour (24-hour clock) as a zero-padded decimal number.
# %M = Minute as a zero-padded decimal number.
today_fmt = '%d %B %Y at %H:%M'

html_last_updated_fmt = '%d %B %Y at %H:%M'