# Automated tests

Although pattern libraries often start as tools for manual tests during development, they can also be useful for automated UI testing. There are a few benefits to doing UI tests with a pattern library:

- Test the components in isolation. When tests fail, you will know exactly which component has issues, rather than having to inspect whole pages to understand what might have changed.
- Test the components with mock data. One of the issues with UI tests is to have test data for your UIs to render – you can reuse the pattern library data for this purpose (although there are [limitations](../guides/multiple-variants.md)).

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

### Accessibility testing in GitLab CI

Here is a practical example of combining [Pa11y](https://pa11y.org/) and django-pattern-library in GitLab CI to run automated accessibility tests. This three-stage build first compiles a project’s static assets (CSS, JS), then generates pattern library static files with Django (with the [`render_patterns` command](../reference/api.md#render_patterns) command can be), and finally tests those static pages with Pa11y.

```yaml
static:
  image: node:16
  stage: build
  script:
    - npm ci
    - npm run build:prod
  artifacts:
    name: "static-$CI_JOB_ID"
    paths:
      - ./demosite/static_compiled
    expire_in: 30 mins

test_python:
  image: python:3.9
  stage: test
  dependencies:
    - static
  services:
    - postgres:12.3
  variables:
    DJANGO_SETTINGS_MODULE: demosite.settings.production
    GIT_STRATEGY: none
  script:
    - pip install poetry==1.1.8
    - poetry install

    - python manage.py collectstatic --verbosity 0 --noinput --clear

    # Render all django-pattern-library patterns, saving a list of the rendered files.
    - python manage.py render_patterns --wrap-fragment 2>&1 >/dev/null | tee dpl-list.txt
    - mv dpl-list.txt dpl-rendered-patterns && cp -R static dpl-rendered-patterns/static && mv dpl-rendered-patterns ../dpl-rendered-patterns
  artifacts:
    name: "test_patterns-$CI_JOB_ID"
    paths:
      - ./dpl-rendered-patterns
    expire_in: 30 mins

pa11y:
  image: registry.gitlab.com/gitlab-org/ci-cd/accessibility:6.1.1
  stage: accessibility
  dependencies:
    - test_python
  variables:
    TEST_ORIGIN: http://localhost:4000
  script:
    # Serve files locally, in the background, waiting for the server to start before we run the test suite.
    - npm install -g http-server@14
    - http-server ./dpl-rendered-patterns --port 4000 &
    - pa11y-ci -j --config pa11y.config.js > dpl-rendered-patterns/gl-accessibility.json
  artifacts:
    # Create artifacts even if the tests fail.
    when: always
    expire_in: 1 week
    paths:
      - dpl-rendered-patterns
    reports:
      accessibility: dpl-rendered-patterns/gl-accessibility.json
```

Here is the `pa11y.config.js`, which will determine what to test based on the output of `render_patterns`, as listed in the `dpl-list.txt` file:

```js
const path = require("path");
const fs = require("fs");

const defaults = {
  chromeLaunchConfig: {
    // Needed to run Pa11y in GitLab CI.
    args: ["--no-sandbox"],
  },
  standard: "WCAG2AA",
  runners: ["axe"],
};

// Assume we run tests over a live django-pattern-library instance, unless TEST_ORIGIN is set;
const local = "http://localhost:8000/pattern-library/render-pattern/patterns";
const origin = process.env.TEST_ORIGIN || local;

let urls = [];

// In CI mode, retrieve the URLs to test from dpl-rendered-patterns.
if (process.env.CI) {
  const list = path.join(__dirname, "dpl-rendered-patterns", "dpl-list.txt");
  const patterns = fs.readFileSync(list, "utf-8").split("\n").filter((p) => p);

  urls = patterns.map((p) => `${origin}/${p.replace("patterns/", "")}`);
}

// Convert the list of URLs to configuration objects.
urls = [...new Set(urls)].map((url) => {
  const config = {
    url,
    screenCapture: `dpl-rendered-patterns/${url.replace(origin, "")}.png`,
  };

  if (url.endsWith("tab-nav-item.html")) {
    config.ignore = [...defaults.ignore, "aria-required-parent"];
  }

  return config;
});

console.log(`Initialising pa11y-ci on ${urls.length} URLs`);

module.exports = {
  defaults,
  urls,
};
```
