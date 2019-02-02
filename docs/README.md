# Overview

As we [already mentioned](../README.md), the main idea of this package is
to allow you use template in both: your pattern library and
production code of your Django project.

To achieve this the package must to provide a way to:

* Define a fake context for templates
* Override template tags (default and custom ones)

## Directory structure

The initial structure of your pattern library should look like this:

```
.
├── templates
|   └── patterns
|       |── atoms
|       |── molecules
|       |── organisms
|       |── templates
|       └── pages
└── templatetags
```

- a `templates/patterns` directory with subfolders for the different levels of
  pattern, following standard atomic design naming conventions.
  - Your `PATTERN_LIBRARY_TEMPLATE_DIR` setting should point to the library's
    root `templates` directory
- a `templatetags` directory for holding template tag overrides (see below)


## Defining fake context for templates

To define fake context you need to create a `yaml` file alongside your
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

You can define a list or a dict or anything that
[`PyYAML`](http://pyyaml.org/wiki/PyYAMLDocumentation)
allows you to create in `yaml` format without creating a custom objects.

## Override template tags

The package overrides the following Django tags:

* `{% extends %}`
* `{% include %}`

It's required to allow us to define fake template context
and override other template tags in `yaml` files.
This package uses custom behaviour for these tags only when
rendering pattern library and falls back to Django's standard behaviour
on all other cases.

The override process has two parts:

1.  Override your template tag with a mock implementation
2.  Define fake result for your tag in a `yaml` file

### When do I need to override a template tag?

Ideally your pattern library should be independent, so it doesn't fail when
you run it with a project that has no entries in DB or on a local machine
without internet connection. This means that you need to override
a template tag when it hits DB or any other resource
(cache, or requests URL, for example).

### Override modes

There are two options when it comes to template tag overriding:

1.  Render another template or pattern (a template with own fake context)
    instead of calling the original template tag
2.  Return raw data. For example, you can return a string,
    that will be rendered instead of the original template tag.
    You can also return a structure (dict or list) which is useful when
    overriding ["Simple tags"](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#simple-tags) or a custom tag that returns an object or dict

### Output into a variable

Some tags can set their value into a variable like:

```django
{# renders something #}
{% my_tag some_arg %}

{# Outputs into a variable for later use #}
{% my_tag some_arg as result_var %}
{{ result_var.some_attr }}
```

The package automatically detects an output variable
(`result_var` in our example) when a custom template tag is a
["Simple tag"](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#simple-tags),
so you don't need to worry about these tags.
But when you need to override a tag which sets result into a variable in
[it's custom `django.template.Node`](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#a-quick-overview)
you would need to specify output var name manually. We will look into how
to do that later in the examples section.

### Overriding examples

Let's assume that we want to override the `{% image image resize_rule %}`
template tag from the `some_package.image_utils` template tag set
(you have something like `{% load image_utils %}` at the top of your template).

This template tag resizes an `image` accordingly
to a specific `resize_rule` and outputs the `<img>` html tag.
It's also possible to assign an image object into a variable
using this syntax: `{% image image resize_rule as my_var_name %}`.
In this case tag doesn't render the `<img>` tag, but you can access
image object's properties (`my_var_name.url`, for example).

First, we need to override a template tag with fake implementation.
Note that the fake implementation will only be used when viewing the
pattern library: you will be using the actual implementation in
our production code.

Assuming that you already have
[module installed in your project](../README.md),
to define a fake implementation we need to:

1.  Create [a `templatetags` package](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#code-layout)
    in one of your apps. Note that your app should be defined in
    [`INSTALLED_APPS`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-INSTALLED_APPS)
    and it should be defined after the package you are
    overriding (`some_package` in our case).
2.  Create `image_utils.py` in this package with the following code:

    ```python
    from some_package.templatetags.image_utils import register

    from pattern_library.monkey_utils import override_tag

    # We are monkey patching here
    # Note that `register` should be an instance of `django.template.Library`
    # and it's important to the instance where the original tag is defined.
    override_tag(register, name='image')
    ```

**Note:** it's recommended to have a single app that contains all template tag
overrides, so it's easy to exclude it from `INSTALLED_APPS` in production,
if you want to.

Now we need to define fake result for each instance of our template tag.
Let's assume that we have a template with two calls of the
`{% image $}` template tag:

```django
`{% load image_utils %}`


<div class="user">
    <div class="user-avatar">
        {% image avatar fill-200x200 %}
    </div>
    <div class="user-data">
        <div>Username: {{ username }}</div>
        <div>
            <div>User photo:</div>
            {% image avatar fill-200x400 %}
        </div>
    </div>
</div>
```

#### Render another template or pattern

Our `yaml` will similar to this:

```yaml
# Override template tags
tags:
    # Name of the template tag we are overriding
    image:
        # Arguments of the template tag
        # Override {% image avatar fill-200x200 %}
        avatar fill-200x200:
            template_name: "patterns/atoms/images/image.html"
        # Override {% image avatar fill-200x400 %}
        avatar fill-200x400:
            template_name: "patterns/atoms/images/image.html"

# Override context, if needed
```

In this example, we override both template tags and
render the same template: `patterns/atoms/images/image.html`.
This template is a regular Django template. If it's a pattern,
like in our example, it will be rendered with its own fake
content defined in `patterns/atoms/images/image.yaml`.

The downside of this approach is that we render the
same template where an image can be rendered in a different size.
So, if `patterns/atoms/images/image.html` has something like
`<img src="http://via.placeholder.com/200x200" width="200" height="200" alt="Placeholder">`
inside, this means that we will render image of size `200x200` few times.

Probably, in the majority of cases, it's ok to render the same
template, but not when we are rendering images
of different sizes.

There are two approaches for this problem:

*   Create a template for every image size you need. It can be a template
    that you will be only using for pattern library: no production use.
    This is a good option, when you want define a fake result for a template
    tag that renders a big piece of HTML code.
    Also it's useful when the template tag renders some other pattern,
    which is a common situation.
*   For tags that render something small like `<img>` tag,
    there is an alternative option: you can define raw data
    in your `yaml` file


#### Return raw data

Let's update our `yaml` to use raw data:

```yaml
# Override template tags
tags:
    # Name of the template tag we are overriding
    image:
        # Arguments of the template tag
        # Override {% image avatar fill-200x200 %}
        avatar fill-200x200:
            raw: >
                <img src="http://via.placeholder.com/200x200" width="200" height="200" alt="Placeholder">
        # Override {% image avatar fill-200x400 %}
        avatar fill-200x400:
            raw: >
                <img src="http://via.placeholder.com/200x400" width="200" height="400" alt="Placeholder">

# Override context, if needed
```

Now we make both `{% image %}` tags return different strings
without creating a separate templates for them.

The `raw` field, can contain any data supported by
[`PyYAML`](http://pyyaml.org/wiki/PyYAMLDocumentation)
without creating a custom object type.

For example, if we have a template like this:

```django
{% comment %}
The following tag assigns result into avatar_thumbnail
for later use and renders nothing (empty string).
{% endcomment %}
{% image avatar fill-200x200 as avatar_thumbnail %}

Avatar file path: {{ avatar_thumbnail.file }}
Avatar URL: {{ avatar_thumbnail.url }}
Avatar: <img src="{{ avatar_thumbnail.url }}" alt="{{ username }}">
```

We can define our `yaml` like this:

```yaml
tags:
    image:
        # Override {% image avatar fill-200x200 as avatar_thumbnail %}
        avatar fill-200x200 as avatar_thumbnail:
            raw:
                file: "/path/to/avatar/file"
                url: "http://via.placeholder.com/200x200"
```

Note that the example above will only work if our `image` is a
["Simple tag"](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#simple-tags).
If it's a more custom implementation, we will need to specify output
variable name explicitly like this:

```yaml
tags:
    image:
        # Override {% image avatar fill-200x200 as avatar_thumbnail %}
        avatar fill-200x200 as avatar_thumbnail:
            target_var: avatar_thumbnail
            raw:
                file: "/path/to/avatar/file"
                url: "http://via.placeholder.com/200x200"
```

Note the `target_var` field.

**TODO:**

- [ ] Check all examples;
- [ ] Describe the approach to the base template
    which should include CSS and JS;
  * The base template should be very minimalistic;
  * Not only docs: We need to decide which templates
    should be rendered in base template and which should
    be rendered on their own. Currently we render only page templates
    without using base template, but it's hardcoded.
    We should, probably, make it configurable.
