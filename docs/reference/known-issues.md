# Known issues and limitations

django-pattern-library has a few known limitations due to its design, which are worth knowing about when authoring templates or attempting to document them in the pattern library.

## No way to specify objects that have attributes and support iteration

See [#10](https://github.com/torchbox/django-pattern-library/issues/10). It’s impossible to mock the context when a variable needs to support iteration _and_ attributes. Here is an example of this impossible case:

```django
{% for result in search_results %}
{# […] #}
{% if search_results.paginator.count %}
```

## Overriding filters is not supported

See [#114](https://github.com/torchbox/django-pattern-library/issues/114). PRs welcome!

## Django form fields are not well supported

See [#113](https://github.com/torchbox/django-pattern-library/issues/113). If a template contains `{% for field in form %}` or even `{% if form %}`, then it's easy enough to render in django-pattern-library so long as we force the form to be null in the YAML context, and are happy not to have the form.

If the form is rendered explicitly by field names, then it requires a lot more work, which can quickly become too much of a maintenance burden – for example creating deeply nested structures for form fields:

```yaml
  form:
    email:
      bound_field:
        field:
          widget:
            class:
              __name__: char_field
```

While this is in theory possible, it’s not a very desirable prospect.

## Can’t override context in a child template

See [#8](https://github.com/torchbox/django-pattern-library/issues/8).

If you have a `some_page.html`, `some_page.yaml`, and `include_me.html`, `include_me.html`, and `some_page.html` includes `include_me.html`.

`some_page.yaml` with something like:

```yaml
context:
  page:
    pk: 1
    title: "my title"
```

and `include_me.yaml` with something like:

```yaml
context:
  page:
    title: "Title from include"
```

`Title from include` will appear on both patterns. It's impossible to override single key in `some_page.html`

## No support for pattern variations

See [#87](https://github.com/torchbox/django-pattern-library/issues/87). There is currently no support for trying out a single component with different variations in context or tag overrides.

This can be worked around by creating pattern-library-only templates, see [Multiple template variants](../guides/multiple-variants.md)

## Can’t mock each use of a template tag with different attributes

For example, with a template that uses the same tag many times like:

```django
{% load wagtailcore_tags %}
  {% for link in primarynav %}
      {% with children=link.value.page.get_children.live.public.in_menu %}
          <div class="primary-nav__item">
              {% include_block link with has_children=children.exists nav_type="primary-nav" %}
              <ul class="sub-nav">
                  <li class="sub-nav__item">{% include_block link with nav_type="sub-nav" %}</li>
                  {% for child in children.all %}
                      <li class="sub-nav__item sub-nav__item--secondary">
                          {% include_block link with page=child nav_type="sub-nav" %}
                      </li>
                  {% endfor %}
              </ul>
          </div>
      {% endwith %}
  {% endfor %}
```

This can’t be mocked for all usage of `include_block`.

## Can’t mock objects comparison by reference

With instances of models, the following works fine in vanilla Django, due to `item` and `page` being the same object:

```django
{% if item == page %}
```

This can’t be mocked with the pattern library’s context mocking support. As a workaround, you can switch equality checks to using literals:

```django
{% if item.id == page.id %}
```
