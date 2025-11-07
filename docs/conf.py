# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HF-Sphinx-Documentation'
copyright = '2025, Haiko Nuding'
author = 'Haiko Nuding'

# These are options specifically for the Wagtail Theme.
html_theme_options = dict(
    project_name = "HF-Sphinx-Documentation",
    logo_alt = "Wagtail",
    logo_height = 59,
    logo_url = "/",
    logo_width = 45,
)

html_theme_options = dict(
    github_url = "https://github.com/Haiko-Nuding/HF-Sphinx-Documentation/"
)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_wagtail_theme']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_wagtail_theme'
html_static_path = ['_static']
