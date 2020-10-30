## Image include

```jinja2
<img src="{{ imageSmall.url }}" data-src="{{ imageLarge.url }}" width="{{ width }}" height="{{ height }}" alt="{{ imageLarge.alt }}" class="{{ classList }} lazyload">
```

YAML:

```yaml
context:
  width: '720'
  height: '400'
  imageSmall:
    url: https://source.unsplash.com/pZ-XFIrJMtE/360x200
  imageLarge:
    url: https://source.unsplash.com/pZ-XFIrJMtE/720x400
```
