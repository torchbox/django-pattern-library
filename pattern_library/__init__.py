import importlib
from functools import wraps

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'
settings = None


def uses_settings(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        global settings
        if settings is None:
            settings = importlib.import_module('django.conf').settings
        return func(*args, **kwargs)
    return wrapped


PATTERN_LIBRARY_SETTINGS = {
    'BASE_TEMPLATE_NAME': 'patterns/base.html',
    'TEMPLATE_SUFFIX': '.html',
    'TEMPLATE_DIR': 'to/remove/',
    'SECTIONS': tuple(),
}


@uses_settings
def get_from_settings(attr):
    library_settings = getattr(settings, 'PATTERN_LIBRARY', PATTERN_LIBRARY_SETTINGS)
    return library_settings.get(attr, PATTERN_LIBRARY_SETTINGS[attr])


@uses_settings
def get_pattern_template_dir():
    return get_from_settings('TEMPLATE_DIR')


def get_pattern_template_suffix():
    return get_from_settings('TEMPLATE_SUFFIX')


def get_pattern_base_template_name():
    return get_from_settings('BASE_TEMPLATE_NAME')


def get_sections():
    return get_from_settings('SECTIONS')


def get_pattern_context_var_name():
    return '__pattern_library_view'
