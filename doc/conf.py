# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'COFFEA-FCC Analyses'
copyright = 'Prayag Yadav'
author = 'Prayag Yadav'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "sphinx_external_toc",
    "myst_nb"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_context = {
    "github_user": "prayagyadav",
    "github_repo": "coffea-fcc-analyses",
    "github_version": "main",
    "doc_path": "doc",
}

# html_theme = 'sphinx_rtd_theme'
html_theme = "pydata_sphinx_theme"
html_title = "COFFEA-FCC-Analyses"

html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

master_doc = "index"

# -- Theme options ------------------------------------------------------------
# https://sphinx-nefertiti.readthedocs.io/en/latest/quick-start.html#customize-the-theme
html_theme_options = {
    "github_url": "https://github.com/prayagyadav/coffea-fcc-analyses",
    "logo": {
      "image_light": "_static/coffea-fcc-analyses-logo.png",
      "image_dark": "_static/coffea-fcc-analyses-logo-inverted.png",
   },
    "navbar_start" : ["navbar-logo"],
    # "navbar_center": [],
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
    "footer_start": ["copyright", "sphinx-version", "funding"],
    "switcher": {
        "json_url": "https://coffea-fcc-analyses.readthedocs.io/en/latest/_static/switcher.json",
        "version_match": 0.1,
    },
    "secondary_sidebar_items": ["page-toc", "sourcelink"]
}
