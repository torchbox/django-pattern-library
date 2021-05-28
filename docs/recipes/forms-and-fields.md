# Forms and fields

Basic Django form definition:

```python
from django import forms


class ExampleForm(forms.Form):
    single_line_text = forms.CharField(
        max_length=255, help_text="This is some help text"
    )
    choices = (("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four"))
    select = forms.ChoiceField(choices=choices)
```

Rendered as:

```jinja2
{% extends "patterns/base.html" %}

{% block content %}
<form method="post" class="form">
    {% csrf_token %}
    <div class="form__container">
        {% for hidden_field in form.hidden_fields %}
            {{ hidden_field }}
        {% endfor %}

        {% for field in form.visible_fields %}
            {% include "patterns/molecules/field/field.html" with field=field %}
        {% endfor %}

        <button class="form__submit button" type="submit">Submit</button>
    </div>
</form>
{% endblock %}
```

Context overrides when rendering the whole form:

```python
from pattern_library import register_context_modifier
from .forms import ExampleForm


@register_context_modifier
def add_common_forms(context, request):
    context['form'] = ExampleForm()
```

Context overrides for `field.html`:

```python
from pattern_library import register_context_modifier
from .forms import ExampleForm


@register_context_modifier(template='patterns/molecules/field/field.html')
def add_field(context, request):
    form = ExampleForm()
    context['field'] = form['single_line_text']
```
