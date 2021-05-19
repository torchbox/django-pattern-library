# Changelog

## [Unreleased]

### Added

- We now officially support Django 3.2, and tentatively Django 4.0

### Fixed

- Update tox config to account for Django's primary branch rename.

## [0.3.0] - 2020-11-02

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

## [0.2.9] - 2020-07-29

### Added
- Atomic design no longer enforced and pattern templates can be from several locations, rather than a single location.
  These changes are currently undocumented, see the tests for examples.

### Fixed
- Templates that are not explicitly part of the pattern library can no longer be rendered by the pattern library

## [0.2.8] - 2020-03-13

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

## [0.2.5] - 2019-11-01

### Added
- Switch to Poetry for dependency management
- Documentation tab for each pattern that will display a markdown file if it is stored along with the html and yaml files
- Extra yaml examples in the README
- Merge request template

### Changed
- Improve documentation for developers

## [0.2.4] - 2019-06-11

### Added
- Compatibility with Django 2.2

[0.2.9]: https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.9
[0.2.8]: https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.8
[0.2.5]: https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.5
[0.2.4]: https://github.com/torchbox/django-pattern-library/releases/tag/v0.2.4
