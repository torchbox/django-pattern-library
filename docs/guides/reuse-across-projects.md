# Reuse across projects

django-pattern-library is designed to be useful for component reuse within a single project, but it can also be set up to create a component library reusable between multiple projects. Reusing pattern library components is a matter of packaging and publishing a Django app (that happens to contain a lot of templates, CSS, and JS).

Here are the rough steps:

- **Decide where to store the shared pattern library**. Whether it has its own repository, whether it’s published on PyPI, or in another way.
- **Choose a versioning and release methodology**. With multiple projects reusing the code, it’s important for them to be able to pin specific versions, and have a clear sense of how to do updates.
- **Provide a pattern library development environment**. Developers will need a way to iterate on pattern library components in isolation from the projects the UI components are reused in.

## Static files

As part of your pattern library’s build process, make sure that the static files (CSS, JS, etc.) of each component can be reused individually of each-other. Different projects likely will reuse different components, and you don’t want to be paying the performance cost of loading components you don’t need.

## Useful resources

- Django’s official [How to write reusable apps](https://docs.djangoproject.com/en/3.1/intro/reusable-apps/)
- InVision’s [Guide to Design Systems](https://www.invisionapp.com/inside-design/guide-to-design-systems/)
