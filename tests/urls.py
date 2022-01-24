from django.conf import settings
from django.urls import include, path

from pattern_library import urls as pattern_library_urls

if settings.GITHUB_PAGES_EXPORT:
    urlpatterns = [
        path("django-pattern-library/demo/", include(pattern_library_urls)),
    ]
else:
    urlpatterns = [
        path("", include(pattern_library_urls)),
    ]
