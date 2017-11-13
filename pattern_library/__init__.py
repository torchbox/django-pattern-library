from django.conf import settings

__version__ = '0.1.0'

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'


def get_pattern_template_dir():
    return settings.PATTERN_LIBRARY_TEMPLATE_DIR


def get_pattern_template_prefix():
    return getattr(settings, 'PATTERN_LIBRARY_TEMPLATE_PREFIX', 'patterns')


def get_pattern_template_suffix():
    return getattr(settings, 'PATTERN_LIBRARY_template_suffix', '.html')
