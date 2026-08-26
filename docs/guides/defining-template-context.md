# Defining template context

To define fake context you need to create a YAML file alongside your
template file. For example, for the template `big_red_button.html` you need to
create a file called `big_red_button.yaml`.

Let's imagine that your `big_red_button.html` template looks like this:

```django
<a href="{{ button_link }}" class="button button--red">
    <span>{{ button_text }}</span>
</a>
```

The `big_red_button.yaml` can be something like this:

```yaml
context:
  button_link: https://example.com/
  button_text: Example link
```

In the same way you can provide context in more complex templates. Here is
an example on how you can define fake context that pretends to be a `QuerySet`.

Let's assume you have the following template:

```django
{% if my_objects.exists %}
    {{ items_title }}
    <ul>
        {% for obj in my_objects.all %}
            <li>
                <a href="{{ obj.link }}">
                    {{ obj.title }}
                </a>
            </li>
        {% endfor %}
    </ul>
{% endif %}
```

You might define a YAML file similar to this to provide fake data:

```yaml
name: My example pattern

context:
  items_title: Related pages
  my_objects:
    exists: true # simulate `QuerySet`'s `exists` method
    all: # simulate `QuerySet`'s `all` method
      - title: Page 1
        link: /page1
      - title: Page 2
        link: /page2
```

You can define a list or a dict or anything that [`PyYAML`](http://pyyaml.org/wiki/PyYAMLDocumentation) allows you to create in YAML format without creating a custom objects.

## Modifying template contexts with Python

While most objects can be faked with YAML, Django has a few common constructs that are difficult to replicate. For example: `Form` and `Paginator` instances. To help with this, django-pattern-library allows you to register any number of 'context modifiers'. Context modifiers are simply Python functions that accept the `context` dictionary generated from the YAML file, and can make additions or updates to it as necessary. For convenience, they also receive the current `HttpRequest` as `request`.

Context modifiers can easily be registered using the `register_context_modifier` decorator. Here is a simple example:

```python

# myproject/core/pattern_contexts.py

from pattern_library import register_context_modifier
from myproject.core.forms import SearchForm, SignupForm

@register_context_modifier
def add_common_forms(context, request):
    if 'search_form' not in context:
        context["search_form"] = SearchForm()
    if 'signup_form' not in context:
        context["signup_form"] = SignupForm()

```

Context modifiers are also great for reducing the amount of template tag patching that is needed. The following examples are from a Wagtail project:

```python

# myproject/core/pattern_contexts.py

from django.core.paginator import Paginator
from wagtail.images import get_image_model
from pattern_library import register_context_modifier


@register_context_modifier
def add_page_images(context, request):
    """
    Replace some common 'image' field values on pages with real `Image`
    instances, so that the {% image %} template tag will work.
    """
    Image = get_image_model()
    if "page" in context:
        if "hero_image" in context["page"]:
            context["hero_image"] = Image.objects.all().order_by("?").first()
        if "main_image" in context["page"]:
            context["main_image"] = Image.objects.all().order_by("?").first()


@register_context_modifier
def replicate_pagination(context, request):
    """
    Replace lists of items using the 'page_obj.object_list' key
    with a real Paginator page, and add a few other pagination-related
    things to the context (like Django's `ListView` does).
    """
    object_list = context.pop('page_obj.object_list', None)
    if object_list is None:
        return

    original_length = len(object_list)

    # add dummy items to force pagination
    for i in range(50):
        object_list.append(None)

    # paginate and add ListView-like values
    paginator = Paginator(object_list, original_length)
    context.update(
        paginator=paginator,
        page_obj=paginator.page(1),
        is_paginated=True,
        object_list=object_list
    )
```

### Registering a context modifier for a specific template

By default, context modifiers are applied to all pattern library templates. If you only wish for a context modifier to be applied to a specific pattern, you can use the `template` parameter to indicate this. For example:

```python

# myproject/accounts/pattern_contexts.py

from pattern_library import register_context_modifier
from my_app.accounts.forms import SubscribeForm


@register_context_modifier(template="patterns/subscribe/form.html")
def add_subscribe_form(context, request):
    """
    Adds an unbound form to 'form.html'
    """
    context["form"] = SubscribeForm()


@register_context_modifier(template="patterns/subscribe/form_invalid.html")
def add_invalid_subscribe_form(context, request):
    """
    Adds a bound form with invalid data to 'form_invalid.html'
    """
    context["form"] = SubscribeForm(data={
        "email": 'invalid-email',
        "name": ''
    })
```

### Controlling the order in which context modifiers are applied

By default, context modifiers are applied in the order they were registered (which can be difficult to predict across multiple apps), with generic context modifiers being applied first, followed by template-specific ones. If you need to control the order in which a series of context modifiers are applied, you can use the `order` parameter to do this.

In the following example, a generic context modifier is registered with an `order` value of `1`, while others receive the default value of `0`. Because `1` is higher than `0`, the generic context modifier will be applied **after** the others.

```python

# myproject/sums/pattern_contexts.py


from pattern_library import register_context_modifier


@register_context_modifier(template='patterns/sums/single_number.html')
def add_single_number(context, request):
    context['first_number'] = 933


@register_context_modifier(template='patterns/sums/two_numbers.html')
def add_two_numbers(context, request):
    context['first_number'] = 125
    context['second_number'] = 22


@register_context_modifier(template='patterns/sums/three_numbers.html')
def add_three_numbers(context, request):
    context['first_number'] = 125
    context['second_number'] = 22
    context['third_number'] = 9


@register_context_modifier(order=1)
def add_total(context, request):
    if 'total' not in context:
        first_num = context.get('first_number', 0)
        second_num = context.get('second_number', 0)
        third_num = context.get('third_number', 0)
        context['total'] = first_num + second_num + third_num
```

## Extending the YAML syntax

You can also take advantage of YAML's local tags in order to insert full-fledged Python objects into your mocked contexts.

To do so, decorate a function that returns the object you want with `@register_yaml_tag` like so:

```python
# myproject/core/pattern_contexts.py

from pattern_library.yaml import register_yaml_tag
from wagtail.images import get_image_model

@register_yaml_tag
def testimage():
    """
    Return a random Image instance.
    """
    Image = get_image_model()
    return Image.objects.order_by("?").first()
```

Once the custom YAML tag is registered, you can use it by adding the `!` prefix:

```yaml
context:
  object_list:
    - title: First item
      image: !testimage
    - title: Second item
      image: !testimage
```

### Registering a tag under a different name

The `@register_yaml_tag` decorator will use the name of the decorated function as the tag name automatically.

You can specify a different name by passing `name=...` when registering the function:

```python
@register_yaml_tag("testimage")
def get_random_image():
    ...
```


### Passing arguments to custom tags

It's possible to create custom tags that take arguments.

```python
@register_yaml_tag
def testimage(collection):
    """
    Return a random Image instance from the given collection.
    """
    Image = get_image_model()
    images = Image.objects.filter(collection__name=collection)
    return images.order_by("?").first()
```

You can then specify arguments positionally using YAML's list syntax:
```yaml
context:
  test_image: !testimage
    - pattern_library
```

Alternatively you can specify keyword arguments using YAML's dictionary syntax:
```yaml
context:
  test_image: !testimage
    collection: pattern_library
```
