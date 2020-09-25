# Changelog

## [Unreleased]

### Added
- Support for Django 3.1

### Removed
- Support for Django 1.11
- Support for Django 2.0
- Support for Django 2.1
- The project no longer includes polyfills for all ES6 features, and only supports modern browsers.

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
