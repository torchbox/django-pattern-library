import importlib
from functools import wraps

__version__ = '0.2.4'

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'
settings = None


def uses_settings(func):
    @wraps(func)
    def wrapped():
        global settings
        if settings is None:
            settings = importlib.import_module('django.conf').settings
        return func()
    return wrapped


@uses_settings
def get_pattern_template_dir():
    return settings.PATTERN_LIBRARY_TEMPLATE_DIR


@uses_settings
def get_pattern_template_prefix():
    return getattr(settings, 'PATTERN_LIBRARY_TEMPLATE_PREFIX', 'patterns')


@uses_settings
def get_pattern_template_suffix():
    return getattr(settings, 'PATTERN_LIBRARY_TEMPLATE_SUFFIX', '.html')


@uses_settings
def get_pattern_base_template_name():
    return getattr(settings, 'PATTERN_LIBRARY_BASE_TEMPLATE_NAME', 'patterns/base.html')


def get_pattern_types():
    return ['atoms', 'molecules', 'organisms', 'templates', 'pages']


def get_pattern_context_var_name():
    return '__pattern_library_view'
