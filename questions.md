# Open questions

> Last edited 2017-11-29T14:27:50Z

## Integration with Wagtail and other custom tags

We want to be able to use patterns in production code to reduce overhead on
maintaingin templates for pattern librarty and for the actuall project.

* How are we going to use `{% pageurl ... %}`, `{% include_block page.streamfield_body %}`, `{% image ... %}`
and `{% image ... as ... %}` tags in the pattern library with stub data.
Options:

  * Implement a way to use Mocks. Must be pluggable to allow users define their
  mocks for Wagtail and any other Django based projects. Sounds complicated
  from both: implementation and usage point of view.
  * Similar to the previous option. Define a snippet (basic function or class) to allow override template
  tags and load stub data from a file to replace output of the template tag.
  * Introduce limitation: do not use pages directly? Not ideal.
  * Any other options?


# Solved

## Basic template for patters

To be able to browse patterns (especially `atoms`, `molecules`, `organisms`
and `templates`) we need a base template which will include styles,
javascript, etc.

* How to deal with `page` patterns? They should be ready for use in
production code and extend from some base template. Possible options:

  * Use something like
  `{% extends pattern_library_base_template|default:'patterns/base.html' %}`.
  The `pattern_library_base_template` template var will only be
  available in pattern library view.
  **UPD:** This will work for page patterms, but not for others;

  * Render base template for all patterns except page patterns.
  
Fixed in a6c7e958dce8fc06185ea58a6dbadf8d9091cc13...5375375e5a0b1d18c4f964bc752e925510959895
