# HF-Sphinx-Documentation

[![CI](https://github.com/Haiko-Nuding/HF-Sphinx-Documentation/actions/workflows/static.yml/badge.svg)](https://github.com/Haiko-Nuding/HF-Sphinx-Documentation/actions/workflows/static.yml)
![Sphinx](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)
[![Theme: Wagtail](https://img.shields.io/badge/Theme-Wagtail-43b1b0)](https://wagtail.org/)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project uses **Sphinx** with the **Wagtail theme** and customizations to generate HTML documentation.

---

## Project Structure

```
.
├── .github/                         # GitHub configuration
│   └── workflows/                   # GitHub Actions workflows (CI/CD)
│       └── static.yml               # Builds & deploys Sphinx docs to GitHub Pages
│
├── docs/                            # Main Sphinx documentation project
│   ├── README.md                    # Project README (shown on GitHub inside /docs)
│   ├── conf.py                      # Sphinx configuration file
│   ├── index.rst                    # Main documentation entry point (homepage)
│   ├── _static/                     # Custom static files (CSS, images, JS)
│   ├── _templates/                  # Custom HTML templates for Sphinx
│   └── _build/                      # Auto-generated HTML output (should be gitignored)
│
├── .venv/                           # Local Python virtual environment (gitignored)
│
├── requirements.txt                # Python dependencies for building the docs
│
└── .gitignore                       # Files & folders excluded from git tracking

```

---

## Installation


```{important}
You will need to install Java for plantUML Support.
```

1. **Clone the repository:**

```bash
git clone https://github.com/Haiko-Nuding/HF-Sphinx-Documentation.git
cd HF-Sphinx-Documentation
```

2. **(Optional) Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1 
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Building the Documentation

You can generate the documentation in several ways:

### 1. Using the Make script (Windows)

```powershell
.\make.bat html
```

This will generate HTML documentation in the `build/html` folder.

### 2. Using Sphinx directly

If you have Sphinx installed separately:

```bash
sphinx-build -b html docs/ build/html
```

### 3. Viewing the documentation

After building, open:

```
build/html/index.html
```

in your browser to view the documentation.


## Running the Spelling Check

This project uses `sphinxcontrib-spelling` to check for typos in the documentation. You can run it in the following ways:

### 1. Using the Make script (Windows)

```powershell
.\make.bat spelling
