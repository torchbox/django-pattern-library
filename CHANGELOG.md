# Changelog

## [Unreleased]

- Disable pointer events on menu chevron to allow clicks ([#202](https://github.com/torchbox/django-pattern-library/issues/202), [#205](https://github.com/torchbox/django-pattern-library/pull/205))

## [1.0.0](https://github.com/torchbox/django-pattern-library/releases/tag/v1.0.0) - 2022-06-10

### Added

- We now use type hints for the package’s public API (`register_context_modifier` and `override_tag`) ([#172](https://github.com/torchbox/django-pattern-library/issues/172), [#189](https://github.com/torchbox/django-pattern-library/pull/189)).

### Removed

- We no longer support Django 2.2, as it has reached its end of life.

## [0.7.0](https://github.com/torchbox/django-pattern-library/releases/tag/v0.7.0) - 2022-01-25

## Added

- Add a way to customise rendering of a pattern with [`is_pattern_library`](https://torchbox.github.io/django-pattern-library/reference/api/#is_pattern_library) context variable ([#156](https://github.com/torchbox/django-pattern-library/issues/156), [#167](https://github.com/torchbox/django-pattern-library/pull/167)).
- Support for Django 4.0 ([#164](https://github.com/torchbox/django-pattern-library/pull/164)).
- Tentative support for Django 4.1 ([#185](https://github.com/torchbox/django-pattern-library/pull/185)).
- Support for Python 3.10 ([#163](https://github.com/torchbox/django-pattern-library/pull/163)).
- Tentative support for Python 3.11 ([#185](https://github.com/torchbox/django-pattern-library/pull/185)).
- VS Code devcontainer for development ([#178](https://github.com/torchbox/django-pattern-library/pull/178)).
- Documented the need to set `X_FRAME_OPTIONS = "SAMEORIGIN"` to see Django debug responses in the iframe UI ([#186](https://github.com/torchbox/django-pattern-library/pull/186)).
- New `/api/v1/render-pattern` [API endpoint to render patterns](https://torchbox.github.io/django-pattern-library/recipes/api-rendering/) via POST requests, with the pattern’s context and tag overrides as a JSON body ([#104](https://github.com/torchbox/django-pattern-library/issues/104), [#168](https://github.com/torchbox/django-pattern-library/pull/168)).

### Changed

- Change Poetry version to be `>=1.1.12,<2` in Docker development setup (prevents `JSONDecodeError` issue under Python 3.10) ([#178](https://github.com/torchbox/django-pattern-library/pull/178)).
- Move demo/test app pattern-library from `/pattern-library/` to `/` ([#178](https://github.com/torchbox/django-pattern-library/pull/178)).
- Allow `.yml` extension for YAML files ([#161](https://github.com/torchbox/django-pattern-library/issues/161), [#169](https://github.com/torchbox/django-pattern-library/pull/169)).
- Python files are now formatted by `black` ([#187](https://github.com/torchbox/django-pattern-library/pull/187)).
- Fix potential Django 4.0 compatibility issue for components using non-string values in tag overrides ([#166](https://github.com/torchbox/django-pattern-library/issues/166), [#188](https://github.com/torchbox/django-pattern-library/pull/188)).

### Removed

- We no longer support Python 3.6, as it has reached its end of life ([#163](https://github.com/torchbox/django-pattern-library/pull/163)).
- Remove support for IE11 in pattern library UI ([#151](https://github.com/torchbox/django-pattern-library/issue/151), [#162](https://github.com/torchbox/django-pattern-library/pull/162)).

## [0.6.0](https://github.com/torchbox/django-pattern-library/releases/tag/v0.6.0) - 2021-12-21

- Make `default_app_config` conditional to avoid [deprecation warnings](https://docs.djangoproject.com/en/3.2/ref/applications/#for-application-authors) for Django versions >= 3.2 ([#153](https://github.com/torchbox/django-pattern-library/issues/153), [#160](https://github.com/torchbox/django-pattern-library/pull/160)).
- Define `AppConfig.default_auto_field` as [required since Django 3.2](https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys) ([#154](https://github.com/torchbox/django-pattern-library/pull/154)).
- Support PyYAML v6 ([#158](https://github.com/torchbox/django-pattern-library/pull/158))

## [0.5.0](https://github.com/torchbox/django-pattern-library/releases/tag/v0.5.0) - 2021-06-04

### Added

Added support for '[context modifiers](https://torchbox.github.io/django-pattern-library/guides/defining-template-context/#modifying-template-contexts-with-python)' - A way to modify template contexts with Python ([#141](https://github.com/torchbox/django-pattern-library/pull/141), [#147](https://github.com/torchbox/django-pattern-library/pull/147), [#106](https://github.com/torchbox/django-pattern-library/issues/106)).

This addresses the following limitations of the pattern library:

- [#10 No way to specify objects that have attributes and support iteration](https://github.com/torchbox/django-pattern-library/issues/10)
- [#113 Django form fields not well supported](https://github.com/torchbox/django-pattern-library/issues/113)
- [#135 Competing tag/context config for image provides inconsistent result](https://github.com/torchbox/django-pattern-library/issues/135)

View the [documentation](https://torchbox.github.io/django-pattern-library/guides/defining-template-context/#modifying-template-contexts-with-python), as well as demos leveraging the new capability: [forms](https://torchbox.github.io/django-pattern-library/demo/pattern/patterns/pages/forms/example_form.html) (see [forms and fields recipe](https://torchbox.github.io/django-pattern-library/recipes/forms-and-fields/)), and [pagination](https://torchbox.github.io/django-pattern-library/demo/pattern/patterns/pages/search/search.html) (see [pagination recipe](https://torchbox.github.io/django-pattern-library/recipes/pagination/)).

## [0.4.0](https://github.com/torchbox/django-pattern-library/releases/tag/v0.4.0) - 2021-05-20

### Added

- We now officially support Django 3.2, and tentatively Django 4.0 ([#144](https://github.com/torchbox/django-pattern-library/pull/144))
- Load templates from template engines’ [`DIRS`](https://docs.djangoproject.com/en/3.2/ref/settings/#dirs) as well as apps’ `templates` subdirectories ([#145](https://github.com/torchbox/django-pattern-library/pull/145))

## [0.3.0](https://github.com/torchbox/django-pattern-library/releases/tag/v0.3.0) - 2020-11-02

We have a new documentation website! Check out [torchbox.github.io/django-pattern-library](https://torchbox.github.io/django-pattern-library/).

### Added

- This package now supports Django 3.1, and has tentative support for Django 3.2
- We also now support Python 3.9
- Implement optional default for [override_tag](https://torchbox.github.io/django-pattern-library/reference/api/#override_tag) ([#125](https://github.com/torchbox/django-pattern-library/issues/125))
- A new `render_patterns` command makes it possible to export the pattern library templates for automated tests or static hosting ([#16](https://github.com/torchbox/django-pattern-library/issues/16), [#17](https://github.com/torchbox/django-pattern-library/issues/17))
- Permit variable template names in extends and include tags ([#112](https://github.com/torchbox/django-pattern-library/pull/112))

### Removed

- We no longer support Django 1.11, 2.0, 2.1
- The project no longer includes polyfills for all ES6 features, and only supports modern browsers.

### Fixed

- Pages and fragments are now handled correctly again ([#119](https://github.com/torchbox/django-pattern-library/issues/119))
- PyPI package metadata now uses absolute URLs to GitHub ([#120](https://github.com/torchbox/django-pattern-library/issues/120)).

## [0.2.9](https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.9) - 2020-07-29

### Added

- Atomic design no longer enforced and pattern templates can be from several locations, rather than a single location.
  These changes are currently undocumented, see the tests for examples.

### Fixed

- Templates that are not explicitly part of the pattern library can no longer be rendered by the pattern library

## [0.2.8](https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.8) - 2020-03-13

### Added

- Moved to github and open sourced
- Support for Django 3.0
- Support for Python 3.8

### Removed

- webpack-dev-server
- references to old name of 'Mikalab'

### Fixed

- Documentation links and improved documentation
- Accessibility issues with pattern library chrome
- JavaScript in IE11 (added polyfills)
- Pattern search (no longer case sensitive)
- Issue with xframe-options header in django 3

## [0.2.5](https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.5) - 2019-11-01

### Added

- Switch to Poetry for dependency management
- Documentation tab for each pattern that will display a markdown file if it is stored along with the html and yaml files
- Extra yaml examples in the README
- Merge request template

### Changed

- Improve documentation for developers

## [0.2.4](https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.4) - 2019-06-11

### Added

- Compatibility with Django 2.2
