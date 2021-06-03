# Pagination

The Django paginator API is impossible to fully recreate in YAML. Instead, we can define context in Python, with [context modifiers](../guides/defining-template-context.md#modifying-template-contexts-with-python). Take a template like:

```jinja2
{% with count=search_results.paginator.count %}
    {{ count }} result{{ count|pluralize }} found.
{% endwith %}

{% for result in search_results %}
    <h4>{{ result.title }}</h4>
{% endfor %}

{% if search_results.paginator.num_pages > 1 %}
    <nav aria-label="Pagination">
        <ul>
            {% if search_results.has_previous %}
                <li><a href="?page={{ search_results.previous_page_number }}{% if search_query %}&amp;query={{ search_query|urlencode }}{% endif %}">previous</a></li>
            {% endif %}

            <li>{{ search_results.number }}/{{ search_results.paginator.num_pages }}</li>

            {% if search_results.has_next %}
                <li><a href="?page={{ search_results.next_page_number }}{% if search_query %}&amp;query={{ search_query|urlencode }}{% endif %}">next</a></li>
            {% endif %}
        </ul>
    </nav>
{% endif %}
```

We can create the needed context by using Django’s [`Paginator` API](https://docs.djangoproject.com/en/3.2/topics/pagination/).

```python
from django.core.paginator import Paginator

from pattern_library import register_context_modifier


@register_context_modifier(template='patterns/pages/search/search.html')
def replicate_pagination(context, request):
    object_list = context.pop('search_results', None)
    if object_list is None:
        return

    original_length = len(object_list)

    # add dummy items to force pagination
    for i in range(50):
        object_list.append(None)

    paginator = Paginator(object_list, original_length)
    context.update(
        paginator=paginator,
        search_results=paginator.page(10),
        is_paginated=True,
        object_list=object_list
    )
```
