# Configuration file for the Sphinx documentation builder.
# Full documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# -- Project information -----------------------------------------------------

project = 'HF-Sphinx-Documentation'
author = 'Haiko Nuding'
copyright = '2025, Haiko Nuding'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_wagtail_theme',
    'myst_parser',  # For Markdown support
    'sphinxcontrib.plantuml',  # PlantUML integration
]

templates_path = ['_templates']
exclude_patterns = []

# Configure MyST Parser
myst_enable_extensions = [
    "html_image",
    "deflist",
    "linkify",
    "colon_fence",
]

# Allows Sphinx to read both .rst and .md files as source files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Top-level index file
master_doc = 'index'

# -- HTML output options -----------------------------------------------------

html_theme = 'sphinx_wagtail_theme'

# Theme-specific options for the Wagtail Theme
html_theme_options = dict(
    project_name="HF Sphinx Documentation",
    logo="img/tofu_logo_color.svg",
    logo_alt="Wagtail",
    logo_height=69,
    logo_width=69,
    logo_url="./",  # Relative path fixes GitHub Pages links
    github_url="https://github.com/Haiko-Nuding/HF-Sphinx-Documentation/blob/main/docs/",
    footer_links=",".join([
        "README|https://haiko-nuding.github.io/HF-Sphinx-Documentation/README.html",
        "Contact|https://haiko-nuding.github.io/HF-Sphinx-Documentation/contact.html",
        "Credits|https://haiko-nuding.github.io/HF-Sphinx-Documentation/credits.html",
    ]),
)

# Base URL for references
html_baseurl = "https://Haiko-Nuding.github.io/HF-Sphinx-Documentation/"

# Add static paths and custom CSS
html_static_path = ['_static']
html_css_files = ['css/custom.css']

# Set favicon
html_favicon = '_static/img/tofu_logo_color.svg'

# Display last updated timestamp
html_last_updated_fmt = "%b %d, %Y"

# -- PlantUML configuration --------------------------------------------------

# Build a portable path to the PlantUML JAR (works on Windows and Linux)
docs_path = os.path.dirname(__file__)
plantuml_jar = os.path.join(docs_path, "third_party", "plantuml-1.2025.10.jar")
plantuml = f"java -jar {plantuml_jar}"
