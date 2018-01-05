# Django pattern library

A module for Django that helps you to build pattern libraries.


## How to install

1. Add `pattern_library` into your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        # ...

        'pattern_library',

        # ...
    ]
    ```

2. Add `pattern_library.loader_tags` into the `TEMPLATES` setting. For example:

    ```python
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

    Note that this module only supports the Django template backend out of the box.

3. Set the `PATTERN_LIBRARY_TEMPLATE_DIR` setting to point to a template directory with your patterns:

    ```python
    PATTERN_LIBRARY_TEMPLATE_DIR = os.path.join(BASE_DIR, 'project_styleguide', 'templates')
    ```

    Note that `PATTERN_LIBRARY_TEMPLATE_DIR` must be available for
    [template loaders](https://docs.djangoproject.com/en/1.11/ref/templates/api/#loader-types).

4. Include `pattern_library.urls` into your `urlpatterns`. Here's an example `urls.py`:

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


TODO:

- [ ] Feature: allow custom tags to be overridden.
    Should be useful for tags that can write to context (similar to the `SimpleNode`-tags),
    but do not extend `SimpleNode`.
- [ ] Docs: Describe directory structure
- [ ] Docs: Describe the approach to the base template
    which should include CSS and JS.
    The base template should be very minimalistic.
- [ ] Docs: Describe YAML structure
    (how to pass context and mock template tags)
- [ ] Add examples of dumb data
- [ ] Add notes on production usage
- [ ] Tests: Add tests.
    It's ok to not bother about tests during prototyping,
    but it will be extremely hard to maintain
    the project without tests.
