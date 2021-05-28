from django.conf import settings
from django.urls import include, path

from pattern_library import urls as pattern_library_urls

if settings.GITHUB_PAGES_EXPORT:
    urlpatterns = [
        path('django-pattern-library/demo/pattern-library/', include(pattern_library_urls)),
    ]
else:
    from .views import example_form

    urlpatterns = [
        path('example-form/', example_form),
        path('pattern-library/', include(pattern_library_urls)),
    ]
