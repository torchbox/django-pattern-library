from django.conf import settings

__version__ = '0.1.1'

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'


def get_pattern_template_dir():
    return settings.PATTERN_LIBRARY_TEMPLATE_DIR


def get_pattern_template_prefix():
    return getattr(settings, 'PATTERN_LIBRARY_TEMPLATE_PREFIX', 'patterns')


def get_pattern_template_suffix():
    return getattr(settings, 'PATTERN_LIBRARY_TEMPLATE_SUFFIX', '.html')


def get_pattern_base_template_name():
    return getattr(settings, 'PATTERN_LIBRARY_BASE_TEMPLATE_NAME', 'patterns/base.html')


def get_pattern_types():
    return ['atoms', 'molecules', 'organisms', 'templates', 'pages']


def get_pattern_context_var_name():
    return '__pattern_library_view'
