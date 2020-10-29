# Examples

## Looping over a template tag

```jinja2
{% social_media_links as social_links %}
<ul class="footer__social-links">
    {% for link in social_links %}
    {# Only render if we have a link #}
        {% if link.url %}
            <li class="social-item social-item--{{link.type}}">
                <a class="social-item__link" href="{{link.url}}" aria-label="{{link.label}}">
                    <svg class="social-item__icon" width="24" height="24">
                        <use xlink:href="#{{link.type}}">
                        </use>
                    </svg>
                </a>
            </li>
        {% endif %}
    {% endfor %}
</ul>
```

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

## Inclusion tags

```jinja2
<div class="footer__action">
    {% footernav %}
</div>
```

```yaml
tags:
  footernav:
    "":
      template_name: "patterns/molecules/navigation/footernav.html"
```

## Image lazy load

```jinja2
{% image slide.image fill-100x71 as imageSmall %}
{% image slide.image fill-829x585 as imageLarge %}

{% include "patterns/atoms/image/image--lazyload.html" with imageSmall=imageSmall width=829 height=585 imageLarge=imageLarge classList='slide__image' %}
```

```yaml
tags:
  image:
    slide.image fill-100x71 as imageSmall:
      target_var: imageSmall
      raw:
        url: '//placekitten.com/100/71'
    slide.image fill-829x585 as imageLarge:
      target_var: imageLarge
      raw:
        url: '//placekitten.com/829/585'
        width: '829'
        height: '585'
```

## Image include

```jinja2
<img src="{{ imageSmall.url }}" data-src="{{ imageLarge.url }}" width="{{ width }}" height="{{ height }}" alt="{{ imageLarge.alt }}" class="{{ classList }} lazyload">
```

YAML:

```yaml
context:
  width: '829'
  height: '585'
  imageSmall:
    url: '//placekitten.com/100/71'
  imageLarge:
    url: '//placekitten.com/829/585'
```
