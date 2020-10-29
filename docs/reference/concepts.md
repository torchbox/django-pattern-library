# Concepts

To understand how `django-pattern-library` works, the following concepts are important.

## Patterns

Any template that is displayed by the pattern library is referred to as a pattern. Patterns are divided into two categories: fragments and pages.

## Fragments

A fragment is a pattern whose markup does not include all of the resources (typically CSS and Javascript) for it to be displayed correctly on its own. This is typical for reusable component templates which depend on global stylesheets or Javascript bundles to render and behave correctly.

To enable them to be correctly displayed in the pattern library, `django-pattern-library` will inject the rendered markup of fragments into the **pattern base template** specified by `PATTERN_LIBRARY['PATTERN_BASE_TEMPLATE_NAME']`.

This template should include references to any required static files. The rendered markup of fragments will be available in the `pattern_library_rendered_pattern` context variable (see the tests for [an example](https://github.com/torchbox/django-pattern-library/blob/master/tests/templates/patterns/base.html)).

## Pages

In contrast to fragments, pages are patterns that include everything they need to be displayed correctly in their markup. Pages are defined by `PATTERN_LIBRARY['BASE_TEMPLATE_NAMES']`.

Any template in that list — or that extends a template in that list — is considered a page and will be displayed as-is when rendered in the pattern library.

It is common practice for page templates to extend the pattern base template to avoid duplicate references to stylesheets and Javascript bundles. Again, [an example](https://github.com/torchbox/django-pattern-library/blob/master/tests/templates/patterns/base_page.html) of this can be seen in the tests.

