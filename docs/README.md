# HF-Sphinx-Documentation

![Sphinx](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)
![Python](https://img.shields.io/badge/python-3.8%7C3.9-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project uses **Sphinx** with the **Wagtail theme** and customizations to generate HTML documentation.

---

## Project Structure

```
docs/
├── .venv/        # Python virtual environment (after setup)
├── build/        # Sphinx documentation build directory
├── conf.py       # Sphinx configuration file
├── index.rst     # Root document
├── _build/       # Build output (ignored in version control)
├── _static/      # Custom static files (CSS, JS, images)
└── _templates/   # Custom templates for theming
```

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Haiko-Nuding/HF-Sphinx-Documentation.git
cd HF-Sphinx-Documentation
```

2. **(Optional) Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
