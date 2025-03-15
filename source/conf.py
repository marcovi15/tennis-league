# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tennis League'
copyright = '2025, Marco Virgili'
author = 'Marco Virgili'
release = '1.0'

# Sphinx Extensions
extensions = [
    'sphinx.ext.autodoc',          # Automatically document Python code
    'sphinx.ext.napoleon',         # Support Google- & NumPy-style docstrings
    'sphinx.ext.viewcode',         # Add links to source code
    'sphinx.ext.autosummary',      # Generate summary tables
    'sphinx_autodoc_typehints'     # Show type hints in docs
]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

