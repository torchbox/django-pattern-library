# API rendering

For additional flexibility, django-pattern-library supports rendering patterns via an API endpoint.
This can be useful when implementing a custom UI while still using the pattern library’s Django rendering features.

The API endpoint is available at `api/v1/render-pattern`. It accepts POST requests with a JSON payload containing the following fields:

- `template_name` – the path of the template to render
- `config` – the configuration for the template, with the same data structure as the configuration files (`context` and `tags`).

Here is an example, with curl:

```bash
echo '{"template_name": "patterns/molecules/button/button.html", "config": {"context": {"target_page": {"title": "API"}}, "tags": {"pageurl":{"target_page":{"raw": "/hello-api"}}}}}' | curl -d @- http://localhost:8000/api/v1/render-pattern
```

The response will be the pattern’s rendered HTML:

```html
<a href="/hello-api" class="button">
    API
</a>
```

Note compared to iframe rendering, this API always renders the pattern’s HTML standalone, never within a base template.
