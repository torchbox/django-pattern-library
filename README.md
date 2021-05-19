# [django-pattern-library](https://torchbox.github.io/django-pattern-library/)

[![PyPI](https://img.shields.io/pypi/v/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![PyPI downloads](https://img.shields.io/pypi/dm/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![Build status](https://github.com/torchbox/django-pattern-library/workflows/CI/badge.svg)](https://github.com/torchbox/django-pattern-library/actions) [![Total alerts](https://img.shields.io/lgtm/alerts/g/torchbox/django-pattern-library.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/torchbox/django-pattern-library/alerts/)

> UI pattern libraries for Django templates. Try our [online demo](https://torchbox.github.io/django-pattern-library/demo/pattern-library/).

![Screenshot of the pattern library UI, with navigation, pattern rendering, and configuration](https://raw.githubusercontent.com/torchbox/django-pattern-library/master/.github/pattern-library-screenshot.webp)

## Features

This package automates the maintenance of UI pattern libraries or styleguides for Django projects, and allows developers to experiment with Django templates without having to create Django views and models.

- Create reusable patterns by creating Django templates files as usual.
- All patterns automatically show up in the pattern library’s interface.
- Define data as YAML files for the templates to render with the relevant Django context.
- Override Django templates tags as needed to mock the template’s dependencies.
- Document your patterns with Markdown.

## Why you need this

Pattern libraries will change your workflow for the better:

- They help separate concerns, both in code, and between members of a development team.
- If needed, they make it possible for UI development to happen before models and views are created.
- They encourage code reuse – defining independent UI components, that can be reused across apps, or ported to other projects.
- It makes it much simpler to test UI components – no need to figure out where they’re used across a site or app.

Learn more by watching our presentation – [Reusable UI components: A journey from React to Wagtail](https://www.youtube.com/watch?v=isrOufI7TKc).

## Online demo

The pattern library is dependent on Django for rendering – but also supports exporting as a static site if needed. Try out our online demo:

- For a component, [accordion.html](https://torchbox.github.io/django-pattern-library/demo/pattern-library/pattern/patterns/molecules/accordion/accordion.html)
- For a page-level template, [person_page.html](https://torchbox.github.io/django-pattern-library/demo/pattern-library/pattern/patterns/pages/people/person_page.html)

## Documentation

Documentation is available at [torchbox.github.io/django-pattern-library](https://torchbox.github.io/django-pattern-library/), with source files in the `docs` directory.

- **[Getting started](https://torchbox.github.io/django-pattern-library/getting-started/)**
- **Guides**
  - [Defining template context](https://torchbox.github.io/django-pattern-library/guides/defining-template-context/)
  - [Overriding template tags](https://torchbox.github.io/django-pattern-library/guides/overriding-template-tags/)
  - [Customizing template rendering](https://torchbox.github.io/django-pattern-library/guides/customizing-template-rendering/)
  - [Usage tips](https://torchbox.github.io/django-pattern-library/guides/usage-tips/)
- **Reference**
  - [API & settings](https://torchbox.github.io/django-pattern-library/reference/api/)
  - [Known issues and limitations](https://torchbox.github.io/django-pattern-library/reference/known-issues/)

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](https://github.com/torchbox/django-pattern-library/blob/master/CONTRIBUTING.md).

If you want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

### Nightly builds

To try out the latest features before a release, we also create builds from every commit to `master`. Note we make no guarantee as to the quality of those pre-releases, and the pre-releases are overwritten on every build so shouldn’t be relied on for reproducible builds. [Download the latest `django_pattern_library-0.0.0.dev0-py3-none-any.whl`](http://torchbox.github.io/django-pattern-library/dist/django_pattern_library-0.0.0.dev0-py3-none-any.whl).

## Credits

View the full list of [contributors](https://github.com/torchbox/django-pattern-library/graphs/contributors). [BSD](https://github.com/torchbox/django-pattern-library/blob/master/LICENSE) licensed.

Project logo from [FxEmoji](https://github.com/mozilla/fxemoji). Documentation website built with [MkDocs](https://www.mkdocs.org/), and hosted in [GitHub Pages](https://pages.github.com/).
