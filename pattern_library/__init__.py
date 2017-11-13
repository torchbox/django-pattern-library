from django.conf import settings

__version__ = '0.1.0'

default_app_config = 'pattern_library.apps.PatternLibraryAppConfig'


def get_base_lookup_dir():
    return settings.PATTERN_LIBRARY_BASE_LOOKUP_DIR
