from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION < (2,):
    from django.core.urlresolvers import reverse  # noqa
else:
    from django.urls import reverse  # noqa
