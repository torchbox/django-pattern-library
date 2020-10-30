# Multiple template variants

See [#87](https://github.com/torchbox/django-pattern-library/issues/87). There is currently no support for trying out a single component with different variations in context or tag overrides, but this can worked around by creating pattern-library-only templates.

For example, for this `call_to_action` template:

```django
<div class="call-to-action">
  <img class="call-to-action__image" src="{{ call_to_action.illustration.url }}" alt="">
  <p class="call-to-action__heading heading heading--three">{{ call_to_action.title }}</p>
  {% include "patterns/atoms/link/link.html" with type="primary" classes="call-to-action__link" href=call_to_action.get_link_url text=call_to_action.get_link_text %}
</div>
```

We can try it out once with the following YAML:

```yaml
context:
  call_to_action:
    title: Will you help us protect these magnificant creatures in the UK waters?
    illustration:
      url: /static/images/illustrations/sharks.svg
    get_link_text: Sign up for our appeal
    get_link_url: '#'
```

If we want to try multiple variants, simply create a custom template for pattern library usage only, that renders `call_to_action` multiple times:

```django
<div class="pl-frame pl-frame--white">
    <h2>Call to action</h2>
    {% for call_to_action in ctas %}
        <div class="pl-row {% if call_to_action.classes %}{{ call_to_action.classes }}{% endif %}">
            <p>{{ call_to_action.type }}</p>
            {% include "patterns/molecules/cta/call_to_action.html" with call_to_action=call_to_action %}
        </div>
    {% endfor %}
</div>
```

```yaml
context:
  ctas:
    - type: Call to action
      title: Will you help us protect these magnificant creatures in the UK waters?
      illustration:
        url: /static/images/illustrations/sharks.svg
      get_link_text: Sign up for our appeal
      get_link_url: '#'
    - type: Call to action with short title
      title: Will you help us?
      illustration:
        url: /static/images/illustrations/sharks.svg
      get_link_text: Sign up for our appeal
      get_link_url: '#'
    - type: Call to action with long title
      title: Will you help us protect these magnificant and learn how to make environmentally responsible choices when buying seafood?
      illustration:
        url: /static/images/illustrations/sharks.svg
      get_link_text: Sign up for our appeal
      get_link_url: '#'
```
