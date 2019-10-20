import os

SECRET_KEY = 'foobar'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'pattern_library',
    'tests',
]

STATIC_URL = '/static/'

ROOT_URLCONF = 'tests.urls'

PATTERN_LIBRARY = {
    'TEMPLATE_DIR': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['pattern_library.loader_tags'],
        },
    },
]

PATTERN_LIBRARY = {
    'SECTIONS': [
        ('atoms', ['patterns/atoms']),
        ('molecules', ['patterns/molecules']),
    ],
}
