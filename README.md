# ReadMe

Built with [mkdocs-material](https://github.com/squidfunk/mkdocs-material)

## install

```
python -m venv .venv
source .venv/bin/activate
pip install -r /path/to/requirements.txt
```

## Overrides

Custom overrides are in `docs/.overrides`

## SCSS for CSS

In VSCode:

```
sass --watch docs/assets/stylesheets/custom.scss:docs/assets/stylesheets/custom.css
```

Watches and rebuilds CSS.

## Local runs

```
mkdocs serve --watch-theme
```

runs local build at <http://127.0.0.1:8000>
## Build

```
mkdocs build
```

builds to `/site`
