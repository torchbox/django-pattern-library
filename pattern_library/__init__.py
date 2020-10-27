default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'

DEFAULT_SETTINGS = {
    # PATTERN_BASE_TEMPLATE_NAME is the template that fragments will be wrapped with.
    # It should include any required CSS and JS and output
    # `pattern_library_rendered_pattern` from context.
    'PATTERN_BASE_TEMPLATE_NAME': 'patterns/base.html',
    # Any template in BASE_TEMPLATE_NAMES or any template that extends a template in
    # BASE_TEMPLATE_NAMES is a "page" and will be rendered as-is without being wrapped.
    'BASE_TEMPLATE_NAMES': ['patterns/base_page.html'],
    'TEMPLATE_SUFFIX': '.html',
    # SECTIONS controls the groups of templates that appear in the navigation. The keys
    # are the group titles and the value are lists of template name prefixes that will
    # be searched to populate the groups.
    'SECTIONS': (
        ('atoms', ['patterns/atoms']),
        ('molecules', ['patterns/molecules']),
        ('organisms', ['patterns/organisms']),
        ('templates', ['patterns/templates']),
        ('pages', ['patterns/pages']),
    ),
}


def get_setting(attr):
    from django.conf import settings
    library_settings = DEFAULT_SETTINGS.copy()
    library_settings.update(getattr(settings, 'PATTERN_LIBRARY', {}))
    return library_settings.get(attr)


def get_pattern_template_suffix():
    return get_setting('TEMPLATE_SUFFIX')


def get_pattern_base_template_name():
    return get_setting('PATTERN_BASE_TEMPLATE_NAME')


def get_base_template_names():
    return get_setting('BASE_TEMPLATE_NAMES')


def get_sections():
    return get_setting('SECTIONS')


def get_pattern_context_var_name():
    return '__pattern_library_view'
