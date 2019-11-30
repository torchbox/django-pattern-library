

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'

DEFAULT_SETTINGS = {
    'BASE_TEMPLATE_NAME': 'patterns/base.html',
    'TEMPLATE_SUFFIX': '.html',
    'SECTIONS': (
        ('atoms', ['patterns/atoms']),
        ('molecules', ['patterns/molecules']),
        ('organisms', ['patterns/organisms']),
        ('templates', ['patterns/templates']),
        ('pages', ['patterns/pages']),
    ),
}


def get_from_settings(attr):
    from django.conf import settings

    library_settings = DEFAULT_SETTINGS.copy()
    library_settings.update(getattr(settings, 'PATTERN_LIBRARY', {}))

    return library_settings.get(attr)


def get_pattern_template_suffix():
    return get_from_settings('TEMPLATE_SUFFIX')


def get_pattern_base_template_name():
    return get_from_settings('BASE_TEMPLATE_NAME')


def get_sections():
    return get_from_settings('SECTIONS')


def get_pattern_context_var_name():
    return '__pattern_library_view'
