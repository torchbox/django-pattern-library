# Customizing template rendering

## Customizing all patterns’ surroundings

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

## Customizing a single pattern’s rendering

There is no API to customize a single pattern’s rendering, but it can be done by using pattern-library-only templates. For example, with our `quote_block.html` component:

```django
<blockquote class="quote-block block--spacing">
    <div class="quote-block__text">
        <p class="quote-block__quote">{{ quote }}</p>
        {% if attribution %}
            <p class="quote-block__attribution">{{ attribution }}</p>
        {% endif %}
    </div>
</blockquote>
```

We could create another template next to it called `quote_block_example.html`,

```django
<div class="pattern-library bg bg--light">
    {% include "patterns/components/quote_block/quote_block.html" with attribution=attribution quote=quote %}
</div>
```

This is a fair amount of boilerplate, but neatly solves the problem per pattern.
