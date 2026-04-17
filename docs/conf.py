import datetime
_build_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')

project   = 'Unofficial Onyx SDK Docs'
copyright = f'2026, Unofficial Onyx SDK Docs contributors. Generated {_build_date}'
author    = 'Unofficial Onyx SDK Docs contributors'
release   = '1.4.12'

extensions = []

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'sidebar_hide_name': False,
}

exclude_patterns = ['_build', '.venv']
