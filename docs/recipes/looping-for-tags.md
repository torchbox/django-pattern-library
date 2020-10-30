## Looping over a template tag

For a template such as:

```jinja2
{% social_media_links as social_links %}
<ul class="footer__social-links">
    {% for link in social_links %}
    {# Only render if we have a link #}
        {% if link.url %}
            <li class="social-item social-item--{{link.type}}">
                <a class="social-item__link" href="{{link.url}}" aria-label="{{link.label}}">
                    <svg class="social-item__icon" width="24" height="24" aria-hidden="true" focusable="false">
                        <use xlink:href="#{{link.type}}"></use>
                    </svg>
                </a>
            </li>
        {% endif %}
    {% endfor %}
</ul>
```

You can use the following syntax to mock the tag’s output:

```yaml
tags:
  social_media_links:
    as social_links:
      raw:
        - url: '#'
          type: twitter
          label: Twitter
        - url: '#'
          type: facebook
          label: Facebook
        - url: '#'
          type: instagram
          label: Instagram
        - url: '#'
          type: youtube
          label: YouTube
        - url: '#'
          type: linkedin
          label: LinkedIn
```
