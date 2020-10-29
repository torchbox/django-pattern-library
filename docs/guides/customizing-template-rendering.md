# Customizing template rendering

## Customizing the patterns’ surroundings

All patterns that are not pages are rendered within a base page template. The pattern library will render patterns inside the `content` block, which you can tweak to change how patterns are displayed.

You can for example add a theme wrapper around the components:

```jinja2
{% block content %}
    {% if pattern_library_rendered_pattern %}
        <div class="pattern-library bg bg--light">
            {{ pattern_library_rendered_pattern }}
        </div>
    {% endif %}
{% endblock %}
```

`pattern_library_rendered_pattern` can also be used to do other modifications on the page for the pattern library only, for example adding an extra class to `<body>`:

```jinja2
<body class="{% block body_class %}{% endblock %}{% if pattern_library_rendered_pattern %} pattern-library-template{% endif %}">
```
