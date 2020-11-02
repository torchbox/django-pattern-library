# Automated tests

Although pattern libraries often start as tools for manual tests during development, they can also be useful for automated UI testing. There are a few benefits to doing UI tests with a pattern library:

- Test the components in isolation. When tests fail, you will know exactly which component has issues, rather than having to inspect whole pages to understand what might have changed.
- Test the components with mock data. One of the issues with UI tests is to have test data for your UIs to render – you can reuse the pattern library data for this purpose (althoug there are [limitations](../guides/multiple-variants.md)).

## Setting up automated UI tests

There are two ways to set up automated tests: by accessing templates as they are rendered by the pattern library directly with Django, or by pre-rendering the templates with [`render_patterns` command](../reference/api.md#render_patterns) and then using this static export to make automated tests.

### Served by Django

Make sure your Django server is up and running, and you can then point your tests directly at the pattern library’s iframe URLs, for example: `http://localhost:8000/pattern-library/render-pattern/patterns/molecules/accordion/accordion.html`.

Note this will always render your templates within the base template ([`PATTERN_BASE_TEMPLATE_NAME`](../reference/api.md#pattern_base_template_name)), which may or may not be appropriate for your tests.

### With `render_patterns`

The [`render_patterns` command](../reference/api.md#render_patterns) command can be used to export all your templates, so you can do bulk checks on them all. For example, testing all templates use valid HTML with the [v.Nu HTML5 validator](https://validator.github.io/validator/):

```sh
./manage.py render_patterns --wrap-fragments
vnu dpl-rendered-patterns/**/*.html
```

One of the advantages of `render_patterns` is the ability for you to test the patterns without wrapping fragments in the base template, should this be more appropriate for your tests.

## Visual regression testing

Pattern libraries are a natural fit for automated visual regression tests. Here is an example [BackstopJS](https://github.com/garris/BackstopJS) configuration file:

```json
{
  "viewports": [
    {
      "label": "tablet",
      "width": 1024,
      "height": 768
    }
  ],
  "scenarios": [
    {
      "label": "accordion.html",
      "url": "https://torchbox.github.io/django-pattern-library/dpl-rendered-patterns/molecules/accordion/accordion.html"
    },
    {
      "label": "person_page.html",
      "url": "https://torchbox.github.io/django-pattern-library/dpl-rendered-patterns/pages/people/person_page.html"
    }
  ],
  "paths": {
    "bitmaps_reference": "backstop_data/bitmaps_reference",
    "bitmaps_test": "backstop_data/bitmaps_test",
    "engine_scripts": "backstop_data/engine_scripts",
    "html_report": "backstop_data/html_report",
    "ci_report": "backstop_data/ci_report"
  },
  "engine": "puppeteer"
}
```

Try this out by saving the file as `backstop.json`, then:

```sh
npm install -g backstopjs
backstop test
```

## Accessibility testing

Here as well, pattern libraries are a natural fit, due to them providing the test data, and making it possible to test components in isolation. Have a look at [Pa11y](https://pa11y.org/) or [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) to get started.

Here is an example Pa11y configuration:

```js
module.exports = {
  defaults: {
    standard: "WCAG2AAA",
    runners: ["axe"],
  },

  urls: [
    "https://torchbox.github.io/django-pattern-library/dpl-rendered-patterns/molecules/accordion/accordion.html",
    "https://torchbox.github.io/django-pattern-library/dpl-rendered-patterns/pages/people/person_page.html",
  ],
};
```

Try this out by saving the file as `pa11y.config.js`, then:

```sh
npm install -g pa11y-ci
pa11y-ci --config pa11y.config.js
```
