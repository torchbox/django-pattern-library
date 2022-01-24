# API and settings

## YAML structure

YAML isn’t everyone’s favorite markup language, but it has the advantage of being very lean, mapping well to both JSON and Python data structures, and supporting comments.

Here is what you need to know:

- Use `.yaml` or `.yml` as the file extension for pattern configuration files. If both are present, the `.yaml` file takes precendence.
- Use Mappings in place of Python Dictionaries.
- Use Sequences in place of Python lists (or iterables like QuerySets).
- The pattern library uses [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) in particular

Here is an example in practice:

```yaml
name: Test
# Nested structure, dependent on template.
context:
  quote: What is love?
  attribution: Haddaway
  my_list:
    - 1
    - 2
    - 3
# Mapping from tag names to tag overrides.
tags:
  error_tag:
    include:
      template_name: "non-patterns/include.html"
```

## Templates

### `pattern_library_rendered_pattern`

`pattern_library_rendered_pattern` is required in the template defined as [`PATTERN_BASE_TEMPLATE_NAME`](#pattern_base_template_name). This gets replaced by the rendered pattern’s HTML when displaying patterns in the library.

```django
<body>
  {% block content %}{{ pattern_library_rendered_pattern }}{% endblock %}
</body>
```

### `is_pattern_library`

`is_pattern_library` is available in the template context of each pattern, and is `True` if the pattern is being rendered in the pattern library.

```django
{% if not is_pattern_library %}
    {% get_hub_menu page as menu %}
{% endif %}

<a class="hub-menu__link href="{{ menu.parent.url }}">
    {{ menu.parent.get_menu_title }}
</a>
```

## Settings

See [Getting started](../getting-started.md) for more guided information.

### `PATTERN_LIBRARY`

All settings should be set as keys of the `PATTERN_LIBRARY` object.

```python
PATTERN_LIBRARY = {
    # […]
}
```

### `SECTIONS`

`SECTIONS` controls the groups of templates that appear in the navigation.
The keys are the group titles and the values are lists of template name prefixes that will be searched to populate the groups. The pattern library searches for templates both in [`DIRS`](https://docs.djangoproject.com/en/3.2/ref/settings/#dirs) directories for template engines, and in the `templates` subdirectory inside each installed application if using [`APP_DIRS`](https://docs.djangoproject.com/en/3.2/ref/settings/#app-dirs).

You can use this to create basic two-folder "includes and pages" hierarchies:

```python
PATTERN_LIBRARY = {
    "SECTIONS": (
        ("components", ["patterns/components"]),
        ("pages", ["patterns/pages"]),
    ),
}
```

Or more detailed structures following [Atomic Design](https://atomicdesign.bradfrost.com/):

```python
PATTERN_LIBRARY = {
    "SECTIONS": (
        ("atoms", ["patterns/atoms"]),
        ("molecules", ["patterns/molecules"]),
        ("organisms", ["patterns/organisms"]),
        ("templates", ["patterns/templates"]),
        ("pages", ["patterns/pages"]),
    ),
}
```

### `TEMPLATE_SUFFIX`

Defaults to `.html`. Only set this if your templates use another file extension.

```python
PATTERN_LIBRARY = {
    "TEMPLATE_SUFFIX": ".dj",
}
```

### `PATTERN_BASE_TEMPLATE_NAME`

`PATTERN_BASE_TEMPLATE_NAME` is the template that fragments will be wrapped with.
It should include any required CSS and JS, and output [`pattern_library_rendered_pattern`](#pattern_library_rendered_pattern) from context.

```python
PATTERN_LIBRARY = {
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
}
```

### `BASE_TEMPLATE_NAMES`

Any template in `BASE_TEMPLATE_NAMES` or any template that extends a template in `BASE_TEMPLATE_NAMES` is a "page" and will be rendered as-is without being wrapped.

```python
PATTERN_LIBRARY = {
    "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
}
```

## `monkey_utils`

### `override_tag`

This function tells the pattern library which Django tags to override, and optionally supports providing a default value. See [Overriding template tags](../guides/overriding-template-tags.md) for more information.

```python
from pattern_library.monkey_utils import override_tag

override_tag(register, 'a_tag_name', default_html="https://example.com/")
```

## `register_context_modifier`

This decorator makes it possible to override or create additional context data with Django / Python code, rather than being limited to YAML. It has to be called from within a `pattern_contexts` module, which can be at the root of any Django app. See [Modifying template contexts with Python](../guides/defining-template-context.md#modifying-template-contexts-with-python) for more information.

```python
# myproject/core/pattern_contexts.py

from pattern_library import register_context_modifier
from myproject.core.forms import SearchForm, SignupForm

@register_context_modifier
def add_common_forms(context, request):
    if 'search_form' not in context:
        context["search_form"] = SearchForm()
```

## Commands

### `render_patterns`

Renders all django-pattern-library patterns to HTML files, in a directory
structure. This can be useful for [automated tests](../guides/automated-tests.md).

Usage:

```sh
# Render all patterns to the default directory.
./manage.py render_patterns
# Render patterns without outputting files.
./manage.py render_patterns --dry-run
# Render all patterns, with fragment patterns wrapped in the base template.
./manage.py render_patterns --wrap-fragments
# Render patterns to a specific directory.
./manage.py render_patterns --output ./my/path/relative/to/cwd
# Render patterns to stdout.
./manage.py render_patterns --dry-run --verbosity 2
# View all options
./manage.py render_patterns --help
```

By default patterns will be saved in a `dpl-rendered-patterns` folder. Make sure to add this to your `.gitignore` and other ignore files, or customize the output directory with `--output`.
