# Configuration file for the Sphinx documentation builder.
# Full documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import subprocess

# -- Project information -----------------------------------------------------

project = 'HF-Sphinx-Documentation'
author = 'Haiko Nuding'
copyright = '2025, Haiko Nuding'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_wagtail_theme',
    'myst_parser',  # For Markdown support
    'sphinxcontrib.plantuml',  # PlantUML integration
    'sphinxcontrib.spelling',
    'rst2pdf.pdfbuilder',
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

# Absolute path to the docs folder
docs_path = os.path.dirname(os.path.abspath(__file__))

# Path to the PlantUML JAR inside your repo
plantuml_jar = os.path.join(docs_path, "third_party", "plantuml-1.2025.10.jar")

# Check if the PlantUML JAR exists
if not os.path.isfile(plantuml_jar):
    raise FileNotFoundError(f"PlantUML JAR not found at {plantuml_jar}. Make sure it is checked into the repo.")

# Verify Java is available
try:
    subprocess.run(["java", "-version"], check=True, capture_output=True)
except Exception as e:
    raise RuntimeError("Java is not available in PATH. Please install Java.") from e

# Optional: Check for Graphviz (dot) if your diagrams need it
dot_path = None
try:
    result = subprocess.run(["dot", "-V"], capture_output=True, text=True)
    dot_path = "dot found"
except FileNotFoundError:
    dot_path = None

if dot_path is None:
    print("Warning: Graphviz 'dot' executable not found. Some PlantUML diagrams may fail.")

# Command Sphinx will use to call PlantUML
plantuml = f'java -jar "{plantuml_jar}"'

spelling_lang = "en_US"   # language
# Optional: Custom word list
spelling_word_list_filename = ["spelling_wordlist.txt"]

# generate PDF:
#  rst2pdf .\docs\SA\tofubox_project.rst -s tango,kerning -o tofu_box_technische_documentation.pdf

# rst2pdf .\docs\SA\tofubox_project.rst -s tango,kerning --footer="###Page###" -o tofu_box_technische_documentation.pdf

#rst2pdf .\docs\OOP\csharp_grundlagen.rst -s .\docs\_static\pdf_styles\compact_spicker.yaml,tango --footer="HF Sphinx Documentation | Seite ###Page###" -o old_c#_spicker_test_2.pdf
