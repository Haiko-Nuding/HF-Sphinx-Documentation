# Configuration file for the Sphinx documentation builder.
# Full documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'HF-Sphinx-Documentation'
author = 'Haiko Nuding'
copyright = '2025, Haiko Nuding'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_wagtail_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# -- HTML output options -----------------------------------------------------

html_theme = 'sphinx_wagtail_theme'

# Theme-specific options for the Wagtail Theme
html_theme_options = dict(
    project_name="HF Sphinx Documentation",
    logo="img/tofu_logo_color.svg",
    logo_alt="Wagtail",
    logo_height=69,
    logo_width=69,
    logo_url="/",
    github_url="https://github.com/Haiko-Nuding/HF-Sphinx-Documentation/blob/main/docs/"
)

html_baseurl = "https://Haiko-Nuding.github.io/HF-Sphinx-Documentation/"


# Add static paths and custom CSS
html_static_path = ['_static']
html_css_files = ['css/custom.css']

# Set favicon
html_favicon = '_static/img/tofu_logo_color.svg'

# Display last updated timestamp
html_last_updated_fmt = "%b %d, %Y"
