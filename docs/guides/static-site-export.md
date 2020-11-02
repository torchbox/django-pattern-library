# Static site export

It can be useful to publish your pattern library as a static site – for example to host it without a runtime dependency on the rest of your code, or to save past versions, or save the output as build artifacts.

## With `render_patterns`

The [`render_patterns` command](../reference/api.md#render_patterns) command can be used to export all your templates, without exporting the pattern library UI.

```sh
# Export all templates, wrapped in the base template like the pattern library UI does.
./manage.py render_patterns --wrap-fragments --output dpl-rendered-patterns
# Or alternatively export all templates without extra wrapping.
./manage.py render_patterns --output dpl-rendered-patterns
```

This command will create a new folder, with a structure matching that of your templates:

```txt
dpl-rendered-patterns
├── atoms
│   ├── icons
│   │   └── icon.html
├── molecules
│   ├── accordion
│   │   └── accordion.html
└── pages
    └── people
        └── person_page.html
```

Note this will export all templates but won’t export static files. If you need static files for your export, additionally run [`collectstatic`](https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#collectstatic), and move its output to be where [`STATIC_URL`](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-STATIC_URL) expects it:

```sh
./manage.py collectstatic
# Moving the collected files to match STATIC_URL
mv static dpl-rendered-patterns/static
```

## With a website scrapper

It’s very straightforward to export the whole pattern library as a static site, including all templates, and the pattern library UI. Here is an example exporting the pattern library with [`wget`](https://en.wikipedia.org/wiki/Wget):

```sh
wget --mirror --page-requisites --no-parent http://localhost:8000/pattern-library/
```
