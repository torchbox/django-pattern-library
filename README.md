# Django pattern library

[![PyPI](https://img.shields.io/pypi/v/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![PyPI downloads](https://img.shields.io/pypi/dm/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![Travis](https://travis-ci.com/torchbox/django-pattern-library.svg?branch=master)](https://travis-ci.com/torchbox/django-pattern-library) [![Total alerts](https://img.shields.io/lgtm/alerts/g/torchbox/django-pattern-library.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/torchbox/django-pattern-library/alerts/)

A module for Django that helps you to build pattern libraries.

![Screenshot of the pattern library UI, with navigation, pattern rendering, and configuration](https://raw.githubusercontent.com/torchbox/django-pattern-library/master/.github/pattern-library-screenshot.webp)

## Documentation

Documentation is located on GitHub in [`docs/`](https://github.com/torchbox/django-pattern-library/tree/master/docs).

## Objective

At the moment, the main focus is to allow developers and designers
use exactly the same Django templates in a design pattern library
and in production code.

There are a lot of alternative solutions for building
pattern libraries already. Have a look at [Pattern Lab](http://patternlab.io/) and
[Astrum](http://astrum.nodividestudio.com/), for example.
But at [Torchbox](https://torchbox.com/) we mainly use Python and Django and
we find it hard to maintain layout on big projects in several places:
in a project's pattern library and in actual production code. This is our
attempt to solve this issue and reduce the amount of copy-pasted code.

To learn more about how this package can be used, have a look at our Wagtail Space 2020 talk: [Reusable UI components: A journey from React to Wagtail](https://www.youtube.com/watch?v=isrOufI7TKc)

[![Reusable UI components: A journey from React to Wagtail](https://raw.githubusercontent.com/torchbox/django-pattern-library/master/.github/pattern-library-talk-youtube.webp)](https://www.youtube.com/watch?v=isrOufI7TKc)

## Concepts
To understand how `django-pattern-library` works, the following concepts are important.

### Patterns
Any template that is displayed by the pattern library is referred to as a pattern. Patterns are divided into two categories: fragments and pages.

### Fragments
A fragment is a pattern whose markup does not include all of the resources (typically CSS and Javascript) for it to be displayed correctly on its own. This is typical for reusable component templates which depend on global stylesheets or Javascript bundles to render and behave correctly.

To enable them to be correctly displayed in the pattern library, `django-pattern-library` will inject the rendered markup of fragments into the **pattern base template** specified by `PATTERN_LIBRARY['PATTERN_BASE_TEMPLATE_NAME']`.

This template should include references to any required static files. The rendered markup of fragments will be available in the `pattern_library_rendered_pattern` context variable (see the tests for [an example](https://github.com/torchbox/django-pattern-library/blob/master/tests/templates/patterns/base.html)).

### Pages
In contrast to fragments, pages are patterns that include everything they need to be displayed correctly in their markup. Pages are defined by `PATTERN_LIBRARY['BASE_TEMPLATE_NAMES']`. 

Any template in that list — or that extends a template in that list — is considered a page and will be displayed as-is when rendered in the pattern library.

It is common practice for page templates to extend the pattern base template to avoid duplicate references to stylesheets and Javascript bundles. Again, [an example](https://github.com/torchbox/django-pattern-library/blob/master/tests/templates/patterns/base_page.html) of this can be seen in the tests.

## How to install

First install the library:

```sh
pip install django-pattern-library
# ... or...
poetry add django-pattern-library
```


Then, in your Django settings, add `pattern_library` into your `INSTALLED_APPS`, and `pattern_library.loader_tags` to `OPTIONS['builtins']` into the `TEMPLATES` setting. For example:

```python
INSTALLED_APPS = [
    # ...
    'pattern_library',
    # ...
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['pattern_library.loader_tags'],
        },
    },
]
```

Note that this module only supports the Django template backend.

### Settings

Next, set the `PATTERN_LIBRARY` setting. Here's an example showing the defaults:

```python
PATTERN_LIBRARY = {
    # PATTERN_BASE_TEMPLATE_NAME is the template that fragments will be wrapped with.
    # It should include any required CSS and JS and output
    # `pattern_library_rendered_pattern` from context.
    'PATTERN_BASE_TEMPLATE_NAME': 'patterns/base.html',
    # Any template in BASE_TEMPLATE_NAMES or any template that extends a template in
    # BASE_TEMPLATE_NAMES is a "page" and will be rendered as-is without being wrapped.
    'BASE_TEMPLATE_NAMES': ['patterns/base_page.html'],
    'TEMPLATE_SUFFIX': '.html',
    # SECTIONS controls the groups of templates that appear in the navigation. The keys
    # are the group titles and the values are lists of template name prefixes that will
    # be searched to populate the groups.
    'SECTIONS': (
        ('atoms', ['patterns/atoms']),
        ('molecules', ['patterns/molecules']),
        ('organisms', ['patterns/organisms']),
        ('templates', ['patterns/templates']),
        ('pages', ['patterns/pages']),
    ),
}

```

Note that the templates in your `PATTERN_LIBRARY` settings must be available to your project's
[template loaders](https://docs.djangoproject.com/en/3.1/ref/templates/api/#loader-types).

### URLs

Include `pattern_library.urls` in your `urlpatterns`. Here's an example `urls.py`:

```python
from django.apps import apps
from django.conf.urls import url, include

urlpatterns = [
    # ... Your URLs
]

if apps.is_installed('pattern_library'):
    urlpatterns += [
        url(r'^pattern-library/', include('pattern_library.urls')),
    ]
```

This package is not intended for production. It is **highly recommended** to only enable this package in testing environments for a restricted, trusted audience. One simple way to do this is to only expose its URLs if `apps.is_installed('pattern_library')`, as demonstrated above, and only have the app installed in environment-specific settings.

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](https://github.com/torchbox/django-pattern-library/blob/master/CONTRIBUTING.md).

If you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

## Credits

View the full list of [contributors](https://github.com/torchbox/django-pattern-library/graphs/contributors). [BSD](https://github.com/torchbox/django-pattern-library/blob/master/LICENSE) licensed.
