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
