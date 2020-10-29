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

You might define a `yaml` file similar to this to provide fake data:

```yaml
name: My example pattern

context:
    items_title: Related pages
    my_objects:
        exists: true  # simulate `QuerySet`'s `exists` method
        all:          # simulate `QuerySet`'s `all` method
            - title: Page 1
              link: /page1
            - title: Page 2
              link: /page2
```

You can define a list or a dict or anything that [`PyYAML`](http://pyyaml.org/wiki/PyYAMLDocumentation) allows you to create in `yaml` format without creating a custom objects.
