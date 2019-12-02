# BinderHub

BinderHub lets you organize your MTG collection in albums/pages based on text files with [Scryfall](https://scryfall.com/) links.

Example website: https://binderhub.github.io/

# Setup

## Install Jekyll
https://jekyllrb.com/docs/installation/

## Install Python requirements
```pip install pyyaml```

## Setup GitHub Pages website
https://pages.github.com/

# Usage

## Create binders

Under `_binders` create binders as directories.

Under each binder directory create a txt file for each page within the binder with scryfall links to the cards you want (each link in its own line).

## Make site

```python /make_site.py```

## Serve site locally

```bundle exec jekyll serve```

## Update public site

Just push your code to your GitHub pages repository!

# Config

To change the ordering of cards within a page, update `_config.yml`:
```
# Field to sort cards by. Leave empty to use order in binder file. Popular options: [name, released_at, collector_number]
card_sort_field: released_at
# Secondary field to sort cards by. Leave empty to use order in binder file. Popular options: [name, released_at, collector_number]
card_sort_field2: collector_number
```
To see what fields are available, visit Scryfall API docs: https://scryfall.com/docs/api/cards
